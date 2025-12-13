# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This defines Lino default settings. You include this (directly or
indirectly) into your local :xfile:`settings.py` using::

  from lino.projects.std.settings import *

"""

from lino.api.ad import Site


def TIM2LINO_LOCAL(alias, obj):
    # Hook for local special treatment on instances that have been
    # imported from TIM. Deprecated. Historic.
    return obj


def TIM2LINO_USERNAME(userid):
    # Deprecated. Historic.
    if userid == "WRITE":
        return None
    return userid.lower()


DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG

ADMINS = [
    # ('Your Name', 'your_email@domain.com'),
]

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = None
TIME_ZONE = "UTC"  # 20190925 avoid "pytz.exceptions.UnknownTimeZoneError: None"
# TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# ~ LANGUAGE_CODE = 'de-BE'
# ~ LANGUAGE_CODE = 'fr-BE'

# ~ SITE_ID = 1 # see also fill.py

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

EMAIL_HOST = "mail.example.com"
# EMAIL_PORT = ""

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# Django wants system admins to define their own `SECRET_KEY
# <https://docs.djangoproject.com/en/5.2/ref/settings/#secret-key>`__
# setting.  Hint: as long as you're on a development server you just
# put some non-empty string and that's okay.

SECRET_KEY = "20227"  # see :djangoticket:`20227`

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# disable migrations:
# MIGRATION_MODULES = dict(contenttypes='lino.fake_migrations', sessions='lino.fake_migrations')

# 20161114
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1", "::1"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# How to set custom options:
# min_len_validator = AUTH_PASSWORD_VALIDATORS[1]
# min_len_validator["OPTIONS"] = {
#     "min_length": 6,
# }
