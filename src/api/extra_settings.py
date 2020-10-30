from .settings import *

DATABASES = {
	'default':{
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'eballot-api-db',
		'USER': 'admin',
		'PASSWORD': 'admin',
		'HOST': 'api_db'
	}
}


INSTALLED_APPS += ['rest_framework', ]
