#####################
# DATABASE SETTINGS #
#####################
import dj_database_url
from django.conf import settings
import os

if 'rolodex' not in settings.DATABASES:
	if 'ROLODEX_DB' in os.environ:
		settings.DATABASES['rolodex'] = dj_database_url.parse(os.environ.get('ROLODEX_DB'))
		settings.DATABASE_ROUTERS.append('rolodex.routers.RolodexRouter')
else:
	settings.DATABASE_ROUTERS.append('rolodex.routers.RolodexRouter')
#######################################################

if not hasattr(settings, 'ROLODEX_SECURE'):
	settings.ROLODEX_SECURE = True

#################
# Custom Config #
#################

from django.apps import AppConfig


class RolodexConfig(AppConfig):
	name = 'rolodex'
	verbose_name = 'Rolodex'
