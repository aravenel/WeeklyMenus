workers = 1
# bind = '127.0.0.1:8888'
bind = '0.0.0.0:8888'
debug = True
loglevel = 'debug'
errorlog = '/srv/www/menus-dev/logs/g-error.log'
accesslog = '/srv/www/menus-dev/logs/g-access.log'
# django_settings = 'settings.staging'
django_settings = 'settings.vagrant'
pythonpath = "/srv/www/menus-dev/http"