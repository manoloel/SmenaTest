from django.contrib.postgres.fields import JSONField
from django.db import models

class Printer(models.Model):
	CLIENT = 'C'
	KITCHEN = 'K'
	CHECK_TYPE = (
		(CLIENT, 'client'),
		(KITCHEN, 'kitchen'))

	name = models.CharField(max_length=20)
	api_key = models.CharField(max_length=20, unique=True)
	check_type = models.CharField(max_length=1, choices=CHECK_TYPE)
	point_id = models.IntegerField()

	def __unicode__(self):
		return self.name

class Check(models.Model):
	CLIENT = 'C'
	KITCHEN = 'K'
	CHECK_TYPE = (
		(CLIENT, 'client'),
		(KITCHEN, 'kitchen'))

	NEW = 'N'
	RENDERED = 'R'
	PRINTED = 'P'
	CHECK_STATUS = (
		(NEW, 'new'),
		(RENDERED, 'rendered'),
		(PRINTED, 'printed'))

	printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
	type = models.CharField(max_length=1, choices=CHECK_TYPE)
	order = JSONField()
	status = models.CharField(max_length=1, choices=CHECK_STATUS, default=NEW)
	pdf_file = models.FileField(default=None, null=True)
