# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-06 20:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0003_strain_internal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strain',
            name='flavor',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default={'ammonia': 0, 'apple': 0, 'apricot': 0, 'berry': 0, 'blue_cheese': 0, 'blueberry': 0,
                         'buttery': 0, 'cheese': 0, 'chemical': 0, 'chestnut': 0, 'citrus': 0, 'coffee': 0, 'diesel': 0,
                         'earthy': 0, 'flowery': 0, 'grape': 0, 'grapefruit': 0, 'herbal': 0, 'honey': 0, 'lavender': 0,
                         'lemon': 0, 'lime': 0, 'mango': 0, 'menthol': 0, 'minty': 0, 'nutty': 0, 'orange': 0,
                         'peach': 0, 'pear': 0, 'pepper': 0, 'pine': 0, 'pineapple': 0, 'plum': 0, 'pungent': 0,
                         'rose': 0, 'sage': 0, 'skunk': 0, 'spicy_herbal': 0, 'strawberry': 0, 'sweet': 0, 'tar': 0,
                         'tea': 0, 'tobacco': 0, 'tree_fruit': 0, 'tropical': 0, 'vanilla': 0, 'violet': 0,
                         'woody': 0}),
        ),
    ]