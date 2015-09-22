# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import rolodex.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, choices=[(b'email', b'email'), (b'phone', b'phone'), (b'link', b'link'), (b'address', b'address')])),
                ('contact', models.CharField(max_length=250, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc', models.FileField(null=True, upload_to=rolodex.models.upload_doc_directory, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenRecordsLaw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('name', models.CharField(max_length=250)),
                ('link', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('orgName', models.CharField(max_length=200)),
                ('notes', models.TextField(null=True, blank=True)),
                ('last_edited_by', models.CharField(max_length=250, null=True, blank=True)),
                ('openRecordsLaw', models.ForeignKey(blank=True, to='rolodex.OpenRecordsLaw', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org2Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(null=True, blank=True)),
                ('to_date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('hierarchy', models.CharField(default=b'none', max_length=10, choices=[(b'parent', b'parent'), (b'child', b'child'), (b'none', b'none')])),
                ('from_ent', models.ForeignKey(related_name='org_from_org', to='rolodex.Org')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org2Org_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('relationship_type', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Org2P',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(null=True, blank=True)),
                ('to_date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('from_ent', models.ForeignKey(related_name='p_from_org', to='rolodex.Org')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrgContactRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('role', models.CharField(max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='P2Org',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(null=True, blank=True)),
                ('to_date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='P2Org_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('relationship_type', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='P2P',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(null=True, blank=True)),
                ('to_date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='P2P_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('relationship_type', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('lastName', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=250, null=True, blank=True)),
                ('department', models.CharField(max_length=250, null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=250, null=True, choices=[(b'Female', b'Female'), (b'Male', b'Male'), (b'Other', b'Other')])),
                ('birthdate', models.CharField(max_length=50, null=True, blank=True)),
                ('race', models.CharField(blank=True, max_length=250, null=True, choices=[(b'White', b'White'), (b'Black', b'Black'), (b'American Indian', b'American Indian'), (b'Asian', b'Asian'), (b'Native Hawaiian and other Pacific Islander', b'Native Hawaiian and other Pacific Islander'), (b'Other', b'Other'), (b'Two or more races', b'Two or more races')])),
                ('ethnicity', models.CharField(blank=True, max_length=250, null=True, choices=[(b'Hispanic', b'Hispanic'), (b'Non-Hispanic', b'Non-Hispanic')])),
                ('notes', models.TextField(null=True, blank=True)),
                ('last_edited_by', models.CharField(max_length=250, null=True, blank=True)),
                ('org_relations', models.ManyToManyField(related_name='people', through='rolodex.P2Org', to='rolodex.Org', blank=True)),
                ('p_relations', models.ManyToManyField(related_name='+', through='rolodex.P2P', to='rolodex.Person', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, editable=False)),
                ('role', models.CharField(max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
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
                ('datestamp', models.DateField(auto_now=True)),
                ('org', models.ForeignKey(related_name='org_log', blank=True, editable=False, to='rolodex.Org', null=True)),
                ('person', models.ForeignKey(related_name='person_log', blank=True, editable=False, to='rolodex.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(related_name='person_role', blank=True, to='rolodex.PersonRole', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='from_ent',
            field=models.ForeignKey(related_name='p_from_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='relation',
            field=models.ForeignKey(related_name='p2p_relation', blank=True, to='rolodex.P2P_Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='to_ent',
            field=models.ForeignKey(related_name='p_to_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='from_ent',
            field=models.ForeignKey(related_name='org_from_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='relation',
            field=models.ForeignKey(related_name='p2org_relation', blank=True, to='rolodex.P2Org_Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='to_ent',
            field=models.ForeignKey(related_name='p_to_org', to='rolodex.Org'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2p',
            name='relation',
            field=models.ForeignKey(related_name='org2p_relation', blank=True, to='rolodex.P2Org_Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2p',
            name='to_ent',
            field=models.ForeignKey(related_name='org_to_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2org',
            name='relation',
            field=models.ForeignKey(related_name='org2org_relation', blank=True, to='rolodex.Org2Org_Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2org',
            name='to_ent',
            field=models.ForeignKey(related_name='org_to_org', to='rolodex.Org'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='org_relations',
            field=models.ManyToManyField(related_name='+', through='rolodex.Org2Org', to='rolodex.Org', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='p_relations',
            field=models.ManyToManyField(related_name='orgs', through='rolodex.Org2P', to='rolodex.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='org',
            field=models.ForeignKey(related_name='org_doc', blank=True, to='rolodex.Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='person',
            field=models.ForeignKey(related_name='person_doc', blank=True, to='rolodex.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='org',
            field=models.ForeignKey(related_name='org_contact', blank=True, editable=False, to='rolodex.Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='person',
            field=models.ForeignKey(related_name='person_contact', blank=True, editable=False, to='rolodex.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.ForeignKey(blank=True, to='rolodex.OrgContactRole', null=True),
            preserve_default=True,
        ),
    ]
