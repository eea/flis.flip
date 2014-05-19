import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# for test only to get the user details. frame.requests.get is mocked
FRAME_URL = True

SKIP_EDIT_AUTHORIZATION = False


# disable frame.Loader in tests, don't need it
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# ASSETS_ROOT = os.path.join(BASE_DIR, 'flip', 'static')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# WARNING!!
# This is a hack until there's a setting in django-assets
# to force using staticfiles finders and avoid the need
# to run collectstatics before each test run.
# see https://github.com/streema/webapp/pull/3079
# Just put this in your test settings.

from django_assets.env import DjangoResolver
use_staticfiles = property(lambda self: True)
DjangoResolver.use_staticfiles = use_staticfiles
