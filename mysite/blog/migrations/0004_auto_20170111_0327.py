# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 03:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('blog', '0003_blogdirpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdirpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='BlogDirPage',
        ),
        migrations.DeleteModel(
            name='BlogPage',
        ),
    ]
