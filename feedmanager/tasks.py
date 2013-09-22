import datetime
from recipemanager.tasks import add_recipe
from celery.task import task
from celery import group
from celery.utils.log import get_task_logger
from feedmanager.models import RecipeFeed
import requests

log = get_task_logger(__name__)

@task
def update_feed(feed, request):
    pass

@task
def update_feed_pinboard(feed_id, session=None):
    """Get pinboard feed of recipes and kick of subtasks to process them"""
    feed_url = 'https://api.pinboard.in/v1/posts/all'
    log.debug("Updating feed ID %s" % feed_id)
    try:
        feed = RecipeFeed.objects.get(pk=feed_id)
        log.info('Updating pinboard feed for user %s' % feed.owner.username)
        if feed.updated is not None:
            log.info("Feed last updated at %s" % feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ'))
            feed_time = feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            log.info("Feed has never been updated.")
            feed_time = None

        payload = {
            'auth_token': feed.feed_apikey,
            'tag': feed.feed_tag_key,
            'format': 'json'
        }

        if feed_time:
            payload['fromdt'] = feed_time

        #Hit API
        r = requests.get(feed_url, params=payload)
        log.debug("Request returned with status code %s" % r.status_code)

        if r.status_code == 200:
            recipes = r.json()
            log.info("%s NEW RECIPES FROM PINBOARD" % len(recipes))

            #Mark completion time so that we know when feed was updated
            #NOTE: This leaves small gap of time b/t calling of task and finishing
            #of task where new recipes could be added but not picked up!
            feed.updated = datetime.datetime.utcnow()
            feed.save()

            if len(recipes) > 0:
                #Call group of subtasks
                job = group(
                        [add_recipe.s(recipe['href'], recipe['description'],
                            feed.owner, 'pinboard', recipe['hash'], recipe['tags'].split(" "))
                        for recipe in recipes]
                        )

                log.debug("STARTING NEW RECIPE SUBTASKS")
                result = job.apply_async()
                result.save()
                feed.celery_task_id = result.id
            else:
                feed.celery_task_id = 0
            feed.save()

    except RecipeFeed.DoesNotExist:
        log.error("Recipe feed with id %s does not exist." % feed_id)
