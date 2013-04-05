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
    # sudo('apt-get -y -qq upgrade')
    sudo('apt-get -y -qq install python python-pip nginx redis-server mysql-server python-mysqldb libmysqlclient-dev libxml2-dev libxslt1-dev python-dev supervisor vim')
    sudo('update-rc.d nginx defaults')
    #install python packages
    sudo('pip install virtualenv virtualenvwrapper')
    #make directories
    sudo('mkdir -p /srv/www/menus-dev')
    sudo('mkdir -p /srv/www/menus-dev/logs')
    # run('mkdir -p ~/apps/menus-staging')
    #config files
    if env.environment == 'vagrant':
        put('settings/config/nginx-%s.conf' % env.environment, '/etc/nginx/nginx.conf', use_sudo=True)
        put('settings/config/supervisord-%s.conf' % env.environment, '/etc/supervisor/supervisord.conf', use_sudo=True)
        with settings(warn_only=True):
            sudo('service nginx restart')
            sudo('service supervisor restart')
    #setup virtualenv
    run('mkdir -p %s' % env.venv_dir)
    run('echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.profile')
    run('mkvirtualenv %s' % env.venv_name)
    #setup mysql databases
    #may fail because already exists, etc--if so, will continue
    with settings(warn_only=True):
        run('mysqladmin -u root create %s' % (DB_NAME))
        run('mysql -uroot -e "GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'"' % (DB_NAME, DB_USER, DB_PASSWORD))
    #do ln last in case it fails on vagrant
    #may fail due to virtualbox weirdness, if so, will continue
    with settings(warn_only=True):
        if env.environment == 'vagrant':
            sudo('ln -s /vagrant /srv/www/menus-dev/http')


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
            #sudo('python manage.py syncdb --settings=settings.%s' % env.environment)
            print "Syncing DB..."
            # run('%s manage.py syncdb --settings=settings.%s' % (env.python, env.environment))
            run('python manage.py syncdb --settings=settings.%s' % (env.environment))
            print "Done."

            #Run South migrations
            #sudo('python manage.py migrate --all --settings=settings.%s' % env.environment)
            print "Running South migrations..."
            # run('%s manage.py migrate --all --settings=settings.%s' % (env.python, env.environment))
            run('python manage.py migrate --all --settings=settings.%s' % (env.environment))
            print "Done."

            #Collect static
            print "Collecting static files..."
            # run('%s manage.py collectstatic --noinput --settings=settings.%s' % (env.python, env.environment))
            sudo('python manage.py collectstatic --noinput --settings=settings.%s' % (env.environment))
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
