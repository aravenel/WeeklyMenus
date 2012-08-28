from recipemanager.models import Recipe, RecipeForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def index(request):

    if request.method == 'POST':
        add_form = RecipeForm(request.POST)
        if add_form.is_valid():
            recipe = add_form.save(commit=False)
            recipe.owner = request.user
            recipe.source = "web"
            recipe.save()
            add_form.save_m2m()
            return redirect('/recipes')
    else:
        add_form = RecipeForm()

    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-added')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('-made_count')[:5]

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
            recipe.source = "web"
            recipe.save()
            form.save_m2m()
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
            recipe_form.save_m2m()
    else:
        recipe_form = RecipeForm(instance=recipe)

    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-added')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('-made_count')[:5]

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

@login_required
def all(request, tag=None):
    sort = request.GET.get('sort')
    page = request.GET.get('page')

    valid_sorts = [
            'title',
            'made_count',
            'last_made',
            ]

    if sort not in valid_sorts:
        sort = 'title'

    if tag is None:
        all_recipes = Recipe.objects.filter(owner=request.user).order_by(sort)
    else:
        all_recipes = Recipe.objects.filter(owner=request.user, tags__name_in=[tag]).order_by(sort)

    paginator = Paginator(all_recipes, 10)
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render_to_response(
            'all_recipes.html',
            {
                'recipes': recipes,
                'num_pages': paginator.num_pages,
                'sort': sort,
            },
            context_instance = RequestContext(request)
            )
