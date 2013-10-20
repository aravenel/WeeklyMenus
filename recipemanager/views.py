from recipemanager.models import Recipe, RecipeForm, RecipeSearchForm
from taggit.models import Tag
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from sorl.thumbnail import get_thumbnail
import logging
import json
# Create your views here.

log = logging.getLogger(__name__)

def build_paginator(page, adjacent_pages=3):
    """Helper function to build paginator with N number of adjacent pages and
    ellipses back until the first and last pages. Helpful for large number of
    pages.

    Returns a list with the numbers of pages (1 indexed) that should be displayed.
    """
    start_page = max(page.number - adjacent_pages, 1)
    if start_page <= 3:
        start_page = 1
    end_page = page.number + adjacent_pages + 1
    if end_page >= page.paginator.num_pages - 1:
        end_page = page.paginator.num_pages + 1
    page_numbers = [n for n in range(start_page, end_page) if n > 0 and n <= page.paginator.num_pages]
    return page_numbers

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
            return redirect(reverse('recipemanager.view.all'))
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
def view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id,
            owner=request.user)
    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-added')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('-made_count')[:5]

    return render_to_response(
            'view_recipe.html',
            {
                'recipe': recipe,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
            },
            context_instance = RequestContext(request),
            )

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
            return redirect('/recipes/%s' % recipe_id)
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

    #Set sort session variable
    if 'sort' in request.GET:
        if request.GET.get('sort') not in settings.VALID_RECIPE_SORTS.keys():
            sort_by = 'title'
        else:
            sort_by = request.GET.get('sort')
        request.session['sort'] = sort_by
    sort = request.session.get('sort', 'title')

    #Set perpage session variable
    if 'perpage' in request.GET:
        try:
            perpage = int(request.GET.get('perpage'))
            if perpage not in settings.VALID_RECIPES_PERPAGE:
                perpage = 20
        except ValueError:
            perpage = 20
        request.session['perpage'] = perpage
    perpage = request.session.get('perpage', 20)

    page = request.GET.get('page')

    log.debug('sort = %s' % sort)
    log.debug('page = %s' % page)
    log.debug('perpage = %s' % perpage)

    #If invalid sort key specified, sort by title
    if sort not in settings.VALID_RECIPE_SORTS.keys():
        sort = 'title'

    #Form the sort string to make sure we sort correctly in asc/desc order
    if settings.VALID_RECIPE_SORTS[sort]['sort_by'] == 'desc':
        sort_string = '-%s' % sort
    else:
        sort_string = sort

    #Get the recipe objects
    if tag is None:
        all_recipes = Recipe.objects.filter(owner=request.user).order_by(sort_string)
        title = "All Recipes"
    else:
        all_recipes = Recipe.objects.filter(owner=request.user, tags__name=tag).order_by(sort_string)
        title = 'Recipes with tag "%s"' % tag

    #Build the paginator
    paginator = Paginator(all_recipes, perpage)
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    #Build the list of pages for the template to render
    page_numbers = build_paginator(recipes)

    return render_to_response(
            'all_recipes.html',
            {
                'recipes': recipes,
                'valid_sorts': settings.VALID_RECIPE_SORTS,
                'valid_perpage': settings.VALID_RECIPES_PERPAGE,
                'recipe_search_form': recipe_search_form,
                'title': title,
                'page_numbers': page_numbers,
                'show_first': 1 not in page_numbers,
                'show_last': paginator.num_pages not in page_numbers,
            },
            context_instance = RequestContext(request)
            )

@login_required
def search(request):
    if request.method == 'GET':
        recipe_search_form = RecipeSearchForm(request.GET)
        if recipe_search_form.is_valid():
            term = recipe_search_form.cleaned_data['term']
            page = request.GET.get('page')

            #Set sort session variable
            if 'sort' in request.GET:
                if request.GET.get('sort') not in settings.VALID_RECIPE_SORTS.keys():
                    sort_by = 'title'
                else:
                    sort_by = request.GET.get('sort')
                request.session['sort'] = sort_by
            sort = request.session.get('sort', 'title')

            #Set perpage session variable
            if 'perpage' in request.GET:
                try:
                    perpage = int(request.GET.get('perpage'))
                    if perpage not in settings.VALID_RECIPES_PERPAGE:
                        perpage = 20
                except ValueError:
                    perpage = 20
                request.session['perpage'] = perpage
            perpage = request.session.get('perpage', 20)

            #If invalid sort key specified, sort by title
            if sort not in settings.VALID_RECIPE_SORTS.keys():
                sort = 'title'

            #Form the sort string to make sure we sort correctly in asc/desc order
            if settings.VALID_RECIPE_SORTS[sort]['sort_by'] == 'desc':
                sort_string = '-%s' % sort
            else:
                sort_string = sort

            #Get unique tag names--that's all we need
            tag_matches = Tag.objects.filter(name__icontains=term, recipe__owner=request.user)
            tag_matches = list(set([tag.name for tag in tag_matches]))

            #Get title matches and create paginator items
            title_matches = Recipe.objects.filter(owner=request.user, title__icontains=term).order_by(sort_string)
            paginator = Paginator(title_matches, perpage)

            try:
                recipes = paginator.page(page)
            except PageNotAnInteger:
                recipes = paginator.page(1)
            except EmptyPage:
                recipes = paginator.page(paginator.num_pages)

            page_numbers = build_paginator(recipes)

        else:
            term = None
            title_matches = None
            tag_matches = None
        return render_to_response(
                'recipe_search.html',
                {
                    'term': term,
                    'title_matches': title_matches,
                    'recipes': recipes,
                    'tag_matches': tag_matches,
                    'valid_sorts': settings.VALID_RECIPE_SORTS,
                    'valid_perpage': settings.VALID_RECIPES_PERPAGE,
                    'recipe_search_form': recipe_search_form,
                    'page_numbers': page_numbers,
                    'show_first': 1 not in page_numbers,
                    'show_last': paginator.num_pages not in page_numbers,
                },
                context_instance = RequestContext(request)
                )
    else:
        return redirect(reverse('recipemanager.views.all'))

@login_required
def ajax_search(request):
    if request.is_ajax():
        term = request.GET.get('term')
        recipes = Recipe.objects.filter(owner=request.user, title__icontains=term)
        response_data = [{'label': recipe.title, 'value': recipe.id} for recipe in recipes]
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad request, must be AJAX")

@login_required
def get_recipe_data(request):
    if request.is_ajax():
        recipe_id = request.GET.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id, owner=request.user)
        thumbnail = get_thumbnail(recipe.image, '270x270', crop='center')
        response_data = {
            'id': recipe.id,
            'title': recipe.title,
            'image': recipe.image,
            'thumbnail': thumbnail.url,
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponseBadRequest("Bad request, must be AJAX")

