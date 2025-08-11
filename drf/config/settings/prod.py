# config/settings/prod.py

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

STATIC_URL = 'static/'
STATIC_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}