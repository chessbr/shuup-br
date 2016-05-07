# -*- coding: utf-8 -*-
import os
import tempfile

SECRET_KEY = "x"


INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    
    'shoop_br',
    
    # shoop themes
    'shoop.themes.classic_gray',
    # shoop
    'shoop.addons',
    'shoop.admin',
    'shoop.core',
    'shoop.default_tax',
    'shoop.front',
    'shoop.front.apps.auth',
    'shoop.front.apps.customer_information',
    'shoop.front.apps.personal_order_history',
    'shoop.front.apps.registration',
    'shoop.front.apps.simple_order_notification',
    'shoop.front.apps.simple_search',
    'shoop.notify',
    'shoop.simple_cms',
    'shoop.customer_group_pricing',
    'shoop.campaigns',
    'shoop.simple_supplier',
    'shoop.order_printouts',
    'shoop.testing',
    'shoop.utils',
    'shoop.xtheme',
    # external apps
    'bootstrap3',
    'django_jinja',
    'easy_thumbnails',
    'filer',
    'registration',
    'rest_framework',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(
            tempfile.gettempdir(),
            'shoop_br_tests.sqlite3'
        ),
    }
}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


STATIC_URL = '/static/'
SOUTH_TESTS_MIGRATE = False
MIGRATION_MODULES = DisableMigrations()
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "var", "media")
ROOT_URLCONF = 'shoop_workbench.urls'

AUTH_USER_MODEL = 'shoop_br.ShoopBRUser'
SHOOP_REGISTRATION_REQUIRES_ACTIVATION = False
SHOOP_CHECKOUT_VIEW_SPEC = "shoop_br.views:ShoopBRCheckoutView"
PARLER_DEFAULT_LANGUAGE_CODE = 'pt-br'
SHOOP_ADDRESS_HOME_COUNTRY = 'BR'
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
]

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
            "newstyle_gettext": True,
            "environment": "shoop.xtheme.engine.XthemeEnvironment",
        },
        "NAME": "jinja2",
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
        }
    },
]


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shoop.front.middleware.ProblemMiddleware',
    'shoop.front.middleware.ShoopFrontMiddleware',
]
