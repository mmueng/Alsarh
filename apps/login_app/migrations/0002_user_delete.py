# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-22 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='delete',
            field=models.CharField(default='active', max_length=255),
            preserve_default=False,
        ),
    ]
