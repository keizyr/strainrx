# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-08 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0007_strain_strain_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strain',
            name='strain_slug',
            field=models.SlugField(blank=True,
                                   help_text='Warning: changing the slug will change the URL of this strain',
                                   max_length=611, null=True),
        ),
    ]
