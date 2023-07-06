# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, '/var/www/u1818887/data/www/idigital38.online/idigital38')
sys.path.insert(1, '/var/www/u1818887/data/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'idigital38.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
