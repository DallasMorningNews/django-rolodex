# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def initial_data(apps, schema_editor):
	p2org_type = apps.get_model('rolodex','p2org_type')
	p2org_type.objects.get_or_create(relationship_type='employment')


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(initial_data,)
    ]
