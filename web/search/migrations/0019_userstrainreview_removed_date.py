# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-20 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0018_userstrainreview_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstrainreview',
            name='removed_date',
            field=models.DateTimeField(null=True),
        ),
    ]