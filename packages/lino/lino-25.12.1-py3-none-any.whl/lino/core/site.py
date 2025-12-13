# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# doctest lino/core/site.py

import os
import re
import sys
from os.path import dirname, join, isdir, relpath, exists
import inspect
import datetime
import warnings
import collections
import locale
import logging
# from pprint import pprint
from logging.handlers import SocketHandler
import time
import rstgen
from importlib.util import find_spec
from importlib import import_module
from pathlib import Path
from asgiref.sync import sync_to_async
from rstgen.confparser import ConfigParser
from django.apps import apps
from django.utils import timezone
from django.utils import translation
from django.utils.html import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from lino import assert_django_code, DJANGO_DEFAULT_LANGUAGE
from lino import logger, __version__
from lino.core.exceptions import ChangedAPI
from lino.utils.html import E, tostring
# from lino.core import constants
from lino.core.plugin import Plugin
from lino.utils import AttrDict, date_offset, i2d, buildurl


NO_REMOTE_AUTH = True
# 20240518 We have only one production site still using remote http
# authentication, and they will migrate to sessions-based auth with their next
# upgrade.

# ASYNC_LOGGING = False
# This is to fix the issue that the "started" and "ended" messages are not logged.
# But setting this to True causes #4986 (Unable to configure handler 'mail_admins')
# because since 20230529 we called logging..config.dictConfig() during
# lino.core.site.Site.setup_logging(). The Django default logger config, when
# activated, accesses settings.DEFAULT_EXCEPTION_REPORTER, which fails at this
# moment because the settings aren't yet loaded.


has_socialauth = find_spec("social_django") is not None
has_elasticsearch = find_spec("elasticsearch_django") is not None
has_haystack = find_spec("haystack") is not None


# from .roles import SiteUser


class LinoSocketHandler(SocketHandler):
    # see: https://code.djangoproject.com/ticket/29186
    def emit(self, record):
        # print("20231019 LinoSocketHandler.emit()", record)
        if hasattr(record, "request"):
            record.request = "Removed by LinoSocketHandler"
        return super().emit(record)
        # try:
        #     return super().emit(record)
        # except Exception as e:
        #     logging.warning(f"Non-picklable LogRecord: {record}\n" + dd.read_exception(sys.exc_info()))


def classdir(cl):
    # return the full absolute resolved path name of the directory containing
    # the file that defines class cl.
    return os.path.realpath(dirname(inspect.getfile(cl)))


LanguageInfo = collections.namedtuple(
    "LanguageInfo", ("django_code", "name", "index", "suffix"))


def to_locale(language):
    p = language.find("-")
    if p >= 0:
        # Get correct locale for sr-latn
        if len(language[p + 1:]) > 2:
            return (
                language[:p].lower()
                + "_"
                + language[p + 1].upper()
                + language[p + 2:].lower()
            )
        return language[:p].lower() + "_" + language[p + 1:].upper()
    return language.lower()


def class2str(cl):
    return cl.__module__ + "." + cl.__name__


def gettext_noop(s): return s


PLUGIN_CONFIGS = {}


# from django.db.models.fields import NOT_PROVIDED
class NOT_PROVIDED(object):
    pass


# def is_socket_alive(sock_file: Path) -> bool:
#     if not sock_file.exists():
#         return False
#     return True
#     # # Inspired by https://stackoverflow.com/questions/48024720/python-how-to-check-if-socket-is-still-connected
#     # try:
#     #     # this will try to read bytes without blocking and also without removing them from buffer (peek only)
#     #     data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
#     #     if len(data) == 0:
#     #         return True
#     # except BlockingIOError:
#     #     return False  # socket is open and reading from it would block
#     # except ConnectionResetError:
#     #     return True  # socket was closed for some other reason
#     # except Exception as e:
#     #     logger.exception("unexpected exception when checking if a socket is closed")
#     #     return False
#     # return False


