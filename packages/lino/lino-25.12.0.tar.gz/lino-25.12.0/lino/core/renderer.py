# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines :class:`HtmlRenderer` and :class:`TextRenderer`.
"""

import os
from html import escape
import rstgen
# from pprint import pformat

from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.core.exceptions import BadRequest
# from django.utils.encoding import force_str
from django.utils.text import format_lazy
from django.utils import translation
from django.utils.translation import gettext as _
from django.utils.translation import get_language

from etgen.html2rst import RstTable
from etgen.utils import join_elems
# from lino import logger
from lino.utils import jsgen
from lino.utils import isiterable
from lino.utils.jsgen import py2js, js_code
from django.utils.html import mark_safe, format_html, SafeString
from lino.utils.html import E, tostring, iselement, forcetext, to_rst
from lino.core import constants
from lino.utils.html import html2text
from lino.core.fields import TableRow

from lino.core.menus import Menu, MenuItem
# from lino.utils.html import _html2rst as html2rst
# from lino.utils.html import html2rst

from lino.modlib.users.utils import get_user_profile, with_user_profile

from .dashboard import DashboardItem
from .views import json_response

# from . import elems

if False:
    from lino.utils.jscompressor import JSCompressor

    jscompress = JSCompressor().compress
else:

    def jscompress(s):
        return s


def text2rst(s):
    if isinstance(s, SafeString):
        return to_rst(s)
    return s


def add_user_language(kw, ar):
    if len(settings.SITE.languages) == 1:
        return
    if constants.URL_PARAM_USER_LANGUAGE in kw:
        return
    lang = get_language()

    # We set 'ul' only when it is not the default language. But

    # print('20170113 add_user_language', lang, ar.request.LANGUAGE_CODE)

    if False:
        # set it aways because it seems that it is rather difficult to
        # verify which will be the default language.
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)
        return
    u = ar.get_user()
    # print("20170113 add_user_language", u, lang)
    # ~ print 2013115, [li.django_code for li in settings.SITE.languages], settings.SITE.get_default_language(), lang, u.language
    if u and u.language and lang != u.language:
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)
    # ~ elif lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
    elif lang != settings.SITE.get_default_language():
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)

    # print("20170113 add_user_language", ar, kw, lang, u.language, settings.SITE.get_default_language())

    # ~ if len(settings.SITE.languages) > 1:
    # ~
    # ~ ul = rqdata.get(constants.URL_PARAM_USER_LANGUAGE,None)
    # ~ if ul:
    # ~ translation.activate(ul)
    # ~ request.LANGUAGE_CODE = translation.get_language()


class Renderer:
    """
    Base class for all Lino renderers.

    See :doc:`/dev/rendering`.
    """

    link_url = mark_safe("…")  # U+2026 Horizontal Ellipsis
    can_auth = False
    is_interactive = False
    readonly = False
    # not_implemented_js = "alert('Not implemented')"
    not_implemented_js = None
    extjs_version = None
    show_detail_links = True

    support_dashboard_layout = False
    """Don't show dashboard items when rendering :xfile:`admin_main.html`.

    """

    def __init__(self, front_end=None):
        # if not isinstance(plugin, Plugin):
        #     raise Exception("{} is not a Plugin".format(plugin))
        self.front_end = front_end

    def ar2js(self, ar, obj, **status):
        """
        Return the Javascript code that would run this `ar` on the client.
        """
        return self.not_implemented_js

    # def get_detail_action(self, ar, obj):
    # a = obj.get_detail_action(ar)

    # if a is not None:
    #     if ar is None or a.get_bound_action_permission(ar, obj, None):
    #         return a

    def add_help_text(self, kw, help_text, title, datasource, fieldname):
        pass

    def get_detail_url(self, *args, **kwargs):
        return self.front_end.get_detail_url(*args, **kwargs)

    def render_action_response(self, ar):
        """Builds a JSON response from response information stored in given
        ActionRequest.

        """
        return json_response(ar.response, ar.content_type)

    def get_action_params(self, ar, ba, obj, **kwargs):
        if ba.action.parameters:
            fv = ba.action.params_layout.params_store.pv2list(
                ar, ar.action_param_values
            )
            kwargs[constants.URL_PARAM_FIELD_VALUES] = fv
        return kwargs

    def build_js_cache(self, *args, **kwargs):
        if settings.SITE.is_installed('jinja'):
            def write(f):
                env = settings.SITE.plugins.jinja.renderer.jinja_env
                template = env.get_template("local.css")
                f.write(template.render(site=settings.SITE))
            return settings.SITE.kernel.make_cache_file(
                "cache/local.css", write, *args, **kwargs)
        return 0

    # def html_page(self, request, *args, **kw):
    #     return str(request)

    html_page_template = None

    def html_page(self, request, *args, **kw):
        """Return a string with the index page.  Content is mostly in the
        :xfile:`extjs/index.html` template.

        """
        user = request.user
        # print 20150427, user
        if True:  # user.user_type.level >= UserLevels.admin:
            if request.subst_user:
                user = request.subst_user

        def getit():
            if settings.SITE.developer_site_cache:
                self.build_js_cache(False)

            # Render template
            env = settings.SITE.plugins.jinja.renderer.jinja_env
            context = {
                "site": settings.SITE,
                "extjs": self.front_end,
                "ext_renderer": self,
                "py2js": py2js,  # TODO: Should be template filter
                "jsgen": jsgen,  # TODO: Should be in filters
                "language": translation.get_language(),
                "request": request,
                "user": user,  # Current user
            }
            context.update(kw)
            if self.html_page_template is None:
                # return pformat(context)
                raise BadRequest(f"{self} has no html_page_template")
            tpl = env.get_template(self.html_page_template)
            return tpl.render(context)

        return with_user_profile(user.user_type, getit)

    # def render_action_response(self, ar):
    #     """In a plain HTML UI this will return a full HTML index page, in
    #     ExtJS it will return JSON code.

    #     """
    #     raise NotImplementedError()


