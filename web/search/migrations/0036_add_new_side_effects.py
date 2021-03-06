# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-12 20:57
from __future__ import unicode_literals

from django.db import migrations


def update(apps, schema_editor):
    Effect = apps.get_model("search", "Effect")

    spacey = Effect(effect_type='side_effect', data_name='spacey', display_name='Spacey')
    spacey.save()

    lazy = Effect(effect_type='side_effect', data_name='lazy', display_name='Lazy')
    lazy.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0035_add_new_side_effects'),
    ]

    operations = [
        migrations.RunPython(update, reverse),
    ]
