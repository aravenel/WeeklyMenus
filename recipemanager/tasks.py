from models import Recipe
from celery.task import task
from django.conf import settings
import requests
import logging

log = logging.getLogger(__name__)

def clean_url_parameters(url):
    """Clean up URL parameter cruft. Inspired by pinboard.
    Will remove all url parameters that start with utm_*"""

    url_parts = url.split("?")
    root = url_parts[0]

    if len(url_parts) > 1:
        params = url_parts[1].split("&")
        cleaned_params = [param for param in params if not param.startswith("utm_")]
        if len(cleaned_params) > 0:
            cleaned_url = "%s?%s" % (root, "&".join(cleaned_params))
        else:
            cleaned_url = root
    else:
        cleaned_url = url

    return cleaned_url

@task
def add_recipe(url, title, owner, source, hash, tags):
    """Add a recipe to the database. Eventually will be extended to fetch images,
    parse recipe contents, etc."""
    try:
        recipe = Recipe.objects.get(owner=owner, hash=hash)
        print "RECIPE WITH THIS HASH ALREADY EXISTS"
        print title
    except Recipe.DoesNotExist:
        print "NEW RECIPE FOUND"
        url = clean_url_parameters(url)

        #Get recipe contents (scrape!)
        #HTML to be saved as content of recipe, as parsed by Readability
        # readable_article = Document(html).summary(html_partial=True)
        payload = {'url': url, 'token': settings.DIFFBOT_API_KEY, 'html': True}
        r = requests.get('http://www.diffbot.com/api/article', params=payload)
        if r.status_code == 200:
            diffbot = r.json()
            content = diffbot['text']
            primary_image_href = None
            if 'media' in diffbot.keys():
                images = [media for media in diffbot['media'] if media['type'] == 'image']

                #Get primary image
                for image in images:
                    #See if anything has primary flag set
                    if 'primary' in image.keys():
                        if image['primary'] in [True, 'true']:
                            primary_image_href = image['link']

                #If primary flag not set, just get first returned image
                if not primary_image_href:
                    primary_image_href = images[0]['link']
            else:
                primary_image_href = None
        else:
            content = None
            primary_image_href = None

        #Save recipe
        recipe = Recipe(
                url = url,
                title = title,
                owner = owner,
                source = source,
                hash = hash,
                content = content,
                image = primary_image_href,
                )
        recipe.save()
        recipe.tags.add(*tags)
    return True
