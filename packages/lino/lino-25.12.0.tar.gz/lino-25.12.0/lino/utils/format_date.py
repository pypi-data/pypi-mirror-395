# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/topics/datetime`.
"""

import datetime
from babel.dates import format_date as babel_format_date

from django.conf import settings
from django.utils import translation
from django.template import defaultfilters
from django.contrib.humanize.templatetags.humanize import naturaltime as hnaturaltime

from lino.core.site import to_locale
from lino.utils import IncompleteDate


def naturaltime(v):
    if settings.SITE.the_demo_date is None:
        return hnaturaltime(v)
    delta = datetime.date.today() - settings.SITE.the_demo_date
    return hnaturaltime(v + delta)


def monthname(n):
    """
    Return the monthname for month # n in current language.
    """
    d = datetime.date(2013, n, 1)
    return defaultfilters.date(d, "F")


def fdmy(d):
    """
    "format date as month and year" :
    return the specified date as a localized string of type 'June 2011'.
    """
    if d is None:
        return ""
    return defaultfilters.date(d, "F Y")


def format_date(d, format="medium"):
    """Return a str expressing the given date `d`
    using
    `Babel's date formatting <https://babel.pocoo.org/en/latest/dates.html>`_
    and Django's current language.

    """
    if not d:
        return ""
    if isinstance(d, IncompleteDate):
        d = d.as_date()
    if not isinstance(d, datetime.date):
        if not isinstance(d, str):
            d = str(d)  # remove the "u" in Python 2
        raise Exception(str("Not a date: {0!r}").format(d))
    lng = translation.get_language()
    if lng is None:  # occured during syncdb
        lng = settings.SITE.languages[0].django_code
    loc = to_locale(lng)
    if loc == "en":
        loc = "en_UK"  # I hate US date format
    return babel_format_date(d, format=format, locale=loc)


def fdf(d):
    """Format date full."""
    return format_date(d, format="full")


def fdl(d):
    """Format date long."""
    return format_date(d, format="long")


def fdm(d):
    """Format date medium."""
    return format_date(d, format="medium")


def fds(d):
    """Format date short."""
    return format_date(d, format="short")


# backwards compatibility:
dtosl = fdf
dtosm = fdm
dtos = fds
dtomy = fdmy  # backward compat

# def day_and_month(d):
#     # this is not used. see also lino_xl.lib.cal.utils.day_and_month
#     return format_date(d, "dd. MMMM")


def day_and_month(d):
    if d is None:
        return "-"
    return defaultfilters.date(d, "d.m.")
    # return d.strftime("%d.%m.")


def day_and_weekday(d):
    if d is None:
        return "-"
    return defaultfilters.date(d, "D d.")
    # return d.strftime("%a%d")


def fts(t):
    # "format time short"
    return t.strftime(settings.SITE.time_format_strftime)


def fdtl(t):
    # "format datetime long"
    return "{} {}".format(
        t.strftime(settings.SITE.date_format_strftime),
        t.strftime(settings.SITE.time_format_strftime))


def fdtf(t):
    # "format datetime full"
    return "{} ({})".format(fdtl(t), naturaltime(t))
