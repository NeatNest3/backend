"""
Django settings for cleaning_app project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
#from dotenv import load_dotenv
import os
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

#load_dotenv()
LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g4#_*pbb@omzq$rc3r=@7b#vaa2l+ahrqnas*p^o28%u$g%!2%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ ]

AUTH_USER_MODEL = 'main.User'


# Application definition

GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdal309.dll"

GEOS_LIBRARY_PATH = r"C:\OSGeo4W\bin\geos_c.dll"




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cleaning_app.main.apps.MainConfig',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


ROOT_URLCONF = 'cleaning_app.cleaning_app.urls'
# Allow all domains (for testing, use with caution in production)
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cleaning_app.cleaning_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


try:
    from .local_settings import *
except ImportError:
    pass


AWS_ACCESS_KEY_ID = 'AKIA6NINTDPMKXSITS4F'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'cleaningapp'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'cleaning_app.main.utils.FirebaseAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


LAMBDA_API_URL = "https://yddlnybva9.execute-api.us-west-2.amazonaws.com/default/s3LambdaFunction"
