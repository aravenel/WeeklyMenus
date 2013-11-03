from models import Recipe
from celery.task import task
from celery.utils.log import get_task_logger
import requests
import lxml
import readability

log = get_task_logger(__name__)

def clean_url_parameters(url):
    """Clean up URL parameter cruft. Inspired by pinboard.
    Will remove all url parameters that start with utm_*"""

    url_parts = url.split("?")
    root = url_parts[0]

    log.debug('URL before cleaning: %s' % url)

    if len(url_parts) > 1:
        params = url_parts[1].split("&")
        cleaned_params = [param for param in params if not param.startswith("utm_")]
        if len(cleaned_params) > 0:
            cleaned_url = "%s?%s" % (root, "&".join(cleaned_params))
        else:
            cleaned_url = root
    else:
        cleaned_url = url

    log.debug('Cleaned URL: %s' % cleaned_url)

    return cleaned_url

@task
def add_recipe(url, title, owner, source, hash, tags):
    """Add a recipe to the database. Eventually will be extended to fetch images,
    parse recipe contents, etc."""
    try:
        recipe = Recipe.objects.get(owner=owner, hash=hash)
        log.warning('Recipe already exists with this hash. URL: %s' % url)
    except Recipe.DoesNotExist:
        log.debug('New recipe found--adding.')
        url = clean_url_parameters(url)

        log.debug('Scraping recipe content via readability')
        r = requests.get(url)
        log.debug("Requests returned status code of %s" % r.status_code)

        if r.status_code == 200:
            #Parse with readability
            read = readability.Document(r.text)
            content = read.summary(True)

            #Pass to lxml to get first image
            l = lxml.html.fromstring(content)
            images = l.cssselect('img')
            log.debug("Found %s images" % len(images))
            if len(images) > 0:
                primary_image_href = images[0].get('src')
            else:
                primary_image_href = None
        else:
            # Cannot get recipe--probably dead link
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
        log.debug("Recipe saved: %s" % title)
    return True
