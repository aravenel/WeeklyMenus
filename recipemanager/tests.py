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


def create_recipe(url='http://www.google.com', title='test title', made_count=0, comments='test comments', owner=None, hash='test hash', source='test source', rating=5, content='test content', image=None, last_made=None):
		return Recipe.objects.create(
			url = url,
		    title = title,
		    made_count = made_count,
		    comments = comments,
		    owner = owner,
		    #Used for hash of recipe title (e.g. from Pinboard)--used for dupe detection
		    hash = hash,
		    source = source,
		    rating = rating,
		    content = content,
		    image = image,
		    last_made = last_made,
			)


class RecipeTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
		self.client.login(username='testuser', password='testpass')
	
		for i in range(200):
			recipe = create_recipe(owner=self.user)
	#
	#	ALL VIEW TESTS
	#
	def test_all_view_base(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)

	def test_all_view_with_recipes(self):
		response = self.client.get(reverse('recipemanager.views.all'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 20)

	def test_all_view_change_per_page(self):
		url = reverse('recipemanager.views.all')
		response = self.client.get('%s?perpage=40' % url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['recipes']), 40)

	def test_all_view_sort_title(self):
		url = reverse('recipemanager.views.all')
		recipe = create_recipe(owner=self.user, title='000')
		response = self.client.get('%s?sort=title' % url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['recipes'][0].title, '000')

	def test_all_view_sort_made_count(self):
		url = reverse('recipemanager.views.all')
		recipe = create_recipe(owner=self.user, title='111', made_count=4)
		response = self.client.get('%s?sort=made_count' % url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['recipes'][0].title, '111')

	def test_all_view_sort_last_made(self):
		ts = datetime.datetime.now()
		url = reverse('recipemanager.views.all')
		recipe = create_recipe(owner=self.user, title='222', last_made=ts)
		response = self.client.get('%s?sort=last_made' % url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['recipes'][0].title, '222')

	def test_all_view_sort_rating(self):
		url = reverse('recipemanager.views.all')
		recipe = create_recipe(owner=self.user, title='333', rating=5)
		response = self.client.get('%s?sort=rating' % url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['recipes'][0].title, '333')

	def test_view_view(self):
		recipe = Recipe.objects.all()[0]
		url = reverse('recipemanager.views.view', args=[recipe.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
