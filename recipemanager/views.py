from recipemanager.models import Recipe, RecipeForm, RecipeSearchForm
from taggit.models import Tag
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
    #recipe_search_form = RecipeAjaxSearchForm()
    recipe_search_form = RecipeSearchForm()
    sort = request.GET.get('sort')
    page = request.GET.get('page')

    #Dict of valid sorts and their sort order (asc, desc)
    valid_sorts = {
            'title': 'asc',
            'made_count': 'desc',
            'last_made': 'desc',
            'rating': 'desc',
            }

    #If invalid sort key specified, sort by title
    if sort not in valid_sorts.keys():
        sort = 'title'

    #Form the sort string to make sure we sort correctly in asc/desc order
    if valid_sorts[sort] == 'desc':
        sort_string = '-%s' % sort
    else:
        sort_string = sort

    #Get the recipe objects
    if tag is None:
        all_recipes = Recipe.objects.filter(owner=request.user).order_by(sort_string)
    else:
        all_recipes = Recipe.objects.filter(owner=request.user, tags__name_in=[tag]).order_by(sort_string)

    #Build the paginator
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
                'recipe_search_form': recipe_search_form,
            },
            context_instance = RequestContext(request)
            )

@login_required
def search(request):
    if request.method == 'POST':
        recipe_search_form = RecipeSearchForm(request.POST)
        if recipe_search_form.is_valid():
            term = recipe_search_form.cleaned_data['term']
            title_matches = Recipe.objects.filter(owner=request.user, title__contains=term)
            tag_matches = Tag.objects.filter(name=term, recipe__owner=request.user)
            #Get unique tag names--that's all we need
            tag_matches = list(set([tag.name for tag in tag_matches]))
        else:
            term = None
            title_matches = None
            tag_matches = None
        return render_to_response(
                'recipe_search.html',
                {
                    'term': term,
                    'title_matches': title_matches,
                    'tag_matches': tag_matches,
                    'recipe_search_form': recipe_search_form,
                },
                context_instance = RequestContext(request)
                )
    else:
        return redirect('/recipes/all')

@login_required
def tag_search(request, tag):
    recipes = Recipe.objects.filter(owner=request.user, tags__name=tag)
    return render_to_response(
            'tag_search.html',
            {
                'recipes': recipes,
                'tag': tag,
            },
            context_instance = RequestContext(request)
            )
