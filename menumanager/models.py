from django.db import models

# Create your models here.
class WeeklyMenu(models.Model):
    #Weekly menu container--holds menus for each day of week
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "Weekly Menu %s to %s" % (self.start_date, self.end_date)

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
