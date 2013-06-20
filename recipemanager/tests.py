"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Recipe
import datetime


def create_recipe(url='http://www.google.com', title='test title', comments='test comments', owner=None, hash='test hash', source='test source', rating=5, content='test content', image=None):
		return Recipe.objects.create(
			url = url,
		    title = title,
		    made_count = 0,
		    comments = comments,
		    owner = owner,
		    #Used for hash of recipe title (e.g. from Pinboard)--used for dupe detection
		    hash = hash,
		    source = source,
		    rating = rating,
		    content = content,
		    image = image,
			)


class RecipeTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
		self.client.login(username='testuser', password='testpass')
	
	#
	#	ALL VIEW TESTS
	#
	def test_all_view_no_recipes(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)

	def test_all_view_with_recipes(self):
		recipe = create_recipe(owner=self.user)
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 1)

	def test_all_view_change_per_page(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)

	def test_all_view_sort_title(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)

	def test_all_view_sort_made_count(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)

	def test_all_view_sort_last_made(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)

	def test_all_view_sort_rating(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 0)
