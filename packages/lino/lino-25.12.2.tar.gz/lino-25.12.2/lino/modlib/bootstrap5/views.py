# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Views for `lino.modlib.bootstrap5`.

"""

from django import http
from django.conf import settings
from django.views.generic import View
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.contrib import auth
from lino.core import auth
# from lino.api import dd
from lino.core import constants
# from lino.core import auth
from lino.core.requests import BaseRequest
from lino.core.tables import AbstractTable
from lino.core.views import action_request
from lino.core.utils import navinfo
from lino.utils.html import E, tostring, buttons2pager, layout2html

raise Exception("No longer used since 20250826")

PLAIN_PAGE_LENGTH = 15

MENUS = dict()


def http_response(ar, tplname, context):
    "Deserves a docstring"
    u = ar.get_user()
    lang = get_language()
    k = (u.user_type, lang)
    menu = MENUS.get(k, None)
    if menu is None:
        menu = settings.SITE.get_site_menu(u.user_type)
        bs5 = settings.SITE.plugins.bootstrap5
        if False:  # 20150803 home button now in base.html
            assert bs5.renderer is not None
            url = bs5.build_plain_url()
            menu.add_url_button(url, label=_("Home"))
        e = bs5.renderer.show_menu(ar, menu)
        menu = tostring(e)
        MENUS[k] = menu
    context.update(menu=menu)
    context = ar.get_printable_context(**context)
    context["ar"] = ar
    context["memo"] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    template = env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context), content_type='text/html;charset="utf-8"'
    )

    return response


class List(View):
    """Render a list of records."""

    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        ar.renderer = settings.SITE.plugins.bootstrap5.renderer

        context = dict(
            title=ar.get_title(),
            heading=ar.get_title(),
        )

        # if isinstance(ar, ActionRequest):
        if ar .actor is not None and issubclass(ar.actor, AbstractTable):
            context.update(main=table2html(ar))
        else:
            context.update(main=layout2html(ar, None))

        context.update(ar=ar)
        return http_response(ar, ar.actor.list_html_template, context)


class Element(View):
    """Render a single record."""

    def get(self, request, app_label=None, actor=None, pk=None):
        # print(request, app_label, actor, pk)
        ar = action_request(app_label, actor, request, request.GET, False)
        ar.renderer = settings.SITE.plugins.bootstrap5.renderer

        navigator = None
        if pk and pk != "-99999" and pk != "-99998":
            elem = ar.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" % (ar.actor, pk))
                # ~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
            if ar.actor.show_detail_navigator:
                ni = navinfo(ar.data_iterator, elem)
                if ni:
                    # m = elem.__class__
                    buttons = []
                    # ~ buttons.append( ('*',_("Home"), '/' ))

                    buttons.append(("<<", _("First page"), ar.pk2url(ni["first"])))
                    buttons.append(("<", _("Previous page"), ar.pk2url(ni["prev"])))
                    buttons.append((">", _("Next page"), ar.pk2url(ni["next"])))
                    buttons.append((">>", _("Last page"), ar.pk2url(ni["last"])))

                    navigator = buttons2pager(buttons)
                else:
                    navigator = E.p("No navinfo")
        else:
            elem = None

        # main = E.div(
        #     E.div(E.div(E.h5(ar.get_title(),
        #              style="display: inline-block;"),
        #         class_="panel-title"),
        #         class_="panel-heading"),
        #     E.div(layout2html(ar, elem),class_="panel-body"), # Content
        #     class_="panel panel-default",
        #     # style="display: inline-block;"
        # )

        # raise Exception("20240404 "+str(elem))

        main = layout2html(ar, elem)

        # The `method="html"` argument isn't available in Python 2.6,
        # only 2.7.  It is useful to avoid side effects in case of
        # empty elements: the default method (xml) writes an empty
        # E.div() as "<div/>" while in HTML5 it must be "<div></div>"
        # (and the ending / is ignored).

        # ~ return tostring(main, method="html")
        # ~ return tostring(main)
        # return main

        context = dict(
            title=ar.get_action_title(),
            obj=elem,
            form=main,
            navigator=navigator,
        )
        # ~ template = web.jinja_env.get_template('detail.html')
        context.update(ar=ar)
        return http_response(ar, ar.actor.detail_html_template, context)


class Authenticate(View):
    def get(self, request, *args, **kw):
        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME)
        if action_name == "logout":
            username = request.session.pop("username", None)
            auth.logout(request)
            # request.user = settings.SITE.user_model.get_anonymous_user()
            # request.session.pop('password', None)
            # ~ username = request.session['username']
            # ~ del request.session['password']
            target = "/"
            return http.HttpResponseRedirect(target)

            # ar = BaseRequest(request)
            # ar.success("User %r logged out." % username)
            # return ar.renderer.render_action_response(ar)
        raise http.Http404()

    def post(self, request, *args, **kw):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        auth.login(request, user)
        target = "/"
        return http.HttpResponseRedirect(target)
        # ar = BaseRequest(request)
        # mw = auth.get_auth_middleware()
        # msg = mw.authenticate(username, password, request)
        # if msg:
        #     request.session.pop('username', None)
        #     ar.error(msg)
        # else:
        #     request.session['username'] = username
        #     # request.session['password'] = password
        #     # ar.user = request....
        #     ar.success(("Now logged in as %r" % username))
        #     # print "20150428 Now logged in as %r (%s)" % (username, user)
        # return ar.renderer.render_action_response(ar)


class Index(View):
    """
    Render the main page.
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kw):
        # raise Exception("20171122 {} {}".format(
        #     get_language(), settings.MIDDLEWARE_CLASSES))
        ui = settings.SITE.plugins.bootstrap5
        # print("20170607", request.user)
        # assert ui.renderer is not None
        ar = BaseRequest(
            # user=user,
            request=request,
            renderer=ui.renderer,
        )
        return index_response(ar)


def index_response(ar):
    ui = settings.SITE.plugins.bootstrap5
    main = settings.SITE.get_main_html(ar, front_end=ui)
    main = ui.renderer.html_text(main)
    context = dict(
        title=settings.SITE.title,
        main=main,
    )
    # if settings.SITE.user_model is None:
    #     user = auth.AnonymousUser.instance()
    # else:
    #     user = request.subst_user or request.user
    # context.update(ar=ar)
    return http_response(ar, "bootstrap5/index.html", context)
