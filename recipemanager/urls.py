from django.conf.urls import patterns, include, url
from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    url(r'^$', 'recipemanager.views.index'),
    url(r'^(?P<recipe_id>\d+)/$', 'recipemanager.views.edit'),
    url(r'^(?P<recipe_id>\d+)/delete/$', 'recipemanager.views.delete'),
    url(r'^add$', 'recipemanager.views.add'),
    url(r'^lookups/', include(ajax_select_urls)),
    #url(r'^(?P<recipe_id>\d)/$', 'recipemanager.views.edit')
)
