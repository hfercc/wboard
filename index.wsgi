import sys
import os.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'wboard.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), 'wboard'))

import sae
#import django.core.handlers.wsgi

#application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler())
from wboard import wsgi
application = sae.create_wsgi_app(wsgi.application)
import pylibmc
sys.modules['memcache'] = pylibmc