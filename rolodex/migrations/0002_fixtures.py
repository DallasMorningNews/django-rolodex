# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def initial_data(apps, schema_editor):
	P2Org_Type = apps.get_model('rolodex','P2Org_Type')
	P2Org_Type.objects.get_or_create(relationship_type='employment')

	OrgContactRole = apps.get_model('rolodex','OrgContactRole')
	OrgContactRole.objects.get_or_create(role='public records contact',description="A contact to receive public records requests.")

	PersonRole = apps.get_model('rolodex','PersonRole')
	PersonRole.objects.get_or_create(role='public information officer', description="A person responsible for fielding public records requests.")

class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(initial_data,)
    ]
