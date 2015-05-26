# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Study'
        db.create_table(u'flip_study', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('study_type', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('blossom', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('requested_by', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('lead_author', self.gf('django.db.models.fields.TextField')()),
            ('other', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('purpose_and_target', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('additional_information', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('phase_of_policy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flip.PhasesOfPolicy'], null=True, blank=True)),
            ('additional_information_phase', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('additional_information_foresight', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('stakeholder_participation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('additional_information_stakeholder', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('geographical_scope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeographicalScope'], null=True, blank=True)),
        ))
        db.send_create_signal(u'flip', ['Study'])

        # Adding M2M table for field foresight_approaches on 'Study'
        m2m_table_name = db.shorten_name(u'flip_study_foresight_approaches')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('study', models.ForeignKey(orm[u'flip.study'], null=False)),
            ('foresightapproaches', models.ForeignKey(orm[u'flip.foresightapproaches'], null=False))
        ))
        db.create_unique(m2m_table_name, ['study_id', 'foresightapproaches_id'])

        # Adding M2M table for field environmental_themes on 'Study'
        m2m_table_name = db.shorten_name(u'flip_study_environmental_themes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('study', models.ForeignKey(orm[u'flip.study'], null=False)),
            ('environmentaltheme', models.ForeignKey(orm[u'common.environmentaltheme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['study_id', 'environmentaltheme_id'])

        # Adding M2M table for field countries on 'Study'
        m2m_table_name = db.shorten_name(u'flip_study_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('study', models.ForeignKey(orm[u'flip.study'], null=False)),
            ('country', models.ForeignKey(orm[u'common.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['study_id', 'country_id'])

        # Adding model 'Outcome'
        db.create_table(u'flip_outcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('study', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outcomes', to=orm['flip.Study'])),
            ('type_of_outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flip.TypeOfOutcome'], null=True, blank=True)),
            ('content_topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flip.ContentTopic'], null=True, blank=True)),
            ('document_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('file_id', self.gf('django.db.models.fields.files.FileField')(default='', max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'flip', ['Outcome'])

        # Adding model 'Language'
        db.create_table(u'flip_language', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'flip', ['Language'])

        # Adding model 'StudyLanguage'
        db.create_table(u'flip_studylanguage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flip.Language'])),
            ('study', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flip.Study'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'flip', ['StudyLanguage'])

        # Adding model 'PhasesOfPolicy'
        db.create_table(u'flip_phasesofpolicy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'flip', ['PhasesOfPolicy'])

        # Adding model 'ForesightApproaches'
        db.create_table(u'flip_foresightapproaches', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'flip', ['ForesightApproaches'])

        # Adding model 'TypeOfOutcome'
        db.create_table(u'flip_typeofoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('blossom', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('doc_type', self.gf('django.db.models.fields.CharField')(default='any', max_length=64)),
        ))
        db.send_create_signal(u'flip', ['TypeOfOutcome'])

        # Adding model 'ContentTopic'
        db.create_table(u'flip_contenttopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'flip', ['ContentTopic'])


    def backwards(self, orm):
        # Deleting model 'Study'
        db.delete_table(u'flip_study')

        # Removing M2M table for field foresight_approaches on 'Study'
        db.delete_table(db.shorten_name(u'flip_study_foresight_approaches'))

        # Removing M2M table for field environmental_themes on 'Study'
        db.delete_table(db.shorten_name(u'flip_study_environmental_themes'))

        # Removing M2M table for field countries on 'Study'
        db.delete_table(db.shorten_name(u'flip_study_countries'))

        # Deleting model 'Outcome'
        db.delete_table(u'flip_outcome')

        # Deleting model 'Language'
        db.delete_table(u'flip_language')

        # Deleting model 'StudyLanguage'
        db.delete_table(u'flip_studylanguage')

        # Deleting model 'PhasesOfPolicy'
        db.delete_table(u'flip_phasesofpolicy')

        # Deleting model 'ForesightApproaches'
        db.delete_table(u'flip_foresightapproaches')

        # Deleting model 'TypeOfOutcome'
        db.delete_table(u'flip_typeofoutcome')

        # Deleting model 'ContentTopic'
        db.delete_table(u'flip_contenttopic')


    models = {
        u'common.country': {
            'Meta': {'object_name': 'Country'},
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'common.environmentaltheme': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'EnvironmentalTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'common.geographicalscope': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'GeographicalScope'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'require_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.contenttopic': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'ContentTopic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'flip.foresightapproaches': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'ForesightApproaches'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'flip.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'content_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.ContentTopic']", 'null': 'True', 'blank': 'True'}),
            'document_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_id': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outcomes'", 'to': u"orm['flip.Study']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.TypeOfOutcome']", 'null': 'True', 'blank': 'True'})
        },
        u'flip.phasesofpolicy': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'PhasesOfPolicy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.study': {
            'Meta': {'object_name': 'Study'},
            'additional_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_information_foresight': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_information_phase': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_information_stakeholder': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'blossom': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Country']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'environmental_themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.EnvironmentalTheme']", 'symmetrical': 'False', 'blank': 'True'}),
            'foresight_approaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.ForesightApproaches']", 'symmetrical': 'False'}),
            'geographical_scope': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.GeographicalScope']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.Language']", 'through': u"orm['flip.StudyLanguage']", 'symmetrical': 'False'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'lead_author': ('django.db.models.fields.TextField', [], {}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phase_of_policy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.PhasesOfPolicy']", 'null': 'True', 'blank': 'True'}),
            'purpose_and_target': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'requested_by': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'stakeholder_participation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'study_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'flip.studylanguage': {
            'Meta': {'object_name': 'StudyLanguage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.Language']"}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.Study']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'flip.typeofoutcome': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'TypeOfOutcome'},
            'blossom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doc_type': ('django.db.models.fields.CharField', [], {'default': "'any'", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['flip']