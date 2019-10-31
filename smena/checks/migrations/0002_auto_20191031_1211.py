# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-31 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.CharField(choices=[('N', 'new'), ('R', 'rendered'), ('P', 'printed')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='check',
            name='type',
            field=models.CharField(choices=[('C', 'client'), ('K', 'kitchen')], max_length=1),
        ),
        migrations.AlterField(
            model_name='printer',
            name='check_type',
            field=models.CharField(choices=[('C', 'client'), ('K', 'kitchen')], max_length=1),
        ),
    ]