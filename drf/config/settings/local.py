# config/settings/local.py

from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = []

# Static
STATIC_URL = 'static/'
STATIC_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

# Media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# PostgreSQL (도커 컨테이너 연결)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}