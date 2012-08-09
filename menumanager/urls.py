from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    url(r'^$', 'menumanager.views.index'),
    url(r'^add/$', 'menumanager.views.add'),
    url(r'^(?P<weeklymenu_id>\d)/$', 'menumanager.views.weekly_edit'),
    url(r'^(?P<weeklymenu_id>\d)/(?P<unix_date>\d)/(?P<menu_type>\d)/$',
        'menumanager.views.menu_edit')
)
