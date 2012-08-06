from recipemanager.models import Recipe, RecipeForm
from django.shortcuts import render_to_response
# Create your views here.

def add(request):
    if request.method == 'POST':
        pass
    else:
        form = RecipeForm()
    return render_to_response('add_recipe.html', {
        'form': form
        })
