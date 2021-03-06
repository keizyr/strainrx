# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-11-04 12:55
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0055_auto_20180527_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='strain',
            name='high_cbd',
            field=models.BooleanField(default=False, help_text="If strain has a CBD concentration of over 5% thrn it's high cbd, this field for manual control to check this box automatically"),
        ),
        migrations.AlterField(
            model_name='strain',
            name='flavor',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'ammonia': 0, 'apple': 0, 'apricot': 0, 'banana': 0, 'berry': 0, 'blue-cheese': 0, 'blueberry': 0, 'buttery': 0, 'cheese': 0, 'chemical': 0, 'cherry': 0, 'chestnut': 0, 'chocolate': 0, 'citrus': 0, 'coffee': 0, 'diesel': 0, 'earthy': 0, 'flowery': 0, 'grape': 0, 'grapefruit': 0, 'herbal': 0, 'honey': 0, 'lavender': 0, 'lemon': 0, 'lime': 0, 'mango': 0, 'menthol': 0, 'minty': 0, 'nutty': 0, 'orange': 0, 'peach': 0, 'pear': 0, 'pepper': 0, 'pine': 0, 'pineapple': 0, 'plum': 0, 'pungent': 0, 'rose': 0, 'sage': 0, 'skunk': 0, 'sour': 0, 'spicy-herbal': 0, 'strawberry': 0, 'sweet': 0, 'tar': 0, 'tea': 0, 'tobacco': 0, 'tree-fruit': 0, 'tropical': 0, 'vanilla': 0, 'violet': 0, 'woody': 0}),
        ),
        migrations.AlterField(
            model_name='usersearch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
