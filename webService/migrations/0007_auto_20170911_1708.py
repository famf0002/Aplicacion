# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webService', '0006_auto_20170909_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='uid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]