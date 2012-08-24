import json
from feedmanager.models import RecipeFeed
from recipemanager.models import Recipe
from celery.task import task
import requests

@task
def update_feed(feed, request):
    pass

@task
def update_feed_pinboard(feed, request):
    """Get pinboard feed of recipes and kick of subtasks to process them"""
    user = request.user
    feed_url = 'https://api.pinboard.in/v1/posts/all?auth_token=%s&tag=%s&format=json' % (
            feed.feed_apikey, feed.feed_tag_key
            )
    
    r = request.get(feed_url)
    if r.status_code == 200:
        recipes = json.loads(r.content)
        for recipe in recipes['posts']:
            pass
