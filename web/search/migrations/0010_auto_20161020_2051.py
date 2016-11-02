# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-20 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_strainimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effect_type', models.CharField(choices=[('effect', 'Effect'), ('benefit', 'Benefit'), ('side_effect', 'Side Effect')], max_length=20)),
                ('data_name', models.CharField(max_length=100)),
                ('display_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='effect',
            unique_together=set([('effect_type', 'data_name')]),
        ),
    ]