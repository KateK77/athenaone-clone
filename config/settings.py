import os
import secrets
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
DEMO_MODE = os.getenv('DEMO_MODE', 'true' if DEBUG else 'false').lower() == 'true'
ALLOW_DEMO_RESET = DEBUG and os.getenv('ALLOW_DEMO_RESET', 'false').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError('SECRET_KEY must be configured when DEBUG=false')
    key_file = BASE_DIR / '.local-secret'
    if not key_file.exists():
        key_file.write_text(secrets.token_urlsafe(64))
    SECRET_KEY = key_file.read_text()
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')
CSRF_TRUSTED_ORIGINS = [x for x in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if x]
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'core', 'clinical', 'revenue', 'engagement']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages', 'core.context.navigation']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': dj_database_url.parse(os.getenv('DATABASE_URL', '').strip() or 'sqlite:///' + str(BASE_DIR / 'demo.sqlite3'), conn_max_age=60)}
if not DEBUG and DATABASES['default']['ENGINE']!='django.db.backends.postgresql':
    raise RuntimeError('Production requires an explicit PostgreSQL DATABASE_URL; ephemeral SQLite is not supported.')
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'}, 'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
LOGIN_URL = '/login/'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REDIRECT_EXEMPT = [r'^health/$']
X_FRAME_OPTIONS = 'DENY'
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
