from models import Recipe
from celery.task import task

@task
def add_recipe(url, title, owner, source, tags):
    """Add a recipe to the database. Eventually will be extended to fetch images,
    parse recipe contents, etc."""
    recipe = Recipe(
            url = url,
            title = title,
            owner = owner,
            source = source,
            )
    recipe.tags.add(tags)
    recipe.save()
    return True
