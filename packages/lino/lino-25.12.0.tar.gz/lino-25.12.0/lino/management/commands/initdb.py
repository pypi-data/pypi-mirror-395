# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

from click import confirm
from lino.api import dd
from django.db import models
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.core.management.color import no_style
from django.db.utils import IntegrityError, OperationalError
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
import os
import shutil
from pathlib import Path
import tempfile

import warnings

warnings.filterwarnings(
    "ignore",
    "No fixture named '.*' found.",
    UserWarning,
    "django.core.management.commands.loaddata",
)
warnings.filterwarnings(
    "ignore",
    "No fixture data found for *",
    RuntimeWarning,
    "django.core.management.commands.loaddata",
)


# ~ from django.core.management.sql import sql_reset


USE_SQLDELETE = True

USE_DROP_CREATE_DB = True
"""
https://stackoverflow.com/questions/3414247/django-drop-all-tables-from-database
http://thingsilearned.com/2009/05/10/drop-database-command-for-django-manager/

"""


def foralltables(using, cmd):
    conn = connections[using]
    cursor = conn.cursor()
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    for tablename in cursor.fetchall():
        cursor.execute(cmd.format(tablename[0]))


def remove_tree(pth):
    # When we do "inv prep" on a developer machine, we really want to remove the
    # media directories of the demo projects. But on a production site we really
    # *don't* want this to happen accidentally. So we introduce an intermediate
    # step: the media directory is not deleted immediately but moved to a
    # directory "media.bak" under the system's temporary directory (returned by
    # tempfile.gettempdir()). Only this temporary media.bak is removed for good if
    # it exists.
    tempdir = Path(tempfile.gettempdir()) / (pth.name + ".bak")
    if not settings.DEBUG:
        settings.SITE.logger.info("Move content of %s to %s", pth, tempdir)
    if tempdir.exists():
        shutil.rmtree(tempdir)
        # really_remove(tempdir)

    oldumask = os.umask(0o000)
    os.mkdir(tempdir, mode=0o775)
    os.umask(oldumask)

    shutil.move(pth, tempdir)
    # pth.rename(tempdir)
    # pth.mkdir()


# def really_remove(top):
#     for pth in top.iterdir():
#         if pth.is_dir():
#             really_remove(pth)
#             pth.rmdir()
#         else:
#             if not settings.DEBUG:
#                 # On a production site let's at least say goodbye to each file.
#                 settings.SITE.logger.info("Remove {}".format(pth))
#             pth.unlink()


