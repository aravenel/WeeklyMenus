from fabric.api import *
#from fabric.operations import *
import os
from sys import exit
from socket import gethostname

CONFIG = {
        'dev': {
            'repo': 'dev',
            },
        'staging': {
            #Name of the branch to use
            'repo': 'staging',
            #Location where the code is stored
            'code_dir': '/home/ravenel/apps/menus-staging/WeeklyMenus',
            #Location of python executable--for virtualenv
            'python': '/home/ravenel/apps/menus-staging/WeeklyMenus/venv/bin/python',
            #gunicorn server name (in supervisord)
            'gunicorn_name': 'menus-staging',
            #celeryd server name (in supervisord)
            'celeryd_name': 'celery-menus-staging',
            #Hosts to use
            'hosts': [
                #'http://menus-dev.alexravenel.com',
                'www.alexravenel.com'
                ],
            },
        'prod': {
            },
        }

key_locations = {
        'usnycaravenel1': r'C:\Users\aravenel\pri-openssh.ppk',
        }


def staging():
    env.hosts = CONFIG['staging']['hosts']
    env.code_dir = CONFIG['staging']['code_dir']
    env.repo = CONFIG['staging']['repo']
    env.environment = 'staging'
    env.python = CONFIG['staging']['python']
    env.gunicorn_name = CONFIG['staging']['gunicorn_name']
    env.celeryd_name = CONFIG['staging']['celeryd_name']
    env.user = 'ravenel'
    env.key_filename = key_locations[gethostname()]

def prod():
    print "\n\nWARNING! You are about to deploy to production!\n\n"
    print "If you wish to continue, enter Yes:"
    ans = raw_input()
    if ans.upper in ['YES']:
        env.hosts = CONFIG['prod']['hosts']
        env.code_dir = CONFIG['prod']['code_dir']
        env.repo = CONFIG['prod']['repo']
        env.environment = 'prod'
        env.python = CONFIG['prod']['python']
        env.gunicorn_name = CONFIG['prod']['gunicorn_name']
        env.celeryd_name = CONFIG['prod']['celeryd_name']
    else:
        exit()

def deploy():
    with cd(env.code_dir):
        #Checkout new code
        #sudo('git pull')
        #sudo('git checkout %s' % env.repo)
        print "Checking out code...",
        run('git reset --hard HEAD')
        run('git pull')
        run('git checkout %s' % env.repo)

        #Push passwords file to host
        settings_file = os.path.join('settings', 'passwords_%s.py' % env.environment)
        if os.path.isfile(settings_file):
            put(settings_file, 'settings')
        else:
            print "Settings file %s does not exist. Cannot copy to host." % settings_file
        print "Done."

        #Sync DB
        #sudo('python manage.py syncdb --settings=settings.%s' % env.environment)
        print "Syncing DB..."
        run('%s manage.py syncdb --settings=settings.%s' % (env.python, env.environment))
        print "Done."

        #Run South migrations
        #sudo('python manage.py migrate --all --settings=settings.%s' % env.environment)
        print "Running South migrations..."
        run('%s manage.py migrate --all --settings=settings.%s' % (env.python, env.environment))
        print "Done."

        #Collect static
        print "Collecting static files..."
        run('%s manage.py collectstatic --noinput --settings=settings.%s' % (env.python, env.environment))
        print "Done."

        #Restart redis
        #sudo('service redis-server restart')

        #Restart celery workers
        #print "Restarting celery workers...."
        #sudo('supervisorctl restart %s' % env.celeryd_name)
        #print "Done."

        #Restart gunicorn server
        print "Restarting gunicorn server..."
        sudo('supervisorctl restart %s' % env.gunicorn_name)
        print "Done."

        #Restart nginx server
        print "Restarting nginx..."
        sudo('service nginx restart')
        print "Done."
