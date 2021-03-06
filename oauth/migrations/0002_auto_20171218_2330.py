# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_id',
            field=models.CharField(editable=False, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='scope',
            field=models.TextField(blank=True, help_text='Requested scopes, space separated'),
        ),
    ]