class HtmlRenderer(Renderer):
    """
    A Lino renderer for producing HTML content.
    """

    tableattrs = dict(cellspacing="3px", bgcolor="#eeeeee", width="100%")
    # tableattrs = dict(cellspacing="3px", bgcolor="#ffffff", width="100%")
    # cellattrs = {"class": "text-cell"}
    # cellattrs = dict(align="left", valign="top", bgcolor="#eeeeee")
    cellattrs = dict(align="left", valign="top", bgcolor="#ffffff")
    """The default attributes to be applied to every table cell.
    """

    def reload_js(self):
        """
        Returns a js string to go inside of a href in the dashboard for reloading the dashboard.
        """
        return ""

    row_classes_map = {}

    def js2url(self, js):
        """There is no Javascript here."""
        return js

    def href(self, url, text):
        return E.a(text, href=url)

    def show_table(self, *args, **kwargs):
        return mark_safe("".join([
            tostring(e) for e in self.table2story(*args, **kwargs)]))

    def show_detail(self, ar, obj, display_mode=None, **kwargs):
        """Show the window that is to be opened by `ar`.

        The output is currently gives no beautiful representation of the window,
        but at least it renders all content. This is the first intended purpose:
        to test whether things work.

        """
        from bs4 import BeautifulSoup
        import rstgen

        if display_mode == constants.DISPLAY_MODE_CARDS:
            layout = ar.actor.card_layout  # or ar.actor.list_layout
            lh = layout.get_layout_handle()
        else:
            lh = ar.bound_action.get_layout_handel()
            # layout = ar.actor.detail_layout
        # print("20210615 show_detail()", ar.bound_action, lh.layout)
        # return
        # obj = None
        # if ar.bound_action.action.select_rows:
        #     rows = ar.selected_rows
        # else:
        #     rows = ar.sliced_data_iterator
        #     # if len(ar.selected_rows) > 0:
        #     #     obj = ar.selected_rows[0]
        # chunks = []

        def tag2rst(t, level=1):
            items = []
            simple = True
            for c in t.children:
                s = c.string
                if s:
                    items.append(s)
                else:
                    simple = False
                    s = tag2rst(c)
                    if s:
                        items.append(s)
            if simple:
                return ", ".join(items)
            else:
                return rstgen.ul(items)

        with ar.get_user().user_type.context():
            html = tostring(lh.main.as_plain_html(ar, obj))
            soup = BeautifulSoup(html, "lxml")
            print(soup.get_text().strip())
            # print(tag2rst(soup.get_text()))
            # print(soup.prettify())
            # print(html)
            # print(tag2rst(soup.body))

            # for e in lh.walk():
            #     chunks.extend(e.as_plain_html(ar, obj))
            #     # for frag in e.as_plain_html(ar, obj):
            #     #     if frag is not None:
            #     #         chunks.append(frag)
            # for ch in chunks:
            #     print(tostring(ch))

    def html_text(self, html):
        """Render a chunk of HTML text.

        This does nothing, it just returns the given chunk of
        HTML. Except on ExtJS, where it wraps the chunk into an
        additional ``<div class="htmlText"></div>`` tag.

        """
        return html

    def table2story(
        self,
        ar,
        nosummary=False,
        stripped=True,
        header_level=None,
        display_mode=None,
        **kwargs
    ):
        """
        Returns an HTML element (or a safe html string) representing the given
        action request as a table. See :meth:`ar.show
        <lino.core.request.BaseRequest.show>`.

        Silently ignores the parameters `stripped` and `header_links`
        since for HTML these options have no meaning.
        """
        if display_mode is None:
            display_mode = ar.actor.get_display_mode()
            if nosummary and display_mode == constants.DISPLAY_MODE_SUMMARY:
                display_mode = constants.DISPLAY_MODE_GRID
        else:
            assert display_mode in ar.actor.extra_display_modes | constants.BASIC_DISPLAY_MODES
            if nosummary:
                raise Exception("Both nosummary and display_mode were specified")

        if display_mode == constants.DISPLAY_MODE_SUMMARY:
            yield ar.actor.get_table_summary(ar)
            return

        if header_level is not None:
            k = "h" + str(header_level)
            txt = escape(ar.get_title()) + " "
            for b in ar.plain_toolbar_buttons():
                txt += tostring(b) + " "
            yield format_html("<{}>{}</{}>", k, mark_safe(txt), k)

        if display_mode == constants.DISPLAY_MODE_LIST:
            yield ar.actor.get_table_as_list(ar.master_instance, ar)
            return

        elif display_mode == constants.DISPLAY_MODE_STORY:
            yield ar.actor.get_table_story(ar.master_instance, ar)
            return

        elif display_mode == constants.DISPLAY_MODE_TILES:
            yield ar.actor.get_table_as_tiles(ar.master_instance, ar)
            return

        yield ar.table2xhtml(**kwargs)

        # if show_toolbar:
        #     toolbar = ar.plain_toolbar_buttons()
        #     if len(toolbar):
        #         yield E.p(*toolbar)

    def request_handler(self, ar, *args, **kw):
        """
        Return a string with Javascript code that would run the given
        action request `ar`.
        """
        return self.not_implemented_js

    def instance_handler(self, ar, obj, ba, **status):
        """
        Return a string of Javascript code that would open a detail window
        on the given database object.
        """
        if ba is None:
            ba = obj.get_detail_action(ar)
        # ba = obj.__class__.get_default_table().detail_action
        if ba is not None:
            # print(f"20250319 instance_handler {ba} {status} {self.action_call}")
            status.update(record_id=obj.pk)
            return self.action_call(ar, ba, status)

    def href_to(self, ar, obj, text=None):
        h = self.obj2url(ar, obj)
        if h is None:
            # return escape(force_str(obj))
            return escape(str(obj))
        uri = self.js2url(h)
        # return self.href(uri, text or force_str(obj))
        return self.href(uri, text or str(obj))

    def href_to_request(self, ar, tar, text=None, **kw):
        """
        Return a string with an URL that would run the given target request
        `tar`."""
        if text is None:
            text = tar.get_title()

        if ar and ar.actor and ar.actor.hide_navigator:
            return text

        uri = self.js2url(self.request_handler(tar))
        return self.href_button_action(tar.bound_action, uri, text, **kw)

    def href_button_action(
        self, ba, url, text=None, title=None, icon_name=NOT_PROVIDED, **kw
    ):
        """

        Return an etree element of a ``<a href>`` tag which when clicked would
        execute the given bound action `ba`.

        """
        # changed 20130905 for "Must read eID card button"
        # but that caused icons to not appear in workflow_buttons.
        if icon_name is NOT_PROVIDED:
            icon_name = ba.action.icon_name
        return self.href_button(url, text, title, icon_name=icon_name, **kw)

    def href_button(self, url, text, title=None, icon_name=None, **kw):
        """Return an etree element of a ``<a href>`` tag to the given URL
        `url`.

        `text` is what goes between the ``<a>`` and the ``</a>``. This
        can be either a string or a tuple (or list) of strings (or
        etree elements).

        If `icon_name` is given, the `text` will be replaced by the
        corresponding image, which may vary depending on the renderer.

        `url` is what goes into the `href` part. If `url` is `None`,
        then we return just a ``<b>`` tag.

        """
        # logger.info('20121002 href_button %s', repr(text))
        if not isinstance(text, (tuple, list)):
            text = (text,)
        text = forcetext(text)
        if url is None:
            return E.b(*text)
        kw.update(href=url)
        if title:
            # Remember that Python 2.6 doesn't like if title is a Promise
            kw.update(title=str(title))

        return self.clickable_link(icon_name, *text, **kw)

    def clickable_link(self, icon_name, *text, **kwargs):
        if icon_name is not None:
            src = settings.SITE.build_static_url("images", "mjames", icon_name + ".png")
            img = E.img(src=src, alt=icon_name)
            if "style" not in kwargs:
                kwargs.update(style="vertical-align:-30%;")
            return E.a(img, **kwargs)
        if "style" not in kwargs:
            kwargs.update(style="text-decoration:none")
            # Experimental. Added 20150430
        return E.a(*text, **kwargs)

    def action_call(self, ar, ba, status):
        return None
        # raise NotImplementedError()

    def open_in_own_window_button(self, ar):
        """
        Return a button that opens the given table request in its own window.

        """
        return self.window_action_button(
            ar,
            ar.actor.default_action,
            label=settings.SITE.expand_panel_symbol,
            style="text-decoration:none;",
            title=_("Show this table in own window"))

    def window_action_button(self, ar, ba, status={}, label=None, title=None, **kw):
        """
        Render the given bound action `ba` as an action button.

        Returns a HTML tree element.

        """
        label = label or ba.get_button_label()
        # print("20240507 window_action_button()", self.action_call(ar, ba, status))
        url = self.js2url(self.action_call(ar, ba, status))
        # ~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(
            ba, url, str(label), title or ba.get_help_text(), **kw)

    def quick_add_buttons(self, ar):
        """Returns a HTML chunk that displays "quick add buttons" for the
        given :class:`action request
        <lino.core.request.ActionRequest>`: a button :guilabel:`[New]`
        followed possibly (if the request has rows) by a
        :guilabel:`[Show last]` and a :guilabel:`[Show all]` button.

        See also :srcref:`docs/tickets/56`.

        """
        buttons = []
        # btn = ar.insert_button(_("New"))
        # if btn is not None:
        sar = ar.actor.insert_action.request_from(ar)
        if sar.get_permission():
            btn = sar.ar2button(None, _("New"))
            buttons.append(btn)
            buttons.append(" ")
        n = ar.get_total_count()
        # ~ print 20120702, [o for o in ar]
        if n > 0:
            obj = ar.data_iterator[n - 1]
            st = ar.get_status()
            st.update(record_id=obj.pk)
            # ~ a = ar.actor.get_url_action('detail_action')
            a = ar.actor.detail_action
            buttons.append(
                self.window_action_button(
                    ar.request,
                    a,
                    st,
                    _("Show Last"),
                    icon_name="application_form",
                    title=_("Show the last record in a detail window"),
                )
            )
            buttons.append(" ")
            # ~ s += ' ' + self.window_action_button(
            # ~ ar.ah.actor.detail_action,after_show,_("Show Last"))
            # ~ s += ' ' + self.href_to_request(ar,"[%s]" % unicode(_("Show All")))
            buttons.append(
                self.href_to_request(
                    None,
                    ar,
                    _("Show All"),
                    icon_name="application_view_list",
                    title=_("Show all records in a table window"),
                )
            )
        # ~ return '<p>%s</p>' % s
        return E.p(*buttons)

    def get_home_url(self, *args, **kw):
        return settings.SITE.kernel.editing_front_end.build_plain_url(*args, **kw)

    def obj2url(self, ar, obj):
        ba = obj.get_detail_action(ar)
        if ba is not None:
            return self.get_detail_url(ar, ba.actor, obj.pk)

    def obj2html(self, ar, obj, text=None, **kwargs):
        """Return a html representation of a pointer to the given database
        object.

        Examples see :ref:`as_summary_item`.

        """
        if text is None:
            text = (obj.as_str(ar), )
        elif isinstance(text, str) or iselement(text):
            text = (text,)
        url = self.obj2url(ar, obj)
        if url is None:
            return E.em(*text)
        if not ar.show_urls:
            url = self.link_url
        return self.href_button(url, text, **kwargs)

    def obj2htmls(self, *args, **kwargs):
        return tostring(self.obj2html(*args, **kwargs))

    def quick_upload_buttons(self, rr):
        return "[?!]"

    def ar2button(self, ar, obj=None, label=None, title=None, **kwargs):
        ba = ar.bound_action
        label = label or ba.get_button_label()
        if ar._status is None:
            # if ar.subst_user:
            #     raise(Exception("20230331 {}".format(ar.subst_user)))
            ar._status = ar.get_status()
        if ar.show_urls:
            uri = ba.action.get_action_url(ar, obj)
        else:
            uri = self.link_url
        if uri and not uri.startswith("javascript:"):
            kwargs.update(target="_blank")
        return self.href_button_action(
            ba, uri, label, title or ba.get_help_text(), **kwargs)

    def menu_item_button(self, ar, mi, label=None, icon_name=None, **kwargs):
        """Render the given menu item `mi` as an action button.

        Returns a HTML tree element.
        Currently supports only window actions.

        """
        label = label or mi.label or mi.bound_action.get_button_label()
        # print("20240507 menu_item_button()", repr(mi), label)
        if mi.instance is not None:
            kwargs.update(status=dict(record_id=mi.instance.pk))
        return self.window_action_button(
            ar, mi.bound_action, label=label, icon_name=icon_name, **kwargs
        )

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        return "[%s]" % label

    def action_call_on_instance(self, obj, ar, ba, request_kwargs={}, **st):
        """Return a string with Javascript code that would run the given
        action `ba` on the given model instance `obj`. The second
        parameter (`ar`) is the calling action request.

        """
        return self.not_implemented_js

    def get_permalink(self, ar, ba, obj, **apv):
        # similar to ar2js() but to be used when permalink_uris is True
        # kwargs.update(self.get_action_params(ar, ba, None, **kwargs))
        kwargs = dict()
        if ba.action.parameters:
            fv = ba.action.params_layout.params_store.pv2list(ar, apv)
            kwargs[constants.URL_PARAM_FIELD_VALUES] = fv

        kwargs[constants.URL_PARAM_ACTION_NAME] = ba.action.action_name
        arguments = ["api", str(ba.actor.app_label), str(ba.actor.__name__)]
        if ba.action.select_rows:
            arguments.append(str(obj.pk))

        # if ar.hash_router:
        #     arguments.insert(0, '#')
        return settings.SITE.buildurl(*arguments, **kwargs)

    def row_action_button(
        self, obj, ar, ba, label=None, title=None, request_kwargs={}, **button_attrs
    ):
        """
        Return a HTML fragment that displays a button-like link
        which runs the bound action `ba` when clicked.

        This does not check user permissions (the caller is assumed to do this).

        """
        label = label or ba.get_button_label()
        if ar.show_urls:
            if ar.permalink_uris:
                apvs = request_kwargs.get("action_param_values", {})
                uri = ar.get_permalink(ba, obj, **apvs)  # "20210712"
            else:
                # TODO: why put obj to selected_rows and then pass it on?
                request_kwargs.update(selected_rows=[obj])
                js = self.action_call_on_instance(obj, ar, ba, request_kwargs)
                uri = self.js2url(js)
        else:
            uri = self.link_url
        return self.href_button_action(
            ba, uri, label, title or ba.get_help_text(), **button_attrs)

    def row_action_button_ar(
        self, obj, ar, label=None, title=None, request_kwargs={}, **kw
    ):
        """
        Return a HTML fragment that displays a button-like link
        which runs the action request `ar` when clicked.
        """
        ba = ar.bound_action
        label = label or ba.get_button_label()
        if ar.show_urls:
            js = self.action_call_on_instance(obj, ar, ba)
            uri = self.js2url(js)
        else:
            uri = self.link_url
        return self.href_button_action(
            ba, uri, label, title or ba.get_help_text(), **kw
        )

    def show_story(self, ar, story, stripped=True, **kwargs):
        """
        Render the given story and return it as a safe HTML string.

        Ignore `stripped` because it makes no sense in HTML.

        """
        from lino.core.actors import Actor
        from lino.core.tables import AbstractTable
        from lino.core.requests import ActionRequest
        # print(f"20240908 show_story {ar}")

        elems = []
        try:
            for item in forcetext(story):
                if isinstance(item, str):
                    # raise Exception(f"20240908 str {item}")
                    elems.append(item)
                elif iselement(item):
                    # 20200501 elems.append(item)
                    elems.append(tostring(item))
                elif isinstance(item, type) and issubclass(item, Actor):
                    ar = item.default_action.create_request(parent=ar)
                    # 20200501 elems.extend(self.table2story(ar, **kwargs))
                    elems += [tostring(e) for e in self.table2story(ar, **kwargs)]
                elif isinstance(item, ActionRequest):
                    assert item.renderer is not None
                    if issubclass(item.actor, AbstractTable):
                        # 20200501 elems.extend(self.table2story(item, **kwargs))
                        elems += [tostring(e)
                                  for e in self.table2story(item, **kwargs)]
                    else:
                        # example : courses.StatusReport in dashboard
                        # 20200501 elems.append(self.show_story(ar, item.actor.get_story(None, ar), **kwargs))
                        elems += [tostring(e)
                                  for e in self.show_story(
                                ar, item.actor.get_story(None, ar), **kwargs)]
                elif isinstance(item, DashboardItem):
                    elems.extend(item.render(ar, **kwargs))
                    # elems += [tostring(e) for e in item.render(ar, **kwargs)]
                    # for s in item.render(ar, **kwargs):
                    #     # s = tostring(e)
                    #     assert_safe(s)
                    #     elems.append(s)

                    # html = self.show_story(ar, item.render(ar), **kwargs)
                    # elems.append(html)
                    # # 20200501 if len(html):
                    # #     elems.append(E.div(
                    # #     html,
                    # #     CLASS="dashboard-item " + item.actor.actor_id.replace(".","-") if getattr(item, "actor", False) else ""
                    # if html: # should always be a string, never a list
                    #     if hasattr(item, "actor"):
                    #         css_class = "dashboard-item " + item.actor.actor_id.replace(".","-")
                    #     else:
                    #         css_class = ''
                    #     elems.append('<div class="{}">{}</div>'.format(css_class, html))

                elif isiterable(item):
                    # raise Exception("20240908")
                    e = self.show_story(ar, item, **kwargs)
                    elems.append(e)
                else:
                    raise Exception("Cannot handle story item %r" % item)
        except Warning as e:
            elems.append(tostring(str(e)))
        # print("20180907 show_story in {} : {}".format(ar.renderer, elems))
        # return E.div(*elems) if len(elems) else ""
        if len(elems):
            # for e in elems:
            #     assert_safe(e)
            # print(f"20240908 elems is {elems}")
            s = format_html("<div>{}</div>", mark_safe("".join(elems)))
            # assert_safe(s)
            # print(f"20240908 s is {s}")
            return s
        # raise Exception("20240908")
        return ""

    def show_menu(self, ar, mnu, level=1):
        """
        Render the given menu as an HTML etree element.

        Used by bootstrap5 front end.
        """
        if not isinstance(mnu, Menu):
            assert isinstance(mnu, MenuItem)
            if mnu.bound_action:
                sar = mnu.bound_action.actor.create_request(
                    action=mnu.bound_action,
                    user=ar.user,
                    subst_user=ar.subst_user,
                    requesting_panel=ar.requesting_panel,
                    renderer=self,
                    **mnu.params,
                )
                # print("20170113", sar)
                url = sar.get_request_url()
            else:
                url = mnu.href
            assert mnu.label is not None
            if url is None:
                return E.p()  # spacer
            return E.li(E.a(str(mnu.label), href=url, tabindex="-1"))

        items = [self.show_menu(ar, mi, level + 1) for mi in mnu.items]
        # ~ print 20120901, items
        if level == 1:
            return E.ul(*items, **{"class": "nav navbar-nav"})
        if mnu.label is None:
            raise Exception("%s has no label" % mnu)
        if level == 2:
            cl = "dropdown"
            menu_title = E.a(
                str(mnu.label),
                E.b(" ", **{"class": "caret"}),
                href="#",
                data_toggle="dropdown",
                **{"class": "dropdown-toggle"},
            )
        elif level == 3:
            menu_title = E.a(str(mnu.label), href="#")
            cl = "dropdown-submenu"
        else:
            raise Exception("Menu with more than three levels")
        return E.li(
            menu_title, E.ul(*items, **{"class": "dropdown-menu"}), **{"class": cl}
        )

    def goto_instance(self, ar, obj, **kw):
        pass


