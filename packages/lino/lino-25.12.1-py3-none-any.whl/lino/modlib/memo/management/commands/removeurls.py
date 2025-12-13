# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Convert [url] memo commands in the text fields of this database into <a href>
tags.
"""

from click import confirm
from django.core.management.base import BaseCommand
from django.conf import settings
from lino.core.utils import full_model_name as fmn
from lino.modlib.memo.parser import Parser, split_name_rest
from lino.api import dd, rt

parser = Parser()


def url2html(ar, s, cmdname, mentions, context):
    url, text = split_name_rest(s)
    if text is None:
        text = url
    return '<a href="%s" target="_blank">%s</a>' % (url, text)


parser.register_command("url", url2html)


class Command(BaseCommand):
    help = __doc__

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

    def handle(self, *args, **options):

        batch = not options.get("interactive")

        settings.SITE.startup()

        for m in rt.models_by_base(dd.Model):
            if len(m._bleached_fields) == 0:
                continue
            print(f"Search for [url] memo commands in {fmn(m)}...")
            for obj in m.objects.all():
                for f in m._bleached_fields:
                    if getattr(f, "format") != "plain":
                        old = getattr(obj, f.name)
                        if old is None:
                            continue
                        new = parser.parse(old)
                        if new != old:
                            print(f"- {obj} {f} :")
                            print(f"- {old} -> {new}")
                            if batch or confirm("Update this ?", default=True):
                                setattr(obj, f.name, new)
                                obj.full_clean()
                                obj.save()
