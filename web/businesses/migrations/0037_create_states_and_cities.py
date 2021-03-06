# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-12 22:41
from __future__ import unicode_literals

from django.db import migrations


def update(apps, schema_editor):
    BusinessLocation = apps.get_model("businesses", "BusinessLocation")
    State = apps.get_model("businesses", "State")
    City = apps.get_model("businesses", "City")

    for l in BusinessLocation.objects.all():
        state = l.state
        city = l.city

        if state and not State.objects.filter(abbreviation__iexact=state.lower()).exists():
            s = State(abbreviation=state)
            s.save()

        if city and not City.objects.filter(state__abbreviation__iexact=state.lower(),
                                            full_name__iexact=city.lower()).exists():
            c = City(state=State.objects.get(abbreviation__iexact=state.lower()), full_name=city)
            c.save()

        l.state_fk = State.objects.get(abbreviation__iexact=state.lower())
        l.city_fk = City.objects.get(state__abbreviation__iexact=state.lower(),
                                     full_name__iexact=city.lower())
        l.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('businesses', '0036_auto_20170313_1905'),
    ]

    operations = [
        migrations.RunPython(update, reverse),
    ]
