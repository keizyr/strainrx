# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-15 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import web.search.models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0029_auto_20170202_0713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.SlugField(help_text='This name must not contain spaces', max_length=100)),
                ('display_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, help_text='Maximum file size allowed is 1Mb', max_length=255, upload_to=web.search.models.upload_flavor_image_to, validators=[web.search.models.validate_flavor_image])),
            ],
        ),
    ]
