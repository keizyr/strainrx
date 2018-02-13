# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-02-12 14:26
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


def data_forward(apps, schema_editor):
    effect_class = apps.get_model('search', 'Effect')
    strain_class = apps.get_model('search', 'Strain')

    effect_class.objects.get_or_create(effect_type='side_effect', data_name='groggy', display_name='Groggy')

    for strain in strain_class.objects.iterator():
        strain.side_effects['groggy'] = 0
        strain.save()


def data_backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0044_auto_20180212_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strain',
            name='side_effects',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'anxiety': 0, 'dizziness': 0, 'dry_eyes': 0, 'dry_mouth': 0, 'groggy': 0, 'headache': 0, 'hungry': 0, 'lazy': 0, 'paranoia': 0, 'spacey': 0}),
        ),
        migrations.RunPython(
            data_forward,
            data_backward,
        )
    ]