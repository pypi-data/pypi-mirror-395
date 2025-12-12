# -*- coding: UTF-8 -*-
# Copyright 2022-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.api import dd, rt, _

if dd.get_plugin_setting("help", "use_contacts"):

    from lino.api.shell import help, contacts
    from lino_xl.lib.contacts.models import PARTNER_NUMBERS_START_AT as PS

    def site_contact(type, company=None, **kwargs):
        return help.SiteContact(site_contact_type=type, company=company, **kwargs)

    def objects():
        yield site_contact("owner", settings.SITE.plugins.contacts.site_owner)
        yield site_contact("serveradmin", contacts.Company.objects.get(pk=PS+6))
        yield site_contact(
            "hotline",
            contact_person=contacts.Person.objects.get(pk=PS+13),
            **dd.babelkw("remark", _("Mon and Fri from 11:30 to 12:00")),
        )

else:

    def objects():
        return []
