# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
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
            name='openRecordsLaw',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
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
                ('orgName', models.CharField(max_length=200)),
                ('openRecordsLaw', models.ForeignKey(blank=True, to='rolodex.openRecordsLaw', null=True)),
            ],
            options={
                'permissions': (('delete_org', 'Can delete organizations.'),),
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
                ('from_ent', models.ForeignKey(related_name=b'org_from_org', to='rolodex.Org')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='org2org_type',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
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
                ('from_ent', models.ForeignKey(related_name=b'p_from_org', to='rolodex.Org')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='org_contact_role',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
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
            name='p2org_type',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
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
            name='p2p_type',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
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
                ('lastName', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=250, null=True, blank=True)),
                ('department', models.CharField(max_length=250, null=True, blank=True)),
                ('gender', models.IntegerField(blank=True, null=True, choices=[(1, b'Female'), (2, b'Male'), (3, b'Other')])),
                ('org_relations', models.ManyToManyField(related_name=b'people', through='rolodex.P2Org', to='rolodex.Org', blank=True)),
                ('p_relations', models.ManyToManyField(related_name=b'+', through='rolodex.P2P', to='rolodex.Person', blank=True)),
            ],
            options={
                'permissions': (('delete_person', 'Can delete people.'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
                ('role', models.CharField(max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.CharField(max_length=250, serialize=False, editable=False, primary_key=True)),
                ('tag_name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(related_name=b'person_role', blank=True, to='rolodex.role', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(to='rolodex.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='from_ent',
            field=models.ForeignKey(related_name=b'p_from_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='relation',
            field=models.ForeignKey(related_name=b'p2p_relation', blank=True, to='rolodex.p2p_type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2p',
            name='to_ent',
            field=models.ForeignKey(related_name=b'p_to_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='from_ent',
            field=models.ForeignKey(related_name=b'org_from_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='relation',
            field=models.ForeignKey(related_name=b'p2org_relation', blank=True, to='rolodex.p2org_type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='p2org',
            name='to_ent',
            field=models.ForeignKey(related_name=b'p_to_org', to='rolodex.Org'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2p',
            name='relation',
            field=models.ForeignKey(related_name=b'org2p_relation', blank=True, to='rolodex.p2org_type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2p',
            name='to_ent',
            field=models.ForeignKey(related_name=b'org_to_p', to='rolodex.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2org',
            name='relation',
            field=models.ForeignKey(related_name=b'org2org_relation', blank=True, to='rolodex.org2org_type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org2org',
            name='to_ent',
            field=models.ForeignKey(related_name=b'org_to_org', to='rolodex.Org'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='org_relations',
            field=models.ManyToManyField(related_name=b'+', through='rolodex.Org2Org', to='rolodex.Org', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='p_relations',
            field=models.ManyToManyField(related_name=b'orgs', through='rolodex.Org2P', to='rolodex.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='org',
            name='tags',
            field=models.ManyToManyField(to='rolodex.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='org',
            field=models.ForeignKey(related_name=b'contact_org', blank=True, editable=False, to='rolodex.Org', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='person',
            field=models.ForeignKey(related_name=b'contact_person', blank=True, editable=False, to='rolodex.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.ForeignKey(blank=True, to='rolodex.org_contact_role', null=True),
            preserve_default=True,
        ),
    ]
