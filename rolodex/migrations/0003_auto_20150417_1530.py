# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0002_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='last_edited_by',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='last_edited_by',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
