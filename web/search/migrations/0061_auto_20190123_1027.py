# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-01-23 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0060_auto_20181231_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strainreview',
            name='review',
            field=models.CharField(blank=True, default='', max_length=1100),
        ),
    ]