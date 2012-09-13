from common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(os.path.split(os.path.abspath(__file__))[0], 'database.sqlite'),                      # Or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_DIR, 'WeeklyMenus', 'database.sqlite'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

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
)
