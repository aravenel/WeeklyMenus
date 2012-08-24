from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WeeklyMenus.views.home', name='home'),
    # url(r'^WeeklyMenus/', include('WeeklyMenus.foo.urls')),
    url(r'^$', 'menumanager.views.index'),
    url(r'^recipes/', include('recipemanager.urls')),
    url(r'^menus/', include('menumanager.urls')),
    url(r'^feeds/', include('feedmanager.urls')),

    #taggit_autocomplete urls
    (r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Login form
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
