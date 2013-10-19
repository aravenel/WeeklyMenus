from django.shortcuts import render_to_response, redirect, get_object_or_404
from menumanager.models import WeeklyMenu, WeeklyMenuForm, MenuItem
from django.contrib.auth.decorators import login_required
from recipemanager.models import Recipe, RecipeAjaxForm
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponse
import datetime, json
import menumanager
import logging

#Helper functions
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def is_int(value): #Return true if int
    try:
        int(value)
        return True
    except ValueError:
        return False

def chunk_list(l, n=3):
    return [l[i:i+n] for i in range(0, len(l), n)]


log = logging.getLogger(__name__)

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        weekly_menu_form = WeeklyMenuForm(request.POST)
        if weekly_menu_form.is_valid():
            weekly_menu = weekly_menu_form.save(commit=False)
            weekly_menu.owner = request.user
            weekly_menu.save()
            return redirect('/menus')
    else:
        weekly_menu_form = WeeklyMenuForm()

    all_menus = WeeklyMenu.objects.filter(owner=request.user)
    today = datetime.date.today()
    current_menu = None
    menu_dict = None
    for menu in all_menus:
        if today >= menu.start_date and today <= menu.end_date:
            current_menu = menu
            menu_dict = current_menu.build_menu_dict()
            break

    upcoming_menus = [menu for menu in all_menus if menu.start_date > today]
    previous_menus = [menu for menu in all_menus if menu.start_date < today and
            menu != current_menu]

    return render_to_response(
            'weekly_menus.html',
            {
                'weekly_menu_form': weekly_menu_form,
                'current_menu': current_menu,
                'menu_dict': menu_dict,
                'upcoming_menus': upcoming_menus,
                'previous_menus': previous_menus,
                'host': request.get_host()
            },
            context_instance=RequestContext(request)
            )

@login_required
def menu_edit(request, weeklymenu_id, menu_date, menu_type):
    if request.method == 'POST':
        recipe_search_form = RecipeAjaxForm(request.POST)
        if recipe_search_form.is_valid():
            menu = get_object_or_404(WeeklyMenu, pk=weeklymenu_id, owner=request.user)
            recipe = get_object_or_404(Recipe, title=recipe_search_form.cleaned_data['title'],
                    owner=request.user)
            dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
            mi = MenuItem(menu=menu, menu_date=dt, menu_type=menu_type, recipe=recipe,
                    owner=request.user)
            mi.save()
            return redirect(request.path)
    else:
        recipe_search_form = RecipeAjaxForm()

    dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
    current_recipes = MenuItem.objects.filter(menu=weeklymenu_id, menu_date=dt,
            menu_type=menu_type, owner=request.user)
    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-added')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('-made_count')[:5]
    info_data = {
            'date': dt,
            'type': menumanager.models.type_mapping[int(menu_type)]
            }

    return render_to_response(
            'menu_items_modal.html',
            {
                'current_recipes': current_recipes,
                'chunked_recipes': chunk_list(current_recipes),
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
                'info_data': info_data,
                'recipe_search_form': recipe_search_form,
                'menu_id': weeklymenu_id,
                'menu_date': menu_date,
                'menu_type': menu_type,
            },
            context_instance=RequestContext(request)
            )

@login_required
def recipe_add(request, weeklymenu_id, menu_date, menu_type, recipe_id):
    menu = get_object_or_404(WeeklyMenu, pk=weeklymenu_id, owner=request.user)
    recipe = get_object_or_404(Recipe, pk=recipe_id, owner=request.user)
    dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
    mi = MenuItem(menu=menu, menu_date=dt, menu_type=menu_type, recipe=recipe,
            owner=request.user)
    mi.save()
    recipe.made_count += 1
    recipe.save()
    next = request.GET.get('next')
    return redirect(next)

@login_required
def item_delete(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, owner=request.user)
    recipe = item.recipe
    recipe.made_count -= 1
    recipe.save()
    item.delete()
    next = request.GET.get('next')
    return redirect(next)

@login_required
def ajax_item_delete(request):
    if request.is_ajax():
        if request.method == "POST":
            menuitem_id = request.POST.get('menuitem_id')
            item = get_object_or_404(MenuItem, pk=menuitem_id, owner=request.user)
            recipe = item.recipe
            recipe.made_count -= 1
            recipe.save()
            item.delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("Must be POST")
    else:
        return HttpResponseBadRequest("Must be AJAX")

@login_required
def weekly_menu_view(request, menu_id):
    menu = get_object_or_404(WeeklyMenu, pk=menu_id, owner=request.user)
    menu_dict = menu.build_menu_dict()
    return render_to_response(
            'weekly_menu_view.html',
            {
                'current_menu': menu,
                'menu_dict': menu_dict,
            },
            context_instance=RequestContext(request)
            )

@login_required
def ajax_add_to_menu(request):
    if request.is_ajax():
        if request.method == 'POST':

            #Get POST variables
            recipe_id = request.POST.get('recipe_id')
            menu_id = request.POST.get('menu_id')
            menu_date = request.POST.get('menu_date')
            menu_type = request.POST.get('menu_type')

            #Get menus and recipes
            #If non-numeric "id", this is an ad-hoc recipe title to be added to DB
            if is_int(recipe_id):
                recipe = get_object_or_404(Recipe, pk=recipe_id, owner=request.user)
            else:
                log.debug("Recipe is not an id, creating new.")
                recipe = Recipe(title=recipe_id, source='ad-hoc', owner=request.user, url='')
                recipe.save()
                log.debug('Added new recipe %s' % recipe_id)

            menu = get_object_or_404(WeeklyMenu, pk=menu_id, owner=request.user)
            dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
            mi = MenuItem(menu=menu, menu_date=dt, menu_type=menu_type, recipe=recipe,
                    owner=request.user)
            mi.save()

            recipe.made_count += 1
            recipe.save()

            response_data = {'menuitem_id': mi.id}

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponseBadRequest("Bad request, must be POST")
    else:
        return HttpResponseBadRequest("Bad request, must be AJAX")
