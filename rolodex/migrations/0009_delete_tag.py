# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0008_auto_20150921_0836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
