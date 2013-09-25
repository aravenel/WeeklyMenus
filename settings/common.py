# Django settings for WeeklyMenus project.
import os
import djcelery

djcelery.setup_loader()

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.,
    os.path.join(PROJECT_DIR, 'WeeklyMenus', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7hpok1(wn!ufh3p=t!bc4a$dmabklxluj*$%b!$za07m8o_j#b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'WeeklyMenus.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'WeeklyMenus.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'WeeklyMenus', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'bootstrap_toolkit',
    'crispy_forms',
    'ajax_select',
    'taggit',
    #'taggit_autocomplete',
    'taggit_autosuggest',
    'south',
    'debug_toolbar',
    'menumanager',
    'recipemanager',
    'feedmanager',
)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(name)s: %(lineno)s] -- %(message)s',
            'datefmt': '%m-%d-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            #'filename': os.path.join(os.path.dirname(SITE_ROOT), 'logs', 'logfile.log'),
            #'filename': '/srv/www/menus-dev/logs/logfile.log',
            'filename': '/vagrant/logs/logfile.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 3,
            'formatter': 'standard'
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            #'filename': os.path.join(os.path.dirname(SITE_ROOT), 'logs', 'debug_logfile.log'),
            #'filename': '/srv/www/menus-dev/logs/debug_logfile.log',
            'filename': '/vagrant/logs/debug_logfile.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'default_logger': {
            'level': 'WARNING',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            #'filename': os.path.join(os.path.dirname(SITE_ROOT), 'logs', 'default.log'),
            #'filename': '/srv/www/menus-dev/logs/default.log',
            'filename': '/vagrant/logs/default.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 2,
            'formatter': 'standard'
        },
        'celery_logger': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            #'filename': os.path.join(os.path.dirname(SITE_ROOT), 'logs', 'default.log'),
            #'filename': '/srv/www/menus-dev/logs/celery.log',
            'filename': '/vagrant/logs/celery.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 2,
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default_logger'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'feedmanager': {
            'handlers': ['logfile', 'debug_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'recipemanager': {
            'handlers': ['logfile', 'debug_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'menumanager': {
            'handlers': ['logfile', 'debug_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery.task': {
            'handlers': ['celery_logger'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

INTERNAL_IPS = ('127.0.0.1')

#Make crispy forms fail loudly for debugging
CRISPY_FAIL_SILENTLY = not DEBUG

#Ajax-selects options
AJAX_LOOKUP_CHANNELS = {
        'recipe': {'model': 'recipemanager.Recipe', 'search_field':'title'},
        'recipe_search': ('recipemanager.lookups', "RecipeSearch"),
        'recipe_add': ('recipemanager.lookups', "RecipeAddToMenu"),
        }
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

#django-taggit-autocomplete settings
#TAGGIT_AUTOCOMPLETE_JS_BASE_URL = ''
#TAGGIT_AUTOSUGGEST_STATIC_BASE_URL = os.path.join()

TAGGIT_TAGCLOUD_MIN = 2

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CELERYD_HIJACK_ROOT_LOGGER = False

#Dict of valid sorts and their sort order (asc, desc)
VALID_RECIPE_SORTS = {
    'title': {
        'display': 'Title',
        'sort_by': 'asc',
    },
    'made_count': {
        'display': 'Made Count',
        'sort_by': 'desc',
    },
    'last_made': {
        'display': 'Last Made',
        'sort_by': 'desc',
    },
    'rating': {
        'display': 'Rating',
        'sort_by': 'desc',
    },
}

#Valid number of recipes per page
VALID_RECIPES_PERPAGE = [20, 40, 100]
