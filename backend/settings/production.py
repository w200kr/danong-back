from backend.settings.base import *

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_WHITELIST = [
    "http://danong-dev.s3-website.ap-northeast-2.amazonaws.com",
    "http://localhost:3000",
]
CSRF_TRUSTED_ORIGINS = [
    'danong-dev.s3-website.ap-northeast-2.amazonaws.com',
    "localhost:3000",
]

# ec2, s3
ALLOWED_HOSTS = ['3.35.207.184']
ALLOWED_HOSTS += ['localhost', '127.0.0.1',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': "danong-db",
        'NAME': "dbmaster",
        'HOST': "ls-5db51d29d29b23f6ec09ad79b01329c88317ebff.ckt4xrz0zrhs.ap-northeast-2.rds.amazonaws.com",
        'PORT': 3306,
        'USER': "asin",
        'PASSWORD': "#|Z:#8]sT6NQF#E2=dIWk-.48ghLe!9=",
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}