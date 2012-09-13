from fabric.api import *
#from fabric.operations import *
import os
from sys import exit

CONFIG = {
        'dev': {
            'repo': 'dev',
            },
        'staging': {
            'repo': 'staging',
            'code_dir': '/home/ravenel/apps/menus-staging/WeeklyMenus',
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
    env.repo = CONFIG['staging']['repo']
    env.environment = 'staging'

def prod():
    print "\n\nWARNING! You are about to deploy to production!\n\n"
    print "If you wish to continue, enter Yes:"
    ans = raw_input()
    if ans.upper in ['YES']:
        env.hosts = CONFIG['prod']['hosts']
        env.code_dir = CONFIG['prod']['code_dir']
        env.repo = CONFIG['prod']['repo']
        env.environment = 'prod'
    else:
        exit()

def deploy():
    with cd(env.code_dir):
        #Checkout new code
        #sudo('git pull')
        #sudo('git checkout %s' % env.repo)
        run('git pull')
        run('git checkout %s' % env.repo)

        #Push passwords file to host
        settings_file = os.path.join('settings', 'passwords_%s.py' % env.environment)
        if os.path.isfile(settings_file):
            put(settings_file, 'settings')
        else:
            print "Settings file %s does not exist. Cannot copy to host." % settings_file

        #Sync DB
        #sudo('python manage.py syncdb --settings=settings.%s' % env.environment)
        run('python manage.py syncdb --settings=settings.%s' % env.environment)

        #Run South migrations
        #sudo('python manage.py migrate --all --settings=settings.%s' % env.environment)
        run('python manage.py migrate --all --settings=settings.%s' % env.environment)

        #Restart redis
        sudo('service redis-server restart')

        #Restart celery workers

        #Restart gunicorn server

        #Restart nginx server