class Command(BaseCommand):
    """Flush the database and load the specified fixtures."""

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("fixtures", nargs="*", help="the fixtures to load")
        (
            parser.add_argument(
                "--noinput",
                action="store_false",
                dest="interactive",
                default=True,
                help="Do not prompt for input of any kind.",
            ),
        )
        # parser.add_argument('--nobuildcache', action='store_false',
        #                     dest='buildcache', default=True,
        #                     help='Does nothing.'),
        (
            parser.add_argument(
                "--removemedia",
                action="store_true",
                dest="removemedia",
                default=False,
                help="Remove all files in the settings.MEDIA_ROOT directory.",
            ),
        )
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            default=DEFAULT_DB_ALIAS,
            help="Nominates a database to reset. "
            'Defaults to the "default" database.',
        )

    def try_sql(self, conn, sql_list):
        hope = False
        pending = []
        errors = []
        cursor = conn.cursor()
        for sql in sql_list:
            try:
                cursor.execute(sql)
                hope = True
            except (IntegrityError, OperationalError) as e:
                pending.append(sql)
                errors.append(e)
        if not hope:
            # a temporary last attempt: run them all in one statement
            # sql = "SET foreign_key_checks=0;" + ';'.join(sql_list)
            # cursor.execute(sql)

            msg = "%d pending SQL statements failed:" % len(pending)
            for i, sql in enumerate(pending):
                e = errors[i]
                msg += "\n%s :\n  %s\n  %s" % (e.__class__, sql, e)
            raise Exception(msg)
        return pending

    def makemigrations(self, verbosity):
        for p in settings.SITE.installed_plugins:
            makemigrations = False
            for prefix in settings.SITE.migratable_plugin_prefixes:
                if p.app_name.startswith(prefix):
                    makemigrations = True
                    break
            if p.app_name.startswith("lino") or makemigrations:
                migrations_dir = Path(p.app_module.__file__).parent / "migrations"
                migrations_dir.mkdir()
                call_command(
                    "makemigrations",
                    p.app_name.split(".")[-1],
                    interactive=False,
                    verbosity=verbosity,
                )

    def removemigrations(self):
        for p in settings.SITE.installed_plugins:
            rm_mig_dir = False
            for prefix in settings.SITE.migratable_plugin_prefixes:
                if p.app_name.startswith(prefix):
                    rm_mig_dir = True
                    break
            if p.app_name.startswith("lino") or rm_mig_dir:
                migrations_dir = Path(p.app_module.__file__).parent / "migrations"
                if migrations_dir.exists():
                    shutil.rmtree(migrations_dir)

    def handle(self, *args, **options):
        interactive = options.get("interactive")
        verbosity = options.get("verbosity")
        using = options.get("database", DEFAULT_DB_ALIAS)
        dbname = settings.DATABASES[using]["NAME"]
        engine = settings.DATABASES[using]["ENGINE"]

        # buildcache = options.pop('buildcache')
        removemedia = options.pop("removemedia")
        assert str(settings.SITE.media_root) == settings.MEDIA_ROOT
        mroot = settings.SITE.media_root
        if not mroot.exists():
            removemedia = False

        if interactive:
            msg = "We are going to flush your database ({})".format(dbname)
            if removemedia:
                msg += "\nAND REMOVE ALL FILES BELOW {}".format(mroot)
            msg += ".\nAre you sure?"
            if not confirm(msg, default=True):
                raise CommandError("User abort.")

        # mroot = Path(settings.MEDIA_ROOT)
        if removemedia:
            remove_tree(mroot)

        fixtures = options.pop("fixtures", args)  # don't keep this option

        # print(20160817, fixtures, options)

        options.update(interactive=False)

        # the following log message was useful on Travis 20150104
        if verbosity > 0:
            dd.logger.info(
                "`initdb %s` started on database %s.", " ".join(fixtures), dbname
            )

        if engine == "django.db.backends.sqlite3":
            if dbname != ":memory:" and os.path.isfile(dbname):
                os.remove(dbname)
                del connections[using]
        elif engine == "django.db.backends.mysql":
            conn = connections[using]
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE %s;" % dbname)
            cursor.execute("CREATE DATABASE %s;" % dbname)
            # We must now force Django to reconnect, otherwise we get
            # "no database selected" since Django would try to
            # continue on the dropped database:
            del connections[using]

            # now reconnect and set foreign_key_checks to 0
            conn = connections[using]
            cursor = conn.cursor()
            cursor.execute("set foreign_key_checks=0;")
        elif engine.startswith("django.db.backends.postgresql"):
            foralltables(using, "DROP TABLE IF EXISTS {} CASCADE;")
            # cmd = """select 'DROP TABLE "' || tablename || '" IF EXISTS CASCADE;' from pg_tables where schemaname = 'public';"""
            # cursor.execute(cmd)
            # cursor.close()
            del connections[using]
        else:
            raise Exception("Not tested for %r" % engine)
            sql_list = []
            conn = connections[using]

            # adds a "DELETE FROM tablename;" for each table
            # sql = sql_flush(no_style(), conn, only_django=False)
            # sql_list.extend(sql)

            if USE_SQLDELETE:
                from django.core.management.sql import sql_delete
                # sql_delete was removed in Django 1.9
                # ~ sql_list = u'\n'.join(sql_reset(app, no_style(), conn)).encode('utf-8')

                app_list = [
                    models.get_app(p.app_label) for p in settings.SITE.installed_plugins
                ]
                for app in app_list:
                    # app_label = app.__name__.split('.')[-2]
                    sql_list.extend(sql_delete(app, no_style(), conn))
                    # print app_label, ':', sql_list

            # ~ print sql_list

            if len(sql_list):
                with conn.constraint_checks_disabled():
                    # for sql in sql_list:
                    #     cursor.execute(sql)

                    pending = self.try_sql(conn, sql_list)
                    while len(pending):
                        pending = self.try_sql(conn, pending)

            transaction.commit_unless_managed()

        if engine.startswith("django.db.backends.postgresql"):
            try:
                call_command("migrate", **options)
                self.makemigrations(verbosity)
                call_command("makemigrations", interactive=False, verbosity=verbosity)
                call_command("migrate", "--run-syncdb", **options)
            finally:
                self.removemigrations()
        else:
            # call_command('makemigrations', '--merge', interactive=False, verbosity=verbosity)
            call_command("makemigrations", interactive=False, verbosity=verbosity)
            call_command("migrate", "--run-syncdb", **options)

        for p in settings.SITE.installed_plugins:
            p.on_initdb(settings.SITE, verbosity=verbosity)

        if len(fixtures):
            # if engine == 'django.db.backends.postgresql':
            #     foralltables(using, "ALTER TABLE {} DISABLE TRIGGER ALL;")

            options.pop("interactive")
            call_command("loaddata", *fixtures, **options)

            # if engine == 'django.db.backends.postgresql':
            #     foralltables(using, "ALTER TABLE {} ENABLE TRIGGER ALL;")

        settings.SITE.clear_site_config()

        # dblogger.info("Lino initdb %s done on database %s.", args, dbname)
