# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-02 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0032_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesslocation',
            name='about',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]