# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-14 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import web.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20161218_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, help_text='Maximum file size allowed is 5Mb', max_length=255, upload_to=web.users.models.upload_image_to, validators=[web.users.validators.validate_image]),
        ),
    ]
