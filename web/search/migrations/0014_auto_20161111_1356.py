# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-11 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0013_strainreview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strainreview',
            old_name='last_modified_data',
            new_name='last_modified_date',
        ),
    ]