class TextRenderer(HtmlRenderer):
    """
    Renders things as reStructuredText to stdout.

    Used for doctests and console output.
    See also :class:`TestRenderer`.
    """

    user = None

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.user = None

    def get_request_url(self, ar, *args, **kw):
        if ar.show_urls:
            return super().get_request_url(ar, *args, **kw)
        return self.link_url
        # return None

    def obj2url(self, ar, obj):
        if ar.show_urls:
            return super().obj2url(ar, obj)
        return self.link_url
        # return None

    def get_detail_url(self, ar, *args, **kwargs):
        if ar.show_urls:
            return super().get_detail_url(ar, *args, **kwargs)
        return self.link_url

    #     # return str(actor)+"/"+str(pk)
    #     return "Detail"  # many doctests depend on this

    def action_call(self, ar, ba, status):
        """Returns the action name. This is not a valid link, but it's
        important to differentiate between clickable and non-clickable
        :meth:`obj2html` calls.

        """
        return self.link_url
        # return str(ba.action)
        # return ""

    def show_table(self, *args, **kwargs):
        for ln in self.table2story(*args, **kwargs):
            print(ln)

    def table2story(
        self,
        ar,
        column_names=None,
        header_level=None,
        header_links=None,
        nosummary=False,
        stripped=True,
        show_links=False,  # added 20241031
        display_mode=None,
        **kwargs
    ):
        """
        Render the given table request as reStructuredText to stdout.  See
        :meth:`ar.show <lino.core.request.BaseRequest.show>`.
        """
        if display_mode is None:
            display_mode = ar.actor.get_display_mode()
            # display_mode = constants.DISPLAY_MODE_GRID
            if nosummary and display_mode == constants.DISPLAY_MODE_SUMMARY:
                display_mode = constants.DISPLAY_MODE_GRID
        else:
            if display_mode not in ar.actor.extra_display_modes | constants.BASIC_DISPLAY_MODES:
                raise Exception(f"Invalid display mode {display_mode} for {ar.actor}")
            if nosummary:
                raise Exception("Both nosummary and display_mode were specified")
        # print(f"20240929 {nosummary} {display_mode} {ar}")
        # yield "20240506 {}".format(ar)
        # if str(ar.actor) == 'cal.EntriesByController':
        #     raise Exception(f"20251020 {ar.get_user()} {display_mode}")

        if display_mode == constants.DISPLAY_MODE_SUMMARY:
            s = to_rst(tostring(E.span(*join_elems(ar.plain_toolbar_buttons()))),
                       stripped=stripped)
            if s:
                s += " | "
            s += to_rst(ar.actor.get_table_summary(ar), stripped=stripped)
            if stripped:
                s = s.strip()
            yield s
            return

        if display_mode == constants.DISPLAY_MODE_CARDS:
            for row in ar.sliced_data_iterator:
                txt = ar.get_card_title(row)
                ar.show_detail(row, display_mode=display_mode)
            # rows = [ar.show_detail]
            return

        if display_mode == constants.DISPLAY_MODE_LIST:
            # s = to_rst(ar.actor.get_table_as_list(ar.master_instance, ar), stripped=stripped)
            cls = ar.actor
            items = []
            if cls.insert_action is not None and cls.editable:
                ir = cls.insert_action.request_from(ar)
                if ir.get_permission():
                    items.append("(+) {}".format(cls.insert_action.get_help_text()))
            # for i, obj in enumerate(ar.data_iterator):
            #     if i == cls.preview_limit:
            #         break
            for obj in ar.sliced_data_iterator:
                # if i == cls.preview_limit:
                #     break
                txt = ar.row_as_paragraph(obj).strip()
                txt = html2text(txt)
                # refuse showing more than one paragraph:
                # txt = txt.split('\n\n')[0]
                items.append(txt)
            yield rstgen.ul(items).strip()
            return

        if display_mode == constants.DISPLAY_MODE_TILES:
            prev = None
            for obj in ar.sliced_data_iterator:
                txt = obj.as_tile(ar, prev)
                txt = html2text(txt)
                yield txt.strip()
                prev = obj
            if prev is None:
                s = str(ar.no_data_text)
                if not stripped:
                    s = "\n" + s + "\n"
                yield s
            return

        # At this point, display_mode is one of story, grid or html.

        if header_level is not None:
            h = rstgen.header(header_level, ar.get_title())
            if stripped:
                h = h.strip()
            yield h
            # s = h + "\n" + s
            # s = tostring(E.h2(ar.get_title())) + s

        fields, headers, widths = ar.get_field_info(column_names)

        # if str(ar.actor) == "working.WorkedHours":
        #     yield "20200306 fields {}".format(headers)

        sums = [fld.zero for fld in fields]
        rows = []
        recno = 0
        for row in ar.sliced_data_iterator:
            recno += 1
            if ar.show_urls or show_links:
                rows.append([to_rst(x) for x in ar.row2html(recno, fields, row, sums)])
            else:
                # only for debugging:
                # for i, x in enumerate(ar.row2text(fields, row, [])):
                #     try:
                #         to_rst(x)
                #     except Exception as e:
                #         raise Exception("20240504 {} {!r}".format(fields[i], x))

                # 20240504 call to_rst() also here because displayfields might
                # return a SafeString
                rows.append([text2rst(x) for x in ar.row2text(fields, row, sums)])

        # if str(ar.actor) == "working.WorkedHours":
        #     yield "20200306 rows {}".format(rows)
        if len(rows) == 0:
            s = str(ar.no_data_text)
            if not stripped:
                s = "\n" + s + "\n"
            yield s
            return

        if not ar.actor.hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    # ~ print '20120914 zero?', repr(i)
                    has_sum = True
                    break
            if has_sum:
                rows.append([x for x in ar.sums2html(fields, sums)])

        t = RstTable(headers, **kwargs)
        yield t.to_rst(rows)

    def show_story(self, ar, story, stripped=True, **kwargs):
        """Render the given story as reStructuredText to stdout."""
        from lino.core.actors import Actor
        from lino.core.tables import AbstractTable
        from lino.core.requests import ActionRequest

        try:
            for item in forcetext(story):
                if iselement(item):
                    print(to_rst(item, stripped))
                elif isinstance(item, type) and issubclass(item, Actor):
                    ar = item.default_action.create_request(parent=ar)
                    self.show_table(ar, stripped=stripped, **kwargs)
                elif isinstance(item, DashboardItem):
                    self.show_story(ar, item.get_story(ar), stripped, **kwargs)
                elif isinstance(item, ActionRequest):
                    assert item.renderer is not None
                    if issubclass(item.actor, AbstractTable):
                        self.show_table(item, stripped=stripped, **kwargs)
                        # print(item.table2rst(*args, **kwargs))
                    else:
                        # example : courses.StatusReport in dashboard
                        self.show_story(ar, item.actor.get_story(None, ar), **kwargs)
                elif isiterable(item):
                    self.show_story(ar, item, stripped, **kwargs)
                    # for i in self.show_story(ar, item, *args, **kwargs):
                    #     print(i)
                else:
                    raise Exception("Cannot handle %r" % item)
        except Warning as e:
            print(e)

    def clickable_link(self, icon_name, *text, **kwargs):
        e = super().clickable_link(icon_name, *text, **kwargs)
        e.attrib.pop("style", None)
        return e

    # def clickable_link(self, icon_name, *text, **kwargs):
    #     if not self.show_urls:
    #         kwargs.update(href="#")
    #     return super().clickable_link(icon_name, *text, **kwargs)

    # def clickable_link(self, icon_name, *text, **kwargs):
    #     if self.show_urls:
    #         return super().clickable_link(icon_name, *text, **kwargs)
    #     if icon_name is not None:
    #         return E.em(icon_name)
    #     return E.em(*text)
    #
    # def clickable_link(self, icon_name, *text, **kwargs):
    #     if icon_name is not None:
    #         src = settings.SITE.build_static_url('images', 'mjames',
    #                                              icon_name + '.png')
    #         img = E.img(src=src, alt=icon_name)
    #         return E.a(img, **kwargs)
    #     return E.a(*text, **kwargs)


