# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-24 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0002_auto_20160624_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='treetype',
            name='image',
            field=models.ImageField(null=True, upload_to=b'fruits_images', verbose_name='Fruit image'),
        ),
    ]