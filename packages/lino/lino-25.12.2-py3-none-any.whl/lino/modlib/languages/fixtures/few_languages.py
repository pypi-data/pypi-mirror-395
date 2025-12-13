# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds an arbitrary selection of a few languages.
"""

from lino.api import dd, rt, _


def objects():

    Language = rt.models.languages.Language

    def language(pk, iso2, name):
        kw = dict(iso2=iso2)
        kw.update(dd.str2kw("name", name))
        try:
            return Language.objects.get(id=pk)
        except Language.DoesNotExist:
            return Language(id=pk, **kw)

    yield language("ger", "de", _("German"))
    yield language("fre", "fr", _("French"))
    yield language("eng", "en", _("English"))
    yield language("dut", "nl", _("Dutch"))
    yield language("est", "et", _("Estonian"))
    yield language("pol", "pl", _("Polish"))
