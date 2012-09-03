from recipemanager.models import Recipe
from ajax_select import LookupChannel
from itertools import chain

class RecipeSearch(LookupChannel):

    model = Recipe

    def get_query(self, q, request):
        recipes_by_title = Recipe.objects.filter(owner=request.user, 
                title__contains=q)
        recipes_by_tag = Recipe.objects.filter(owner=request.user, 
                tags__name__contains=q)
        return list(chain(recipes_by_title, recipes_by_tag))

    def get_result(self, obj):
        return obj.title

    def format_match(self, obj):
        return u"<a href='/recipes/%s'>%s<a>" % (obj.id, obj.title)

class RecipeAddToMenu(LookupChannel):

    model = Recipe

    def get_query(self, q, request):
        recipes = Recipe.objects.filter(owner = request.user, title__contains=q)
        return recipes

