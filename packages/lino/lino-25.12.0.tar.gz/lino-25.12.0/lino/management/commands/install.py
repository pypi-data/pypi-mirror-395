# -*- coding: UTF-8 -*-
# Copyright 2019-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import sys
import subprocess
from click import confirm
from django.core.management.base import BaseCommand
from django.conf import settings


def runcmd(cmd, **kw):  # same code as in getlino.py
    """Run the cmd similar as os.system(), but stop when Ctrl-C."""
    # kw.update(stdout=subprocess.PIPE)
    # kw.update(stderr=subprocess.STDOUT)
    kw.update(shell=True)
    kw.update(universal_newlines=True)
    kw.update(check=True)
    # subprocess.check_output(cmd, **kw)
    subprocess.run(cmd, **kw)
    # os.system(cmd)


class Command(BaseCommand):
    help = "Run 'pip install --upgrade' for all Python packages required by this site."

    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_false",
            dest="interactive",
            default=True,
            help="Do not prompt for input of any kind.",
        )
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            dest="list",
            default=False,
            help="Just list the requirements, don't install them.",
        )

    def handle(self, *args, **options):
        reqs = set(settings.SITE.get_requirements())
        reqs = sorted(reqs)
        if options["list"]:
            print("\n".join(reqs))
            return
        if len(reqs) == 0:
            print("No requirements")
            return
        # cmd = "pip install --upgrade --trusted-host svn.forge.pallavi.be {}".format(' '.join(reqs))
        cmd = sys.executable + " -m pip install --upgrade pip {}".format(" ".join(reqs))
        if not options["interactive"] or confirm("{} ?".format(cmd), default=True):
            runcmd(cmd)
