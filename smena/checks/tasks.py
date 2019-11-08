from django_rq import job
from django.template.loader import render_to_string
from .models import Check
from smena.settings import BASE_DIR
import base64, requests

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
	filename = f"{BASE_DIR}/media/pdf/'{check.order['id']}_{check.get_type_display()}.pdf"
	with open(filename, 'wb') as f:
	    f.write(response.content)
	check.status = Check.RENDERED
	check.pdf_file = filename
	check.save()