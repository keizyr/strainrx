# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-12-15 12:00
from __future__ import unicode_literals

from django.db import migrations


def create_grown_strain(apps, schema_editor):
    BusinessLocationGrownStrainItem = apps.get_model('businesses', 'BusinessLocationGrownStrainItem')
    BusinessLocationMenuItem = apps.get_model('businesses', 'BusinessLocationMenuItem')

    for menu in BusinessLocationMenuItem.objects.filter(business_location__grow_house=True, removed_date=None):
        BusinessLocationGrownStrainItem.objects.create(
            business_location_id=menu.business_location_id,
            strain_id=menu.strain_id)


def reverse(apps, schema_editor):
    BusinessLocationGrownStrainItem = apps.get_model('businesses', 'BusinessLocationGrownStrainItem')
    BusinessLocationGrownStrainItem.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0064_auto_20181211_2039'),
    ]

    operations = [
        migrations.RunPython(create_grown_strain, reverse),
    ]
