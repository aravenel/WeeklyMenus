from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    #url(r'^recipes/', include('recipes.urls')),
    #url(r'^menus/', include('menus.urls')),
    url(r'^$', 'feedmanager.views.index'),
    url(r'^(?P<feed_id>\d+)/$', 'feedmanager.views.edit'),
    url(r'^(?P<feed_id>\d+)/delete$', 'feedmanager.views.edit'),
)
