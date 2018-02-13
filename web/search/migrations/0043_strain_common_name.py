# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-02-07 15:19
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    strain_class = apps.get_model('search', 'Strain')

    to_migrate = [
        ('3C Banana Kraken, OG', 'Banana Kraken OG'),
        ('3C Enoch OG', 'Enoch OG'),
        ('3C Kraken', 'Kraken'),
        ('3C Vanilla OG', 'Vanilla OG'),
        ('3C Banana Split OG', 'Banana Split OG'),
        ('3C Blue Velvet Cookies', 'Blue Velvet Cookies'),
        ('3C Sour Sunset', 'Sour Sunset'),
        ('3C Strawberry Fields', 'Strawberry Fields'),
        ('Crockett\'s Strawberry Fields', 'Strawberry Fields'),
        ('Kumba Hills Farms White Tahoe Cookies', 'White Tahoe Cookies'),
        ('TJ\'s Purple Kush', 'Purple Kush'),
        ('TJ\'s Platinum Cookies', 'Platinum Cookies'),
        ('Happy Cabbage Farms White Tahoe Cookies', 'White Tahoe Cookies'),
        ('Eco Firma Farms Golden Pineapple', 'Golden Pineapple'),
        ('Eco Firma Farms Hazy Girl', 'Hazy Girl'),
        ('Emerald Cannabis Worx Afgoo', 'Afgoo'),
        ('Emerald Cannabis Worx Cookies And Cream', 'Cookies And Cream'),
        ('Happy Cabbage Farms Cookies And Cream', 'Cookies And Cream'),
        ('Happy Cabbage Farms Light Saber', 'Light Saber'),
        ('Emerald Cannabis Worx Strawberry Cough', 'Strawberry Cough'),
        ('Chernobyl (Sylmer Cut)', 'Chernobyl'),
        ('Oregon Roots Obama Kush', 'Obama Kush'),
        ('Trichome Farms Obama Kush', 'Obama Kush'),
        ('H&H Gardens Purple Kush', 'Purple Kush'),
        ('Northwest Greeneries Blue Dragon', 'Blue Dragon'),
        ('TJ\'s Durban Poison', 'Durban Poison'),
        ('Trichome Farms Black Widow', 'Black Widow'),
    ]

    for name, common_name in to_migrate:
        try:
            strain = strain_class.objects.get(name=name)
            strain.common_name = common_name
            strain.save()
        except Exception:
            pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0042_auto_20180105_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='strain',
            name='common_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]