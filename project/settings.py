"""
Django settings for unicaronas_api project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
from datetime import timedelta
from celery.schedules import crontab

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Website root url
ROOT_URL = os.environ.get('ROOT_URL', 'http://localhost:8000')

# Project name
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Unicaronas')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production a secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'abc123')
# 256 bit prime
SECRET_PRIME = int(os.environ.get('SECRET_PRIME', '1'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get('DEBUG', 'False').capitalize())

# manage.py test mode that disables fb connection stuff
TEST_MODE = eval(os.environ.get('TEST_MODE', 'False').capitalize())

ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS', '["*"]'))

# Sentry

if not DEBUG and os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )


# Application definition

INSTALLED_APPS = [
    'scout_apm.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.humanize',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',

    'oauth',
    'user_data',
    'trips',
    'search',
    'third_parties',
    'alarms',

    'maintenance_mode',

    'debug_toolbar',

    'oauth2_provider',
    'rest_framework',
    'rest_framework_filters',
    'corsheaders',

    'django_extensions',

    'captcha',
    'analytical',

    'drf_yasg',
    'silk',
    'nplusone.ext.django',
    'djcelery_email',
    'django_celery_beat',
    'phonenumber_field',
    'watchman',

    'storages',
    'versatileimagefield',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'nplusone.ext.django.NPlusOneMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.fb_handle',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Since the site is behind Cloudflare, manually set it to use https
if eval(os.environ.get('USE_HTTPS', 'False')):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    os.environ['wsgi.url_scheme'] = 'https'
    os.environ['HTTPS'] = "on"

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True

FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
if not DEBUG and AWS_STORAGE_BUCKET_NAME:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Celery stuff
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_IMPORTS = ['project.tasks']
CELERY_BEAT_SCHEDULE = {
    'Clear old OAuth2 tokens': {
        'task': 'oauth.tasks.clear_oauth_tokens',
        'schedule': crontab(minute=0, hour=3)
    },
    'Clear old alarms': {
        'task': 'alarms.tasks.clear_alarms',
        'schedule': crontab(minute=30, hour=3)
    }
}


# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Email settings
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = eval(os.environ.get('EMAIL_USE_TLS', 'True'))
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
DEFAULT_CONTACT_EMAIL = os.environ.get('DEFAULT_CONTACT_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', EMAIL_HOST_USER)

ADMINS = [('Admin', os.environ.get('ADMIN_ACCOUNT')), ]

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'


# Debug Toolbar
SHOW_TOOLBAR_CALLBACK = eval(os.environ.get('SHOW_TOOLBAR_CALLBACK', 'DEBUG'))
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: SHOW_TOOLBAR_CALLBACK and r.user.is_superuser  # disables it
}


# Maintenance mode
MAINTENANCE_MODE = eval(os.environ.get('MAINTENANCE_MODE', 'False'))
MAINTENANCE_MODE_TEMPLATE = 'project/errors/503.html'
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_SUPERUSER = True


# OAuth2
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'basic:read': 'Seu primeiro e segundo nome',
        'profile:read': 'Seu aniversário e gênero',
        'phone:read': 'Seu número de celular',
        'email:read': 'Seu endereço de email principal e acadêmico',
        'student:read': 'Seu perfil de aluno na sua universidade',
        'driver:read': 'Informações sobre seu carro',
        'driver:preferences:read': 'Suas preferências como motorista',
        'alarms:read': 'Detalhes sobre os alarmes de caronas criados por você',
        'alarms:write': 'Criar, editar e apagar seus alarmes de caronas',
        'trips:read': 'Pesquisar caronas por você',
        'trips:driver:read': 'Detalhes sobre as caronas, e seus passageiros, em que você é motorista',
        'trips:driver:write': 'Criar, editar e apagar as caronas em que você é motorista e gerenciar seus passageiros',
        'trips:passenger:read': 'Informações sobre as caronas em que você é passageiro',
        'trips:passenger:write': 'Entrar e sair de caronas por você'
    },
    "DEFAULT_SCOPES": ['basic:read'],
    'REQUEST_APPROVAL_PROMPT': 'auto',
    'APPLICATION_MODEL': 'oauth.Application',
    'SCOPES_BACKEND_CLASS': 'oauth.scopes.CustomSettingsScopes',
    "REFRESH_TOKEN_GRACE_PERIOD_SECONDS": 120,
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
    "REFRESH_TOKEN_EXPIRE_SECONDS": timedelta(days=60)  # Refresh tokens live up to 60 days
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth.Application'


# Rest settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'project.pagination.CustomLimitOffsetPagination',
    # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser'],
    'EXCEPTION_HANDLER': 'project.exceptions.custom_exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1.0',
    'ALLOWED_VERSIONS': ['v1.0'],
    'DEFAULT_THROTTLE_CLASSES': (
        'project.throttling.ApplicationBurstRateThrottle',
        'project.throttling.ApplicationSustainedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'application_burst': '60/min',  # Burst application calls
        'application_sustained': '10000/day',   # Sustained application calls
    }
}


# Sites framework
SITE_ID = int(os.environ.get('SITE_ID', '1'))

# AllAuth settings
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"
ACCOUNT_FORMS = {
    'signup': 'user_data.forms.CustomSignupForm',
    'login': 'user_data.forms.CustomLoginForm',
}
SOCIALACCOUNT_FORMS = {
    'signup': 'user_data.forms.CustomSocialSignupForm'
}
ACCOUNT_SIGNUP_FORM_CLASS = 'user_data.forms2.ExtraSignupFields'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# ACCOUNT_ADAPTER = "project.adapters.AccountAdapter"


def ACCOUNT_USER_DISPLAY(user):
    return user.first_name


SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_LOGOUT_ON_GET = True


# Captcha Settings
NOCAPTCHA = True
if not DEBUG:
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
else:
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Documentation settings
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'project.swagger_schema.CustomTagAutoSchema',
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'OAuth2': {
            'type': 'oauth2',
            'description': """
