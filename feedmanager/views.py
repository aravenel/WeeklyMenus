import logging
from feedmanager.models import RecipeFeed, RecipeFeedForm
import feedmanager.tasks
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.core.urlresolvers import reverse
from celery import result
# Create your views here.

log = logging.getLogger(__name__)

@login_required
def index(request):
    if request.method == "POST":
        feed_form = RecipeFeedForm(request.POST)
        if feed_form.is_valid():
            feed = feed_form.save(commit=False)
            feed.owner = request.user
            #feed.updated = datetime.datetime.utcnow()
            feed.save()
            return redirect('/feeds')
    else:
        feed_form = RecipeFeedForm()

    all_feeds = RecipeFeed.objects.filter(owner=request.user)
    title = 'Add A Feed'

    #Update feeds to get statuses
    for feed in all_feeds:
        if not feed.celery_task_id:
            feed.status = "Not Run"
        elif feed.celery_task_id == '0':
            feed.status = "No new feeds"
        else:
            resultset = result.GroupResult.restore(feed.celery_task_id)
            if not resultset.ready():
                feed.status = "Updating: %s new recipes added" % resultset.completed_count()
            else:
                feed.status = "Completed: %s new recipes added" % resultset.completed_count()

    return render_to_response(
            'feeds/feeds.html',
            {
                'feed_form': feed_form,
                'all_feeds': all_feeds,
                'title': title,
            },
            context_instance=RequestContext(request)
            )

@login_required
def edit(request, feed_id):
    feed = get_object_or_404(RecipeFeed, pk=feed_id, owner=request.user)

    if request.method == 'POST':
        feed_form = RecipeFeedForm(request.POST, instance=feed)
        if feed_form.is_valid():
            updated_feed = feed_form.save(commit=False)
            updated_feed.owner = request.user
            updated_feed.updated = None
            updated_feed.save()
    else:
        feed_form = RecipeFeedForm(instance=feed)

    all_feeds = RecipeFeed.objects.filter(owner=request.user)
    title = 'Edit feed: %s' % feed.get_feed_type_display()

    return render_to_response(
            'feeds/feeds.html',
            {
                'feed_form': feed_form,
                'all_feeds': all_feeds,
                'title': title,
            },
            context_instance=RequestContext(request)
            )

@login_required
def delete(request, feed_id):
    feed = get_object_or_404(RecipeFeed, pk=feed_id, owner=request.user)
    feed.delete()
    return redirect('/feeds')

@login_required
def update(request, feed_id):
    """Kick off the celery task to update a recipe feed"""
    feed = get_object_or_404(RecipeFeed, pk=feed_id, owner=request.user)
    if feed.ready_to_update():
        log.debug('Mode reports ready to update')
        r = feedmanager.tasks.update_feed_pinboard.delay(feed_id)
        messages.add_message(request, messages.INFO, "Feed queued for update.")
    else:
        log.debug('Model reports not ready to update')
        messages.add_message(request, messages.WARNING, "A feed update is already running.")
        prev_result = result.GroupResult(feed.celery_task_id)
        messages.add_message(request, messages.INFO, "Celery task state is %s" % prev_result.state)
    return redirect(reverse('feedmanager.views.index'))
