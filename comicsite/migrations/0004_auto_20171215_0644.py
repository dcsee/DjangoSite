# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsite', '0003_auto_20171215_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='hover_text',
            field=models.CharField(default=b'', max_length=160, blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image_path',
            field=models.CharField(default=b'', unique=True, max_length=160, blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail_path',
            field=models.CharField(default=b'', unique=True, max_length=160, blank=True),
        ),
    ]
