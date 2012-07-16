# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Podcast'
        db.create_table('podcasts_podcast', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('podcasts', ['Podcast'])

        # Adding model 'RssFeed'
        db.create_table('podcasts_rssfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('podcast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcasts.Podcast'])),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('podcasts', ['RssFeed'])

        # Adding model 'Episode'
        db.create_table('podcasts_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('podcast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcasts.Podcast'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('raw_description', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('podcasts', ['Episode'])

        # Adding model 'MultimediaFile'
        db.create_table('podcasts_multimediafile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcasts.Episode'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('podcasts', ['MultimediaFile'])


    def backwards(self, orm):
        # Deleting model 'Podcast'
        db.delete_table('podcasts_podcast')

        # Deleting model 'RssFeed'
        db.delete_table('podcasts_rssfeed')

        # Deleting model 'Episode'
        db.delete_table('podcasts_episode')

        # Deleting model 'MultimediaFile'
        db.delete_table('podcasts_multimediafile')


    models = {
        'podcasts.episode': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Episode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'podcast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Podcast']"}),
            'raw_description': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'podcasts.multimediafile': {
            'Meta': {'object_name': 'MultimediaFile'},
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'podcasts.podcast': {
            'Meta': {'ordering': "['name']", 'object_name': 'Podcast'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'podcasts.rssfeed': {
            'Meta': {'object_name': 'RssFeed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'podcast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['podcasts.Podcast']"}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['podcasts']