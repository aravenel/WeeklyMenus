from recipemanager.models import Recipe, RecipeForm
from django.shortcuts import render_to_response
# Create your views here.

def index(request):

    add_form = RecipeForm()
    recent_recipes = Recipe.objects.orderby('last_made')[:5]
    popular_recipes = Recipe.objects.orderby('made_count')[:5]

    return render_to_response('recipes.html',{
        'add_form': add_form,
        'recent_recipes': recent_recipes,
        'popular_recipes': popular_recipes,
        })

def add(request):
    if request.method == 'POST':
        pass
    else:
        form = RecipeForm()
    return render_to_response('add_recipe.html', {
        'form': form
        })
