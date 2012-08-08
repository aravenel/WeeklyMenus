# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeeklyMenu'
        db.create_table('menumanager_weeklymenu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('menumanager', ['WeeklyMenu'])

        # Adding model 'Menu'
        db.create_table('menumanager_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weekly_menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menumanager.WeeklyMenu'])),
            ('menu_date', self.gf('django.db.models.fields.DateField')()),
            ('menu_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('menumanager', ['Menu'])

        # Adding model 'MenuItem'
        db.create_table('menumanager_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menumanager.Menu'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipemanager.Recipe'])),
        ))
        db.send_create_signal('menumanager', ['MenuItem'])


    def backwards(self, orm):
        # Deleting model 'WeeklyMenu'
        db.delete_table('menumanager_weeklymenu')

        # Deleting model 'Menu'
        db.delete_table('menumanager_menu')

        # Deleting model 'MenuItem'
        db.delete_table('menumanager_menuitem')


    models = {
        'menumanager.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_date': ('django.db.models.fields.DateField', [], {}),
            'menu_type': ('django.db.models.fields.IntegerField', [], {}),
            'weekly_menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menumanager.WeeklyMenu']"})
        },
        'menumanager.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menumanager.Menu']"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipemanager.Recipe']"})
        },
        'menumanager.weeklymenu': {
            'Meta': {'object_name': 'WeeklyMenu'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'recipemanager.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_made': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'made_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['menumanager']