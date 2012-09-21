from models import Recipe
from celery.task import task

def clean_url_parameters(url):
    """Clean up URL parameter cruft. Inspired by pinboard.
    Will remove all url parameters that start with urm_*"""

    url_parts = url.split("?")
    root = url_parts[0]

    if len(url_parts) > 1:
        param_string = url_parts[1]
        params = param_string.split("&")
        cleaned_params = [param for param in params if not param.starts_with("utm_")]
        cleaned_url = "%s?%s" % (root, "&".join(cleaned_params))
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
        recipe = Recipe(
                url = url,
                title = title,
                owner = owner,
                source = source,
                hash = hash
                )
        recipe.save()
        recipe.tags.add(*tags)
    return True
