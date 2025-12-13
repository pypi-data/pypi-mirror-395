# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
A selection of names to be used in tested documents as follows:

>>> from lino.api.doctest import *

This is by convention everything we want to have in the global namespace of a
tested document. It includes

- well-known Python standard modules like os, sys, datetime and collections.
- A variable :data:`test_client`

"""

import pytest
import os
import sys
import datetime
import collections
import six  # TODO: remove here and then run all doctests
import logging
import sqlparse
import json
import textwrap
import rstgen

from lino.api.shell import *
from lino.core.constants import *

from bs4 import BeautifulSoup
from pprint import pprint, pformat
from urllib.parse import urlencode
from rstgen.utils import unindent, rmu, sixprint
from rstgen import attrtable
from django.db import connection, reset_queries as reset_sql_queries
from django.test import Client
from django.utils.encoding import force_str
from django.utils import translation

from lino.mixins.clonable import Clonable
from lino.utils.fieldutils import get_fields, fields_help
from lino.core.boundaction import BoundAction
from lino.core.atable import AbstractTable
from lino.core.actions import Action
from django.db.models import Model
from lino.core.actions import ShowTable
from lino.core.menus import Menu
from lino.utils.html import html2text
from lino.utils import dbhash
from lino.core.utils import get_models
from lino.core.utils import full_model_name
from lino.core.utils import full_model_name as fmn
from lino.utils.diag import visible_for
from lino.sphinxcontrib.actordoc import menuselection_text
from lino import logger
from lino.core.menus import find_menu_item
from lino.core import constants
from lino.core import actors, kernel
from lino.utils.sql import sql_summary
from lino.utils import diag
from lino.utils.diag import analyzer
from lino.utils.html import E, tostring, to_rst
from lino.utils import i2d
from lino.utils import AttrDict

import django
django.setup()


# from rstgen import table, ul


# from lino.core.utils import PseudoRequest

test_client = Client()
"""An instance of :class:`django.test.Client`.

N.B. Naming it simply "client" caused conflict with a
:class:`lino_welfare.pcsw.models.Client`

