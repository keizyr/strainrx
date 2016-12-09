# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-06 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='location_raw',
            field=models.CharField(blank=True, max_length=20000, null=True, verbose_name='Location Raw JSON'),
        ),
    ]
