# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150615_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForesightApproaches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('sort_id', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'ordering': ('sort_id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('code', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_title', models.CharField(max_length=255, verbose_name=b'title')),
                ('text', models.TextField(null=True, verbose_name=b'text', blank=True)),
                ('file_id', models.FileField(default=b'', upload_to=b'outcomes', max_length=256, blank=True, null=True, verbose_name=b'File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhasesOfPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('sort_id', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'ordering': ('sort_id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('user_id', models.CharField(max_length=64, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'title in English')),
                ('url', models.URLField(blank=True)),
                ('study_type', models.CharField(max_length=128, null=True, verbose_name=b'I want to add a new', choices=[(b'activity', b'Forward looking activity'), (b'assessment', b'Assessment')])),
                ('blossom', models.IntegerField(default=0, verbose_name=b'Approach to assessment', choices=[(1, b'BLOSSOM study'), (0, b'other study')])),
                ('requested_by', models.CharField(blank=True, max_length=64, verbose_name=b'who requested the study?', choices=[(b'eea', b'EEA'), (b'other', b'Other')])),
                ('start_date', models.DateField(null=True, verbose_name=b'start date', blank=True)),
                ('end_date', models.DateField(verbose_name=b'end date')),
                ('lead_author', models.TextField(verbose_name=b'lead author')),
                ('other', models.TextField(verbose_name=b'other organisations/authors or contact persons', blank=True)),
                ('purpose_and_target', models.CharField(blank=True, max_length=128, verbose_name=b'purpose and target audience', choices=[(b'policy', b'Support to policy'), (b'non_policy', b'Non-policy (research, civil initiative, NGOs...')])),
                ('additional_information', models.TextField(verbose_name=b'additional information', blank=True)),
                ('additional_information_phase', models.TextField(verbose_name=b'additional information about the application', blank=True)),
                ('additional_information_foresight', models.TextField(verbose_name=b'additional information', blank=True)),
                ('stakeholder_participation', models.BooleanField(default=False, verbose_name=b'stakeholder participation')),
                ('additional_information_stakeholder', models.TextField(verbose_name=b'additional information about stakeholder involvement', blank=True)),
                ('countries', models.ManyToManyField(to='common.Country', verbose_name=b'countries', blank=True)),
                ('environmental_themes', models.ManyToManyField(to='common.EnvironmentalTheme', verbose_name=b'topics', blank=True)),
                ('foresight_approaches', models.ManyToManyField(to='flip.ForesightApproaches', verbose_name=b'foresight approaches used')),
                ('geographical_scope', models.ForeignKey(verbose_name=b'geographical scope', blank=True, to='common.GeographicalScope', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'title in original language')),
                ('language', models.ForeignKey(verbose_name=b'language of the study', to='flip.Language')),
                ('study', models.ForeignKey(to='flip.Study')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeOfOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('blossom', models.BooleanField(default=False)),
                ('doc_type', models.CharField(default=b'all', max_length=128, null=True, verbose_name=b'Type', choices=[(b'all', b'All'), (b'activity', b'Forward looking activity'), (b'assessment', b'Assessment')])),
                ('sort_id', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
                'ordering': ('sort_id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='study',
            name='languages',
            field=models.ManyToManyField(to='flip.Language', verbose_name=b'language of the study', through='flip.StudyLanguage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='study',
            name='phase_of_policy',
            field=models.ForeignKey(verbose_name=b'phases of policy cycle', blank=True, to='flip.PhasesOfPolicy', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='outcome',
            name='study',
            field=models.ForeignKey(related_name=b'outcomes', to='flip.Study'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='outcome',
            name='type_of_outcome',
            field=models.ForeignKey(verbose_name=b'type of output', blank=True, to='flip.TypeOfOutcome', null=True),
            preserve_default=True,
        ),
    ]
