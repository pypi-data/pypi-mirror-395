# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.api import dd


def objects():
    # logger.info("20150323 %s", settings.SITE.languages)
    SITE = settings.SITE
    User = SITE.user_model
    if User is None:
        return
    for lang in SITE.languages:
        if (SITE.hidden_languages is None
                or lang.django_code not in SITE.hidden_languages):
            kw = dd.plugins.users.get_root_user_fields(lang)
            if kw:
                u = User(**kw)
                if SITE.is_demo_site:
                    u.set_password(SITE.plugins.users.demo_password)
                yield u
