from django.db import models

# Create your models here.
class WeeklyMenu(models.Model):
    #Weekly menu container--holds menus for each day of week
    start_date = models.DateField()
    end_date = models.DateField()

class Menu(models.Model):
    #Individual menu--breakfast, lunch, or dinner
    weekly_menu = models.ForeignKey('WeeklyMenu')
    menu_date = models.DateField()
    #0 = Breakfast, 1 = Lunch, 2 = Dinner
    menu_type = models.IntegerField()

class MenuItem(models.Model):
    #Item that belongs to a menu. Can have multiple items on a menu
    menu = models.ForeignKey('Menu')
    recipe = models.ForeignKey('recipemanager.Recipe')
