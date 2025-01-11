from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-gr&*j1(p!)n&fqgf=%)3ql0p_(rr2u^&kzol9^z)l5vsyg(r0+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}