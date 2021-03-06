# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-01-23 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0068_auto_20181231_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesslocation',
            name='street1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='businesslocation',
            name='zip_code',
            field=models.CharField(blank=True, db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='locationreview',
            name='review',
            field=models.CharField(blank=True, default='', max_length=1100),
        ),
    ]
