# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.core.management.base import BaseCommand
from rstgen.confparser import ConfigParser


class Command(BaseCommand):
    def handle(self, **options):
        cfgp = ConfigParser()
        ini_file = settings.SITE.project_dir / "lino.ini"
        cfgp.read(ini_file)

        def set_conf(gens):
            for conf in gens:
                if isinstance(conf, tuple):
                    if len(conf) != 3:
                        raise Exception
                    if not cfgp.has_option(*conf[:-1]):
                        if not cfgp.has_section(conf[0]):
                            cfgp.add_section(conf[0])
                        cfgp.stringify_set(*conf)
                else:
                    set_conf(conf)

        set_conf(settings.SITE.get_plugin_configs())

        with ini_file.open("w+") as f:
            cfgp.update_file(f)
