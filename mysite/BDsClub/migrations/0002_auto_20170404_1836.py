# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDsClub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='pid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apply',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
