import os

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']

STATIC_URL = 'django_static/'
STATIC_ROOT = 'django_static/'
MEDIA_URL = 'django_media/'
STATIC_MEDIA = 'django_media/'
REQUEST_RATE_LIMIT = int(os.environ.get('REQUEST_RATE_LIMIT', 15))
AUTH_API_LOGIN_URL = 'http://nginx/api/v1/users/login'
