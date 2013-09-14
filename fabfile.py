from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['kanjidoc@kanjidoc.webfactional.com']
prompt("Enter key: ", "password") 

def push():
	run('cd /home/kanjidoc/webapps/kibun/; git pull origin master')

def static_media():
	run('cd /home/kanjidoc/webapps/kibun/; python2.7 manage.py collectstatic')

def restart():
	run('/home/kanjidoc/webapps/kibun/apache2/bin/restart')

def stop():
	run('/home/kanjidoc/webapps/kibun/apache2/bin/stop')

def check_memory():
	run('cat /home/kanjidoc/logs/user/cron/cron.log | tail')
	run("ps -u kanjidoc -o rss,command | sed -e '1d' | awk '{s+=$1} END {print s}'")
	run("ps -u kanjidoc -o rss,command")

def deploy():
	push()
	static_media()
	restart()