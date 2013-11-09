from common import *
from sys import exit

try:
    from passwords_prod import *
except ImportError:
    print "Cannot import passwords file."
    exit()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,
        'USER': DB_USER,                      # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,                  # Not used with sqlite3.
        'HOST': DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': DB_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sessions',
    'crispy_forms',
    'ajax_select',
    'taggit',
    'taggit_autosuggest',
    'south',
    'menumanager',
    'recipemanager',
    'feedmanager',
    'djcelery',
    'taggit_templatetags',
    'debug_toolbar',
    'sorl.thumbnail',
    'registration',
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

DEBUG = False

#Sorl-thumbnail settings
THUMBNAIL_DEBUG = True
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

STATIC_ROOT = '/srv/www/menus-prod/static_files'

BROKER_URL = 'redis://localhost:6379/0'

DIFFBOT_API_KEY = DIFFBOT_API_KEY

MEDIA_ROOT = '/srv/www/menus-prod/media'
MEDIA_URL = '/media/'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'

REGISTRATION_OPEN = False

# LOGGING['handlers']['logfile']['filename'] = r'/srv/www/menus-dev/http/logs/logfile.log'
# LOGGING['handlers']['debug_logfile']['filename'] = r'/srv/www/menus-dev/http/logs/debug_logfile.log'
# LOGGING['handlers']['default_logger']['filename'] = r'/srv/www/menus-dev/http/logs/default.log'
# LOGGING['handlers']['celery.task']['filename'] = r'/srv/www/menus-dev/http/logs/celery.log'
