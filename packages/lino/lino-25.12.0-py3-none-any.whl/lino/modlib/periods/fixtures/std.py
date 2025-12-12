# -*- coding: UTF-8 -*-
# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from django.conf import settings
from lino.api import dd, rt, _

start_year = dd.get_plugin_setting("periods", "start_year", None)


def objects():
    StoredYear = rt.models.periods.StoredYear

    site = settings.SITE
    if site.the_demo_date is not None:
        if start_year > site.the_demo_date.year:
            raise Exception("plugins.periods.start_year is after the_demo_date")
    today = site.the_demo_date or datetime.date.today()
    for y in range(start_year, today.year + 6):
        yield StoredYear.get_or_create_from_date(datetime.date(y, today.month, today.day))
