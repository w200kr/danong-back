from backend.settings.base import *

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INTERNAL_IPS = [
    '127.0.0.1',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