class TestRenderer(TextRenderer):
    """
    Like :class:`TextRenderer` but returns a string instead of
    printing to stdout.

    Experimentally used in :mod:`lino_book.projects.watch.tests`
    and :mod:`lino_book.projects.tera1.tests`.
    """

    def show_table(self, *args, **kwargs):
        return "\n".join(self.table2story(*args, **kwargs))


# class MailRenderer(HtmlRenderer):
#     """
#     A Lino renderer to be used when sending emails.
#
#     Subclassed by :class:`lino.modlib.jinja.renderer.JinjaRenderer`
#     """
#     def show_story(self, *args, **kwargs):
#         """Render the story and return it as a string."""
#         e = super(MailRenderer, self).show_story(*args, **kwargs)
#         return tostring(e)


class JsRenderer(HtmlRenderer):
    """
    A Lino renderer for HTML with JavaScript.
    Common base for
    :class:`lino_react.react.renderer.Renderer`,
    :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and
    :class:`lino_extjs6.extjs.ext_renderer.ExtRenderer`.
    """

    def reload_js(self):
        """
        Returns a js string to go inside of a href in the dashboard for reloading the dashboard.
        """
        return "Lino.viewport.refresh();"

    def check_visibility(self, ar):
        for obj in ar.selected_rows:
            try:
                ar.get_row_by_pk(obj.pk)
                return
            except obj.__class__.DoesNotExist:
                ar.set_response(
                    record_deleted=True,
                    message=_("Row {} is longer visible").format(obj))

    def goto_instance(self, ar, obj, detail_action=None, **kw):
        """Instruct the client to display a detail window on the given
        record.
        """
        # print("20250319 goto_instance", ar.get_user(), obj, detail_action, js)
        js = self.instance_handler(ar, obj, detail_action)
        kw.update(eval_js=js)
        ar.set_response(**kw)
        # print("20201230c", ar.actor, js)

    def js2url(self, js):
        if not js:
            return None
        js = escape(js, quote=False)
        return SafeString("javascript:" + js)

    def get_action_status(self, ar, ba, obj, **kw):
        kw.update(ar.get_status())
        if ba.action.parameters and not ba.action.keep_user_values:
            apv = ar.action_param_values
            if apv is None:
                apv = ba.action.action_param_defaults(ar, obj)
            ps = ba.action.params_layout.params_store
            kw.update(field_values=ps.pv2dict(ar, apv))
        if isinstance(obj, (models.Model, TableRow)):
            kw.update(record_id=obj.pk)
        else:
            kw.update(record_id=obj)
        return kw

    def ar2js(self, ar, obj, **status):
        """Implements :meth:`lino.core.renderer.HtmlRenderer.ar2js`."""
        rp = ar.requesting_panel
        ba = ar.bound_action

        if ba.action.is_window_action():
            # Window actions have been generated by
            # js_render_window_action(), so we just call its `run(`)
            # method:
            status.update(self.get_action_status(ar, ba, obj))
            return "Lino.%s.run(%s,%s)" % (ba.full_name(), py2js(rp), py2js(status))

        # It's a custom ajax action generated by
        # js_render_custom_action().

        # 20140429 `ar` is now None, see :ref:`welfare.tested.integ`
        if ba.action.select_rows:
            params = self.get_action_params(ar, ba, obj, **status)
            pk = obj.pk if isinstance(obj, models.Model) else obj
            return f"Lino.{ba.full_name()}({py2js(rp)},{py2js(ar.is_on_main_actor)},{py2js(pk)},{py2js(params)})"
        # assert obj is None
        # params = self.get_action_params(ar, ba, obj)
        # url = ar.get_request_url()

        url = self.front_end.build_plain_url(ar.actor.app_label, ar.actor.__name__)
        rqData = py2js(status.get("rqdata", None))
        xcallback = py2js(status.get("xcallback", None))
        base_params = ar.get_status().get(
            "base_params", None
        )  # dont use **status on ar.get_status() to not modify existing code.
        pp = "function() {return %s;}" % py2js(base_params)

        return "Lino.list_action_handler(%s,%s,%s,%s,%s,%s)()" % (
            py2js(url),
            py2js(ba.action.action_name),
            py2js(ba.action.http_method),
            pp,
            rqData,
            xcallback)

    def obj2url(self, ar, obj):
        ba = obj.get_detail_action(ar)
        if ba is None:
            return None
        if not ba.get_row_permission(ar, obj, None):
            # fixes #3857 (Lino links to a ticket and then says it doesn't exist)
            return None
        if ar.permalink_uris:
            return self.get_detail_url(ar, ba.actor, obj.pk)
        return self.js2url(self.instance_handler(ar, obj, ba))

    def add_help_text(self, kw, help_text, title, datasource, fieldname):
        if settings.SITE.use_quicktips:
            title = title or ""
            if settings.SITE.show_internal_field_names:
                ttt = format_lazy("{} ({}.{})", title, datasource, fieldname)
            else:
                ttt = title
            if help_text:
                ttt = format_lazy("{} : {}", ttt, help_text)
            if ttt:
                # kw.update(qtip=self.field.help_text)
                # kw.update(toolTipText=self.field.help_text)
                # kw.update(tooltip=self.field.help_text)
                kw.update(
                    listeners=dict(
                        render=js_code(
                            "Lino.quicktip_renderer(%s,%s)" % (py2js(title), py2js(ttt))
                        )
                    )
                )


