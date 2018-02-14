# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsite', '0004_auto_20171215_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='tumblr_uri',
            field=models.CharField(default=b'', max_length=254, blank=True),
        ),
    ]
