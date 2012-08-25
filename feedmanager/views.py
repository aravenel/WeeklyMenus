import datetime
from feedmanager.models import RecipeFeed, RecipeFeedForm
import feedmanager.tasks
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
# Create your views here.

@login_required
def index(request):
    if request.method == "POST":
        feed_form = RecipeFeedForm(request.POST)
        if feed_form.is_valid():
            feed = feed_form.save(commit=False)
            feed.owner = request.user
            feed.updated = datetime.datetime.utcnow()
            feed.save()
            return redirect('/feeds')
    else:
        feed_form = RecipeFeedForm()

    all_feeds = RecipeFeed.objects.filter(owner=request.user)
    title = 'Add A Feed'

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
            feed = feed_form.save(commit=False)
            feed.owner = request.user
            feed.updated = datetime.datetime.utcnow()
            feed.save()
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
    feedmanager.tasks.update_feed_pinboard.delay(feed, request)
    next = request.GET.get('next')
    return redirect(next)
