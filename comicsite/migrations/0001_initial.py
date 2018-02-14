# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=161)),
                ('subtitle', models.CharField(max_length=160)),
                ('hover_text', models.CharField(max_length=160)),
                ('description', models.TextField()),
                ('category', models.CharField(default=b'uncategorized', max_length=40)),
                ('tags', models.CharField(max_length=160)),
                ('image_path', models.CharField(unique=True, max_length=160)),
                ('thumbnail_path', models.CharField(max_length=160, unique=True, null=True)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, unique=True)),
            ],
        ),
    ]
