# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0006_auto_20150920_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='org',
            old_name='tags',
            new_name='oldtags',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='tags',
            new_name='oldtags',
        ),
        migrations.AlterField(
            model_name='document',
            name='org',
            field=models.ForeignKey(related_name='org_doc', blank=True, to='rolodex.Org', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='person',
            field=models.ForeignKey(related_name='person_doc', blank=True, to='rolodex.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='ethnicity',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'Hispanic', b'Hispanic'), (b'Non-Hispanic', b'Non-Hispanic')]),
            preserve_default=True,
        ),
    ]