"""

HttpQuery = collections.namedtuple(
    "HttpQuery", ["username", "url_base", "json_fields", "expected_rows", "kwargs"]
)

# settings.SITE.is_testing = True

ADMIN_FRONT_END = settings.SITE.kernel.editing_front_end


def get_json_dict(username, uri, an="detail", **kwargs):
    url = "/api/{0}?fmt=json&an={1}".format(uri, an)
    if kwargs:
        url += "&" + urlencode(kwargs, True)
    # for k, v in kwargs.items():
    #     url += "&{}={}".format(k, v)
    test_client.force_login(rt.login(username).user)
    res = test_client.get(url, REMOTE_USER=username)
    if res.status_code != 200:
        raise Exception(f"GET {url} got status code {res.status_code}")
    s = res.content.decode()
    try:
        return json.loads(s)
    except Exception as e:
        raise Exception(f"GET {url} got non-JSON response:\n{s}") from None


def get_json_soup(username, uri, fieldname, **kwargs):
    """Being authentified as `username`, perform a web request to `uri` of
    the test client.

    """
    d = get_json_dict(username, uri, **kwargs)
    html = d["data"][fieldname]
    return beautiful_soup(html)


def beautiful_soup(html):
    """Parse the given HTML into a BeautifulSoup object.

    This supports URIs that return a `delayed_value`.
    """
    if isinstance(html, dict):
        uri = "/" + html["delayed_value_url"]
        res = test_client.get(uri)
        assert res.status_code == 200
        d = json.loads(res.content.decode())
        html = d["data"]
        # raise Exception("20230710 {}".format(html))
    return BeautifulSoup(html, "lxml")


def post_json_dict(username, url, data, **extra):
    """Send a POST with given username, url and data. The client is
    expected to respond with a JSON encoded response. Parse the
    response's content (which is expected to contain a dict), convert
    this dict to an AttrDict before returning it.

    """
    test_client.force_login(rt.login(username).user)
    res = test_client.post(url, data, REMOTE_USER=username, **extra)
    if res.status_code != 200:
        raise Exception(
            "{} gave status code {} instead of 200".format(url, res.status_code)
        )
    return AttrDict(json.loads(res.content.decode()))


def check_json_result(response, expected_keys=None, msg=""):
    """Checks the result of response which is expected to return a
    JSON-encoded dictionary with the expected_keys.

    """
    # print("20150129 response is %r" % response.content)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                msg, response.status_code
            )
        )
    try:
        result = json.loads(response.content.decode())
    except ValueError as e:
        raise Exception("{0} in {1}".format(e, response.content))
    if expected_keys is not None:
        if set(result.keys()) != set(expected_keys.split()):
            raise Exception(
                "'{0}' != '{1}'".format(" ".join(list(result.keys())), expected_keys)
            )
    return result


def demo_get(username, url_base, json_fields=None, expected_rows=None, **kwargs):
    case = HttpQuery(username, url_base, json_fields, expected_rows, kwargs)
    # Django test client does not like future pseudo-unicode strings
    # See #870
    url = str(settings.SITE.buildurl(case.url_base, **case.kwargs))
    # print(20160329, url)
    if False:
        msg = "Using remote authentication, but no user credentials found."
        try:
            response = test_client.get(url)
            raise Exception("Expected '%s'" % msg)
        except Exception:
            pass
            # ~ self.tc.assertEqual(str(e),msg)
            # ~ if str(e) != msg:
            # ~ raise Exception("Expected %r but got %r" % (msg,str(e)))

    if False:
        # removed 20161202 because (1) it was relatively useless and
        # (2) caused a PermissionDenied warning
        response = test_client.get(url, REMOTE_USER=str("foo"))
        if response.status_code != 403:
            raise Exception(
                "Status code %s other than 403 for anonymous on GET %s"
                % (response.status_code, url)
            )
    ses = rt.login(username)
    test_client.force_login(ses.user)
    response = test_client.get(url, REMOTE_USER=username)
    # try:
    if True:
        what = "GET %s for user %s" % (url, ses.user)
        # user = settings.SITE.user_model.objects.get(
        #     username=case.username)
        result = check_json_result(response, case.json_fields, what)

        num = case.expected_rows
        if num is None:
            return
        if num == -1:
            print("{} got\n{}".format(what, pformat(result)))
            # print("got {} rows".format(result['count']))
        else:
            if not isinstance(num, tuple):
                num = [num]
            if result["count"] not in num:
                msg = "%s got %s rows instead of %s" % (url, result["count"], num)
                raise Exception(msg)

    # except Exception as e:
    #     print("%s:\n%s" % (url, e))
    #     raise


def show_menu_path(spec, language=None):
    """
    Print the menu path of the given actor or action.

    Deprecated.  You should rather use
    :meth:`lino.core.requests.BaseRequest.show_menu_path`, which
    automatically sets the language of the user and works for any user
    type.
    """
    user_type = rt.models.users.UserTypes.get_by_value("900")
    mi = user_type.find_menu_item(spec)
    if mi is None:
        raise Exception("Invalid spec {0}".format(spec))
    if language:
        with translation.override(language):
            print(menuselection_text(mi))
    else:
        print(menuselection_text(mi))

    # items = [mi]
    # p = mi.parent
    # while p:
    #     items.insert(0, p)
    #     p = p.parent
    # return " --> ".join([i.label for i in items])


def noblanklines(s):
    """Remove blank lines from output. This is used to increase
    readability when some expected output would otherweise contain
    disturbing `<BLANKLINE>` that are not relevant to the test
    itself.

    """
    return "\n".join([ln for ln in s.splitlines() if ln.strip()])


def show_choices(username, url, show_count=False):
    """Print the choices returned via web client.

    If `show_count` is `True`, show only the number of choices.

    """
    test_client.force_login(rt.login(username).user)
    response = test_client.get(url, REMOTE_USER=username)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                url, response.status_code
            )
        )

    result = json.loads(response.content.decode())
    for r in result["rows"]:
        print(r["text"])
        # print(r['value'], r['text'])
    if show_count:
        print("{} rows".format(result["count"]))


def show_workflow(actions, all=False, language=None):
    """
    Show the given actions as a table.  Usage example in
    :ref:`avanti.specs.cal`.

    """

    def doit():
        cells = []
        cols = [
            "Action name",
            "Verbose name",
            "Help text",
            "Target state",
            "Required states",
        ]  # , "Required roles"]
        for a in actions:
            ht = a.help_text or ""
            if ht or all:
                # required_roles = ' '.join(
                #     [str(r) for r in a.required_roles])
                cells.append(
                    [
                        a.action_name,
                        a.label,
                        unindent(ht),
                        a.target_state,
                        a.required_states or "",
                        # required_roles
                    ]
                )
        print(rstgen.table(cols, cells).strip())

    if language:
        with translation.override(language):
            return doit()
    return doit()


def show_fields(*args, **kwargs):
    print(fields_help(*args, **kwargs))


def show_fields_by_type(fldtype):
    """Print a list of all fields (in all models) that have the specified type."""
    from lino.core.utils import sorted_models_list

    items = []
    for model in sorted_models_list():
        flds = []
        for f in model._meta.fields:
            if isinstance(f, fldtype):
                name = f.name
                verbose_name = force_str(f.verbose_name).strip()
                txt = "{verbose_name} ({name})".format(**locals())
                flds.append(txt)
        if len(flds):
            txt = "{model} : {fields}".format(
                model=full_model_name(model), fields=", ".join(flds)
            )
            items.append(txt)
    print(rstgen.ul(items))


def show_columns(*args, **kwargs):
    """Like :func:`show_fields` but with `columns` defaulting to True."""
    kwargs.update(columns=True)
    return show_fields(*args, **kwargs)


def py2rst(x, doctestfmt=True):
    return diag.py2rst(x, doctestfmt)


# def show_dialog_actions():
#     return analyzer.show_dialog_actions(True)


# def show_db_overview():
#     print(analyzer.show_db_overview())


def walk_menu_items(username=None, severe=True):
    """

    Print a list of all :term:`application menu` items and, for items that open
    a :term:`data table`, the number of data rows the grid contains.

    """

    renderer = settings.SITE.kernel.default_renderer

    def doit(ar):
        if ar is None:
            user_type = None
        else:
            user_type = ar.user.user_type
            test_client.force_login(ar.user)
        mnu = settings.SITE.get_site_menu(user_type)
        items = []
        for mi in mnu.walk_items():
            if ba := mi.bound_action:
                item = menuselection_text(mi)
                # item += " ({})".format(mi)
                item += " : "
                if isinstance(ba.action, ShowTable) and not mi.params:
                    # url = settings.SITE.kernel.default_ui.renderer.request_handler()
                    # sar = ba.request(parent=ar)
                    if False:
                        url = ar.get_permalink(ba, mi.instance)
                    else:
                        mt = ba.actor
                        baseurl = "api/{}/{}".format(mt.app_label, mt.__name__)
                        kwargs = dict(fmt="json")
                        # url = settings.SITE.buildurl(baseurl, **kwargs)
                        url = ADMIN_FRONT_END.build_plain_url(baseurl, **kwargs)

                    try:
                        response = test_client.get(url)
                        # response = test_client.get(url,
                        #                            REMOTE_USER=str(username))
                        result = check_json_result(
                            response, None, f"GET {url} for user {username}")
                        item += str(result["count"])
                        # Also ask in display_mode "list" to cover assert_safe() bugs.
                        # But not e.g. UserRoles because it's not on a model and doesn't have a list mode
                        if mt.model:
                            kwargs[
                                constants.URL_PARAM_DISPLAY_MODE
                            ] = constants.DISPLAY_MODE_LIST
                            url = ADMIN_FRONT_END.build_plain_url(baseurl, **kwargs)
                            response = test_client.get(url)
                            result = check_json_result(
                                response, None, f"GET {url} for user {username}"
                            )
                            # if ar is not None:
                            #     sar = mt.request(parent=ar)
                            #     print(renderer.show_table(sar, display_mode="list"))
                            #     # sar.show(mt, display_mode="list")
                    except Exception as e:
                        if severe:
                            raise
                        else:
                            item += str(e)
                else:
                    item += "(not tested)"
                items.append(item)

        s = rstgen.ul(items)
        print(s)

    if settings.SITE.user_types_module:
        ar = rt.login(username)
        with translation.override(ar.user.language):
            doit(ar)
    else:
        doit(None)


def show_sql_queries():
    """
    Print the SQL queries that have been made since last call.

    Usage example: :ref:`specs.noi.sql`.
    """
    for qry in connection.queries:
        sql = qry["sql"].strip()
        print(sql.replace('"', ""))
    # reset_sql_queries()


def show_sql_summary(**kwargs):
    """Print a summary of the SQL queries that have been made since last
    call.

    Usage example: :ref:`specs.tera.sql`.

    """

    def func():
        for qry in connection.queries:
            try:
                yield "({time}) {sql};".format(**qry)
            except KeyError as e:
                yield "{} : {}".format(qry, e)

    sql_summary(func(), **kwargs)
    # reset_sql_queries()


def add_call_logger(owner, name):
    """Replace the callable named name on owner by a wrapper which
    additionally prints a message on each call.

    """
    func = getattr(owner, name)
    msg = "{}() on {} was called".format(name, owner)

    def w(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)

    setattr(owner, name, w)


def str2languages(txt):
    """
    Return a list of all translations for the given translatable text.
    """
    lst = []
    for lng in settings.SITE.languages:
        with translation.override(lng.django_code):
            lst.append(str(txt))
    return lst


def show_choicelist(cls):
    """
    Similar to :func:`rt.show`, but the `text` is shown in all
    languages instead of just the current language.
    """
    headers = ["value", "name"] + [lng.name for lng in settings.SITE.languages]
    rows = []
    for i in cls.get_list_items():
        row = [i.value, i.name] + str2languages(i.text)
        rows.append(row)
    print(rstgen.table(headers, rows))


def show_choicelists():
    """
    Show all the choicelists defined in this application.
    """
    headers = ["name", "#items", "preferred_width"] + [
        lng.name for lng in settings.SITE.languages
    ]
    rows = []
    for i in sorted(kernel.CHOICELISTS.values(), key=lambda s: str(s)):
        row = [str(i), len(i.choices), i.preferred_width] + str2languages(
            i.verbose_name_plural
        )
        rows.append(row)
    print(rstgen.table(headers, rows))


def show_parent_layouts():
    """
    Show all actors having a parent layout.
    """
    headers = ["actor", "is used in"]
    rows = []
    for a in actors.actors_list:
        if issubclass(a, AbstractTable) and a.parent_layout:
            parent = a.parent_layout._datasource
            row = [str(a), str(parent)]  # , parent.__module__]
            rows.append(row)
    print(rstgen.table(headers, sorted(rows)))


def show_permissions(*args):
    print(visible_for(*args))


def show_translations(things, fmt, languages=None):
    if languages is None:
        languages = [lng.name for lng in settings.SITE.languages]
    elif isinstance(languages, str):
        languages = languages.split()
    headers = ["Name"] + languages
    rows = []
    for thing in things:
        name, x = fmt(thing)
        cells = [name]
        for lng in languages:
            with translation.override(lng):
                x, txt = fmt(thing)
                cells.append(txt)
        rows.append(cells)
    print(rstgen.table(headers, rows))


def show_model_translations(*models, **kwargs):
    def fmt(m):
        return (
            full_model_name(m),
            "{0.verbose_name}\n{0.verbose_name_plural}".format(m._meta),
        )

    show_translations(models, fmt, **kwargs)


def show_field_translations(model, fieldnames=None, wrap_width=40, **kwargs):
    """
    Print a table with the verbose name and the help text of the specified
    fields in multiple languages.

    If `fieldnames` is not given, print all fields.

    If `languages` is not given, print all languages defined by the
    :term:`language distribution` of this :term:`Lino site`.

    """

    def fmt(fld):
        if getattr(fld, "help_text", None):
            txt = "{} : {}".format(fld.verbose_name, fld.help_text)
        else:
            txt = str(getattr(fld, "verbose_name", fld.__class__))
        txt = "\n".join(textwrap.wrap(txt, wrap_width))
        return (fld.name, txt)

    show_translations(get_fields(model, fieldnames), fmt, **kwargs)


def show_quick_search_fields(*args):
    for m in args:
        print(str(m._meta.verbose_name_plural))
        for fld in m.quick_search_fields:
            print("- {} ({})".format(fld.verbose_name, fld.name))


def pprint_json_string(s):
    """
    Used to doctest json values and have them be python 2/3 passable.
    :param s: json string

    """
    print(json.dumps(json.loads(s), indent=2, sort_keys=True, separators=(",", ": ")))


def show_dashboard(username, show_urls=False, **options):
    """Show the dashboard of the given user.

    Useful options:

    - show_urls=False
    - ignore_links=True

    For more options, see
    https://pypi.org/project/html2text/ and
    https://github.com/Alir3z4/html2text/blob/master/docs/usage.md

    This is currently not much used because the result is difficult to maintain.
    One reason for this is that :func:`naturaltime` (from
    :mod:`django.contrib.humanize.templatetags.humanize`) ignores
    :attr:`lino.core.site.Site.the_demo_date` and therefore produces results that
    depend on the current date/time.

    """
    renderer = settings.SITE.kernel.text_renderer
    ar = rt.login(username, renderer=renderer, show_urls=show_urls)
    html = settings.SITE.get_main_html(ar)
    print(html2text(html, **options).strip())


def menu2rst(mnu, level=1):
    """Recursive utility used by :func:`show_menu`."""
    if not isinstance(mnu, Menu):
        return str(mnu.label)

    has_submenus = False
    for i in mnu.items:
        if isinstance(i, Menu):
            has_submenus = True
    items = [menu2rst(mi, level + 1) for mi in mnu.items]
    if has_submenus:
        s = rstgen.ul(items).strip() + "\n"
        if mnu.label is not None:
            s = str(mnu.label) + " :\n\n" + s
    else:
        s = ", ".join(items)
        if mnu.label is not None:
            s = str(mnu.label) + " : " + s
    return s


def show_menu(username=None, language=None, stripped=True, level=1):
    """

    Print the main menu for the given user as a reStructuredText-formatted
    bullet list.

    :username: the username of the user to select. If this is not specified,
               anonymous user will be used.
    :language: explicitly select another language than that
               specified in the requesting user's :attr:`language
               <lino.modlib.users.models.User.language>` field.
    :stripped: remove lots of blanklines that are necessary for
               reStructuredText but disturbing in a doctest
               snippet.

    """
    if username is None:
        user_type = None
    else:
        ar = rt.login(username)
        user = ar.get_user()
        user_type = user.user_type
        if language is None:
            language = user.language
    with translation.override(language):
        mnu = settings.SITE.get_site_menu(user_type)
        s = menu2rst(mnu, level)
        if stripped:
            for ln in s.splitlines():
                if ln.strip():
                    print(ln)
        else:
            print(s)


def walk_store_fields(only_detail_fields=False):
    """

    Iterate over all the atomizers (:class:`lino.core.store.StoreField`) in this
    application.

    """
    # found = set()
    for a in actors.actors_list:
        if not a.is_abstract():
            if a.get_handle_name is not None:
                continue  # debts.PrintEntriesByBudget
            ah = a.get_handle()
            if not hasattr(ah, "store"):
                raise Exception("{} has no store".format(ah.actor))
            if only_detail_fields:
                lst = ah.store.detail_fields
            else:
                lst = ah.store.all_fields
            for sf in lst:
                # if sf.field in found:
                #     continue
                # found.add(sf.field)
                yield a, sf


def set_log_level(level):
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


def printsql(qs):
    """
    Print the SQL query of the given Django queryset.
    Uses sqlparse for formatting, after removing quotes around field names for
    readability.
    """
    sql = str(qs.query).replace('"', "")
    print(sqlparse.format(sql, reindent=True, keyword_case="upper"))


def show_change_watchers():
    """
    Show information about the change watchers that have been installed using
    :func:`lino.modlib.changes.utils.watch_changes`.
    """
    headers = ["model", "master_key", "ignored_fields"]
    rows = []
    for m in get_models():
        ws = m.change_watcher_spec
        if ws:
            rows.append(
                [fmn(m), ws.master_key, " ".join(sorted(ws.ignored_fields))]
            )
    print(rstgen.table(headers, rows, max_width=40))


def show_display_modes():
    """
    Show the availble display modes per actor.
    """
    dml = sorted(constants.DISPLAY_MODES - constants.BASIC_DISPLAY_MODES)
    headers = ["actor"]
    headers += dml
    rows = []
    for a in sorted(actors.actors_list, key=str):
        if not a.is_abstract():
            rows.append(
                [str(a)] + [
                    ("x" if dm in a.extra_display_modes else "")
                    for dm in dml]
            )
    print(rstgen.table(headers, rows))


def show_choosers():
    """
    Show the availble choosers per actor.
    """
    headers = ["field"]
    headers = ["field", "context_fields", "can_create_choice"]
    rows = []
    # for a in sorted(actors.actors_list, key=str):
    for m in sorted(get_models(), key=full_model_name):
        if (cd := getattr(m, "_choosers_dict", None)) is None:
            continue
        for fld in get_fields(m):
            if (c := cd.get(fld.name, None)):
                cf = ", ".join([cf.name for cf in c.context_fields])
                rows.append([
                    f"{full_model_name(m)}.{fld.name}",
                    str(cf),
                    str(c.can_create_choice)])
    print(rstgen.table(headers, rows))


def checkdb(m, num):
    """
    Raise an exception if the database doesn't contain the specified number of
    rows of the specified model.

    This is for usage in :xfile:`startup.py` scripts.

    """
    if m.objects.count() != num:
        raise Exception(
            f"Model {m} should have {num} rows but has {m.objects.count()}")


def show_clonables():
    """
    Print a list of all :class:`Clonable <lino.mixins.clonable.Clonable>`
    models, together with their related slaves, i.e. the data that will be
    cloned in cascade with their master.
    """
    items = []
    for m in get_models():
        if issubclass(m, Clonable):
            rels = []
            if (obj := m.objects.first()) is not None:
                new, related = obj.duplication_plan()
                for fk, qs in related:
                    rels.append(f"{fmn(qs.model)}.{fk.name}")
            if len(rels):
                x = ", ".join(rels)
                items.append(f"{fmn(m)} : {x}")
            else:
                items.append(fmn(m))
    items = sorted(items)
    print(rstgen.ul(items).strip())
