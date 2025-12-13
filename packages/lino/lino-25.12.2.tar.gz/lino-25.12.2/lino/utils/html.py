# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Some HTML utilities for Lino.
"""

import types
from lxml import etree
from etgen.html import E, to_rst, fromstring, iselement, join_elems, forcetext, lines2p
from etgen import html as xghtml
from html2text import HTML2Text
from django.utils.html import SafeString, mark_safe, escape
from django.utils.html import format_html  # some other modules import this from here

from lino.api import _
from lino.core import constants

SAFE_EMPTY = mark_safe("")
PLAIN_PAGE_LENGTH = 15


def html2text(html, **kwargs):
    """
    Convert the given HTML-formatted text into equivalent Markdown-structured
    text using `html2text <https://pypi.org/project/html2text/>`__.

    """

    text_maker = HTML2Text()
    text_maker.unicode_snob = True
    # text_maker.table_start = True
    text_maker.pad_tables = True
    for k, v in kwargs.items():
        setattr(text_maker, k, v)
    return text_maker.handle(html)


def py2html(obj, name):
    for n in name.split("."):
        obj = getattr(obj, n, "N/A")
    if callable(obj):
        obj = obj()
    if getattr(obj, "__iter__", False):
        obj = list(obj)
    return escape(str(obj))


def tostring(v, *args, **kw):
    """
    Render the given ElementTree element `v` as an escaped ("safe")
    :class:`str` containing HTML.

    If the value is not an ElementTree element, just convert it into a
    :class:`str`.

    If the value is a generator, list or tuple, convert each item individually
    and concatenate their HTML.

    This started as a copy of :func:`etgen.html.tostring` but uses Django's
    concept of safe strings.
    """
    if isinstance(v, SafeString):
        return v
    if isinstance(v, (types.GeneratorType, list, tuple)):
        return mark_safe("".join([tostring(x, *args, **kw) for x in v]))
    if etree.iselement(v):
        # kw.setdefault('method', 'html')
        kw.setdefault("encoding", "unicode")
        return mark_safe(etree.tostring(v, *args, **kw))
    return escape(str(v))


def assert_safe(s):
    """Raise an exception if the given text `s` is not a safe string."""
    if not isinstance(s, SafeString):
        raise Exception("%r is not a safe string" % s)
    # assert isinstance(s, SafeString)


class Grouper:

    def __init__(self, ar):
        self.ar = ar
        if ar.actor.group_by is None:
            return
        self.last_values = [None for f in ar.actor.group_by]

    def begin(self):
        if self.ar.actor.group_by is None:
            return SAFE_EMPTY
        return SAFE_EMPTY

    def stop(self):
        if self.ar.actor.group_by is None:
            return SAFE_EMPTY
        return SAFE_EMPTY

    def before_row(self, obj):
        if self.ar.actor.group_by is None:
            return SAFE_EMPTY
        self.current_values = [f(obj) for f in self.ar.actor.group_by]
        if self.current_values == self.last_values:
            return SAFE_EMPTY
        return self.ar.actor.before_group_change(self, obj)

    def after_row(self, obj):
        if self.ar.actor.group_by is None:
            return SAFE_EMPTY
        if self.current_values == self.last_values:
            return SAFE_EMPTY
        self.last_values = self.current_values
        return self.ar.actor.after_group_change(self, obj)


def buttons2pager(buttons, title=None):
    items = []
    if title:
        items.append(E.li(E.span(title)))
    for symbol, label, url in buttons:
        if url is None:
            items.append(E.li(E.span(symbol, **{"class": "page-link"}),
                              **{"class": "disabled"}))
        else:
            items.append(
                E.li(E.a(symbol, href=url, **{"class": "page-link"}),
                     **{"class": "page-item"}))
    # https://getbootstrap.com/docs/5.3/components/pagination/
    # return E.div(E.ul(*items), class_='pagination')
    return E.ul(*items, **{"class": "pagination pagination-sm"})


def ar2pager(ar, display_mode, initial_values={}):
    if ar.limit is None:
        ar.limit = PLAIN_PAGE_LENGTH
    pglen = ar.limit
    if ar.offset is None:
        page = 1
    else:
        """
        (assuming pglen is 5)
        offset page
        0      1
        5      2
        """
        page = ar.offset // pglen + 1

    buttons = []

    kw = dict(**initial_values)
    # kw = {}
    if pglen != PLAIN_PAGE_LENGTH:
        kw[constants.URL_PARAM_LIMIT] = pglen

    if page > 1:
        kw[constants.URL_PARAM_START] = pglen * (page - 2)
        prev_url = ar.get_request_url(**kw)
        kw[constants.URL_PARAM_START] = 0
        first_url = ar.get_request_url(**kw)
    else:
        prev_url = None
        first_url = None
    buttons.append(("<<", _("First page"), first_url))
    buttons.append(("<", _("Previous page"), prev_url))

    next_start = pglen * page
    if next_start < ar.get_total_count():
        kw[constants.URL_PARAM_START] = next_start
        next_url = ar.get_request_url(**kw)
        last_page = (ar.get_total_count() - 1) // pglen
        kw[constants.URL_PARAM_START] = pglen * last_page
        last_url = ar.get_request_url(**kw)
    else:
        next_url = None
        last_url = None
    buttons.append((">", _("Next page"), next_url))
    buttons.append((">>", _("Last page"), last_url))

    def add_dm(symbol, text, dm):
        if display_mode == dm:
            url = None
        else:
            kw.update({constants.URL_PARAM_DISPLAY_MODE: dm})
            # url = ar.get_request_url(**{constants.URL_PARAM_DISPLAY_MODE: dm})
            url = ar.get_request_url(**kw)
        buttons.append((symbol, text, url))

    add_dm("G", _("Grid"), constants.DISPLAY_MODE_HTML)
    add_dm("T", _("Tiles"), constants.DISPLAY_MODE_TILES)
    add_dm("L", _("List"), constants.DISPLAY_MODE_LIST)
    add_dm("S", _("Summary"), constants.DISPLAY_MODE_SUMMARY)

    return buttons2pager(buttons)


def table2html(ar, as_main=True):
    """Represent the given table request as an HTML table.

    `ar` is the request to be rendered, an instance of
    :class:`lino.core.requests.ActionRequest`.

    The returned HTML enclosed in a ``<div>`` tag and generated using
    :mod:`etgen.html`.

    If `as_main` is True, include additional elements such as a paging
    toolbar. (This argument is currently being ignored.)

    """
    # as_main = True
    t = xghtml.Table()
    t.attrib.update(**{"class": "table table-striped table-hover"})
    ar.dump2html(t, ar.sliced_data_iterator, header_links=as_main)
    if not as_main:
        url = ar.get_request_url() or "#"  # open in own window
        return E.div(
            E.div(
                E.div(
                    E.a(
                        E.span(**{"class": "glyphicon glyphicon-folder-open"}),
                        href=url,
                        style="margin-left: 4px;",
                        **{"class": "btn btn-default pull-right"},
                    ),
                    E.h5(str(ar.get_title()), style="display: inline-block;"),
                    **{"class": "panel-title"},
                ),
                **{"class": "panel-heading"},
            ),
            t.as_element(),
            style="display: inline-block;",
            **{"class": "panel panel-default"},
        )

    return E.div(ar2pager(ar), t.as_element())


def layout2html(ar, elem):
    wl = ar.bound_action.get_window_layout()
    if wl is None:
        raise Exception("{!r} has no window layout".format(ar.bound_action))
    # ~ print 20120901, wl.main
    lh = wl.get_layout_handle()

    items = list(lh.main.as_plain_html(ar, elem))
    # if navigator:
    #     items.insert(0, navigator)
    # ~ print tostring(E.div())
    # ~ if len(items) == 0: return ""
    return E.form(*items)
    # ~ print 20120901, lh.main.__html__(ar)


more_text = mark_safe("...")


def qs2summary(ar, objects, separator=", ", max_items=5, wraptpl="<p>{}</p>", **kw):
    """Render a collection of objects as a single paragraph.

    :param separator: separator to use between objects.

    :param max_items: don't include more than the specified number of items.

    :param wraptpl: the string template to use as outer paragraph tag. If this
                    is `None`, the returned string won't have a wrapper tag.

    """
    elems = mark_safe("")
    separator = mark_safe(separator)
    n = 0
    for i in objects:
        if n:
            elems += separator
        n += 1
        # if ar is None:
        #     elems += i.as_summary_row(None, **kw)
        # else:
        # s = ar.row_as_summary(i, **kw)
        # assert_safe(s)  # temporary 20240506
        # elems += s
        e = ar.row_as_summary(i, **kw)
        # print("20240613", repr(e))
        elems += tostring(e)
        if n >= max_items:
            elems += separator + more_text
            break
    # assert isinstance(elems, SafeString)  # temporary 20240506
    # assert not "<lt;" in elems
    if wraptpl is None:
        return elems
    return format_html(wraptpl, elems)
