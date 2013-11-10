from fabric.api import *
#from fabric.operations import *
import os
from sys import exit, path
from socket import gethostname

#
#   TODO
#   -Make passwords file dependent on environment (dev vs staging vs vagrant)
#   -Make gunicorn conf dependent on environment
#

key_locations = {
    'usnycaravenel1': r'C:\Users\aravenel\pri-openssh.ppk',
    'glaurung': r'/home/ravenel/.ssh/id_rsa',
}

#Insert current dir into path so we can do imports
path.insert(0, os.path.dirname(os.path.realpath(__file__)))


##################################################
#
#   ENVIRONMENT CONFIG
#
##################################################

def staging():
    env.environment = 'staging'
    env.hosts = ['www.alexravenel.com']
    env.code_dir = '/home/ravenel/apps/menus-staging/WeeklyMenus'
    env.repo = 'staging'
    env.venv_dir = '/home/vagrant/.venvs'
    env.venv_name = 'menus-dev'
    env.merges_from = 'develop'
    env.python = '/home/ravenel/apps/menus-staging/WeeklyMenus/venv/bin/python',
    env.supervisord_group = 'menus-staging'
    env.user = 'ravenel'
    env.key_filename = key_locations[gethostname()]
    env.pw = import_pwfile(env.environment)


def vagrant():
    env.environment = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    env.code_dir = '/vagrant'
    env.repo = 'develop'
    env.venv_dir = '/home/vagrant/.venvs'
    env.venv_name = 'menus-dev'
    env.user = 'vagrant'
    env.run_user = 'www-data'
    env.merges_from = 'develop'
    env.python = '~/apps/menus-staging/WeeklyMenus/venv/bin/python',
    env.supervisord_group = 'menus-staging'
    ssh_keyfile = local('vagrant ssh-config | grep IdentityFile', capture=True)
    if os.name == 'nt':
        env.key_filename = ssh_keyfile.split()[1].replace(r'/', '\\').replace('\"', '')
    else:
        env.key_filename = ssh_keyfile.split()[1].replace('\"', '')
    env.pw = import_pwfile(env.environment)


def prod():
    print "\n\nWARNING! You are about to deploy to production!\n\n"
    print "If you wish to continue, enter Yes:"
    ans = raw_input()
    if ans.upper in ['YES']:
        env.environment = 'prod'
        env.hosts = ['www.alexravenel.com']
        env.code_dir = '/srv/www/menus-prod'
        env.repo = 'master'
        env.venv_dir = '/home/vagrant/.venvs'
        env.venv_name = 'menus-prod'
        env.merges_from = 'develop'
        env.python = '/home/ravenel/apps/menus-staging/WeeklyMenus/venv/bin/python',
        env.supervisord_group = 'menus-staging'
        env.user = 'ravenel'
        env.key_filename = key_locations[gethostname()]
        env.pw = import_pwfile(env.environment)
    else:
        exit()


##################################################
#
#   HELPER FUNCTIONS
#
##################################################

def import_pwfile(environment):
    try:
        # from settings.passwords_staging import DB_NAME, DB_USER, DB_PASS
        #from settings.passwords_staging import *
        return __import__("settings.passwords_%s" % environment)
    except ImportError, e:
        print "Cannot import passwords file:"
        print e
        print '\nCurrent import paths:\n%s' % '\n'.join(p for p in path)
        exit()

def merge():
    local('git checkout %s' % env.repo)
    local('git merge %s' % env.merges_from)

def push():
    local('git push origin %s' % env.repo)

def install_prereqs(upgrade=False):
    """Install system packages and python prereqs"""
    #install packages
    sudo('apt-get -qq update')
    if upgrade:
        sudo('apt-get -y -qq upgrade')
    sudo('apt-get -y -qq install python python-pip nginx redis-server postgresql postgresql-server-dev-all libxml2-dev libxslt1-dev python-dev supervisor vim libjpeg62 libjpeg62-dev zlib1g-dev')
    sudo('update-rc.d nginx defaults')

    #install python packages
    sudo('pip install virtualenv virtualenvwrapper')

