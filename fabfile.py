from fabric.operations import put, local, run
from fabric.context_managers import cd, prefix, lcd


def export():
    """Create a clean copy of the source code in /tmp
    This avoids us uploading git metadata.

    """
    local('rm -rf /tmp/podkastaro')
    local("git checkout-index -a -f --prefix=/tmp/podkastaro/")
    local('cp live_settings.py /tmp/podkastaro')
    with lcd('/tmp'):
        local('rm -f podkastaro.tar.gz')
        local('tar -zcf podkastaro.tar.gz podkastaro')
        local('rm -rf podkastaro')


def upload():
    run('mv ~/webapps/podkastaro/podkastaro ~/webapps/podkastaro/podkastaro_previous')
    put('/tmp/podkastaro.tar.gz', '~/webapps/podkastaro/podkastaro.tar.gz')
    run('tar -xzf ~/webapps/podkastaro/podkastaro.tar.gz --directory ~/webapps/podkastaro')
    run('rm ~/webapps/podkastaro/podkastaro.tar.gz')


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
