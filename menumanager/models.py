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
        menu_dict = {}
        #All related menu items
        menus = Menu.objects.filter(weekly_menu=self)

        md = {}
        for menu in menus:

            #Setup the sub dict if needed
            if menu.menu_date not in md.keys():
                md[menu.menu_date] = {}

            for meal in range(0, 3):
                pass

        for date in daterange(self.start_date, self.end_date + datetime.timedelta(1)):
            menu_dict[date] = {}
            for menu in menus:
                if menu.menu_date == date:
                    pass



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

class Menu(models.Model):
    #Individual menu--breakfast, lunch, or dinner
    weekly_menu = models.ForeignKey('WeeklyMenu')
    menu_date = models.DateField()
    #0 = Breakfast, 1 = Lunch, 2 = Dinner
    menu_type = models.IntegerField()

    def __unicode__(self):
        type_mapping = {
                0: 'Breakfast',
                1: 'Lunch',
                2: 'Dinner',
                }

        return "%s %s" % (type_mapping[self.menu_type], self.menu_date)

class MenuItem(models.Model):
    #Item that belongs to a menu. Can have multiple items on a menu
    menu = models.ForeignKey('Menu')
    recipe = models.ForeignKey('recipemanager.Recipe')
