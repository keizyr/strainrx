# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-14 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0015_auto_20161113_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strainreview',
            name='review',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
