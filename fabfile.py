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
            #Group containing programs in supervisord.conf
            'supervisord_group': 'menus-staging',
            #Hosts to use
            'hosts': [
                #'http://menus-dev.alexravenel.com',
                'www.alexravenel.com'
                ],
            },
        'vagrant': {
            #Name of the branch to use
            'repo': 'staging',
            #Location where the code is stored
            'code_dir': '~/apps/menus-staging/WeeklyMenus',
            #Location of python executable--for virtualenv
            'python': '~/apps/menus-staging/WeeklyMenus/venv/bin/python',
            #Group containing programs in supervisord.conf
            'supervisord_group': 'menus-staging',
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
        'glaurung': r'/home/ravenel/.ssh/id_rsa',
        }


def staging():
    env.hosts = CONFIG['staging']['hosts']
    env.code_dir = CONFIG['staging']['code_dir']
    env.repo = CONFIG['staging']['repo']
    env.environment = 'staging'
    env.merges_from = 'develop'
    env.python = CONFIG['staging']['python']
    env.supervisord_group = CONFIG['staging']['supervisord_group']
    env.user = 'ravenel'
    env.key_filename = key_locations[gethostname()]

def vagrant():
    env.hosts = ['127.0.0.1:2222']
    env.code_dir = CONFIG['vagrant']['code_dir']
    env.user = 'vagrant'
    env.repo = CONFIG['staging']['repo']
    env.environment = 'vagrant'
    env.merges_from = 'develop'
    env.python = CONFIG['staging']['python']
    env.supervisord_group = CONFIG['staging']['supervisord_group']
    ssh_keyfile = local('vagrant ssh-config | grep IdentityFile', capture=True)
    if os.name == 'nt':
        env.key_filename = ssh_keyfile.split()[1].replace(r'/', '\\').replace('\"', '')
    else:
        env.key_filename = ssh_keyfile.split()[1]


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
        env.supervisord_group = CONFIG['prod']['supervisord_group']
        env.user = 'ravenel'
        env.key_filename = key_locations[gethostname()]
    else:
        exit()

def merge():
    local('git checkout %s' % env.repo)
    local('git merge %s' % env.merges_from)

def push():
    local('git push origin %s' % env.repo)

def provision():
    #install basic background
    sudo('apt-get -qq update')
    sudo('apt-get -y -qq upgrade')
    sudo('apt-get -y -qq install python python-pip nginx redis-server mysql-server python-mysqldb')
    sudo('update-rc.d nginx defaults')
    #install python packages
    sudo('pip install supervisor gunicorn')
    #make directories
    sudo('mkdir -p /srv/www/menus-dev')
    run('mkdir -p ~/apps/menus-staging')
    sudo('ln -s /vagrant /srv/www/menus-dev/http')
    #deploy config files
    #nginx config
    if env.environment == 'vagrant':
        put('config/nginx.conf', '/etc/nginx/nginx.conf', use_sudo=True)
        put('config/nginx-enabled.conf', '/etx/nginx/sites-available/', use_sudo=True)
    elif env.environment == 'staging':
        pass

def deploy():
    with cd(env.code_dir):
        #Checkout new code
        #sudo('git pull')
        #sudo('git checkout %s' % env.repo)
        print "Checking out code...",
        run('git reset --hard HEAD')
        run('git checkout %s' % env.repo)
        run('git pull')

        #Push passwords file to host
        settings_file = os.path.join('settings', 'passwords_%s.py' % env.environment)
        if os.path.isfile(settings_file):
            put(settings_file, 'settings')
        else:
            print "Settings file %s does not exist. Cannot copy to host." % settings_file
        print "Done."

        #Make sure all packages are up to date
        sudo('pip install -r requirements.txt')

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

        #Restart supervisord groups
        print "Restarting supervisord programs..."
        sudo('supervisorctl restart %s:' % env.supervisord_group)
        print "Done."

        #Restart nginx server
        #print "Restarting nginx..."
        #sudo('service nginx restart')
        #print "Done."
