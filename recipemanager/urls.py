from django.conf.urls import patterns, include, url
from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    #url(r'^$', 'recipemanager.views.index'),
    url(r'^$', 'recipemanager.views.all'),
    #url(r'^all/$', 'recipemanager.views.all'),
    url(r'^search/$', 'recipemanager.views.search'),
    url(r'^ajax_search/$', 'recipemanager.views.ajax_search'),
    url(r'^get_recipe_data/$', 'recipemanager.views.get_recipe_data'),
    #url(r'^tags/(?P<tag>\w+)/$', 'recipemanager.views.tag_search'),
    url(r'^tags/(?P<tag>\w+)/$', 'recipemanager.views.all'),
    url(r'^(?P<recipe_id>\d+)/$', 'recipemanager.views.view'),
    url(r'^(?P<recipe_id>\d+)/edit$', 'recipemanager.views.edit'),
    url(r'^(?P<recipe_id>\d+)/delete/$', 'recipemanager.views.delete'),
    url(r'^add$', 'recipemanager.views.add'),

    #Ajax-select URLs
    url(r'^lookups/', include(ajax_select_urls)),
)
