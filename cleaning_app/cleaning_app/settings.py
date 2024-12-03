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
import dj_database_url

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

DATABASES = {}
DATABASES["default"] = dj_database_url.parse("postgresql://cleaning_app_user:58vLesjsuDZQIhTzZWfVfQjPUqQ9PIza@dpg-ct2g58lsvqrc73ai5grg-a.virginia-postgres.render.com/cleaning_app")


#load_dotenv()
LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g4#_*pbb@omzq$rc3r=@7b#vaa2l+ahrqnas*p^o28%u$g%!2%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [ 'localhost', '127.0.0.1' ]

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
    # 'cleaning_app.middleware.DebugMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

# apiexample/settings.py

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'cleaning_app.main.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'cleaning_app.main.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': '{https://neatnest.tech}',
    'JWT_ISSUER': 'https://dev-jbo3q8bi8aocdmxp.us.auth0.com/',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

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

STATIC_URL = '/static/'

#Needed for Deployment (Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


try:
    from .local_settings import *
except ImportError:
    pass


AWS_ACCESS_KEY_ID = 'AKIAXZEFHXWUJ577PGU7'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = ' neatnest'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = '/media/'

MEDIA_URL = "https:// neatnest.s3.amazonaws.com/media/"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),                                        
}

# Default Auth in rest framework (simplejwt) is to integrate AuthO for Authentication on the backend

LAMBDA_API_URL = "https://cmfjyilffk.execute-api.us-west-2.amazonaws.com/default/s3LambdaFunction"

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}