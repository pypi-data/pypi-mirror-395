# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from django.db import models

from lino import mixins
from lino.api import dd, _
from lino.modlib.office.roles import OfficeStaff


class Language(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ["name"]

    preferred_foreignkey_width = 10

    id = models.CharField(max_length=3, primary_key=True)
    iso2 = models.CharField(max_length=2, blank=True)  # ,null=True)


class Languages(dd.Table):
    model = "languages.Language"
    required_roles = dd.login_required(OfficeStaff)
