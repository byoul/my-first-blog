# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-22 02:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_trade'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Trade',
        ),
    ]
