# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-31 05:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Avtoregion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fraction',
            field=models.CharField(blank=True, max_length=10, verbose_name='Фракция'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Название'),
        ),
    ]
