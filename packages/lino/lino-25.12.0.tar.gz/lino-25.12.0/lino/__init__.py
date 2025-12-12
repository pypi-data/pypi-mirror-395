# -*- coding: UTF-8 -*-
# Copyright 2002-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The :mod:`lino` package is the main plugin used by all Lino applications,
and the root for the subpackages that define core functionalites.

As a plugin it is added automatically to your :setting:`INSTALLED_APPS`. It
defines no models, some template files, a series of :term:`django-admin commands
<django-admin command>`, the core translation messages and the core
:xfile:`help_texts.py` file.

.. autosummary::
   :toctree:

   core
   hello
   api
   utils
   mixins
   projects
   modlib
   sphinxcontrib
   management.commands


"""

from django.utils.translation import gettext_lazy as _
from django import VERSION
from django.apps import AppConfig
from django.conf import settings
import warnings
__version__ = '25.12.0'

# import setuptools  # avoid UserWarning "Distutils was imported before Setuptools"?

import sys
import os
import logging

# intersphinx_urls = dict(docs="http://core.lino-framework.org")
srcref_url = "https://gitlab.com/lino-framework/lino/blob/master/%s"
# srcref_url = 'https://github.com/lino-framework/lino/tree/master/%s'
# doc_trees = ['docs']

# The Lino logger is meant to be used by most Lino code
logger = logging.getLogger("lino")

# import random
# import inspect
# def seed(self, a=None, version=2):
#     stk = "\n".join(["{}:{}".format(s.filename, s.lineno) for s in inspect.stack()[1:3]])
#     logger.info("20240420 random.seed(%s, %s) is called from %s", a, version, stk)
#     self.original_seed(a=a, version=version)
# random.Random.original_seed = random._inst.seed
# random.Random.seed = seed
# random.seed = random._inst.seed
#

if sys.version_info[0] > 2:
    PYAFTER26 = True
elif sys.version_info[0] == 2 and sys.version_info[1] > 6:
    PYAFTER26 = True
else:
    PYAFTER26 = False


warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime (.*) while time zone support is active.",
    RuntimeWarning,
    "django.db.models.fields",
)

# TODO: Is it okay to ignore the followgin warning? It's because e.g.
# lino.modlib.excerpts has a pre_analyze receiver set_excerpts_actions(), which
# accesses the database to set actions before Lino analyzes the models. It
# catches OperationalError & Co because --of course-- it fails e.g. for
# admin-commands like "pm prep".
warnings.filterwarnings(
    "ignore",
    r"Accessing the database during app initialization is discouraged\. To fix this warning, avoid executing queries in AppConfig\.ready\(\) or when your app modules are imported\.",
    RuntimeWarning,
    "django.db.backends.utils",
)

# from django.utils.deprecation import RemovedInDjango50Warning
# warnings.filterwarnings("error", "", RemovedInDjango50Warning)

# doesn't work here because that's too late:
# warnings.filterwarnings(
#     "ignore", "Distutils was imported before Setuptools. This usage is discouraged and may exhibit undesirable behaviors or errors. Please use Setuptools' objects directly or at least import Setuptools first.",
#     UserWarning, "setuptools.distutils_patch")

# TODO: get everything to work even when ResourceWarning gives an error
# warnings.filterwarnings("error", category=ResourceWarning)

warnings.filterwarnings("error", category=SyntaxWarning)

# 20250401 Activating the following line caused `doctest docs/plugins/linod.rst`
# to fail with "Fatal Python error: Segmentation fault":
# warnings.filterwarnings("error", category=DeprecationWarning)


# def setup_project(settings_module):
#     os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
#     from lino.api.shell import settings

DJANGO_DEFAULT_LANGUAGE = "en"


def assert_django_code(django_code):
    if "_" in django_code:
        raise Exception(
            "Invalid language code %r. "
            "Use values like 'en' or 'en-us'." % django_code
        )


AFTER17 = True
AFTER18 = True
DJANGO2 = True
if VERSION[0] == 1:
    DJANGO2 = False
    if VERSION[1] < 10:
        raise Exception("Unsupported Django version {}".format(VERSION))
elif VERSION[0] == 2:
    AFTER17 = True
    AFTER18 = True
else:
    pass  # version 3 or above


def startup(settings_module=None):
    """
    Start up Django and Lino.

    TODO: move this to doctest (and adapt all tested docs).

    Optional `settings_module` is the name of a Django settings
    module.  If this is specified, set the
    :envvar:`DJANGO_SETTINGS_MODULE` environment variable.

    This is called automatically when a process is invoked by a
    :term:`django-admin command`.

    This is usually called in the initialization code snippet of a :doc:`tested
    document </dev/doctests>`.

    If your doctest reports a failure of the following type::

        Failed example:
            startup('lino_amici.projects.amici1.settings')
        Expected nothing
        Got:
            Started /usr/lib/python3.10/doctest.py ... docs/specs/overview.rst (using lino_amici.projects.amici1.settings.demo) --> PID 217238

    then it's because your project directory contains a :xfile:`log` directory.


    """
    if settings_module:
        os.environ["DJANGO_SETTINGS_MODULE"] = settings_module

    # print("20231019 startup() 1")
    import django

    django.setup()
    # print("20231019 startup() 2")


class AppConfig(AppConfig):
    """

    This is the only :class:`django.apps.AppConfig` object used by Lino. Lino
    applications instead use the :class:`lino.core.plugins.Plugin` class to
    define plugins. See :doc:`/dev/plugins`.

    """

    name = "lino"

    def ready(self):
        if False:
            settings.SITE.startup()
        else:
            try:
                settings.SITE.startup()
            except ImportError as e:
                import traceback

                # traceback.print_exc(e)
                # sys.exit(-1)
                raise Exception(
                    "ImportError during startup:\n" + traceback.format_exc(e)
                )
            except Exception as e:
                print(e)
                raise


default_app_config = "lino.AppConfig"

# deprecated use, only for backwards compat:
