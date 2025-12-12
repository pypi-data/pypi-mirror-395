# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
This started as a copy of :mod:`lino.modlib.plain` and moved to the
version 3 of `Bootstrap <https://getbootstrap.com/>`_ CSS toolkit.

.. autosummary::
   :toctree:

    views
    renderer
    models
"""

from lino.api.ad import Plugin

PAGE_TITLE_TEMPLATE = '<p class="display-4">{}</p>'
# PAGE_TITLE_TEMPLATE = "<h1>{}</h1>"


class Plugin(Plugin):
    # ui_label = _("Bootstrap")
    # site_js_snippets = ['snippets/plain.js']
    needs_plugins = ["lino.modlib.jinja"]
    media_name = "bootstrap-5.3.7"
    # media_base_url = "http://maxcdn.bootstrapcdn.com/bootstrap/5.3.7/"

    # ui_handle_attr_name = "bootstrap5_handle"
    # url_prefix = "bs5"
    #
    # def on_ui_init(self, kernel):
    #     from .renderer import Renderer
    #
    #     self.renderer = Renderer(self)
    #     # ui.bs5_renderer = self.renderer
    #
    # def get_patterns(self):
    #     # from django.conf.urls import url
    #     from django.urls import re_path as url
    #     from . import views
    #
    #     rx = "^"
    #
    #     urls = [
    #         # url(rx + r'/?$', views.Index.as_view()),
    #         url(rx + r"$", views.Index.as_view()),
    #         url(rx + r"auth", views.Authenticate.as_view()),
    #         # NB app_label must be at least 3 chars long to avoid clash with
    #         # publisher patterns
    #         url(rx + r"(?P<app_label>\w\w\w+)/(?P<actor>\w+)$", views.List.as_view()),
    #         url(
    #             rx + r"(?P<app_label>\w\w\w+)/(?P<actor>\w+)/(?P<pk>.+)$",
    #             views.Element.as_view(),
    #         ),
    #     ]
    #     return urls

    def get_detail_url(self, ar, actor, pk, *args, **kw):
        return self.build_plain_url(
            actor.app_label, actor.__name__, str(pk), *args, **kw
        )

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Bootstrap", "5.3.7", "https://getbootstrap.com")
            # yield ("jQuery", '?', "http://...")

    # def get_index_view(self):
    #     from . import views
    #
    #     return views.Index.as_view()