class JsCacheRenderer(JsRenderer):
    """
    Mixin for:
    :class:`lino_react.react.renderer.Renderer`,
    :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and
    :class:`lino_extjs6.extjs.ext_renderer.ExtRenderer`.

    Includes linoweb.js cacheing functionality.

    """

    lino_web_template = "extjs/linoweb.js"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepare_layouts()

    def write_lino_js(self, f):
        """

        :param f: File object
        :return: 1
        """
        raise NotImplementedError("Need to implement a lino_web.js writing script")

        user_type = get_user_profile()

        context = dict(
            ext_renderer=self,
            site=settings.SITE,
            settings=settings,
            lino=lino,
            language=get_language(),
            # ext_requests=constants,
            constants=constants,
            extjs=self.plugin,  # 20171227
        )

        context.update(_=_)

        tpl = self.linolib_template()

        f.write(tpl.render(**context) + "\n")

        return 1

    def prepare_layouts(self):
        from lino.core import kernel

        self.actors_list = [
            rpt
            for rpt in kernel.master_tables
            + kernel.slave_tables
            + list(kernel.generic_slaves.values())
            + kernel.virtual_tables
            + kernel.frames_list
            + list(kernel.CHOICELISTS.values())
        ]

        # self.actors_list.extend(
        #     [a for a in kernel.CHOICELISTS.values()
        #      if settings.SITE.is_installed(a.app_label)])

        # don't generate JS for abstract actors
        self.actors_list = [a for a in self.actors_list if not a.is_abstract()]

        # Lino knows three types of form layouts:

        self.form_panels = set()
        self.param_panels = set()
        self.action_param_panels = set()
        self.other_panels = set()

        def add(res, collector, fl, formpanel_name, choice_name=None):
            # res: an actor class or action instance
            # collector: one of form_panels, param_panels or
            # action_param_panels
            # fl : a FormLayout
            # if str(fl).endswith("Given"):
            #     print("20210223 add", fl)
            # if str(res).endswith("MyCoursesGiven"):
            #     print("20210223 gonna add {} for {}".format(fl, res))
            if fl is None:
                return
            if fl._datasource is None:
                # raise Exception("20210223 {}".format(res))
                return  # 20130804

            if fl._datasource != res:
                fl.add_datasource(res)
                # if str(res).endswith("MyCoursesGiven"):
                #     print("20210223 added", fl._other_datasources)
                # if str(res).startswith('newcomers.AvailableCoaches'):
                #     logger.info("20150716 %s also needed by %s", fl, res)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py {2}: {0} != {1}".format(
                #         fl._datasource, res, fl))

            if False:
                try:
                    lh = fl.get_layout_handle()
                except Exception as e:
                    # logger.exception(e)
                    raise Exception(
                        "Could not define %s for %r: %s" % (formpanel_name, res, e)
                    )

                # lh.main.loosen_requirements(res)
                for e in lh.main.walk():
                    e.loosen_requirements(res)

            if fl not in collector:
                fl._formpanel_name = formpanel_name
                fl._url = res.actor_url()
                if choice_name:
                    fl.choice_name = choice_name
                collector.add(fl)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py collected {}".format(fl))

        for res in self.actors_list:
            add(res, self.form_panels, res.detail_layout, "%s.DetailFormPanel" % res)
            for name, fl in res.extra_layouts.items():
                add(
                    res,
                    self.form_panels,
                    fl,
                    "{}._{}_DetailFormPanel".format(res, name),
                    name,
                )
            add(res, self.form_panels, res.insert_layout, "%s.InsertFormPanel" % res)
            # if res.parameters is not None:
            add(res, self.param_panels, res.params_layout, "%s.ParamsPanel" % res)
            add(res, self.other_panels, res.card_layout, "%s.CardsPanel" % res)
            # add(res, self.other_panels, res.list_layout, "%s.ItemsPanel" % res)

            for ba in res.get_actions():
                if ba.action.parameters:
                    add(
                        res,
                        self.action_param_panels,
                        ba.action.params_layout,
                        "%s.%s_ActionFormPanel" % (res, ba.action.action_name),
                    )

    def lino_js_parts(self):
        user_type = get_user_profile()
        filename = "lino_"
        file_type = self.lino_web_template.rsplit(".")[-1]
        if user_type is not None:
            filename += user_type.value + "_"
        filename += get_language() + "." + file_type
        return ("cache", file_type, filename)

    def linolib_template(self):
        # env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        #     os.path.dirname(__file__)))
        # return env.get_template('linoweb.js')
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        return env.get_template(self.lino_web_template)

    def build_js_cache(self, force, verbosity=1):
        """Build the :term:`site cache` files for the current user type and the
        current language.  If the file exists and is up to date, don't
        generate it unless `force` is `True`.

        """
        fn = os.path.join(*self.lino_js_parts())

        def write(f):
            self.write_lino_js(f)

        count = settings.SITE.kernel.make_cache_file(fn, write, force, verbosity)

        count += super().build_js_cache(force, verbosity)

        return count
