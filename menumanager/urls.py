from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    url(r'^$', 'menumanager.views.index'),
    url(r'^delete/(?P<item_id>\d+)/$', 'menumanager.views.item_delete'),
    url(r'^ajax_delete/$', 'menumanager.views.ajax_item_delete'),
    url(r'^(?P<menu_id>\d+)/$', 'menumanager.views.weekly_menu_view'),
    url(r'^edit/(?P<weeklymenu_id>\d+)/(?P<menu_date>\d+)/(?P<menu_type>\d+)/$',
        'menumanager.views.menu_edit'),
    url(r'^edit/(?P<weeklymenu_id>\d+)/(?P<menu_date>\d+)/(?P<menu_type>\d+)/add/(?P<recipe_id>\d+)/$',
        'menumanager.views.recipe_add'),
    url(r'^ajax_add_to_menu/$', 'menumanager.views.ajax_add_to_menu'),
)
