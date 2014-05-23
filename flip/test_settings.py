import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# disable frame.Loader in tests, don't need it
TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# ASSETS_ROOT = os.path.join(BASE_DIR, 'flip', 'static')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

USER_ID = 'tester'
USER_GROUPS = []
USER_ROLES = ['Administrator']

VIEW_ROLES = ('Administrator', 'Contributor', 'Viewer')
EDIT_ROLES = ('Administrator', 'Contributor')

SKIP_EDIT_AUTH = False

# WARNING!!
# This is a hack until there's a setting in django-assets
# to force using staticfiles finders and avoid the need
# to run collectstatics before each test run.
# see https://github.com/streema/webapp/pull/3079
# Just put this in your test settings.

from django_assets.env import DjangoResolver
use_staticfiles = property(lambda self: True)
DjangoResolver.use_staticfiles = use_staticfiles