OAuth2 é uma forma de autenticação que permite que seu aplicativo obtenha acesso granular aos dados dos seus usuários. Seu usuário tem controle total sobre quais informações deseja compartilhar e você acessa a API usando endpoints comuns HTTP. OAuth2 possui flows para aplicativos web, desktop e mobile, todos implementados na API do Unicaronas. Para saber mais, [visite o guia de OAuth2](/what_is_oauth/)

Abaixo você encontrará os `scopes` disponíveis e suas descrições, além das URLs de autorização e troca de tokens.

*Atenção!* `refresh_token`s do Unicaronas têm vida útil de 60 dias e tokens antigos são removidos todo dia.""",
            'authorizationUrl': f'{ROOT_URL}/o/authorize/',
            'tokenUrl': f'{ROOT_URL}/o/token/',
            'flow': 'accessCode',
            'scopes': OAUTH2_PROVIDER['SCOPES']
        }
    },
    'OAUTH2_CONFIG': {
        'clientId': '9hzg1FNkZPeR1761B460TTDyYH8dkfjkzTXgYuaz',
        'clientSecret': 'Bg76qkj0ci7gPCtWrqvZniVkuh1KAYpVKcWzq4o1ryDtWu60qHJDg50a7bkSxEHFUVPGSvRnPPBvc6zEle5jKrlpb7n0jX8p7ulL5HBE9OP1S7mwZabHTRBP7SL1OACQ',
        'appName': 'Seu aplicativo'
    },
}


# Phonenumbers
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'BR'

# Geocoding API
GEOCODING_API_KEY = os.environ.get('GEOCODING_API_KEY')

# Analytics
GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get('GOOGLE_ANALYTICS_PROPERTY_ID')
GOOGLE_ANALYTICS_SITE_SPEED = True


# Profiling
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PERMISSIONS = lambda user: user.is_superuser
SILKY_META = True
SILKY_MAX_RECORDED_REQUESTS = 10**3
SILKY_INTERCEPT_PERCENT = 100 if DEBUG else 0


# Watchman
WATCHMAN_CHECKS = (
    'project.status_checks.redis_check',
    'project.status_checks.celery_check',
    'project.status_checks.google_apis',
    'project.status_checks.facebook',
    'project.status_checks.blablacar',
    'project.status_checks.email',
    'watchman.checks.databases',
    'watchman.checks.caches',
    'watchman.checks.storage',
)
WATCHMAN_ENABLE_PAID_CHECKS = not DEBUG


# Scout settings
SCOUT_MONITOR = not DEBUG
SCOUT_KEY = os.environ.get('SCOUT_KEY')
SCOUT_NAME = os.environ.get('SCOUT_NAME', 'Unicaronas')


# Email variables
FACEBOOK_HANDLE = os.environ.get('FACEBOOK_HANDLE', 'Unicaronas2.0')

# BlaBlaCar API Key
BLABLACAR_API_KEY = os.environ.get('BLABLACAR_API_KEY')

# Facebook Page token
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')

# Get GDAL_LIBRARY_PATH from env during heroku's build
_GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', None)
if _GDAL_LIBRARY_PATH:
    GDAL_LIBRARY_PATH = _GDAL_LIBRARY_PATH
_GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH', None)
if _GEOS_LIBRARY_PATH:
    GEOS_LIBRARY_PATH = _GEOS_LIBRARY_PATH


# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^(\/api\/.*|\/o\/token\/)$'
