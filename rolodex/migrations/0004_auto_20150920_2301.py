# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rolodex.models


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0003_auto_20150417_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc', models.FileField(null=True, upload_to=rolodex.models.upload_doc_directory, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('org', models.ForeignKey(related_name='org_doc', blank=True, editable=False, to='rolodex.Org', null=True)),
                ('person', models.ForeignKey(related_name='person_doc', blank=True, editable=False, to='rolodex.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=250)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('org', models.ForeignKey(related_name='org_log', blank=True, editable=False, to='rolodex.Org', null=True)),
                ('person', models.ForeignKey(related_name='person_log', blank=True, editable=False, to='rolodex.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='birthdate',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='ethnicity',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Hispanic'), (2, b'Not Hispanic')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='race',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'White'), (2, b'Black'), (3, b'American Indian'), (4, b'Asian'), (5, b'Native Hawaiian and Other Pacific Islander'), (6, b'Other'), (7, b'Two or More Races')]),
            preserve_default=True,
        ),
    ]
