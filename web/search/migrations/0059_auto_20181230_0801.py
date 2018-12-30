# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-12-30 08:01
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F, CharField, Value
from django.db.models.functions import Concat


def populate_meta(apps, schema_editor):
    Strain = apps.get_model('search', 'Strain')

    # meta_title = `{ strain_name } { strain_variety } strain`
    # meta_desc = `Everything you need to know about the { strain_name } { strain_variety } strain: medical benefits,
    #              negative & positive effects and where to get it in your area.`
    Strain.objects.all().update(
        meta_title=Concat(F('name'), Value(' '), F('variety'), Value(' strain'), output_field=CharField()),
        og_title='',
        og_description='',
        meta_desc=Concat(
            Value('Everything you need to know about the '), F('name'), Value(' '), F('variety'),
            Value(' strain: medical benefits, negative & positive effects and where to get it in your area.'))
    )


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0058_auto_20181216_1931'),
    ]

    operations = [
        migrations.RunPython(populate_meta, migrations.RunPython.noop)
    ]
