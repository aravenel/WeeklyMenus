from django.shortcuts import render_to_response, redirect
from menumanager.models import WeeklyMenu, WeeklyMenuForm
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
    for menu in all_menus:
        if today >= menu.start_date and today <= menu.end_date:
            current_menu = menu
            break

    return render_to_response(
            'weekly_menus.html',
            {
                'weekly_menu_form': weekly_menu_form,
                'current_menu': current_menu,
            },
            context_instance=RequestContext(request)
            )

def add(request):
    pass

def menu_edit(request):
    pass

def weekly_edit(request):
    pass
