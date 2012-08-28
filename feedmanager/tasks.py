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
def update_feed_pinboard(feed, user):
    """Get pinboard feed of recipes and kick of subtasks to process them"""
    if feed.updated is not None:
        print "Feed last updated at %s" % feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
        feed_time = feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
        feed_url = 'https://api.pinboard.in/v1/posts/all?auth_token=%s&tag=%s&format=json&fromdt=%s' % (
                feed.feed_apikey, feed.feed_tag_key, feed_time)
    else:
        print "Feed has never been updated."
        feed_url = 'https://api.pinboard.in/v1/posts/all?auth_token=%s&tag=%s&format=json' % (
                feed.feed_apikey, feed.feed_tag_key)


    #Hit API
    r = requests.get(feed_url)

    if r.status_code == 200:
        recipes = json.loads(r.content)
        print "%s NEW RECIPES FROM PINBOARD" % len(recipes)

        #Mark completion time so that we know when feed was updated
        #NOTE: This leaves small gap of time b/t calling of task and finishing
        #of task where new recipes could be added but not picked up!
        feed.updated = datetime.datetime.utcnow()
        feed.save()

        if len(recipes) > 0:
            #Call group of subtasks
            job = group(
                    [add_recipe.s(recipe['href'], recipe['description'],
                        user, 'pinboard', recipe['hash'], recipe['tags'])
                    for recipe in recipes]
                    )

            print "STARTING NEW RECIPE SUBTASKS"
            result = job.apply_async()
