from models import Recipe
from celery.task import task

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
        recipe = Recipe(
                url = url,
                title = title,
                owner = owner,
                source = source,
                hash = hash
                )
        recipe.save()
        recipe.tags.add(tags)
    return True
