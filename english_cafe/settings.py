import os
import environ

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# SECRET_KEY = 'django-insecure-8m!j8c&kvbkjf)g+%x8d(g1uk&w(8m3s5$gjnv25v#hck=-0qq'
SECRET_KEY = env('SECRET_KEY')

ENCRYPT_KEY = 'KJnV7b3HBayCUulAnxi5TsCo6W1FBiRccaBfpVAA95k='

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=env.int("ACCESS_TOKEN_LIFETIME")),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env.int("REFRESH_TOKEN_LIFETIME")),
}


DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = [ '*']

CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'ckeditor',
    'mailqueue',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'general',
    'courses',
    'company_profile',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'general.middlewares.RequestMiddleware',
]

ROOT_URLCONF = 'english_cafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'english_cafe.wsgi.application'


# Database

DATABASES = {
    'default': env.db(),
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT', cast=int)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_REPLY_TO_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = EMAIL_HOST_USER


# Static files (CSS, JavaScript, Images)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_URL = '/static/'
STATIC_FILE_ROOT = os.path.join(BASE_DIR, "static")
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
if not DEBUG:
    STATIC_ROOT = os.path.join('static')
    
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'class': 'django.utils.log.AdminEmailHandler',
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'include_html': True,
            },
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': "/var/log/english_cafe/project.log"
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False,
            },
            'mailqueue': {
                'handlers': ['logfile'],
                'level': 'DEBUG',
                'propagate': False
            },
        },
    }
