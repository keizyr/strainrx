# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-12 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0022_businesslocation_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesslocation',
            name='slug_name',
            field=models.SlugField(blank=True, help_text='Warning: changing the slug will change the URL of this location', max_length=611, null=True),
        ),
    ]
