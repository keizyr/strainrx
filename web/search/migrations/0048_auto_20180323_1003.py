# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-03-23 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0047_auto_20180223_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='strain',
            name='cup_winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='strain',
            name='is_clean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='strain',
            name='is_indoor',
            field=models.BooleanField(default=True),
        ),
    ]
