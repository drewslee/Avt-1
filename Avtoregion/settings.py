"""
Django settings for Avtoregion project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import hashlib
import logging
from envconf import Env


env = Env(DEBUG=(bool, False))
env.read_env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename=u'avt.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)    

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
TOKEN = env('TOKEN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list)
INTERNAL_IPS = env('INTERNAL_IPS', cast=list, default=[])
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'DENY'

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Avtoregion',
    'bootstrap3',
    'Avtoregion.templatetags.verbose_names',
    'braces',
    'debug_toolbar',
    'django_telegrambot'
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

ROOT_URLCONF = 'Avtoregion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Avtoregion.template_context_processors.settings_context_processor',

            ],
        },
    },
]


WSGI_APPLICATION = 'Avtoregion.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': env.db(),
    'OPTIONS': {
        'init_command': 'SET sql_mode=STRICT_TRANS_TABLES'
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/Race'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Avtoregion', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
try:
    JS_FILE_MAIN = os.path.join(os.path.join(STATIC_ROOT, 'js'), 'main.js')
    JS_MAIN = md5sum(JS_FILE_MAIN)
    JS_FILE_BOOTSTRAP = os.path.join(os.path.join(STATIC_ROOT, 'js'), 'bootstraptable-config.js')
    JS_BOOTSTRAP = md5sum(JS_FILE_BOOTSTRAP)
    JS_FILE_CHOSEN = os.path.join(os.path.join(STATIC_ROOT, 'js'), 'chosen-config.js')
    JS_CHOSEN = md5sum(JS_FILE_CHOSEN)
    JS_FILE_DATERANGE = os.path.join(os.path.join(STATIC_ROOT, 'js'), 'datarange-config.js')
    JS_DATERANGE = md5sum(JS_FILE_DATERANGE)
    JS_FILE_MODAL = os.path.join(os.path.join(STATIC_ROOT, 'js'), 'modal-config.js')
    JS_MODAL = md5sum(JS_FILE_MODAL)
except:
    JS_MAIN = ""
    JS_BOOTSTRAP = ""
    JS_DATERANGE = ""
    JS_MODAL = ""
    JS_CHOSEN = ""

    
#Django Telegram Bot settings
DJANGO_TELEGRAMBOT = {
    'MODE' : env('MODE'),
    'WEBHOOK_SITE' : env('WEBHOOK_SITE'),
    'WEBHOOK_PREFIX' : '/bot',
    'WEBHOOK_CERTIFICATE' : env('CERTIFICATE'),
    'STRICT_INIT': True,
    'REQUEST_KWARGS': {
        'proxy_url': env('PROXY_URL'), 
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': env('PROXY_USER'),
            'password': env('PROXY_PASS'),
        },
    },
    'BOTS' : [
        {
           'TOKEN': env('TOKEN'),
           #'ALLOWED_UPDATES':(Optional[list[str]]), # List the types of
                                                   #updates you want your bot to receive. For example, specify
                                                   #``["message", "edited_channel_post", "callback_query"]`` to
                                                   #only receive updates of these types. See ``telegram.Update``
                                                   #for a complete list of available update types.
                                                   #Specify an empty list to receive all updates regardless of type
                                                   #(default). If not specified, the previous setting will be used.
                                                   #Please note that this parameter doesn't affect updates created
                                                   #before the call to the setWebhook, so unwanted updates may be
                                                   #received for a short period of time.

           #'TIMEOUT':(Optional[int|float]), # If this value is specified,
                                   #use it as the read timeout from the server

           #'WEBHOOK_MAX_CONNECTIONS':(Optional[int]), # Maximum allowed number of
                                   #simultaneous HTTPS connections to the webhook for update
                                   #delivery, 1-100. Defaults to 40. Use lower values to limit the
                                   #load on your bot's server, and higher values to increase your
                                   #bot's throughput.

           #'POLL_INTERVAL' : (Optional[float]), # Time to wait between polling updates from Telegram in
                           #seconds. Default is 0.0

           #'POLL_CLEAN':(Optional[bool]), # Whether to clean any pending updates on Telegram servers before
                                   #actually starting to poll. Default is False.

           #'POLL_BOOTSTRAP_RETRIES':(Optional[int]), # Whether the bootstrapping phase of the `Updater`
                                   #will retry on failures on the Telegram server.
                                   #|   < 0 - retry indefinitely
                                   #|     0 - no retries (default)
                                   #|   > 0 - retry up to X times

           #'POLL_READ_LATENCY':(Optional[float|int]), # Grace time in seconds for receiving the reply from
                                   #server. Will be added to the `timeout` value and used as the read timeout from
                           #server (Default: 2).
        },        
    ]
}