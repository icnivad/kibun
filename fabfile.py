from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['kanjidoc@kanjidoc.webfactional.com']
prompt("Enter key: ", "password") 


#### local commands
def prep_deploy():
	local('git push origin master')

def local_migrate():
	local('python manage.py schemamigration ActivityChooser --auto')
	local('python manage.py syncdb')
	local('python manage.py migrate ActivityChooser')

####### Server Commands
def push():
	run('cd /home/kanjidoc/webapps/kibun/kibun/; git pull origin master')

def static_media():
	run('cd /home/kanjidoc/webapps/kibun/kibun/; python2.7 manage.py collectstatic')

def migrate_db():
	run('cd /home/kanjidoc/webapps/kibun/kibun/; python2.7 manage.py syncdb')
	run('cd /home/kanjidoc/webapps/kibun/kibun/; python2.7 manage.py migrate ActivityChooser')

def restart():
	run('/home/kanjidoc/webapps/kibun/apache2/bin/restart')

def stop():
	run('/home/kanjidoc/webapps/kibun/apache2/bin/stop')

def check_memory():
	run('cat /home/kanjidoc/logs/user/cron/cron.log | tail')
	run("ps -u kanjidoc -o rss,command | sed -e '1d' | awk '{s+=$1} END {print s}'")
	run("ps -u kanjidoc -o rss,command")

def deploy():
	prep_deploy()
	push()
	static_media()
	restart()

def migrate_deploy():
	prep_deploy()
	push()
	static_media()
	migrate_db()
	restart()

def get_fixture():
	run('cd /home/kanjidoc/webapps/kibun/kibun/; python2.7 manage.py dumpdata ActivityChooser > Fixtures/all_data.json')
	get('/home/kanjidoc/webapps/kibun/kibun/Fixtures/all_data.json', '~/Desktop/MoodToolkit/kibun/Fixtures/all_data.json')

