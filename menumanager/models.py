from django.db import models
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field
import datetime

#Helper functions
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

# Create your models here.
class WeeklyMenu(models.Model):
    #Weekly menu container--holds menus for each day of week
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "Weekly Menu %s to %s" % (self.start_date, self.end_date)

    def build_menu_dict(self):
        """Build a nested dict containing all menu items for WeeklyMenu"""
        #Dict to contain final values
        menu_dict = []
        #All related menu items
        menus = MenuItem.objects.filter(menu=self)
        #Force queryset to be evaluated so it is cached
        menus = list(menus)

        for date in daterange(self.start_date, self.end_date + datetime.timedelta(1)):
            md = {}
            md['date'] = date
            md['items'] = []
            for meal in range(0, 3):
                #items = menus.filter(menu_date = date, menu_type = meal)
                items = [menu for menu in menus if menu.menu_date == date
                        and menu.menu_type == meal]
                if len(items) == 0:
                    items = None
                md['items'].append(items)
            menu_dict.append(md)

        return menu_dict

class WeeklyMenuForm(ModelForm):
    #Form to add a new weekly menu
    class Meta:
        model = WeeklyMenu

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-WeeklyMenuForm'
        self.helper.form_class = 'well form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        #self.helper.form_style = 'inline'
        self.helper.layout = Layout(
                Field('start_date', css_class='datepicker'),
                Field('end_date', css_class='datepicker'),
                FormActions(
                    Submit('submit', 'Add Menu', css_class='btn-primary'),
                    ),
                )

        super(WeeklyMenuForm, self).__init__(*args, **kwargs)

class MenuItem(models.Model):
    #Item that belongs to a menu. Can have multiple items on a menu
    menu = models.ForeignKey('WeeklyMenu')
    menu_date = models.DateField()
    menu_type = models.IntegerField()
    recipe = models.ForeignKey('recipemanager.Recipe')

    def __unicode__(self):
        type_mapping = {
                0: 'Breakfast',
                1: 'Lunch',
                2: 'Dinner',
                }

        return "%s %s" % (type_mapping[self.menu_type], self.menu_date)
