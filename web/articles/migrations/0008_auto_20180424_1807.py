# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-04-24 18:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_is_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='deleted_date',
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_page',
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=1024, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=1024, unique=True),
            preserve_default=False,
        ),
    ]
