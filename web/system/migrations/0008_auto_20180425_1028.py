# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-04-25 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_permanentlyremoved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permanentlyremoved',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(301, 301), (410, 410)]),
        ),
    ]
