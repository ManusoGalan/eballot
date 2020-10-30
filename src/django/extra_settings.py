from .settings import *

DATABASES = {
	'default':{
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'eballot-django-db',
		'USER': 'admin',
		'PASSWORD': 'admin',
		'HOST': 'django_db'
	}
}
