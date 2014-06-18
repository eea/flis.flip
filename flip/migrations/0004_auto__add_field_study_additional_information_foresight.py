# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Study.additional_information_foresight'
        db.add_column(u'flip_study', 'additional_information_foresight',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Study.additional_information_foresight'
        db.delete_column(u'flip_study', 'additional_information_foresight')


    models = {
        u'flip.country': {
            'Meta': {'object_name': 'Country'},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.environmentaltheme': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'EnvironmentalTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.foresightapproaches': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'ForesightApproaches'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.geographicalscope': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'GeographicalScope'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'require_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'flip.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'flip.outcome': {
            'Meta': {'object_name': 'Outcome'},
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
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.Country']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'environmental_themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.EnvironmentalTheme']", 'symmetrical': 'False', 'blank': 'True'}),
            'foresight_approaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.ForesightApproaches']", 'symmetrical': 'False'}),
            'geographical_scope': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.GeographicalScope']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flip.Language']", 'through': u"orm['flip.StudyLanguage']", 'symmetrical': 'False'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'lead_author': ('django.db.models.fields.TextField', [], {}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phases_of_policy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flip.PhasesOfPolicy']", 'null': 'True', 'blank': 'True'}),
            'purpose_and_target': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'requested_by': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'stakeholder_participation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "('-pk',)", 'object_name': 'TypeOfOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['flip']