class Site(object):
    KB = 2**10
    MB = 2**20

    quantity_max_length = 6
    # upload_to_tpl = "uploads/%Y/%m"
    auto_fit_column_widths = True
    site_locale = None
    confdirs = None
    kernel = None
    readonly = False
    the_demo_date = None
    hoster_status_url = "http://bugs.saffre-rumma.net/"
    title = None
    verbose_name = "yet another Lino application"
    description = None
    version = None
    url = None
    # 23CF eject symbol. Looks strange on bootstrap's default font:
    expand_panel_symbol = "⏏"

    migratable_plugin_prefixes = []
    """
    List of prefixes used in :manage:`initdb` and :cmd:`pm prep` command
    for plugins other then the plugins whose name startswith `lino`.
    For example: for plugins in welfare app, put 'welfare' in the list,
    so it the commands will prepare the postgres database properly.
    """

    make_missing_dirs = True
    userdocs_prefix = ""
    site_dir = None
    project_dir = None
    media_root = None
    project_name = None
    languages = None
    hidden_languages = None
    BABEL_LANGS = tuple()
    not_found_msg = "(not installed)"
    django_settings = None
    startup_time = None
    plugins = None
    models = None

    top_level_menus = [
        ("master", _("Master")),
        ("main", None),
        ("reports", _("Reports")),
        ("config", _("Configure")),
        ("explorer", _("Explorer")),
        ("site", _("Site")),
    ]

    ignore_model_errors = False
    """Not yet sure whether this is needed. Maybe when generating
    documentation.

    """

    loading_from_dump = False

    # see docs/settings.rst
    migration_class = None
    """
    If you maintain a data migrator module for your application,
    specify its name here.

    See :ref:`datamig` and/or :func:`lino.utils.dpy.install_migrations`.

    TODO: rename this to `migrator_class`

    """

    migrations_package = None
    """The full Python name of
    the local package that holds Django migrations for all plugins
    of this site.

    You might manually specify a name, but the recommended way is to create a
    :xfile:`migrations` directory.  See :doc:`/specs/migrate`.

    """

    partners_app_label = "contacts"
    """
    Temporary setting, see :ref:`polymorphism`.
    """

    # three constants used by lino_xl.lib.workflows:
    max_state_value_length = 20
    max_action_name_length = 50
    max_actor_name_length = 100

    trusted_templates = False
    """
    Set this to True if you are sure that the users of your site won't try to
    misuse Jinja's capabilities.

    """

    uid = "myuid"
    """A universal identifier for this Site.  This is needed when
    synchronizing with CalDAV server.  Locally created calendar
    components in remote calendars will get a UID based on this
    parameter, using ``"%s@%s" % (self.pk, settings.SITE.kernel)``.

    The default value is ``'myuid'``, and you should certainly
    override this on a production server that uses remote calendars.

    """

    project_model = None
    user_model = None
    auth_middleware = None

    legacy_data_path = None
    """
    Deprecated. Was used by tim2lino and pp2lino to import data from some legacy
    database.

    """

    propvalue_max_length = 200
    """
    Used by :mod:`lino_xl.lib.properties`.
    """

    show_internal_field_names = True
    use_elasticsearch = False
    use_solr = False
    developer_site_cache = None
    keep_erroneous_cache_files = False
    use_java = True
    use_systemd = False
    use_silk_icons = False
    use_new_unicode_symbols = False
    use_experimental_features = False
    site_config_defaults = {}

    # default_build_method = "appypdf"
    # default_build_method = "appyodt"
    # default_build_method = "wkhtmltopdf"
    default_build_method = None

    is_demo_site = False

    demo_email = "demo@example.com"

    # demo_fixtures = ['std', 'demo', 'demo2']
    demo_fixtures = []

    use_spinner = False  # doesn't work. leave this to False

    # ~ django_admin_prefix = '/django'
    django_admin_prefix = None

    calendar_start_hour = 7
    calendar_end_hour = 21

    time_format_extjs = "H:i"
    alt_time_formats_extjs = (
        "g:ia|g:iA|g:i a|g:i A|h:i|g:i|H:i|ga|ha|gA|h a|g a|g A|gi|hi"
        "|gia|hia|g|H|gi a|hi a|giA|hiA|gi A|hi A"
        "|Hi|g.ia|g.iA|g.i a|g.i A|h.i|g.i|H.i"
    )

    date_format_extjs = "d.m.Y"
    alt_date_formats_extjs = "d/m/Y|Y-m-d"
    default_number_format_extjs = "0,000.00/i"
    # default_number_format_extjs = '0,00/i'
    uppercase_last_name = False
    last_name_first = False
    jasmine_root = None
    default_user = None
    remote_user_header = None
    use_gridfilters = True
    use_eid_applet = False
    use_esteid = False
    use_awesome_uploader = False

    use_tinymce = True
    """Replaced by :mod:`lino.modlib.tinymce`.
    """

    use_jasmine = False
    use_quicktips = True
    use_css_tooltips = False
    use_vinylfox = False

    # the following attributes are documented in hg/docs/admin/settings.py
    # default_ui = 'lino_extjs6.extjs6'
    default_ui = "lino.modlib.extjs"
    # default_ui = 'lino.modlib.extjs'
    web_front_ends = None

    webdav_root = None
    webdav_url = None
    webdav_protocol = None
    use_security_features = False
    use_ipdict = False
    user_types_module = None
    workflows_module = None
    custom_layouts_module = None
    root_urlconf = "lino.core.urls"
    social_auth_backends = None

    sidebar_width = 0
    """
    Used by :mod:`lino.modlib.plain`.
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.

    """

    preview_limit = 15

    # admin_ui = None

    detail_main_name = "main"

    textfield_bleached = True
    textfield_format = "plain"
    verbose_client_info_message = False

    stopsignal = "SIGTERM"
    help_url = "https://www.lino-framework.org"

    help_email = "users@lino-framework.org"

    catch_layout_exceptions = True

    strict_master_check = False
    strict_dependencies = True

    strict_choicelist_values = True

    csv_params = dict()

    # attributes documented in book/docs/topics/logging.rst:
    _history_aware_logging = False
    log_each_action_request = False
    default_loglevel = "INFO"
    logger_filename = "lino.log"
    logger_format = (
        "%(asctime)s %(levelname)s [%(name)s %(process)d %(thread)d] : %(message)s"
    )
    auto_configure_logger_names = "atelier lino"

    # appy_params = dict(ooPort=8100)
    appy_params = dict(
        ooPort=8100, pythonWithUnoPath="/usr/bin/python3", raiseOnError=True
    )
    # ~ decimal_separator = '.'
    decimal_separator = ","

    # decimal_group_separator = ','
    # decimal_group_separator = ' '
    # decimal_group_separator = '.'
    decimal_group_separator = "\u00A0"

    time_format_strftime = "%H:%M"

    date_format_strftime = "%d.%m.%Y"

    date_format_regex = r"/^[0123]?\d\.[01]?\d\.-?\d+$/"

    datetime_format_strftime = "%Y-%m-%dT%H:%M:%S"

    datetime_format_extjs = r"Y-m-d\TH:i:s"

    quick_startup = False

    master_site = None

    # for internal use:
    _logger = None
    _starting_up = False
    _shutdown_tasks = []

    _hidden_plugins = None
    # A set containing the names of plugins that are installed but inactive.

    override_modlib_models = None

    installed_plugin_modules = None

    def __init__(self, settings_globals=None, local_apps=[], **kwargs):
        # print(f"20251125 Site.__init__() {self}")
        # if hasattr(self, 'default_ui'):
        #     raise ChangedAPI("`default_ui` is replaced by `web_front_ends`")
        if hasattr(self, "allow_duplicate_cities"):
            raise ChangedAPI(
                "allow_duplicate_cities is now a setting of the countries plugin"
            )
        if hasattr(self, "get_installed_apps"):
            raise ChangedAPI(
                "Please rename get_installed_apps() to get_installed_plugins()"
            )
        if hasattr(self, "get_apps_modifiers"):
            raise ChangedAPI(
                "Please rename get_apps_modifiers() to get_plugin_modifiers()"
            )
        if hasattr(self, "setup_choicelists"):
            raise ChangedAPI("setup_choicelists is no longer supported")
        if hasattr(self, "setup_workflows"):
            raise ChangedAPI("setup_workflows is no longer supported")
        if hasattr(self, "beid_protocol"):
            raise ChangedAPI(
                "Replace Site.beid_protocol by plugins.beid.urlhandler_prefix"
            )
        if hasattr(self, "use_linod"):
            raise ChangedAPI("Replace Site.use_linod by plugins.linod.use_channels")

        if "no_local" in kwargs:
            kwargs.pop("no_local")
            raise ChangedAPI("The no_local argument is no longer needed.")

        self._hidden_plugins = set()
        self._welcome_handlers = []
        self._quicklinks = None
        self.plugins = AttrDict()
        self.models = AttrDict()
        self.modules = self.models  # backwards compat
        # self.actors = self.models  # backwards compat
        # self.actors = AttrDict()

        if isinstance(self.the_demo_date, (str, int)):
            self.the_demo_date = i2d(self.the_demo_date)

        if settings_globals is None:
            settings_globals = {}
        self.init_before_local(settings_globals, local_apps)
        self.setup_logging()
        # self.run_lino_site_module()

        self.override_settings(**kwargs)
        self.load_plugins()

        for p in self.installed_plugins:
            p.on_plugins_loaded(self)

        if self.migrations_package is None:
            MPNAME = "migrations"
            mpp = self.project_dir / MPNAME
            if mpp.exists():
                # parts = self.__module__.split('.')
                parts = os.getenv("DJANGO_SETTINGS_MODULE").split(".")
                # i = parts.index('settings')
                # mpn = '.'.join(parts[i]) + '.' + MPNAME
                mpn = ".".join(parts[:-1]) + "." + MPNAME
                # print("Local migrations package {} ({}).".format(mpn, mpp))
                self.migrations_package = mpn
                # self.migrations_package = self.__module__ + '.' + MPNAME
                # sm = import_module()
                # self.migrations_package = sm.__name__ + '.' + MPNAME
                fn = mpp / "__init__.py"
                if not fn.exists():
                    fn.write_text("")  # touch __init__ file.
            else:
                # print("No Django migrations because {} does not exist.".format(mpp))
                pass

        if self.migrations_package is not None:
            migrations_module = import_module(self.migrations_package)
            MIGRATION_MODULES = {}
            for p in self.installed_plugins:
                if p.app_label in ("contenttypes", "sessions", "staticfiles"):
                    # pure django plugins handle their own migrations
                    continue
                dir = join(
                    migrations_module.__file__.rstrip("__init__.py"), p.app_label
                )
                self.makedirs_if_missing(dir)
                open(join(dir, "__init__.py"), "a").close()  # touch __init__ file.
                MIGRATION_MODULES[p.app_label] = (
                    self.migrations_package + "." + p.app_label
                )
            self.django_settings.update(MIGRATION_MODULES=MIGRATION_MODULES)

        self.setup_plugins()
        self.install_settings()

        for p in self.installed_plugins:
            if p.is_hidden():
                self._hidden_plugins.add(p.app_label)

        from lino.utils.config import ConfigDirCache

        self.confdirs = ConfigDirCache(self)

        for k in ("ignore_dates_before", "ignore_dates_after"):
            if hasattr(self, k):
                msg = "{0} is no longer a site attribute"
                msg += " but a plugin attribute on lino_xl.lib.cal."
                msg = msg.format(k)
                raise ChangedAPI(msg)

        if self.title is None:
            self.title = self.project_name

    def init_before_local(self, settings_globals, local_apps):
        if not isinstance(settings_globals, dict):
            raise Exception(
                """
            The first argument when instantiating a %s
            must be your settings.py file's `globals()`
            and not %r
            """
                % (self.__class__.__name__, settings_globals)
            )

        if isinstance(local_apps, str):
            local_apps = [local_apps]
        self.local_apps = local_apps

        self.django_settings = settings_globals
        project_file = settings_globals.get("__file__", ".")

        self.project_dir = Path(dirname(project_file)).absolute().resolve()

        # inherit `project_name` from parent?
        # if self.__dict__.get('project_name') is None:
        if self.project_name is None:
            parts = reversed(str(self.project_dir).split(os.sep))
            # print(20150129, list(parts))
            for part in parts:
                if part != "settings":
                    self.project_name = part
                    break

        if self.master_site is None:
            self.site_dir = self.project_dir
            self.django_settings.update(DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": str(self.site_dir / "default.db")
                }
            })
        else:
            self.site_dir = self.master_site.site_dir
            self._history_aware_logging = self.master_site._history_aware_logging
            for k in ("DATABASES", "SECRET_KEY"):
                self.django_settings[k] = self.master_site.django_settings[k]

        self.update_settings(
            EMAIL_SUBJECT_PREFIX=f'[{self.project_name}] ')
        self.update_settings(
            SERIALIZATION_MODULES={
                "py": "lino.utils.dpy",
            }
        )

        # before Django 3.2 an automatic id was always django.db.models.AutoField
        # self.update_settings(DEFAULT_AUTO_FIELD='django.db.models.AutoField')
        self.update_settings(DEFAULT_AUTO_FIELD="django.db.models.BigAutoField")

        if self.site_prefix != "/":
            if not self.site_prefix.endswith("/"):
                raise Exception("`site_prefix` must end with a '/'!")
            if not self.site_prefix.startswith("/"):
                raise Exception("`site_prefix` must start with a '/'!")
            self.update_settings(SESSION_COOKIE_PATH=self.site_prefix[:-1])
            # self.update_settings(SESSION_COOKIE_NAME='ssid')

        self.VIRTUAL_FIELDS = set()
        self._startup_done = False
        self.startup_time = datetime.datetime.now()

    def setup_logging(self):
        # documented in book/docs/topics/logging.rst

        if self.auto_configure_logger_names is None:
            return

        # if len(logging.root.handlers) > 0:
        #
        #     # Logging has been configured by something else. This can happen
        #     # when Site is instantiated a second time. Or accidentaly (e.g. when
        #     # you call logging.basicConfig() in the settings.py), Or when some
        #     # testing environment runs multiple doctests in a same process.  We
        #     # don't care, we restart configuration from scratch.
        #
        #     for handler in logging.root.handlers[:]:
        #         logging.root.removeHandler(handler)

        from django.utils.log import DEFAULT_LOGGING

        d = DEFAULT_LOGGING

        # if d.get("logger_ok", False):
        #     # raise Exception("20231017")
        #     return

        level = os.environ.get("LINO_LOGLEVEL", self.default_loglevel).upper()
        file_level = os.environ.get("LINO_FILE_LOGLEVEL", level).upper()
        sql_level = os.environ.get("LINO_SQL_LOGLEVEL", level).upper()

        min_level = min(*[getattr(logging, k) for k in (
            level, file_level, sql_level)])

        # print("20231017 level is", level)

        loggercfg = {
            "handlers": ["console", "mail_admins"],
            "level": logging.getLevelName(min_level),
        }

        handlers = d.setdefault("handlers", {})
        if True:
            # We override Django's default config: write to stdout (not
            # stderr) and remove the 'require_debug_true' filter.
            console = handlers.setdefault("console", {})
            console["stream"] = sys.stdout
            if "filters" in console:
                del console["filters"]
            console["level"] = level

        # when Site is instantiated several times, we keep the existing file handler
        # print("20231016", self.logger_filename, handlers.keys())
        if "file" not in handlers:
            logdir = self.site_dir / "log"
            if logdir.is_dir():
                self._history_aware_logging = True
                log_file_path = logdir / self.logger_filename
                # print("20231019 logging", file_level, "to", log_file_path)
                if True:
                    # print("20231019 log directly to file")
                    formatters = d.setdefault("formatters", {})
                    formatters.setdefault(
                        "verbose",
                        dict(format=self.logger_format, datefmt="%Y%m-%d %H:%M:%S"),
                    )
                    handlers["file"] = {
                        "level": file_level,
                        "class": "logging.handlers.WatchedFileHandler",
                        "filename": str(log_file_path),
                        "encoding": "UTF-8",
                        "formatter": "verbose",
                    }
            elif self.use_systemd:
                try:
                    from systemd.journal import JournalHandler
                    handlers["file"] = {
                        "class": "systemd.journal.JournalHandler",
                        "SYSLOG_IDENTIFIER": str(self.project_name),
                    }
                except ImportError:
                    # Silenly ignore. Can happen when use_systemd is True but
                    # `pm install` hasn't yet been run.
                    pass

        # when a file handler exists, we have the loggers use it even if this
        # instance didn't create it:
        if "file" in handlers:
            loggercfg["handlers"].append("file")

        for name in self.auto_configure_logger_names.split():
            # if name not in d['loggers']:
            d["loggers"][name] = loggercfg

        if sql_level != level:
            dblogger = d["loggers"].setdefault("django.db.backends", {})
            dblogger["level"] = sql_level
            dblogger["handlers"] = loggercfg["handlers"]

        # # https://code.djangoproject.com/ticket/30554
        # logger = d['loggers'].setdefault('django.utils.autoreload', {})
        # logger['level'] = 'INFO'

        # if 'linod' in d['loggers']:
        #     for item in d['loggers'].keys():
        #         if item not in ['linod', 'root']:
        #             d['loggers'][item]['propagate'] = True

        # if ASYNC_LOGGING:
        #     config = d.copy()
        #
        #     try:
        #         logging.config.dictConfig(config)
        #         # logging.config.dictConfig(d)
        #     finally:
        #         d.clear()
        #         # d["logger_ok"] = True
        #         d["version"] = 1
        #         d["disable_existing_loggers"] = False
        # else:
        #     d["logger_ok"] = True
        # self.update_settings(LOGGING=d)
        # pprint(d)
        # print("20161126 Site %s " % d['loggers'].keys())
        # import yaml
        # print("20231019", yaml.dump(d))

    def get_anonymous_user(self):
        # The code below works even when users is not installed
        from lino.modlib.users.choicelists import UserTypes

        return UserTypes.get_anonymous_user()

    # def run_lino_site_module(self):
    #     """Deprecated. Probably no longer used. See :ref:`lino.site_module`.
    #
    #     """
    #     site_module = os.environ.get('LINO_SITE_MODULE', None)
    #     if site_module:
    #         mod = import_module(site_module)
    #         func = getattr(mod, 'setup_site', None)
    #         if func:
    #             func(self)
    #     # try:
    #     #     from djangosite_local import setup_site
    #     # except ImportError:
    #     #     pass
    #     # else:
    #     #     setup_site(self)

    def override_settings(self, **kwargs):
        # Called internally during `__init__` method.
        # Also called from :mod:`lino.utils.djangotest`

        # ~ logger.info("20130404 lino.site.Site.override_defaults")

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

        self.apply_languages()

    def get_plugin_configs(self):
        return []

    def load_plugins(self):
        # Called internally during `__init__` method.

        if hasattr(self, "hidden_apps"):
            raise ChangedAPI("Replace hidden_apps by get_plugin_modifiers()")

        def setpc(pc):
            if isinstance(pc, tuple):
                if len(pc) != 3:
                    raise Exception("20190318")
                app_label, k, value = pc
                d = PLUGIN_CONFIGS.setdefault(app_label, {})
                d[k] = value
            else:  # expect an iterable returned by super()
                for x in pc:
                    setpc(x)

        for pc in self.get_plugin_configs():
            setpc(pc)

        cfgp = ConfigParser()
        cfgp.read(self.project_dir / "lino.ini")
        for section in cfgp.sections():
            if section.startswith("getlino") or section == "DEFAULT":
                continue
            if section not in PLUGIN_CONFIGS:
                PLUGIN_CONFIGS[section] = dict()
            for option in cfgp.options(section):
                PLUGIN_CONFIGS[section][option] = cfgp.parsed_get(section, option)

        requested_apps = []
        apps_modifiers = self.get_plugin_modifiers()

        def add(x):
            if isinstance(x, str):
                app_label = x.split(".")[-1]
                x = apps_modifiers.pop(app_label, x)
                if x is not None:
                    requested_apps.append(x)
            else:
                # if it's not a string, then it's an iterable of strings
                for xi in x:
                    add(xi)

        for x in self.get_installed_plugins():
            add(x)
        add("django.contrib.staticfiles")

        for x in self.local_apps:
            add(x)

        plugins = []

        def install_plugin(app_name, needed_by=None):
            # print("20210305 install_plugin({})".format(app_name))
            # Django does not accept newstr, and we don't want to see
            # ``u'applabel'`` in doctests.
            # app_name = str(app_name)
            # print("20160524 install_plugin(%r)" % app_name)
            app_mod = import_module(app_name)

            # print "Loading plugin", app_name
            k = app_name.rsplit(".")[-1]
            x = apps_modifiers.pop(k, 42)
            if x is None:
                return
            elif x == 42:
                pass
            else:
                raise Exception("20160712")
            if k in self.plugins:
                other = self.plugins[k]
                if other.app_name == app_name:
                    # If a plugin is installed more than once, only
                    # the first one counts and all others are ignored
                    # silently. Happens e.g. in Lino Noi where
                    # lino_noi.lib.noi is both a required plugin and
                    # the default_ui.
                    return
                raise Exception(
                    "Tried to install {}, but {} is already installed.".format(
                        app_name, other
                    )
                )

            # Can an `__init__.py` file explicitly set ``Plugin =
            # None``? Is that feature being used?
            app_class = getattr(app_mod, "Plugin", Plugin)
            # if app_class is None:
            #     app_class = Plugin
            cfg = PLUGIN_CONFIGS.pop(k, None)
            ip = app_class(self, k, app_name, app_mod, needed_by, cfg or dict())

            self.plugins.define(k, ip)

            needed_by = ip
            # while needed_by.needed_by is not None:
            #     needed_by = needed_by.needed_by
            for dep in ip.get_needed_plugins():
                k2 = dep.rsplit(".")[-1]
                if k2 not in self.plugins:
                    install_plugin(dep, needed_by=needed_by)
                    # plugins.append(dep)

            plugins.append(ip)

        # lino is always the first plugin:
        install_plugin("lino")

        for app_name in requested_apps:
            install_plugin(app_name)

        # raise Exception("20190318 {} {}".format([p.app_label for p in plugins], ''))

        if apps_modifiers:
            raise Exception(
                "Invalid app_label '{0}' in your get_plugin_modifiers!".format(
                    list(apps_modifiers.keys())[0]
                )
            )

        # The return value of get_auth_method() may depend on a
        # plugin, so if needed we must add the django.contrib.sessions
        # afterwards.
        # if self.get_auth_method() == 'session':
        if self.user_model:
            k = "django.contrib.sessions"
            if k not in self.plugins:
                install_plugin(k)

        self.update_settings(INSTALLED_APPS=tuple([p.app_name for p in plugins]))
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is not None:
            raise ChangedAPI("override_modlib_models no longer allowed")

        self.override_modlib_models = dict()

        # def reg(p, pp, m):
        #     name = pp.__module__ + '.' + m
        #     self.override_modlib_models[name] = p

        def plugin_parents(pc):
            for pp in pc.__mro__:
                if issubclass(pp, Plugin):
                    # if pp not in (Plugin, p.__class__):
                    if pp is not Plugin:
                        yield pp

        def reg(pc):
            # If plugin p extends some models, then tell all parent
            # plugins to make their definition of each model abstract.
            extends_models = pc.__dict__.get("extends_models")
            if extends_models is not None:
                for m in extends_models:
                    for pp in plugin_parents(pc):
                        if pp is pc:
                            continue
                        name = pp.__module__ + "." + m
                        self.override_modlib_models[name] = pc
                        # if m == "Company":
                        #     print("20160524 tell %s that %s extends %s" % (
                        #         pp, p.app_name, m))

            for pp in plugin_parents(pc):
                if pp is pc:
                    continue
                reg(pp)

            # msg = "{0} declares to extend_models {1}, but " \
            #       "cannot find parent plugin".format(p, m)
            # raise Exception(msg)

        for p in self.installed_plugins:
            reg(p.__class__)

        self.installed_plugin_modules = set()
        for p in self.installed_plugins:
            self.installed_plugin_modules.add(p.app_module.__name__)
            for pp in plugin_parents(p.__class__):
                self.installed_plugin_modules.add(pp.__module__)

        # print("20160524 %s", self.installed_plugin_modules)
        # raise Exception("20140825 %s", self.override_modlib_models)

    def get_requirements(self):
        reqs = set()
        for p in self.installed_plugins:
            for r in p.get_requirements(self):
                reqs.add(r)
        if self.textfield_bleached:
            reqs.add("beautifulsoup4")
        if self.use_systemd:
            reqs.add("systemd-python")
        return sorted(reqs)

    def setup_plugins(self):
        pass

    def install_settings(self):
        assert not self.help_url.endswith("/")
        assert not self.server_url.endswith("/")

        for p in self.installed_plugins:
            p.install_django_settings(self)

        # import django
        # django.setup()
        if self.site_dir is not None:
            self.media_root = self.site_dir / "media"
            if self.webdav_url is None:
                self.webdav_url = self.site_prefix + "media/webdav/"
            if self.webdav_root is None:
                self.webdav_root = self.media_root / "webdav"
            self.update_settings(MEDIA_ROOT=str(self.media_root))

        self.update_settings(ROOT_URLCONF=self.root_urlconf)
        self.update_settings(MEDIA_URL="/media/")

        if "STATIC_ROOT" not in self.django_settings:
            # cache_root = os.environ.get("LINO_CACHE_ROOT", None)
            # if cache_root:
            #     p = Path(cache_root)
            # else:
            #     p = self.site_dir
            p = self.site_dir
            self.update_settings(STATIC_ROOT=str(p / "static_root"))
        if "STATIC_URL" not in self.django_settings:
            self.update_settings(STATIC_URL="/static/")

        if "USE_TZ" not in self.django_settings:
            # django.utils.deprecation.RemovedInDjango50Warning: The default
            # value of USE_TZ will change from False to True in Django 5.0. Set
            # USE_TZ to False in your project settings if you want to keep the
            # current default behavior.
            self.update_settings(USE_TZ=False)

        # loaders = [
        #     'lino.modlib.jinja.loader.Loader',
        #     'django.template.loaders.filesystem.Loader',
        #     'django.template.loaders.app_directories.Loader',
        #     #~ 'django.template.loaders.eggs.Loader',
        # ]

        tcp = []

        tcp += [
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.contrib.messages.context_processors.messages",
        ]
        # self.update_settings(TEMPLATE_LOADERS=tuple(loaders))
        # self.update_settings(TEMPLATE_CONTEXT_PROCESSORS=tuple(tcp))

        TEMPLATES = [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": tcp,
                    # 'loaders': loaders
                },
            },
        ]
        TEMPLATES.append(
            {
                "BACKEND": "django.template.backends.jinja2.Jinja2",
                "DIRS": [],
                "OPTIONS": {"environment": "lino.modlib.jinja.get_environment"},
            }
        )

        self.update_settings(TEMPLATES=TEMPLATES)

        if self.user_model:
            self.update_settings(AUTH_USER_MODEL="users.User")
            if self.use_security_features:
                self.update_settings(
                    CSRF_USE_SESSIONS=True,
                    SESSION_COOKIE_SECURE=True,
                    CSRF_COOKIE_SECURE=True,
                )

        # self.define_settings(AUTH_USER_MODEL=self.user_model)

        self.define_settings(MIDDLEWARE=tuple(self.get_middleware_classes()))

        # if self.get_auth_method() == 'session':
        #     self.define_settings(AUTHENTICATION_BACKENDS=[
        #         'django.contrib.auth.backends.RemoteUserBackend'
        #     ])

        backends = []
        # if self.use_ipdict:
        #     backends.append('lino.modlib.ipdict.backends.Backend')
        if self.get_auth_method() == "remote":
            backends.append("lino.core.auth.backends.RemoteUserBackend")
        else:
            backends.append("lino.core.auth.backends.ModelBackend")

        if self.social_auth_backends is not None:
            backends += self.social_auth_backends

        self.define_settings(AUTHENTICATION_BACKENDS=backends)

        self.update_settings(
            LOGIN_URL="/accounts/login/",
            LOGIN_REDIRECT_URL=self.site_prefix,
            # LOGIN_REDIRECT_URL = '/accounts/profile/',
            LOGOUT_REDIRECT_URL=None,
        )

        def collect_settings_subdirs(lst, name, max_count=None):
            def add(p):
                p = p.replace(os.sep, "/")
                if p not in lst:
                    lst.append(p)

            for p in self.get_settings_subdirs(name):
                # if the parent of a settings subdir has a
                # `models.py`, then it is a plugin and we must not add
                # the subdir because Django does that.
                if exists(join(p, "..", "models.py")):
                    self.logger.debug(
                        "Not loading %s %s because Django does that", p, name
                    )
                else:
                    add(str(p))
                    if (max_count is not None) and len(lst) >= max_count:
                        break

            # local_dir = self.site_dir.child(name)
            # if local_dir.exists():
            #     print "20150427 adding local directory %s" % local_dir
            #     add(local_dir)
            # The STATICFILES_DIRS setting should not contain the
            # STATIC_ROOT setting

            if False:
                # If a plugin has no "fixtures" ("config") directory
                # of its own, inherit it from parents.  That would be
                # nice and it even works, but with a stud: these
                # fixtures will be loaded at the end.
                for ip in self.installed_plugins:
                    if not ip.get_subdir(name):
                        pc = ip.extends_from()
                        while pc and issubclass(pc, Plugin):
                            p = pc.get_subdir(name)
                            if p:
                                add(p)
                            pc = pc.extends_from()

        fixture_dirs = list(self.django_settings.get("FIXTURE_DIRS", []))
        locale_paths = list(self.django_settings.get("LOCALE_PATHS", []))
        # sfd = list(self.django_settings.get('STATICFILES_DIRS', []))
        # sfd.append(self.site_dir.child('genjs'))
        collect_settings_subdirs(fixture_dirs, "fixtures", 1)
        collect_settings_subdirs(locale_paths, "locale")
        # collect_settings_subdirs(sfd, 'static')
        self.update_settings(FIXTURE_DIRS=tuple(fixture_dirs))
        self.update_settings(LOCALE_PATHS=tuple(locale_paths))
        # root = self.django_settings['STATIC_ROOT']
        # sfd = tuple([x for x in sfd if x != root])
        # self.update_settings(STATICFILES_DIRS=sfd)

        # print(20150331, self.django_settings['FIXTURE_DIRS'])

    def set_user_model(self, spec):
        # print(f"20251125 Site.set_user_model() {self} {repr(spec)}")
        # if self.user_model is not None:
        #     msg = "Site.user_model was already set!"
        #     Theoretically this should raise an exception. But in a
        #     transitional phase after 20150116 we just ignore it. A
        #     warning would be nice, but we cannot use the logger here
        #     since it is not yet configured.
        #     self.logger.warning(msg)
        #     raise Exception(msg)
        self.user_model = spec
        if self.user_types_module is None:
            self.user_types_module = "lino.core.user_types"

    def get_auth_method(self):
        if self.user_model is None:
            return None
        if self.default_user is not None:
            return None
        # 20240518:
        if NO_REMOTE_AUTH:
            return "session"
        if self.remote_user_header is None:
            return "session"  # model backend
        return "remote"  # remote user backend

    def get_plugin_modifiers(self, **kwargs):
        return kwargs

    def is_hidden_plugin(self, app_label):
        if not self.is_installed(app_label):
            return False
        return app_label in self._hidden_plugins

    def is_hidden_app(self, app_label):
        # Return True if the named plugin is installed, known, but has been disabled using
        # :meth:`get_plugin_modifiers`.
        am = self.get_plugin_modifiers()
        if am.get(app_label, 1) is None:
            return True

    def update_settings(self, **kw):
        """This may be called from within a :xfile:`lino_local.py`."""
        self.django_settings.update(**kw)

    def define_settings(self, **kwargs):
        """Same as :meth:`update_settings`, but raises an exception if a
        setting already exists.

        TODO: Currently this exception is deactivated.  Because it
        doesn't work as expected.  For some reason (maybe because
        settings is being imported twice on a devserver) it raises a
        false exception when :meth:`override_defaults` tries to use it
        on :setting:`MIDDLEWARE_CLASSES`...

        """
        if False:
            for name in kwargs.keys():
                if name in self.django_settings:
                    raise Exception("Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)

    def startup(self):
        from lino.core.kernel import site_startup

        site_startup(self)

        if self.site_locale is None:
            self.site_locale = '.'.join(locale.getlocale())
        try:
            locale.setlocale(locale.LC_ALL, self.site_locale)
        except locale.Error as e:
            self.logger.warning("%s : %s", self.site_locale, e)
        self.clear_site_config()

    def register_shutdown_task(self, task):
        self._shutdown_tasks.append(task)

    def shutdown(self):
        for t in self._shutdown_tasks:
            t()

    def do_site_startup(self):
        # self.logger.info("20160526 %s do_site_startup() a", self.__class__)
        # self.logger.info("20160526 %s do_site_startup() b", self.__class__)
        pass

    logger = logger  # backwards-compat. Don't use this.

    def get_settings_subdirs(self, subdir_name):
        found = set()
        # print("20200701 compare", self.site_dir, classdir(self.__class__))
        # if self.site_dir != classdir(self.__class__):
        if True:
            pth = self.project_dir / subdir_name
            if pth.is_dir():
                yield pth
                # print("20200701 found", pth)
                found.add(pth)

        # If the settings.py doesn't subclass Site, then we also want to get
        # the inherited subdirs.
        for cl in self.__class__.__mro__:
            # print("20130109 inspecting class %s" % cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(classdir(cl), subdir_name)
                if isdir(pth) and not pth in found:
                    # if isdir(pth):
                    yield pth
                    found.add(pth)

    def makedirs_if_missing(self, dirname):
        if dirname and not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" % dirname)

    def is_abstract_model(self, module_name, model_name):
        app_name = ".".join(module_name.split(".")[:-1])
        model_name = app_name + "." + model_name
        # if 'avanti' in model_name:
        #     print("20170120", model_name,
        #           self.override_modlib_models,
        #           [m for m in self.installed_plugin_modules])
        rv = model_name in self.override_modlib_models
        if not rv:
            if app_name not in self.installed_plugin_modules:
                return True
        # if model_name.endswith('Company'):
        #     self.logger.info(
        #         "20160524 is_abstract_model(%s) -> %s", model_name, rv)
        # self.logger.info(
        #     "20160524 is_abstract_model(%s) -> %s (%s, %s)",
        #     model_name, rv, self.override_modlib_models.keys(),
        #     os.getenv('DJANGO_SETTINGS_MODULE'))
        return rv

    def is_installed_model_spec(self, model_spec):
        """
        Deprecated. This feature was a bit too automagic and caused bugs
        to pass silently.  See e.g. :blogref:`20131025`.
        """
        if False:  # mod_wsgi interprets them as error
            warnings.warn(
                "is_installed_model_spec is deprecated.", category=DeprecationWarning
            )

        if model_spec == "self":
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

    def is_installed(self, app_label):
        if self.installed_plugin_modules is None:
            raise Exception("Plugins are not yet loaded.")
        return app_label in self.plugins

    def resolve_model(self, *args, **kwargs):
        from lino.core.utils import resolve_model
        return resolve_model(*args, **kwargs)

    def setup_model_spec(self, obj, name):
        spec = getattr(obj, name)
        if spec and isinstance(spec, str):
            if not self.is_installed_model_spec(spec):
                # print(f"20251125 {spec} is not installed")
                setattr(obj, name, None)
                return
            msg = "Unresolved model '%s' in {0}.".format(name)
            msg += " ({})".format(str(self.installed_plugins))
            value = self.resolve_model(spec, strict=msg)
            setattr(obj, name, value)
            # print(f"20251125 {spec} has been set up to {value}")

    def on_each_app(self, methname, *args):
        modules = [a.models_module for a in apps.get_app_configs()]
        for mod in modules:
            meth = getattr(mod, methname, None)
            if meth is not None:
                if False:  # 20150925 once we will do it for good...
                    raise ChangedAPI(
                        "{0} still has a function {1}".format(mod, methname)
                    )
                meth(self, *args)

    def for_each_app(self, func, *args, **kw):
        from importlib import import_module

        done = set()
        for p in self.installed_plugins:
            for b in p.__class__.__mro__:
                if b not in (object, Plugin):
                    if b.__module__ not in done:
                        done.add(b.__module__)
                        parent = import_module(b.__module__)
                        func(b.__module__, parent, *args, **kw)
            if p.app_name not in done:
                func(p.app_name, p.app_module, *args, **kw)

    def demo_date(self, *args, **kwargs):
        base = self.the_demo_date or self.startup_time.date()
        return date_offset(base, *args, **kwargs)

    def today(self, *args, **kwargs):
        if self.site_config is None:
            base = self.the_demo_date
        else:
            base = self.site_config.simulate_today or self.the_demo_date
        if base is None:
            # base = datetime.date.today()
            base = timezone.now().date()
        return date_offset(base, *args, **kwargs)

    async def atoday(self, *args, **kwargs):
        return await sync_to_async(self.today)(*args, **kwargs)

    def now(self, *args, **kwargs):
        t = self.today(*args, **kwargs)
        now = timezone.now()
        return now.replace(year=t.year, month=t.month, day=t.day)

    def welcome_text(self):
        return "This is %s using %s." % (self.site_version(), self.using_text())

    def using_text(self):
        return ", ".join(["%s %s" % (n, v) for n, v, u in self.get_used_libs()])

    def site_version(self):
        if self.version:
            return self.verbose_name + " " + self.version
        return self.verbose_name

    # def configure_plugin(self, app_label, **kw):
    #     raise Exception("Replace SITE.configure_plugin by ad.configure_plugin")

    def install_migrations(self, *args):
        from lino.utils.dpy import install_migrations

        install_migrations(self, *args)

    def parse_date(self, s):
        ymd = tuple(reversed(list(map(int, s.split(".")))))
        if len(ymd) != 3:
            raise ValueError(
                "{} is not a valid date (format must be dd.mm.yyyy).".format(s)
            )
        return ymd
        # ~ return datetime.date(*ymd)

    def parse_time(self, s):
        # hms = list(map(int, s.split(':')))
        # return datetime.time(*hms)
        reg = re.compile(r"^(\d(?:\d(?=[.,:; ]?\d\d|[.,:; ]\d|$))?)?[.,:; ]?(\d{0,2})$")
        match = reg.match(s)
        if match is None:
            raise ValueError("%s is not a valid time" % s)
        hours, mins = match.groups()
        hours = int(hours) if hours != "" else 0
        mins = int(mins) if mins != "" else 0
        return datetime.time(hour=hours, minute=mins)

    def parse_datetime(self, s):
        # ~ print "20110701 parse_datetime(%r)" % s
        # ~ s2 = s.split()
        s2 = s.split("T")
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = list(map(int, s2[0].split("-")))
        hms = list(map(int, s2[1].split(":")))
        return datetime.datetime(*(ymd + hms))
        # ~ d = datetime.date(*self.parse_date(s[0]))
        # ~ return datetime.combine(d,t)

    def strftime(self, t):
        if t is None:
            return ""
        return t.strftime(self.time_format_strftime)

    def resolve_virtual_fields(self):
        # print("20181023 resolve_virtual_fields()")
        for vf in self.VIRTUAL_FIELDS:
            vf.lino_resolve_type()
        self.VIRTUAL_FIELDS = set()

    def register_virtual_field(self, vf):
        """Call lino_resolve_type after startup."""
        if self._startup_done:
            # raise Exception("20190102")
            vf.lino_resolve_type()
        else:
            # print("20181023 postpone resolve_virtual_fields() for {}".format(vf))
            self.VIRTUAL_FIELDS.add(vf)

    def find_config_file(self, *args, **kwargs):
        return self.confdirs.find_config_file(*args, **kwargs)

    def find_template_config_files(self, *args, **kwargs):
        return self.confdirs.find_template_config_files(*args, **kwargs)

    def setup_actions(self):
        from lino.core.merge import MergeAction

        for m in apps.get_models():
            if m.allow_merge_action:
                m.define_action(merge_row=MergeAction(m))

    def add_user_field(self, name, fld):
        if self.user_model:
            from lino.core.inject import inject_field
            inject_field(self.user_model, name, fld)

    def get_used_libs(self, html=None):
        yield ("Lino", __version__, "https://www.lino-framework.org")

        try:
            import mod_wsgi

            if getattr(mod_wsgi, "version", None) is None:
                raise ImportError
            version = "{0}.{1}".format(*mod_wsgi.version)
            yield ("mod_wsgi", version, "http://www.modwsgi.org/")
        except ImportError:
            pass

        import django

        yield ("Django", django.get_version(), "https://www.djangoproject.com")

        import sys

        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python", version, "https://www.python.org")

        import babel

        yield ("Babel", babel.__version__, "https://babel.edgewall.org/")

        import jinja2

        version = getattr(jinja2, "__version__", "")
        yield ("Jinja", version, "http://jinja.pocoo.org/")

        import dateutil

        version = getattr(dateutil, "__version__", "")
        yield ("python-dateutil", version, "https://dateutil.readthedocs.io/en/stable/")

        for p in self.sorted_plugins:
            for u in p.get_used_libs(html):
                yield u

    def get_social_auth_links(self, chunks=False):
        # print("20171207 site.py")
        # elems = []
        if self.social_auth_backends is None or not has_socialauth:
            return
        from social_core.backends.utils import load_backends

        # from collections import OrderedDict
        # from django.conf import settings
        # from social_core.backends.base import BaseAuth
        # backend = module_member(auth_backend)
        # if issubclass(backend, BaseAuth):
        for b in load_backends(self.social_auth_backends).values():
            if chunks:
                yield (b.name, "/oauth/login/" + b.name)  # name, href
            else:
                yield E.a(b.name, href="/oauth/login/" + b.name)
        # print("20171207 a", elems)
        # return E.div(*elems)

    def apply_languages(self):
        if isinstance(self.languages, tuple) and isinstance(
            self.languages[0], LanguageInfo
        ):
            # e.g. override_defaults() has been called explicitly, without
            # specifying a languages keyword.
            return

        self.language_dict = dict()  # maps simple_code -> LanguageInfo

        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict()  # used in lino.modlib.users
        must_set_language_code = False

        # ~ self.AVAILABLE_LANGUAGES = (to_locale(self.DEFAULT_LANGUAGE),)
        if self.languages is None:
            self.languages = [DJANGO_DEFAULT_LANGUAGE]
            # ~ self.update_settings(USE_L10N = False)

            # ~ info = LanguageInfo(DJANGO_DEFAULT_LANGUAGE,to_locale(DJANGO_DEFAULT_LANGUAGE),0,'')
            # ~ self.DEFAULT_LANGUAGE = info
            # ~ self.languages = (info,)
            # ~ self.language_dict[info.name] = info
        else:
            if isinstance(self.languages, str):
                self.languages = str(self.languages).split()
            # ~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            # ~ lc = language_choices(*self.languages)
            # ~ self.update_settings(LANGUAGES = lc)
            # ~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            # ~ self.update_settings(LANGUAGE_CODE = self.languages[0])
            # self.update_settings(USE_L10N=True)
            must_set_language_code = True

        languages = []
        for i, django_code in enumerate(self.languages):
            assert_django_code(django_code)
            name = str(to_locale(django_code))
            if name in self.language_dict:
                raise Exception(
                    "Duplicate name %s for language code %r" % (name, django_code)
                )
            if i == 0:
                suffix = ""
            else:
                suffix = "_" + name
            info = LanguageInfo(str(django_code), str(name), i, str(suffix))
            self.language_dict[name] = info
            languages.append(info)

        new_languages = languages
        for info in tuple(new_languages):
            if "-" in info.django_code:
                base, loc = info.django_code.split("-")
                if base not in self.language_dict:
                    self.language_dict[base] = info

                    # replace the complicated info by a simplified one
                    # ~ newinfo = LanguageInfo(info.django_code,base,info.index,info.suffix)
                    # ~ new_languages[info.index] = newinfo
                    # ~ del self.language_dict[info.name]
                    # ~ self.language_dict[newinfo.name] = newinfo

        # ~ for base,lst in simple_codes.items():
        # ~ if len(lst) == 1 and and not base in self.language_dict:
        # ~ self.language_dict[base] = lst[0]

        self.languages = tuple(new_languages)
        self.DEFAULT_LANGUAGE = self.languages[0]

        self.BABEL_LANGS = tuple(self.languages[1:])

        if must_set_language_code:
            self.update_settings(LANGUAGE_CODE=self.languages[0].django_code)
            # Note: LANGUAGE_CODE is what *Django* believes to be the
            # default language.  This should be some variant of
            # English ('en' or 'en-us') if you use
            # `django.contrib.humanize`
            # https://code.djangoproject.com/ticket/20059

        self.setup_languages()

    def setup_languages(self):
        from django.conf.global_settings import LANGUAGES

        def langtext(code):
            for k, v in LANGUAGES:
                if k == code:
                    return v
            # returns None if not found

        def _add_language(code, lazy_text):
            self.LANGUAGE_DICT[code] = lazy_text
            self.LANGUAGE_CHOICES.append((code, lazy_text))

        if self.languages is None:
            _add_language(DJANGO_DEFAULT_LANGUAGE, _("English"))

        else:
            for lang in self.languages:
                code = lang.django_code
                text = langtext(code)
                if text is None:
                    # Django doesn't know these
                    if code == "de-be":
                        text = gettext_noop("German (Belgium)")
                    elif code == "de-ch":
                        text = gettext_noop("German (Swiss)")
                    elif code == "de-at":
                        text = gettext_noop("German (Austria)")
                    elif code == "en-us":
                        text = gettext_noop("American English")
                    else:
                        raise Exception(
                            "Unknown language code %r (must be one of %s)"
                            % (lang.django_code, [x[0] for x in LANGUAGES])
                        )

                text = _(text)
                _add_language(lang.django_code, text)

            # Cannot activate the site's default language
            # because some test cases in django.contrib.humanize
            # rely on en-us as default language
            # ~ set_language(self.get_default_language())

            # reduce Django's LANGUAGES to my babel languages:
            self.update_settings(
                LANGUAGES=[x for x in LANGUAGES if x[0] in self.LANGUAGE_DICT]
            )

    def get_language_info(self, code):
        return self.language_dict.get(code, None)

    def resolve_languages(self, languages):
        rv = []
        if isinstance(languages, str):
            languages = str(languages).split()
        for k in languages:
            if isinstance(k, str):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception(
                        "Unknown language code %r (must be one of %s)"
                        % (str(k), [i.name for i in self.languages])
                    )
                rv.append(li)
            else:
                assert k in self.languages
                rv.append(k)
        return tuple(rv)

    def language_choices(self, language, choices):
        l = choices.get(language, None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l

    def get_default_language(self):
        return self.DEFAULT_LANGUAGE.django_code

    def str2dict(self, txt, **kw):
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[simple] = str(txt)
        return kw

    def str2kw(self, field_name, txt, **kw):
        # from django.utils import translation
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[field_name + info.suffix] = str(txt)
        return kw

    def babelkw(self, name, txt=None, **translations):
        # Note that kwargs are *not* passed to str2kw()
        if txt is None:
            d = dict()
        else:
            d = self.str2kw(name, txt)
        for simple, info in self.language_dict.items():
            v = translations.get(simple, None)
            if v is not None:
                d[name + info.suffix] = str(v)
        return d

    def args2kw(self, name, *args):
        assert len(args) == len(self.languages)
        kw = {name: args[0]}
        for i, lang in enumerate(self.BABEL_LANGS):
            kw[name + "_" + lang] = args[i + 1]
        return kw

    def field2kw(self, obj, name, **known_values):
        # d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lng in self.languages:
            v = getattr(obj, name + lng.suffix, None)
            if v:
                known_values[lng.name] = v
        return known_values

    def field2args(self, obj, name):
        return [str(getattr(obj, name + li.suffix)) for li in self.languages]
        # ~ l = [ getattr(obj,name) ]
        # ~ for lang in self.BABEL_LANGS:
        # ~ l.append(getattr(obj,name+'_'+lang))
        # ~ return l

    def babelitem(self, *args, **values):
        if len(args) == 0:
            info = self.language_dict.get(get_language(), self.DEFAULT_LANGUAGE)
            default_value = None
            if info == self.DEFAULT_LANGUAGE:
                return values.get(info.name)
            x = values.get(info.name, None)
            if x is None:
                return values.get(self.DEFAULT_LANGUAGE.name)
            return x
        elif len(args) == 1:
            info = self.language_dict.get(get_language(), None)
            if info is None:
                return args[0]
            default_value = args[0]
            return values.get(info.name, default_value)
        # args = tuple_py2(args)
        # print(type(args))
        raise ValueError("%(values)s is more than 1 default value." % dict(values=args))

    # babel_get(v) = babelitem(**v)

    def babeldict_getitem(self, d, k):
        v = d.get(k, None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)

    def babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None):
        if language is None:
            language = get_language()
        info = self.language_dict.get(language, self.DEFAULT_LANGUAGE)
        if info.index != 0:
            v = getattr(obj, attrname + info.suffix, None)
            if v:
                return v
        if default is NOT_PROVIDED:
            return getattr(obj, attrname)
        else:
            return getattr(obj, attrname, default)
        # ~ if lang is not None and lang != self.DEFAULT_LANGUAGE:
        # ~ v = getattr(obj,attrname+"_"+lang,None)
        # ~ if v:
        # ~ return v
        # ~ return getattr(obj,attrname,*args)

    def diagnostic_report_rst(self, *args):
        """Returns a string with a diagnostic report about this
        site. :manage:`diag` is a command-line shortcut to this.

        """
        s = ""
        s += rstgen.header(1, "Plugins")
        for n, p in enumerate(self.installed_plugins):
            s += "%d. " % (n + 1)
            s += "{} : {}\n".format(p.app_label, p)
        # s += "config_dirs: %s\n" % repr(self.confdirs.config_dirs)
        s += "\n"
        s += rstgen.header(1, "Config directories")
        for n, cd in enumerate(self.confdirs.config_dirs):
            s += "%d. " % (n + 1)
            ln = relpath(cd.name)
            if cd.writeable:
                ln += " [writeable]"
            s += ln + "\n"
        # for arg in args:
        #     p = self.plugins[arg]
        return s

    # def get_db_overview_rst(self):
    #     from lino.utils.diag import analyzer
    #     analyzer.show_db_overview()

    def override_defaults(self, **kwargs):
        self.override_settings(**kwargs)
        self.install_settings()

    def is_imported_partner(self, obj):
        # Deprecated.
        # ~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        # ~ return obj.id is not None and (obj.id > 10 and obj.id < 21)

    def site_header(self):
        if self.is_installed("contacts"):
            if (owner := self.plugins.contacts.site_owner) is not None:
                return owner.get_address("<br/>")

    # def setup_main_menu(self):
    #     """
    #     To be implemented by applications.
    #     """
    #     pass

    def get_dashboard_items(self, user):
        if user:
            for p in self.installed_plugins:
                for i in p.get_dashboard_items(user):
                    yield i

    @property
    def copyright_name(self):
        """Name of copyright holder of the site's content."""
        if (owner := self.get_plugin_setting('contacts', 'site_owner')) is not None:
            # print("20230423", self.site_company)
            return str(owner)

    @property
    def copyright_url(self):
        if (owner := self.get_plugin_setting('contacts', 'site_owner')) is not None:
            return owner.url

    @property
    def site_config(self):
        if "system" not in self.models:
            return None
        return self.models.system.SiteConfig.get_site_config()

    def get_config_value(self, name, default=None):
        if self.site_config is None:
            return default
            # self.site_config_defaults.get(name, default)
        return getattr(self.site_config, name)

    # ~ def shutdown(self):
    # ~ self.clear_site_config()
    # ~ return super(Site,self).shutdown()

    def clear_site_config(self):
        # from lino.core.utils import obj2str
        # print("20180502 clear_site_config {}".format(
        #     obj2str(self._site_config, True)))
        if "system" in self.models:
            self.models.system.SiteConfig.clear_site_config()

    @property
    def quicklinks(self):
        if self._quicklinks is None:
            from lino.core.menus import QuickLinksList

            qll = QuickLinksList()
            for ql in self.get_quicklinks():
                qll.add_action(ql)
            self.setup_quicklinks(None, qll)
            self._quicklinks = qll
        return self._quicklinks

    def get_quicklink_items(self, user_type):
        for ql in self.quicklinks.items:
            if ql.bound_action.get_view_permission(user_type):
                yield ql

    def get_quicklinks_html(self, ar, user):
        qll = []
        for ql in self.get_quicklink_items(user.user_type):
            if ql.bound_action.get_bound_action_permission(ar):
                qll.append(tostring(ar.menu_item_button(ql)))

        # if getattr(ar.renderer.front_end, 'autorefresh_seconds', 0) > 0:
        #     qll.append(
        #         '<a href="javascript:Lino.autorefresh();">autorefresh</a>')
        # if False:
        #     qll.append(
        #         '<a href="javascript:{}" style="text-decoration:none">{}</a>'.
        #         format(self.kernel.default_renderer.reload_js(), _("Refresh")))

        return mark_safe(" | ".join(qll))

    def get_quicklinks(self):
        return []

    def setup_quicklinks(self, unused, tb):
        for p in self.sorted_plugins:
            p.setup_quicklinks(tb)
            for spec in p.get_quicklinks():
                tb.add_action(spec)

    def get_site_menu(self, user_type, ar=None):
        from lino.core import menus

        main = menus.Toolbar(user_type, "main")
        self.setup_menu(user_type, main, ar)
        main.compress()
        return main

    _sorted_plugins = None

    @property
    def sorted_plugins(self):
        # change the "technical" plugin order into the order visible to the end
        # user.  The end user wants to see menu entries of explicitly installed
        # plugins before those of automatically installed plugins.
        if self._sorted_plugins is None:
            self._sorted_plugins = []
            for p in self.installed_plugins:
                if not p.is_hidden() and p.needed_by is None:
                    # explicitly installed
                    self._sorted_plugins.append(p)
            for p in self.installed_plugins:
                if not p.is_hidden() and p.needed_by is not None:
                    # automatically installed
                    self._sorted_plugins.append(p)
        return self._sorted_plugins

    def setup_menu(self, user_type, main, ar=None):
        for k, label in self.top_level_menus:
            methname = "setup_{0}_menu".format(k)

            if label is None:
                menu = main
            else:
                menu = main.add_menu(k, label)
            for p in self.sorted_plugins:
                meth = getattr(p, methname, None)
                if meth is not None:
                    meth(self, user_type, menu, ar)
                    # print("20190430 {} {} ({}) --> {}".format(
                    #       k, p.app_label, p.needed_by, [i.name for i in main.items]))

    def get_middleware_classes(self):
        yield "django.middleware.common.CommonMiddleware"
        if self.languages and len(self.languages) > 1:
            yield "django.middleware.locale.LocaleMiddleware"

        if self.user_model:
            yield "django.contrib.sessions.middleware.SessionMiddleware"
            # yield 'django.contrib.auth.middleware.AuthenticationMiddleware'
            yield "lino.core.auth.middleware.AuthenticationMiddleware"
            yield "lino.core.auth.middleware.WithUserMiddleware"
            # yield 'lino.core.auth.middleware.DeviceTypeMiddleware'
        else:
            yield "lino.core.auth.middleware.NoUserMiddleware"

        if self.get_auth_method() == "remote":
            # yield 'django.contrib.auth.middleware.RemoteUserMiddleware'
            yield "lino.core.auth.middleware.RemoteUserMiddleware"
        # if self.use_ipdict:
        #     yield 'lino.modlib.ipdict.middleware.Middleware'
        if has_socialauth and self.get_plugin_setting(
            "users", "third_party_authentication", False
        ):
            yield "social_django.middleware.SocialAuthExceptionMiddleware"

        # removed 20240921, see #5755 (Should we remove AjaxExceptionResponse?)
        if False:
            yield "lino.utils.ajax.AjaxExceptionResponse"

        if self.use_security_features:
            yield "django.middleware.security.SecurityMiddleware"
            yield "django.middleware.clickjacking.XFrameOptionsMiddleware"
            # yield 'django.middleware.csrf.CsrfViewMiddleware'

        if False:
            # ~ yield 'lino.utils.sqllog.ShortSQLLogToConsoleMiddleware'
            yield "lino.utils.sqllog.SQLLogToConsoleMiddleware"
            # ~ yield 'lino.utils.sqllog.SQLLogMiddleware'

    def __deepcopy__(self):
        raise Exception("Who is copying me?!")

    def __copy__(self):
        raise Exception("Who is copying me?!")

    def get_main_html(self, ar, **context):
        # assert request is not None
        # print("20210615 get_main_html()", ar)
        # if front_end is None:
        #     front_end = self.kernel.default_ui
        s = self.plugins.jinja.render_from_ar(ar, "admin_main.html", **context)
        return mark_safe(s)

    def build_site_cache(self, force=False, later=False, verbosity=1):
        from lino.modlib.users.utils import with_user_profile
        from lino.modlib.users.choicelists import UserTypes
        self.kernel.touch_lino_version()
        # raise Exception("20251011")

        if later:
            # print("20230823 later")
            return

        # verbosity = 3

        if verbosity > 0:
            self.logger.info("Build site cache in %s.", self.media_root)

        started = time.time()
        count = 0
        # rnd = self.kernel.default_ui.renderer
        # renderers = [p.renderer for p in self.installed_plugins if p.renderer is not None]
        for lng in self.languages:
            with translation.override(lng.django_code):
                for user_type in UserTypes.get_list_items():
                    if verbosity > 0:
                        self.logger.info(
                            "Build JS cache for %s (%s).",
                            user_type, lng.name)
                    for wf in self.kernel.web_front_ends:
                        count += with_user_profile(
                            user_type, wf.renderer.build_js_cache,
                            force, verbosity)

        if verbosity > 0:
            self.logger.info(
                "%d site cache files have been built in %s seconds.",
                count, time.time() - started)

    _top_link_generator = []

    def get_top_links(self, ar):
        messages = []
        for g in self._top_link_generator:
            for msg in g(ar):
                messages.append(msg)
        return tostring(E.div(*messages))

    def add_top_link_generator(self, func):
        self._top_link_generator.append(func)

    def get_footer_html(self, ar):
        return mark_safe("<p>This is a new feature.</p>")

    def get_welcome_messages(self, ar):
        for h in self._welcome_handlers:
            for msg in h(ar):
                yield msg
        # for a in self._welcome_actors:
        #     for msg in a.get_welcome_messages(ar):
        #         yield msg

    def add_welcome_handler(self, func, actor=None, msg=None):
        # print(
        #     "20161219 add_welcome_handler {} {} {}".format(
        #         actor, msg, func))
        self._welcome_handlers.append(func)

    def get_installed_plugins(self):
        if self.django_admin_prefix:
            yield "django.contrib.admin"  # not tested

        # yield 'django.contrib.staticfiles'
        yield "lino.modlib.about"

        if self.use_ipdict:
            yield "lino.modlib.ipdict"

        if (
            isinstance(self.social_auth_backends, list)
            and len(self.social_auth_backends) == 0
        ):
            raise Exception(
                "Incorrect value for social_auth_backends,"
                "social_auth_backends should be None or non-empty list."
            )

        if self.default_ui is not None:
            yield self.default_ui
        if self.web_front_ends is not None:
            for prefix, modname in self.web_front_ends:
                yield modname

        # if self.admin_ui is not None:
        #     if self.admin_ui == self.default_ui:
        #         raise Exception(
        #             "admin_ui (if specified) must be different "
        #             "from default_ui")
        #     yield self.admin_ui

        # if self.use_linod:
        #     yield 'lino.modlib.linod'

        # if self.default_ui == "extjs":
        #     yield 'lino.modlib.extjs'
        #     yield 'lino.modlib.bootstrap5'
        # elif self.default_ui == "bootstrap5":
        #     yield 'lino.modlib.bootstrap5'

        # yield "lino.modlib.lino_startup"

    server_url = "http://127.0.0.1:8000"
    """The "official" URL used by "normal" users when accessing this Lino
    site.

    This is used by templates such as :xfile:`summary.eml` (used by
    :mod:`lino.modlib.notify` to send notification emails)

    Django has a `HttpRequest.build_absolute_uri()
    <https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpRequest.build_absolute_uri>`__
    method, but e.g. notification emails are sent via :manage:`linod` where no
    HttpRequest exists. That's why we need to manually set :attr:`server_url`.

    """

    site_prefix = "/"
    """The string to prefix to every URL of the Lino web interface.

    This must *start and end* with a *slash*.  Default value is
    ``'/'``.

    Don't change this. Other values than the default value are not tested.

    This must be set if your project is not being served at the "root"
    URL of your server.

    If this is different from the default value, Lino also sets
    :setting:`SESSION_COOKIE_PATH`.

    When this Site is running under something else than a development
    server, this setting must correspond to your web server's
    configuration.  For example if you have::

        WSGIScriptAlias /foo /home/luc/mypy/lino_sites/foo/wsgi.py

    Then your :xfile:`settings.py` should specify::

        site_prefix = '/foo/'

    See also :ref:`mass_hosting`.

    """

    # def urlkwargs(self, **kw):
    #     """
    #
    #     Return the current url preferences as a dict to pass to buildurl in
    #     order to forward them to a next url.
    #
    #     """
    #     lng = get_language()
    #     if len(self.languages) > 1 and self.DEFAULT_LANGUAGE.django_code != lng:
    #         kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lng)
    #     return kw

    def buildurl(self, *args, **kw):
        return buildurl(self.site_prefix, *args, **kw)

    def build_media_url(self, *args, **kw):
        return buildurl(settings.MEDIA_URL, *args, **kw)

    def build_static_url(self, *args, **kw):
        return buildurl(settings.STATIC_URL, *args, **kw)

    def welcome_html(self, ui=None):
        from django.utils.translation import gettext as _

        p = []
        sep = ""
        if self.verbose_name:
            p.append(_("This website runs "))
            if self.url:
                p.append(E.a(str(self.verbose_name), href=self.url, target="_blank"))
            else:
                p.append(E.b(str(self.verbose_name)))
            if self.version:
                p.append(" ")
                p.append(self.version)
            if self.is_installed("about"):
                p.append(_(" and "))
                p.append(E.a(_("more"), href="/about/about_html"))
            sep = _(" using ")

        if False:
            for name, version, url in self.get_used_libs(html=E):
                p.append(sep)
                p.append(E.a(name, href=url, target="_blank"))
                p.append(" ")
                p.append(version)
                sep = ", "

        yield E.span(*p)

    def get_letter_date_text(self, today=None):
        if self.is_installed("contacts"):
            if (sc := self.plugins.contacts.site_owner) is None:
                return
        if today is None:
            today = self.today()
        from lino.utils.format_date import fdl

        if sc and sc.city:
            return _("%(place)s, %(date)s") % dict(
                place=str(sc.city.name), date=fdl(today)
            )
        return fdl(today)

    def decfmt(self, v, places=2, **kw):
        kw.setdefault("sep", self.decimal_group_separator)
        kw.setdefault("dp", self.decimal_separator)
        from lino.utils import moneyfmt

        if v is None:
            return ""
        return moneyfmt(v, places=places, **kw)

    def format_currency(self, *args, **kwargs):
        return locale.currency(*args, **kwargs)

    LOOKUP_OP = "__iexact"

    def lookup_filter(self, fieldname, value, **kw):
        from django.db.models import Q

        kw[fieldname + self.LOOKUP_OP] = value
        # ~ kw[fieldname] = value
        flt = Q(**kw)
        del kw[fieldname + self.LOOKUP_OP]
        for lng in self.BABEL_LANGS:
            kw[fieldname + lng.suffix + self.LOOKUP_OP] = value
            flt = flt | Q(**kw)
            del kw[fieldname + lng.suffix + self.LOOKUP_OP]
        return flt

    # def relpath(self, p):
    #     """Used by :class:`lino.mixins.printable.EditTemplate` in order to
    #     write a testable message...

    #     """
    #     if p.startswith(self.project_dir):
    #         p = "$(PRJ)" + p[len(self.project_dir):]
    #     return p

    def resolve_plugin(self, app_label):
        return self.plugins.get(app_label, None)

    def get_plugin_setting(self, plugin_name, option_name, *default):
        if self.installed_plugin_modules is None:
            p = PLUGIN_CONFIGS.get(plugin_name, {})
            return p.get(option_name, *default)
        if self.is_installed(plugin_name):
            p = self.plugins.get(plugin_name)
            return getattr(p, option_name, *default)
        if len(default) == 0:
            raise Exception(
                "Plugin {} is not installed and no default was provided".format(
                    plugin_name
                )
            )
        return default[0]


class TestSite(Site):
    def __init__(self, *args, **kwargs):
        # kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        g.update(SECRET_KEY="20227")  # see :djangoticket:`20227`
        super(TestSite, self).__init__(g, *args, **kwargs)

        # 20140913 Hack needed for doctests in :mod:`ad`.
        # from django.utils import translation
        translation._default = None
