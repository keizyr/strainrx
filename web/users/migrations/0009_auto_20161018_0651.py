# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-18 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_pwresetlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pwresetlink',
            name='last_modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
