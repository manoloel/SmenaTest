from django.shortcuts import render, render_to_response
from smena.settings import BASE_DIR
from wsgiref.util import FileWrapper
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django_rq import job
from io import StringIO
import json, requests, base64
from .models import Printer, Check
from django.db.models import Q

# Create your views here.
def create_checks(request):
	order = json.loads(request.body)
	point_id=order['point_id']
	try:
		printer_k = Printer.objects.get(point_id=point_id, check_type=Printer.KITCHEN)
		printer_c = Printer.objects.get(point_id=point_id, check_type=Printer.CLIENT)
	except ObjectDoesNotExist:
		message = 'Для данной точки не настроено ни одного принтера'
		return JsonResponse({'error': message}, status=400)

	if Check.objects.filter(order__id=order['id']).exists():
		message = 'Для данного заказа уже созданы чеки'
		return JsonResponse({'error': message}, status=400)

	check_k = Check.objects.create(type=Check.KITCHEN, printer_id=printer_k, order=order)
	check_c = Check.objects.create(type=Check.CLIENT, printer_id=printer_c, order=order)
	create_pdf.delay(check_k.id)
	create_pdf.delay(check_c.id)

	message = 'Чеки успешно созданы'	
	return JsonResponse({'ok': message}, status=200)


def new_checks(request):
	api_key = request.GET.get('api_key')
	try:
		printer = Printer.objects.get(api_key=api_key)
		checks = Check.objects.filter(Q(printer_id=printer), Q(status=Check.NEW)|Q(status=Check.RENDERED)).values('id')
		data = json.loads(json.dumps({'checks': list(checks)}))
		return JsonResponse(data, safe=False)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Ошибка авторизации'}, status=401)

def check(request):
	api_key = request.GET.get('api_key')
	check_id = request.GET.get('check_id')
	try:
		printer = Printer.objects.get(api_key=api_key)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Ошибка авторизации'}, status=401)
	try:
		check = Check.objects.get(pk=check_id, printer_id=printer)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Данного чека не существует'}, status=400)
	if check.status == Check.NEW:
		return JsonResponse({'error': 'Для данного чека не сгенерирован PDF-файл'}, status=400)
	else:
		with open(check.pdf_file.name, 'rb') as file:
			response = HttpResponse(FileWrapper(file), content_type='application/pdf')
		check.status = Check.PRINTED
		check.save()
		return response


@job
def create_pdf(check_id):
	check = Check.objects.get(pk=check_id)
	context = {
	'check': check
	}
	if check.type == Check.KITCHEN:
		html = render_to_string('kitchen_check.html', context=context)
	else:
		html = render_to_string('client_check.html', context=context)
	url = 'http://localhost:80/'
	utf = html.encode('utf-8')
	base = base64.b64encode(utf)
	html = base.decode('utf-8')
	data = {
	    'contents': html,
		}
	headers = {
	    'Content-Type': 'application/json'
	}
	response = requests.post(url, data=json.dumps(data), headers=headers)
	filename = BASE_DIR+'/media/pdf/'+str(check.order['id'])+'_'+check.get_type_display()+'.pdf'
	with open(filename, 'wb') as f:
	    f.write(response.content)
	check.status = Check.RENDERED
	check.pdf_file = filename
	check.save()