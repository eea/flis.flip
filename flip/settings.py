"""
Django settings for flip project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

DEBUG = False

TEMPLATE_DEBUG = False

ASSETS_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frame',
    'django_assets',
    'widget_tweaks',
    'gunicorn',
    'flip_auth',
    'flis_metadata.common',
    'flis_metadata.client',
    'flip',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'frame.middleware.RequestMiddleware',
    'frame.middleware.UserMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'frame.middleware.SeenMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'frame.backends.FrameUserBackend',
)

TEMPLATE_LOADERS = (
    'frame.loaders.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'flip.context_processors.site',
)

ROOT_URLCONF = 'flip.urls'

WSGI_APPLICATION = 'flip.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Dynamic config
FORCE_SCRIPT_NAME = os.environ.get('FORCE_SCRIPT_NAME', '')
if FORCE_SCRIPT_NAME:
    USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = FORCE_SCRIPT_NAME + '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {'mail_admins': {'level': 'ERROR',
                                 'class': 'django.utils.log.AdminEmailHandler',
                                 },
                 },
    'loggers': {'django.request': {'handlers': ['mail_admins'],
                                   'level': 'ERROR',
                                   'propagate': True,
                                   },
                },
    }

FRAME_SEEN_MODELS = (
    ('flip.models.Study', 'created_on'),
)

FRAME_SEEN_EXCLUDE = ('/_lastseencount/', )

SKIP_EDIT_AUTH = False

SITE_URL = ''

METADATA_URL = ''

try:
    from local_settings import *
except ImportError:
    pass


if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass
