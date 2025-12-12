# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--pretty", "-p", action="store_true", default=False)

    def handle(self, *args, **options):
        site = settings.SITE

        configs = {"plugins": {}}

        for attr in dir(site):
            if (
                hasattr(site.__class__, attr)
                and isinstance(getattr(site.__class__, attr), property)
            ) or attr.startswith("_"):
                continue
            value = getattr(site, attr)
            if isinstance(value, Path):
                value = str(value)
            if not callable(value):
                try:
                    json.dumps({"data": value})
                except:
                    continue
                configs[attr] = value

        for pname, plugin in site.plugins.items():
            if plugin not in configs["plugins"]:
                configs["plugins"][pname] = {}

            for attr in dir(plugin):
                if (
                    hasattr(plugin.__class__, attr)
                    and isinstance(getattr(plugin.__class__, attr), property)
                ) or attr.startswith("_"):
                    continue
                value = getattr(plugin, attr)
                if isinstance(value, Path):
                    value = str(value)
                if not attr.startswith("_") and not callable(value):
                    try:
                        json.dumps({"data": value})
                    except:
                        continue
                    configs["plugins"][pname][attr] = value

        dump_kw = {}

        if options["pretty"]:
            dump_kw["indent"] = 4

        json.dump(configs, sys.stdout, **dump_kw)
