# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-09 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_twitterpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterusers',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]