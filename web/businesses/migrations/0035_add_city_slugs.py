# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-12 22:41
from __future__ import unicode_literals

from django.db import migrations
from django.template.defaultfilters import slugify


def generate_city_slug(apps, schema_editor):
    BusinessLocation = apps.get_model("businesses", "BusinessLocation")

    for l in BusinessLocation.objects.all():
        l.city_slug = slugify(l.city)
        l.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('businesses', '0034_auto_20170306_1956'),
    ]

    operations = [
        migrations.RunPython(generate_city_slug, reverse),
    ]
