"""
Django settings for prototype1 project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import timedelta

import os
import sys




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+7dv_n%_&1qiy%$e)$qvz@6p+y*v+g)j(-teu_eim%r-%=d4+n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Allow all hosts in development

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'debug_toolbar',
    'cloudinary',
    'cloudinary_storage',
    'social_django',
    'rest_framework_simplejwt',
    'prototype1',
    'main',
    'api',
    'inventory',
    'locker',
    'log',
    'session',
    'notification',
    'user',
    'qr_app',
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'prototype1.middleware.AutoLoginMiddleware',
    #'prototype1.middleware.JWTAuthMiddleware',
    



]
CSRF_TRUSTED_ORIGINS = [
    #"https://yourwebsite.com",
    "http://localhost:8000"
]
ROOT_URLCONF = 'prototype1.urls'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

        'rest_framework.permissions.IsAuthenticated',  # Only allow authenticated users to access certain views

    ], 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #cant use JWT without using JS to send headers
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ], 
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    
    'ROTATE_REFRESH_TOKENS': False,  # Get a new refresh token every time
    'BLACKLIST_AFTER_ROTATION': True,  # If True, blacklist the old refresh token after using it
    
    'USER_ID_FIELD': 'user_id', 
    
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
#SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_REQUIRE_POST = True

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/api/token'
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = "http://127.0.0.1:8000/auth/complete/google-oauth2/"  # Change for production

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dmlbtzzfx',  
    'API_KEY': '855239969956629',        
    'API_SECRET': 'LUxp_bytBTCajWA7z7EKZR7hTIg', 
}
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '112464825553-eb2pa2no6imar69ssprcnmru641p4hij.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'openid',  # Basic authentication
    'profile',  # Access to profile information
    'email',  # Access to email address
    'https://www.googleapis.com/auth/userinfo.profile',  # Access to user profile info
    'https://www.googleapis.com/auth/user.organization.read',  # Access to organization info
    #'https://www.googleapis.com/auth/user.birthday.read',
]
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    #"social_core.pipeline.social_auth.associate_by_email",  # Optional: Match by email
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.user.get_username",
    #"user.pipeline.check_user_domain",  
    "social_core.pipeline.user.create_user",

    #'user.pipeline.print_google_response',
    #"user.pipeline.allow_reassociation",
    #"user.pipeline.auto_login_existing_user",
    'user.pipeline.save_google_profile',
    'user.pipeline.save_google_session',
    #"user.pipeline.set_student_defaults",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
SOCIAL_AUTH_RAISE_EXCEPTIONS = True
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login/"  # Redirect to login page

AUTH_USER_MODEL = 'user.CustomUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'prototype1/templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        #'DIRS': [BASE_DIR / "prototype1/templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'prototype1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Check if we're running in Docker (deployment)
IN_DOCKER = os.environ.get('IN_DOCKER', False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'test3'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '1212312121'),
        'HOST': os.environ.get('DB_HOST', 'db' if IN_DOCKER else 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'TEST': {
            'NAME': 'test_se_locker',  # This will create a new database for testing
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Create static directory if it doesn't exist
if not os.path.exists(BASE_DIR / 'static'):
    os.makedirs(BASE_DIR / 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
