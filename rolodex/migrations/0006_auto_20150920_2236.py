# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0005_auto_20150921_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='ethnicity',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'Hispanic', b'Hispanic'), (b'Not Hispanic', b'Not Hispanic')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'Female', b'Female'), (b'Male', b'Male'), (b'Other', b'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='race',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'White', b'White'), (b'Black', b'Black'), (b'American Indian', b'American Indian'), (b'Asian', b'Asian'), (b'Native Hawaiian and other Pacific Islander', b'Native Hawaiian and other Pacific Islander'), (b'Other', b'Other'), (b'Two or more races', b'Two or more races')]),
            preserve_default=True,
        ),
    ]
