"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.utils import setup_test_environment
from models import Recipe
import datetime


def create_recipe():
	pass

class RecipeTestCase(TestCase):
	# def setUp(self):
	# 	Recipe.objects.create(
	# 		url = 'http://www.google.com',
	# 	    title = 'test title'
	# 	    added = datetime.datetime.now()
	# 	    made_count = datetime.datetime.now()
	# 	    comments = 'Test comments'
	# 	    owner = None
	# 	    #Used for hash of recipe title (e.g. from Pinboard)--used for dupe detection
	# 	    hash = 'test hash'
	# 	    source = 'Test source'
	# 	    rating = 5
	# 	    content = 'Test content'
	# 	    image = None
	# 		)
	
	def test_recipe_view_all(self):
		pass