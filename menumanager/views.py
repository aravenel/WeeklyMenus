from django.shortcuts import render_to_response, redirect, get_object_or_404
from menumanager.models import WeeklyMenu, WeeklyMenuForm, MenuItem
from django.contrib.auth.decorators import login_required
import menumanager
from recipemanager.models import Recipe, RecipeAjaxForm
from django.template import RequestContext
import datetime

#Helper functions
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

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
    recent_recipes = Recipe.objects.filter(owner=request.user).order_by('-last_made')[:5]
    popular_recipes = Recipe.objects.filter(owner=request.user).order_by('made_count')[:5]
    info_data = {
            'date': dt,
            'type': menumanager.models.type_mapping[int(menu_type)]
            }

    return render_to_response(
            'menu_items.html',
            {
                'current_recipes': current_recipes,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
                'info_data': info_data,
                'recipe_search_form': recipe_search_form,
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
    next = request.GET.get('next')
    return redirect(next)

@login_required
def item_delete(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, owner=request.user)
    item.delete()
    next = request.GET.get('next')
    return redirect(next)

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
