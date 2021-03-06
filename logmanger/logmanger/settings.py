"""
Django settings for logmanger project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_%7b!%1^i)5$oc)70h9+)8*vh33q)yny^=1@cbj(51x1jy&w(k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'logmangerapp',
    'updateapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'logmanger.urls'

WSGI_APPLICATION = 'logmanger.wsgi.application'

APP_PATH=os.path.dirname(os.path.dirname(__file__))
# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
 #       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  #  }
'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'logmanger',
        'USER':'root',
        'PASSWORD':'abc123?',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),
    os.path.join('templates'),
)



# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
  os.path.join(BASE_DIR + '/static/'),
)
LOGGING = {
        'version':1,
        'disable_existing_loggers':True,
        'formatters':{
            'standard':{
                'format':'%(levelname)s %(asctime)s %(message)s',
                },
            
        },
        'filters':{
            
            },
        'handlers':{
            'mail_admins':{
                'level':'ERROR',
                'class':'django.utils.log.AdminEmailHandler',
                'formatter':'standard',
                },
            'test1_handler':{
                'level':'ERROR',
                'class':'django.utils.log.AdminEmailHandler',
                'formatter':'standard',
                },
            
            },
        'loggers':{
            'django.request':{
                'handlers':['mail_admins'],
                'level':'ERROR',
                'propagate':True,
                },
            'test1':{
                'handlers':['test1_handler'],
                'level':'ERROR',
                'propagate':False,
                },
            
            }
        
        
        }
try:
    from settings_local import *
except ImportError:
    pass
