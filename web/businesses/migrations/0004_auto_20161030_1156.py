# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-30 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0003_business_trial_period_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businesslocation',
            old_name='zip',
            new_name='zip_code',
        ),
        migrations.AddField(
            model_name='business',
            name='is_business_verified',
            field=models.BooleanField(default=False),
        ),
    ]
