# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-09 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0015_auto_20161208_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesslocation',
            name='lat',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='businesslocation',
            name='lng',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Longitude'),
        ),
    ]