# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand, CommandError

from lino.modlib.checkdata.choicelists import Checkers
from lino.modlib.checkdata.models import check_data

from lino.api import dd, rt


class Command(BaseCommand):
    args = "[app1.Model1.Checker1] [app2.Model2.Checker2] ..."
    help = """

    Update the table of checkdata messages.

    If no arguments are given, run it on all data checkers.
    Otherwise every positional argument is expected to be a model name in
    the form `app_label.ModelName`, and only these models are being
    updated.

    """

    def add_arguments(self, parser):
        parser.add_argument("checkers", nargs="*", help="the checkers to run")
        (
            parser.add_argument(
                "-l",
                "--list",
                action="store_true",
                dest="list",
                default=False,
                help="Don't check, just show a list of available checkers.",
            ),
        )
        parser.add_argument(
            "-f",
            "--fix",
            action="store_true",
            dest="fix",
            default=False,
            help="Fix any repairable problems.",
        )
        parser.add_argument(
            "-p",
            "--prune",
            action="store_true",
            dest="prune",
            default=False,
            help="Remove all existing problem messages first.",
        )

    def handle(self, *args, **options):
        app = options.get("checkers", args)
        if app:
            args += tuple(app)
        ar = rt.login(dd.plugins.users.demo_username)
        if options["list"]:
            ar.show(Checkers, column_names="value text")
        else:
            rt.startup()
            check_data(ar, args=args, fix=options["fix"], prune=options["prune"])
