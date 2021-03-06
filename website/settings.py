from pathlib import Path
import os
from django.conf.global_settings import gettext_noop as _
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

# environ.Env.read_env(env_file=".env")


############################ START TEST ################################

SECRET_KEY = '(gj1d*7w2y9$h2bp08om@e^nb2&8ype-@9)%^$pl#^_ki$&3^k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'student_grade.apps.StudentGradeConfig',
    'intro.apps.IntroConfig',
    'import_export',
    'bootstrap_pagination',
    'bootstrap4',
    'mathfilters',
    'ipware',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

# Special to AWS storage
AWS_ACCESS_KEY_ID = "AKIAVMWQFTTT7INMWRPJ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "django-testing-files"
AWS_HEADERS = {'Cache-Control': str('public, max-age=3')}
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = True
DEFAULT_FILE_STORAGE = "website.storage_backends.MediaStorage"
# The specified key does not exist.
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'


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

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eduhkchi',
        'USER': 'root',
        'PASSWORD': 'Tswnt31!',
        'HOST': 'localhost'
    },
    'default2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost'
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo',
        'USER': 'medoabdin',
        'PASSWORD': 'medo_rko96',
        'HOST': 'localhost'
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_COOKIE_NAME = 'language'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

############################# END TEST #################################

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env("SECURITY_KEY")
#
# ALLOWED_HOSTS = ['*']
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#
# # Application definition
# INSTALLED_APPS = [
#     'modeltranslation',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'student_grade.apps.StudentGradeConfig',
#     'intro.apps.IntroConfig',
#     'import_export',
#     'bootstrap_pagination',
#     'bootstrap4',
#     'mathfilters',
#     'ipware',
#     'storages'
# ]
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
#
# ROOT_URLCONF = 'website.urls'
#
# # Special to AWS storage
# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_HEADERS = {'Cache-Control': str('public, max-age=3')}
# AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL")
# AWS_S3_FILE_OVERWRITE = env("AWS_S3_FILE_OVERWRITE")
# DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
# # The specified key does not exist.
# AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
# AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION")
#
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# WSGI_APPLICATION = 'website.wsgi.application'
#
#
# # Database
# # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#
# DATABASES = {
#     'default1': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'eduhkchi',
#         'USER': 'root',
#         'PASSWORD': 'Tswnt31!',
#         'HOST': 'localhost'
#     },
#     'default2': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'demo',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost'
#     },
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env("DB_NAME"),
#         'USER': env("DB_USER"),
#         'PASSWORD': env("DB_PASSWORD"),
#         'HOST': env("DB_HOST")
#     },
# }
#
#
# # Password validation
# # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
#
#
# # Internationalization
# # https://docs.djangoproject.com/en/3.1/topics/i18n/
#
# LANGUAGE_CODE = 'en'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True
#
# LANGUAGE_COOKIE_NAME = 'language'
#
# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]


LANGUAGES = [
    ('zh-hans', _('Simplified Chinese')),
    ('zh-hant', _('Traditional Chinese')),
    ('en', 'English')
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Change the Django static URL to the Django S3boto3storage
# AWS_LOCATION = 'media'
# Domain Name Distribution => https://d1g3ayfrf0i21j.cloudfront.net
# AWS_S3_CUSTOM_DOMAIN = 'd1g3ayfrf0i21j.cloudfront.net'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "website.storage_backends.StaticStorage"
# STATIC_LOCATION = 'static'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
# MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_ROOT = MEDIA_URL
