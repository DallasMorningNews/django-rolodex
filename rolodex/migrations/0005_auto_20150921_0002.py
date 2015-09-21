# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0004_auto_20150920_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchlog',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='searchlog',
            name='datestamp',
            field=models.DateField(auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='race',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'White'), (2, b'Black'), (3, b'American Indian'), (4, b'Asian'), (5, b'Native Hawaiian and other Pacific Islander'), (6, b'Other'), (7, b'Two or more races')]),
            preserve_default=True,
        ),
    ]
