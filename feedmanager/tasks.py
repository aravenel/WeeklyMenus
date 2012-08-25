import json
import datetime
from recipemanager.tasks import add_recipe
from celery.task import task
from celery import group
import requests

@task
def update_feed(feed, request):
    pass

@task
def update_feed_pinboard(feed, request):
    """Get pinboard feed of recipes and kick of subtasks to process them"""
    feed_time = feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
    feed_url = 'https://api.pinboard.in/v1/posts/all?auth_token=%s&tag=%s&format=json&fromdt=%s' % (
            feed.feed_apikey, feed.feed_tag_key, feed_time)
    
    r = requests.get(feed_url)
    if r.status_code == 200:
        recipes = json.loads(r.content)
        #List to hold all subtasks for celery task group
        #recipe_tasks = []
        #for recipe in recipes:
            ##Get the required information
            #url = recipe['href']
            #title = recipe['description']
            #owner = request.user
            #source = 'pinboard'
            #tags = recipe['tags']

            ##Instantiate the task and add it to list for group
            #recipe_task = add_recipe(url, title, owner,
                    #source, tags)
            #recipe_tasks.append(recipe_task)

        #Mark completion time so that we know when feed was updated
        #NOTE: This leaves small gap of time b/t calling of task and finishing
        #of task where new recipes could be added but not picked up!
        feed.updated = datetime.datetime.utcnow()
        feed.save()

        #Call group of subtasks
        job = group(
                add_recipe.s(recipe['href'], recipe['description'],
                    request.user, 'pinboard', recipe['tags'])
                for recipe in recipes
                )
        result = job.apply_async()