def setup_folders(run_user):
    """Setup and permission folders"""
    #make directories
    sudo('mkdir -p /srv/www/menus-dev')
    sudo('mkdir -p /srv/www/menus-dev/logs')
    sudo('chown %s /srv/www/menus-dev/logs' % run_user)
    #FIX THIS FOR REAL
    sudo('chmod -R 777 /srv/www/menus-dev/logs')

    sudo('mkdir -p /srv/www/menus-dev/http/logs')
    sudo('chown %s /srv/www/menus-dev/http/logs' % run_user)
    #FIX THIS FOR REAL
    sudo('chmod -R 777 /srv/www/menus-dev/http/logs')

    sudo('mkdir -p /srv/www/menus-dev/media')
    sudo('mkdir -p /srv/www/menus-dev/media/cache')
    sudo('chown %s /srv/www/menus-dev/media' % run_user)
    sudo('chmod -R 777 /srv/www/menus-dev/media')
    # run('mkdir -p ~/apps/menus-staging')

def push_config_files(environment):
    """Push config files (nginx, supervisord) to host"""
    #config files
    if environment == 'vagrant':
        put('settings/config/nginx-%s.conf' % environment, '/etc/nginx/nginx.conf', use_sudo=True)
        put('settings/config/supervisord-%s.conf' % environment, '/etc/supervisor/supervisord.conf', use_sudo=True)
        #put('settings/config/supervisord.conf', '/etc/supervisor/supervisord.conf', use_sudo=True)
        with settings(warn_only=True):
            sudo('service nginx restart')
            sudo('service supervisor restart')

def setup_virtualenv(venv_dir, venv_name):
    """Setup virtual environments on the host"""
    run('mkdir -p %s' % venv_dir)
    run('echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.profile')
    run('mkvirtualenv %s' % venv_name)

def create_database(user, password, name):
    """Create database and user"""
    #may fail because already exists, etc--if so, will continue
    with settings(warn_only=True):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD \'%s\'"' % (user, password), user='postgres')
        sudo('psql -c "CREATE DATABASE %s WITH OWNER %s ENCODING \'UTF8\' LC_CTYPE=\'en_US.utf8\' LC_COLLATE=\'en_US.utf8\' TEMPLATE=template0"' % (name, user), user='postgres')

def update_code(code_dir, repo):
    """Get new code on the host"""
    with cd(code_dir):
        #sudo('git pull')
        #sudo('git checkout %s' % env.repo)
        print "Checking out code...",
        run('git reset --hard HEAD')
        run('git checkout %s' % repo)
        run('git pull')

def push_passwords(code_dir, environment):
    """Push password files to host"""
    with cd(code_dir):
        settings_file = os.path.join('settings', 'passwords_%s.py' % environment)
        if os.path.isfile(settings_file):
            put(settings_file, 'settings')
        else:
            print "Settings file %s does not exist. Cannot copy to host." % settings_file
        print "Done."

def prepare_django(code_dir, venv_name, environment):
    """Do django stuff--install python packages, sync db, run migrations, collect static"""
    with cd(code_dir):
        with prefix('workon %s' % venv_name):
            #Make sure all packages are up to date
            sudo('pip install -r requirements.txt')

            #Sync DB
            print "Syncing DB..."
            run('python manage.py syncdb --settings=settings.%s' % (environment))
            print "Done."

            #Run South migrations
            print "Running South migrations..."
            #What. The. Fuck. Why do I have to run them indiv before --all?
            run('python manage.py migrate recipemanager --settings=settings.%s' % (environment))
            run('python manage.py migrate menumanager --settings=settings.%s' % (environment))
            run('python manage.py migrate feedmanager --settings=settings.%s' % (environment))
            run('python manage.py migrate --all --settings=settings.%s' % (environment))
            print "Done."

            #Collect static
            print "Collecting static files..."
            sudo('python manage.py collectstatic --noinput --settings=settings.%s' % (environment))
            print "Done."



##################################################
#
#   MAIN FUNCTIONS
#
##################################################

def provision():
    """Setup a new host from scratch--install prereqs, database, etc"""

    #Setup the base software on the system
    install_prereqs()

    #Setup folders
    setup_folders(env.run_user)

    #Push over the config files
    push_config_files(env.environment)

    #setup virtualenv
    setup_virtualenv(env.venv_dir, env.venv_name)

    #setup pgsql databases
    create_database(env.pw.DB_USER, env.pw.DB_PASSWORD, env.pw.DB_NAME)

    #do ln last in case it fails on vagrant
    with settings(warn_only=True):
        if env.environment == 'vagrant':
            sudo('ln -s /vagrant /srv/www/menus-dev/http')

    #Start supervisor
    sudo('service supervisor start')


def deploy():
    """Deploy code to host"""

    if env.environment != 'vagrant':
        #Checkout new code
        update_code(env.code_dir, env.repo)

        #Push passwords file to host
        push_passwords(code_dir, env.environment)

    prepare_django(env.code_dir, env.venv_name, env.environment)

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
