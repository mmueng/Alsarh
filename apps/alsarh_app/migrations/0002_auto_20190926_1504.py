# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-26 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('alsarh_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.DateField(default='1999-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='joined_users',
            field=models.ManyToManyField(related_name='joined_order', to='login_app.User'),
        ),
    ]
