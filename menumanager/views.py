from django.shortcuts import render_to_response, redirect, get_object_or_404
from menumanager.models import WeeklyMenu, WeeklyMenuForm, MenuItem
from recipemanager.models import Recipe
from django.template import RequestContext
import datetime

#Helper functions
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

# Create your views here.
def index(request):
    if request.method == 'POST':
        weekly_menu_form = WeeklyMenuForm(request.POST)
        if weekly_menu_form.is_valid():
            weekly_menu_form.save()
            return redirect('/menus')
    else:
        weekly_menu_form = WeeklyMenuForm()
    
    all_menus = WeeklyMenu.objects.all()
    today = datetime.date.today()
    current_menu = None
    menu_dict = None
    for menu in all_menus:
        if today >= menu.start_date and today <= menu.end_date:
            current_menu = menu
            menu_dict = current_menu.build_menu_dict()
            break

    return render_to_response(
            'weekly_menus.html',
            {
                'weekly_menu_form': weekly_menu_form,
                'current_menu': current_menu,
                'menu_dict': menu_dict,
            },
            context_instance=RequestContext(request)
            )

def menu_edit(request, weeklymenu_id, menu_date, menu_type):
    dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
    current_recipes = MenuItem.objects.filter(menu=weeklymenu_id, menu_date=dt,
            menu_type=menu_type)
    recent_recipes = Recipe.objects.order_by('-last_made')[:5]
    popular_recipes = Recipe.objects.order_by('made_count')[:5]

    return render_to_response(
            'menu_items.html',
            {
                'current_recipes': current_recipes,
                'recent_recipes': recent_recipes,
                'popular_recipes': popular_recipes,
            },
            context_instance=RequestContext(request)
            )

def recipe_add(request, weeklymenu_id, menu_date, menu_type, recipe_id):
    menu = get_object_or_404(WeeklyMenu, pk=weeklymenu_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    dt = datetime.datetime.strptime(menu_date, "%Y%m%d").date()
    mi = MenuItem(menu=menu, menu_date=dt, menu_type=menu_type, recipe=recipe)
    mi.save()
    next = request.GET.get('next')
    return redirect(next)

def weekly_edit(request):
    pass
