from fabric.operations import put, local, run
from fabric.context_managers import cd, prefix


def export():
    """Create a clean copy of the source code in /tmp
    This avoids us uploading git metadata.

    """
    local('rm -rf /tmp/podkastaro')
    local("git checkout-index -a -f --prefix=/tmp/podkastaro/")


def upload():
    run('mv ~/webapps/podkastaro/podkastaro ~/webapps/podkastaro/podkastaro_previous')
    run('mkdir -p ~/webapps/podkastaro/podkastaro')
    put('/tmp/podkastaro', '~/webapps/podkastaro') # note this creates ~/webapps/podkastaro/podkastaro
    put('live_settings.py', '~/webapps/podkastaro/podkastaro')


def update_dependencies():
    with prefix(". ~/.virtualenvs/podkastaro/bin/activate"):
        run("pip install -r ~/webapps/podkastaro/podkastaro/requirements.txt")


def update_db():
    with prefix(". ~/.virtualenvs/podkastaro/bin/activate"):
        with cd('~/webapps/podkastaro/podkastaro'):
            # FIXME
            run("python manage.py syncdb")
            run("python manage.py migrate podcasts")
    

def cleanup():
    """Remove local build artifacts and the previously deployed version."""
    local('rm -rf /tmp/podkastaro')
    run('rm -rf ~/webapps/podkastaro/podkastaro_previous')


def start():
    run('~/webapps/podkastaro/apache2/bin/start')
    

def stop():
    run('~/webapps/podkastaro/apache2/bin/stop')
    

def restart():
    run('~/webapps/podkastaro/apache2/bin/restart')
    

def deploy():
    # TODO: tag

    export()
    upload()

    stop()

    update_dependencies()
    update_db()

    start()
    cleanup()
