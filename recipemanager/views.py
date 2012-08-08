from recipemanager.models import Recipe, RecipeForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# Create your views here.

def index(request):

    if request.method == 'POST':
        add_form = RecipeForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('/recipes')
    else:
        add_form = RecipeForm()

    recent_recipes = Recipe.objects.order_by('-last_made')[:5]
    popular_recipes = Recipe.objects.order_by('made_count')[:5]

    return render_to_response(
            'recipes.html',
            {
                'add_form': add_form,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
            },
            context_instance=RequestContext(request)
            )

def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        pass
    return redirect('/recipes')
