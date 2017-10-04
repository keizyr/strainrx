# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-09-21 00:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20170920_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
