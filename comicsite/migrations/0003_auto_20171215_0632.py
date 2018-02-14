# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsite', '0002_blogpost_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='hover_text',
            field=models.CharField(max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image_path',
            field=models.CharField(max_length=160, unique=True, null=True),
        ),
    ]
