# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-05-10 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0053_auto_20180504_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='strain',
            name='growing_method',
            field=models.IntegerField(blank=True, choices=[(1, 'Indoor Soil'), (2, 'Indoor Hydro'), (3, 'Indoor Coco'), (4, 'Outdoor'), (5, 'Greenhouse'), (6, 'Aquaponics')], default=1, null=True),
        ),
        migrations.AddField(
            model_name='strain',
            name='lighting',
            field=models.IntegerField(blank=True, choices=[(1, 'Natural Light Schedule'), (2, 'HID'), (3, 'LED'), (4, 'Double Ended'), (5, 'Halogen')], default=1, null=True),
        ),
        migrations.AddField(
            model_name='strain',
            name='nutrient_base',
            field=models.IntegerField(blank=True, choices=[(1, 'Synthetic Nutrients'), (2, 'Organic Nutrients'), (3, 'Blended Nutrients')], default=1, null=True),
        ),
    ]