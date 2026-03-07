from pathlib import Path
import dj_database_url 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-event-management-secret-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com', 'http://127.0.0.1:8000']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'event_management.urls'

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

WSGI_APPLICATION = 'event_management.wsgi.application'


# Database
# For SQLite (uncomment to use)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://event_manager_db_c8mi_user:zRRLlBiaqk0hmJfbC52ospDAstHSUJFU@dpg-d6kr53ili9vc73ferq2g-a.oregon-postgres.render.com/event_manager_db_c8mi',
        conn_max_age=600
    )
}

# For PostgreSQL (default)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'event_management',
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
