# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-04 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0004_auto_20161030_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='business',
            name='dispensary',
        ),
        migrations.RemoveField(
            model_name='business',
            name='grow_house',
        ),
        migrations.RemoveField(
            model_name='businesslocation',
            name='business_type',
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='dispensary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='grow_house',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='manager_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]