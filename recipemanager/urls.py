from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    url(r'^$', 'recipemanager.views.index'),
    url(r'^add$', 'recipemanager.views.add'),
    #url(r'^(?P<recipe_id>\d)/$', 'recipemanager.views.edit')
)
