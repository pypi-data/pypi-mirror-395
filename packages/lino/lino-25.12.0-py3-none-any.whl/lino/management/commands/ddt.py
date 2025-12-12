# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# import shutil
from click import confirm
import subprocess
from django.db import DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Run a double-dump test on this site."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        (
            parser.add_argument(
                "-b", "--batch", "--noinput",
                action="store_false",
                dest="interactive",
                default=True,
                help="Do not prompt for input of any kind.",
            ),
        )

    def runcmd(self, cmd, **options):
        bashopts = dict(shell=True, universal_newlines=True)
        cp = subprocess.run(cmd, **bashopts)
        if cp.returncode != 0:
            # subprocess.run("sudo journalctl -xe", **kw)
            raise CommandError(f"{cmd} ended with return code {cp.returncode}")

    def handle(self, *args, **options):
        if len(args) > 0:
            raise CommandError("This command takes no arguments (got %r)" % args)

        using = options.get("database", DEFAULT_DB_ALIAS)
        dbname = settings.DATABASES[using]["NAME"]
        interactive = options.get("interactive")
        if interactive:
            msg = f"WARNING: running this test can break your database ({dbname})."
            msg += "\nAre you sure?"
            if not confirm(msg, default=True):
                raise CommandError("User abort.")

        kwargs = dict()
        kwargs["interactive"] = False
        kwargs["verbosity"] = options.get("verbosity")
        tmpdir = settings.SITE.site_dir / "tmp"
        # call_command("prep", '--keepmedia', **kwargs)
        call_command("dump2py", '-o', tmpdir / "a", **kwargs)
        self.runcmd(f"python manage.py run {str(tmpdir / 'a' / 'restore.py')} -b")
        call_command("dump2py", '-o', tmpdir / "b", **kwargs)
        self.runcmd(f"diff {tmpdir / 'a'} {tmpdir / 'b'}")
        print(f"Successfully ran double-dump test in {tmpdir}.")
        # print(f"The double-dump test was successful, we can remove {tmpdir}.")
        # shutil.rmtree(tmpdir)
