# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-21 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0004_auto_20160620_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestforparticipation',
            name='comment_about_participation',
            field=models.TextField(blank=True, null=True, verbose_name='Comment about participation'),
        ),
    ]
