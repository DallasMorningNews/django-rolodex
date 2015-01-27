# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.conf import settings

def initial_data(apps, schema_editor):
	if settings.DATABASES.has_key('rolodex'):
		if not schema_editor.connection.alias == 'rolodex':
			return
	else:
		if not schema_editor.connection.alias == 'default':
			return
	P2Org_Type = apps.get_model('rolodex','P2Org_Type')
	P2Org_Type.objects.get_or_create(slug='employment',relationship_type='employment')

	OrgContactRole = apps.get_model('rolodex','OrgContactRole')
	OrgContactRole.objects.get_or_create(slug='public-records-contact',role='public records contact',description="A contact to receive public records requests.")

	PersonRole = apps.get_model('rolodex','PersonRole')
	PersonRole.objects.get_or_create(slug='public-information-officer',role='public information officer', description="A person responsible for fielding public records requests.")

class Migration(migrations.Migration):

	dependencies = [
		('rolodex', '0001_initial'),
	]

	operations = [
		migrations.RunPython(initial_data),
	]
