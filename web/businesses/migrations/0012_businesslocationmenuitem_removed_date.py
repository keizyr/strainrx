# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-08 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesslocationmenuitem',
            name='removed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
