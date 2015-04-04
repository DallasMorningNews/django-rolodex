
#######################
## DATABASE SETTINGS ##
#######################
import dj_database_url
from django.conf import settings
import os

if not settings.DATABASES.has_key('rolodex'):
	if os.environ.has_key('ROLODEX_DB'):
	    settings.DATABASES['rolodex'] = dj_database_url.parse(os.environ.get('ROLODEX_DB'))
	    settings.DATABASE_ROUTERS.append('rolodex.routers.RolodexRouter')
else:
	settings.DATABASE_ROUTERS.append('rolodex.routers.RolodexRouter')
#######################################################

if not hasattr(settings, 'ROLODEX_SECURE'):
	settings.ROLODEX_SECURE = True

settings.TEMPLATE_CONTEXT_PROCESSORS += ('rolodex.context_processors.modal_context',)

###################
## Custom Config ##
###################

from django.apps import AppConfig

class RolodexConfig(AppConfig):
	name = 'rolodex'
	verbose_name='Rolodex'