# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table('menumanager_menu')

        # Adding field 'MenuItem.menu_date'
        db.add_column('menumanager_menuitem', 'menu_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 8, 9, 0, 0)),
                      keep_default=False)

        # Adding field 'MenuItem.menu_type'
        db.add_column('menumanager_menuitem', 'menu_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


        # Changing field 'MenuItem.menu'
        db.alter_column('menumanager_menuitem', 'menu_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menumanager.WeeklyMenu']))

    def backwards(self, orm):
        # Adding model 'Menu'
        db.create_table('menumanager_menu', (
            ('menu_type', self.gf('django.db.models.fields.IntegerField')()),
            ('weekly_menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menumanager.WeeklyMenu'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('menumanager', ['Menu'])

        # Deleting field 'MenuItem.menu_date'
        db.delete_column('menumanager_menuitem', 'menu_date')

        # Deleting field 'MenuItem.menu_type'
        db.delete_column('menumanager_menuitem', 'menu_type')


        # Changing field 'MenuItem.menu'
        db.alter_column('menumanager_menuitem', 'menu_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menumanager.Menu']))

    models = {
        'menumanager.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menumanager.WeeklyMenu']"}),
            'menu_date': ('django.db.models.fields.DateField', [], {}),
            'menu_type': ('django.db.models.fields.IntegerField', [], {}),
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