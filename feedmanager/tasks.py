from recipemanager.tasks import add_recipe
from django.utils import timezone
from celery.task import task
from celery import group
from celery.utils.log import get_task_logger
from feedmanager.models import RecipeFeed
import requests
import datetime
import pytz

log = get_task_logger(__name__)

@task
def update_all_feeds(*args, **kwargs):
    log.info('UPDATING ALL FEEDS')
    log.debug('%s FEEDS TO UPDATE' % len(RecipeFeed.objects.all()))
    job = group([update_feed_pinboard.s(feed.id) for feed in RecipeFeed.objects.all()])
    job.apply_async()

@task
def update_feed_pinboard(feed_id):
    """Get pinboard feed of recipes and kick of subtasks to process them"""

    def get_last_update():
        """Check to see when last recipe added to pinboard. Return Datetime obj for this time or None"""
        timestamp_url = 'https://api.pinboard.in/v1/posts/update'
        payload = {
            'auth_token': feed.feed_apikey,
            'format': 'json',
        }

        r = requests.get(timestamp_url, params=payload)
        if r.status_code == 200:
            dt = datetime.datetime.strptime(r.json()['update_time'], "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.replace(tzinfo=pytz.utc)
            return dt
        else:
            log.error('Pinboard returned response code %s when trying to get last update time.' % r.status_code)
            return None

    def new_recipes(feed):
        """Return True if there are new recipes on Pinboard"""
        last_update = get_last_update()
        if last_update > feed.updated:
            log.debug('New bookmarks on pinboard since last check')
            return True
        log.debug('No new bookmarks on pinboard since last check')
        return False

    log.debug("Updating feed ID %s" % feed_id)
    try:
        feed = RecipeFeed.objects.get(pk=feed_id)
        log.info('Updating pinboard feed for user %s' % feed.owner.username)
        if feed.ready_to_update():
            if feed.updated:
                log.debug("Feed last updated at %s" % feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ'))
                feed_time = feed.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                log.debug("Feed has never been updated.")
                feed_time = None

            if new_recipes(feed):
                log.info("Pinboard says new recipes since last update")
                #Get recipes added since last update date
                feed_url = 'https://api.pinboard.in/v1/posts/all'
                payload = {
                    'auth_token': feed.feed_apikey,
                    'tag': feed.feed_tag_key,
                    'format': 'json'
                }

                if feed_time:
                    payload['fromdt'] = feed_time

                r = requests.get(feed_url, params=payload)
                log.debug("Request returned with status code %s" % r.status_code)

                if r.status_code == 200:
                    recipes = r.json()
                    log.info("%s NEW RECIPES FROM PINBOARD" % len(recipes))

                    #Mark completion time so that we know when feed was updated
                    #NOTE: This leaves small gap of time b/t calling of task and finishing
                    #of task where new recipes could be added but not picked up!
                    feed.updated = timezone.now()
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
                        #If no new recipes, set the task ID to zero
                        feed.celery_task_id = 0
                    feed.save()
                else:
                    log.info("Pinboard says no new feeds since last update")
        else:
            log.info("Feed %s has a previous update still running with ID %s" % (feed, feed.celery_task_id))

    except RecipeFeed.DoesNotExist:
        log.error("Recipe feed with id %s does not exist." % feed_id)
