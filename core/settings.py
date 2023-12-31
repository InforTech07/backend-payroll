"""
Django settings for core project.
"""

from pathlib import Path
import os
import environ
from datetime import timedelta
env = environ.Env()
environ.Env.read_env()

ENVIRONMENT = env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='secret!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL="user.User"

# django apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

#project apps
PROJECT_APPS=[
    'apps.user', 
    'apps.company',
    'apps.employee',
    'apps.payroll',
    'apps.store',
    'apps.media',
]

#third party apps
THIRD_PARTY_APPS=[
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
]

INSTALLED_APPS= DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS 


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
#postgres
# DATABASES = {
#     'default': {
# 		'ENGINE': 'django.db.backends.postgresql_psycopg2',
# 		'NAME' : 'tconsultingsa-db',
# 		'USER' : 'InforTech07',
# 		'PASSWORD' : 'vogNu23qOhdK',
# 		'HOST' : 'ep-square-snow-67721858.us-west-2.aws.neon.tech', # localhost en caso de tenerlo en local y la URL de la base de datos en caso de tenerlo en algún servicio en la nube
# 		'PORT' : '5432' # Si usas el puerto default no pongas esta línea y si lo has cambiado especifícaselo aquí
# 	}
# }
DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME' : 'postgres',
		'USER' : 'postgres',
		'PASSWORD' : 'Payroll123db',
		'HOST' : 'payroll-db.cb118c6vvezx.us-east-2.rds.amazonaws.com', # localhost en caso de tenerlo en local y la URL de la base de datos en caso de tenerlo en algún servicio en la nube
		'PORT' : '5432' # Si usas el puerto default no pongas esta línea y si lo has cambiado especifícaselo aquí
	}
}
#DATABASES["default"]["ATOMIC_REQUESTS"] = True

# DATABASES = {
#     "default": env.db("DATABASE_URL", default="postgres:///ninerogues"),
# }
CORS_ALLOWED_ORIGINS = [
    'https://main.dyw6xlgeicklk.amplifyapp.com/',
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ORIGIN_WHITELIST = [
    'https://main.dyw6xlgeicklk.amplifyapp.com/',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'https://main.dyw6xlgeicklk.amplifyapp.com/',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if not DEBUG:
        # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    # ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     #'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12
}

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
# )

# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('JWT', ),
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10080),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
#     'ROTATE_REFRESFH_TOKENS':True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_TOKEN_CLASSES': (
#         'rest_framework_simplejwt.tokens.AccessToken',
#     )
# }

# DJOSER = {
#     'LOGIN_FIELD': 'email',
#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
#     'SEND_CONFIRMATION_EMAIL': True,
#     'SET_USERNAME_RETYPE': True,
#     'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
#     'SET_PASSWORD_RETYPE': True,
#     'PASSWORD_RESET_CONFIRM_RETYPE': True,
#     'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
#     'ACTIVATION_URL': 'activate/{uid}/{token}',
#     'SEND_ACTIVATION_EMAIL': True,
#     'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
#     'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['http://localhost:8000/google', 'http://localhost:8000/facebook'],
#     'SERIALIZERS': {
#         'user_create': 'apps.user.serializers.UserCreateSerializer',
#         'user': 'apps.user.serializers.UserCreateSerializer',
#         'current_user': 'apps.user.serializers.UserCreateSerializer',
#         'user_delete': 'djoser.serializers.UserDeleteSerializer',
#     },
# }




MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# STATIC_URL = '/assets/'

#EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

# if not DEBUG:
#     DEFAULT_FROM_EMAIL = 'Vudera - Academia de Software <mail@vudera.com>'
#     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = env('EMAIL_HOST')
#     EMAIL_HOST_USER = env('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
#     EMAIL_PORT = env('EMAIL_PORT')
#     EMAIL_USE_TLS = env('EMAIL_USE_TLS') 