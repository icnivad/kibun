import os
import sys

from django.core.handlers.wsgi import WSGIHandler

#os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = 'kibun.settings'
application=WSGIHandler() 
