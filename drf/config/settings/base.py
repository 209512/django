# config/settings/base.py

from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 .env 파일 로드
load_dotenv()


# SECRET KEY (공통 환경변수에서 불러오기)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


# 프로젝트 최상위 폴더 기준 경로
BASE_DIR = Path(__file__).resolve().parent.parent
# ↑ settings 폴더가 config 밑에 있으니 .parent 세 번


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'apps.users',
    'apps.restaurants',
    'apps.reviews',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'django_cleanup',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# DRF 설정
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# auth
AUTH_USER_MODEL = 'users.User'


# simple jwt
SIMPLE_JWT = {
    # 엑세스 토큰의 유효 기간 설정
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    # 리프레쉬 토큰의 유효 기간 설정
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # jwt 로그인 시 last_login 업데이트 설정
    "UPDATE_LAST_LOGIN": True,
    # jwt 암호화 알고리즘
    "ALGORITHM": "HS256",
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'