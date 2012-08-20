from recipemanager.models import Recipe, RecipeForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
# Create your views here.

@login_required
def index(request):

    if request.method == 'POST':
        add_form = RecipeForm(request.POST)
        if add_form.is_valid():
            recipe = add_form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            return redirect('/recipes')
    else:
        add_form = RecipeForm()

    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-last_made')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('made_count')[:5]

    return render_to_response(
            'recipes.html',
            {
                'add_form': add_form,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
            },
            context_instance=RequestContext(request)
            )

@login_required
def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit = False)
            recipe.owner = request.user
            recipe.save()
    else:
        pass
    return redirect('/recipes')

@login_required
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id,
            owner=request.user)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        if recipe_form.is_valid():
            updated_recipe = recipe_form.save(commit=False)
            updated_recipe.owner = request.user
            updated_recipe.save()
    else:
        recipe_form = RecipeForm(instance=recipe)

    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-last_made')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('made_count')[:5]

    return render_to_response(
            'edit_recipe.html',
            {
                'recipe': recipe,
                'recipe_form': recipe_form,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
            },
            context_instance = RequestContext(request)
            )

@login_required
def delete(request, recipe_id):
    pass

