from fabric.api import *

dev_repo = 'dev'
staging_repo = 'staging'
prod_repo = 'prod'

CONFIG = {
        'dev': {
            'repo': 'dev',
            },
        'staging': {
            'repo': 'staging',
            'code_dir': '/srv/www/menus-dev/http/WeeklyMenus',
            'hosts': [
                'http://menus-dev.alexravenel.com',
                ],
            },
        'prod': {
            },
        }

def staging():
    env.hosts = CONFIG['staging']['hosts']
    env.code_dir = CONFIG['staging']['code_dir']

def prod():
    pass

def push():
    pass

def pull():
    pass

def pushpul():
    pass
