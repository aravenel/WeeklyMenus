from fabric.api import *
#from fabric.operations import *
import os
from sys import exit
from socket import gethostname

try:
    # from settings.passwords_staging import DB_NAME, DB_USER, DB_PASS
    from settings.passwords_staging import *
except ImportError:
    print "Cannot import passwords_staging file."
    exit()

#
#   TODO
#
#   -Remove config dict--put in environment sections
#   -Separate out install steps into functions
#   -Make passwords file dependent on environment (dev vs staging vs vagrant)
#   -Make gunicorn conf dependent on environment
#

CONFIG = {
    'dev': {
        'repo': 'dev',
    },
    'staging': {
        #Name of the branch to use
        'repo': 'staging',
        #Location where the code is stored
        'code_dir': '/home/ravenel/apps/menus-staging/WeeklyMenus',
        #Virtualenvwrapper directory
        'venv_dir': '/home/vagrant/.venvs',
        #Virtualenvwrapper venv name
        'venv_name': 'menus-dev',
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
        'repo': 'develop',
        #Location where the code is stored
        'code_dir': '/vagrant',
        #Virtualenvwrapper directory
        'venv_dir': '/home/vagrant/.venvs',
        #Virtualenvwrapper venv name
        'venv_name': 'menus-dev',
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
    env.environment = 'staging'
    env.hosts = CONFIG[env.environment]['hosts']
    env.code_dir = CONFIG[env.environment]['code_dir']
    env.repo = CONFIG[env.environment]['repo']
    env.venv_dir = CONFIG[env.environment]['venv_dir']
    env.venv_name = CONFIG[env.environment]['venv_name']
    env.merges_from = 'develop'
    env.python = CONFIG[env.environment]['python']
    env.supervisord_group = CONFIG[env.environment]['supervisord_group']
    env.user = 'ravenel'
    env.key_filename = key_locations[gethostname()]


def vagrant():
    env.environment = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    env.code_dir = CONFIG[env.environment]['code_dir']
    env.repo = CONFIG[env.environment]['repo']
    env.venv_dir = CONFIG[env.environment]['venv_dir']
    env.venv_name = CONFIG[env.environment]['venv_name']
    env.user = 'vagrant'
    env.run_user = 'www-data'
    env.merges_from = 'develop'
    env.python = CONFIG[env.environment]['python']
    env.supervisord_group = CONFIG[env.environment]['supervisord_group']
    ssh_keyfile = local('vagrant ssh-config | grep IdentityFile', capture=True)
    if os.name == 'nt':
        env.key_filename = ssh_keyfile.split()[1].replace(r'/', '\\').replace('\"', '')
    else:
        env.key_filename = ssh_keyfile.split()[1].replace('\"', '')


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
    #install packages
    sudo('apt-get -qq update')
    #sudo('apt-get -y -qq upgrade')
    sudo('apt-get -y -qq install python python-pip nginx redis-server postgresql postgresql-server-dev-all libxml2-dev libxslt1-dev python-dev supervisor vim libjpeg62 libjpeg62-dev zlib1g-dev')
    sudo('update-rc.d nginx defaults')

    #install python packages
    sudo('pip install virtualenv virtualenvwrapper')

    #make directories
    sudo('mkdir -p /srv/www/menus-dev')
    sudo('mkdir -p /srv/www/menus-dev/logs')
    sudo('chown %s /srv/www/menus-dev/logs' % env.run_user)
    #FIX THIS FOR REAL
    sudo('chmod -R 777 /srv/www/menus-dev/logs')

    sudo('mkdir -p /srv/www/menus-dev/http/logs')
    sudo('chown %s /srv/www/menus-dev/http/logs' % env.run_user)
    #FIX THIS FOR REAL
    sudo('chmod -R 777 /srv/www/menus-dev/http/logs')

    sudo('mkdir -p /srv/www/menus-dev/media')
    sudo('mkdir -p /srv/www/menus-dev/media/cache')
    sudo('chown %s /srv/www/menus-dev/media' % env.run_user)
    sudo('chmod -R 777 /srv/www/menus-dev/media')
    # run('mkdir -p ~/apps/menus-staging')

    #config files
    if env.environment == 'vagrant':
        put('settings/config/nginx-%s.conf' % env.environment, '/etc/nginx/nginx.conf', use_sudo=True)
        put('settings/config/supervisord-%s.conf' % env.environment, '/etc/supervisor/supervisord.conf', use_sudo=True)
        #put('settings/config/supervisord.conf', '/etc/supervisor/supervisord.conf', use_sudo=True)
        with settings(warn_only=True):
            sudo('service nginx restart')
            sudo('service supervisor restart')

    #setup virtualenv
    run('mkdir -p %s' % env.venv_dir)
    run('echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.profile')
    run('mkvirtualenv %s' % env.venv_name)

    #setup pgsql databases
    #may fail because already exists, etc--if so, will continue
    with settings(warn_only=True):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD \'%s\'"' % (DB_USER, DB_PASSWORD), user='postgres')
        sudo('psql -c "CREATE DATABASE %s WITH OWNER %s ENCODING \'UTF8\' LC_CTYPE=\'en_US.utf8\' LC_COLLATE=\'en_US.utf8\' TEMPLATE=template0"' % (DB_NAME, DB_USER), user='postgres')

    #do ln last in case it fails on vagrant
    #may fail due to virtualbox weirdness, if so, will continue
    with settings(warn_only=True):
        if env.environment == 'vagrant':
            sudo('ln -s /vagrant /srv/www/menus-dev/http')

    #Start supervisor
    sudo('service supervisor start')


def deploy():
    with cd(env.code_dir):
        if env.environment != 'vagrant':
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

        with prefix('workon %s' % env.venv_name):
            #Make sure all packages are up to date
            sudo('pip install -r requirements.txt')

            #Sync DB
            print "Syncing DB..."
            run('python manage.py syncdb --settings=settings.%s' % (env.environment))
            print "Done."

            #Run South migrations
            print "Running South migrations..."
            #What. The. Fuck. Why do I have to run them indiv before --all?
            run('python manage.py migrate recipemanager --settings=settings.%s' % (env.environment))
            run('python manage.py migrate menumanager --settings=settings.%s' % (env.environment))
            run('python manage.py migrate feedmanager --settings=settings.%s' % (env.environment))
            run('python manage.py migrate --all --settings=settings.%s' % (env.environment))
            print "Done."

            #Collect static
            print "Collecting static files..."
            # run('%s manage.py collectstatic --noinput --settings=settings.%s' % (env.python, env.environment))
            sudo('python manage.py collectstatic --noinput --settings=settings.%s' % (env.environment))
            print "Done."


        #Restart supervisord groups
        print "Restarting supervisord programs..."
        sudo('supervisorctl restart %s:' % env.supervisord_group)
        print "Done."

        #Restart redis
        #sudo('service redis-server restart')

        #Restart nginx server
        #print "Restarting nginx..."
        #sudo('service nginx restart')
        #print "Done."
