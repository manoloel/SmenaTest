from django.contrib import admin
from checks.models import Printer, Check
# Register your models here.

class CheckAdmin(admin.ModelAdmin):
	list_display = ('id','printer_id', 'type', 'status')
	list_filter = ('type', 'status', 'printer_id__point_id', 'printer_id__name')

class PrinterAdmin(admin.ModelAdmin):
	list_display = ('name','check_type', 'point_id')

admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
