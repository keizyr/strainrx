# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-12 22:41
from __future__ import unicode_literals

from django.db import migrations
from django.template.defaultfilters import slugify


def update(apps, schema_editor):
    BusinessLocation = apps.get_model("businesses", "BusinessLocation")

    for bl in BusinessLocation.objects.all():
        slugified_name = slugify(bl.location_name)
        slugified_name_and_street = '{0}-{1}'.format(slugify(bl.location_name), slugify(bl.street1))

        if not BusinessLocation.objects.filter(slug_name=slugified_name).exists():
            bl.slug_name = slugified_name
        elif not BusinessLocation.objects.filter(slug_name=slugified_name_and_street).exists():
            bl.slug_name = slugified_name_and_street
        else:
            for x in range(1, 1000):
                new_slug_name = '{0}-{1}'.format(slugified_name_and_street, x)
                if not BusinessLocation.objects.filter(slug_name=new_slug_name).exists():
                    bl.slug_name = new_slug_name
                    break

        bl.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('businesses', '0041_auto_20170316_1750'),
    ]

    operations = [
        migrations.RunPython(update, reverse),
    ]