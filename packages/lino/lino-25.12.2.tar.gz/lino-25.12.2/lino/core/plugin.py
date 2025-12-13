# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import inspect
from os.path import join, dirname, isdir, abspath
from collections.abc import Iterable
from urllib.parse import urlencode
from lino.core.exceptions import ChangedAPI


class Plugin:
    verbose_name = None
    short_name = None
    needs_plugins = []
    needed_by = None
    extends_models = None
    ui_label = None
    ui_handle_attr_name = None
    menu_group = None
    media_base_url = None
    media_name = None
    url_prefix = None
    site_js_snippets = []
    support_async = False
    renderer = None
    hidden = False

    def __init__(self, site, app_label, app_name, app_module, needed_by, configs: dict):
        # site.logger.info("20140226 Plugin.__init__() %s",
        #                  app_label)
        assert not site._startup_done

        if hasattr(self, "on_site_startup"):
            raise ChangedAPI(
                "20240330 Plugin.on_site_startup() was renamed to "
                "Plugin.pre_site_startup()"
            )
        self.site = site
        self.app_name = app_name
        self.app_label = app_label
        self.app_module = app_module
        self.needed_by = needed_by
        if self.verbose_name is None:
            self.verbose_name = app_label.title()
        if self.short_name is None:
            self.short_name = self.verbose_name
        self.configure(**configs)
        self.on_init()
        # import pdb; pdb.set_trace()
        # super(Plugin, self).__init__()

    def is_hidden(self):
        return self.hidden

    def hide(self):
        if self.site._startup_done:
            raise Exception(
                "Tried to deactivate plugin {} after startup".format(self))
        self.hidden = True

    def configure(self, **kw):
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_needed_plugins(self):
        return self.needs_plugins

    def get_used_libs(self, html=None):
        return []

    def get_site_info(self, ar=None):
        return ""

    def on_init(self):
        pass

    def on_plugins_loaded(self, site):
        pass

    def pre_site_startup(self, site):
        pass

    def install_django_settings(self, site):
        pass

    def before_actors_discover(self):
        pass

    # def after_discover(self):
    #     """
    #     This is called exactly once during startup, when actors have been
    #     discovered. Needed by :mod:`lino.modlib.help`.
    #     """
    #     pass

    def post_site_startup(self, site):
        pass

    def get_migration_steps(self, sources):
        return []

    @classmethod
    def extends_from(cls):
        # for p in self.__class__.__bases__:
        for p in cls.__bases__:
            if issubclass(p, Plugin):
                return p
        # raise Exception("20140825 extends_from failed")

    @classmethod
    def get_subdir(cls, name):
        p = dirname(inspect.getfile(cls))
        p = abspath(join(p, name))
        if isdir(p):
            return p
        # print("20150331 %s : no directory %s" % (cls, p))

    def before_analyze(self):
        pass

    def on_ui_init(self, kernel):
        pass

    def __repr__(self):
        desc = self._get_desc()
        if desc:
            what = "{}({})".format(self.app_name, desc)
        else:
            what = self.app_name
        return "<{}.{} {}>".format(self.__module__, self.__class__.__name__, what)

    def __str__(self):
        # desc = self._get_desc()
        # if desc:
        #     return "{}({})".format(self.app_name, desc)
        return self.app_name

    def _get_desc(self):
        l = []
        if False:
            for k in ("media_name", "media_base_url", "extends_models"):
                v = getattr(self, k, None)
                if v:
                    l.append("{}={}".format(k, v))
        if self.needed_by:
            l.append("needed by {}".format(self.needed_by.app_name))
        if self.needs_plugins:
            # l.append('needs_plugins={}'.format([p.app_name for p in self.needs_plugins]))
            l.append("needs {}".format(self.needs_plugins))
        if len(l) == 0:
            return ""
        return ", ".join(l)

    def get_patterns(self):
        return []

    def get_requirements(self, site) -> Iterable[str]:
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        return []

    def get_body_lines(cls, site, request):
        return []

    def get_row_edit_lines(self, e, panel):
        return []

    def on_initdb(self, site, force=False, verbosity=1):
        pass

    def build_static_url(self, *parts, **kw):
        raise Exception("Renamed to build_lib_url")

    def build_lib_url(self, *parts, **kw):
        if self.media_base_url:
            url = self.media_base_url + "/".join(parts)
            if len(kw):
                url += "?" + urlencode(kw)
            return url
        return self.site.build_static_url(self.media_name, *parts, **kw)

    def buildurl(self, *args, **kw):
        if self.url_prefix:
            return self.site.buildurl(self.url_prefix, *args, **kw)
        return self.site.buildurl(*args, **kw)

    build_plain_url = buildurl

    def get_menu_group(self):
        if self.menu_group:
            mg = self.site.plugins.get(self.menu_group, None)
            if mg and not mg.hidden:
                return mg

        if self.needed_by is not None:
            return self.needed_by.get_menu_group()
        return self
        # mg = self
        # while mg.needed_by is not None:
        #     assert mg.needed_by is not mg
        #     mg = mg.needed_by  # .get_menu_group()
        # return mg

    def setup_user_prefs(self, up):
        pass

    def get_quicklinks(self):
        return []

    def setup_quicklinks(self, tb):
        pass

    def get_dashboard_items(self, user):
        return []

    # def setup_layout_element(self, el):
    #     pass

    def get_detail_url(self, ar, actor, pk, *args, **kw):
        from lino.core.renderer import TextRenderer

        if ar.renderer.__class__ is TextRenderer:
            return "Detail"  # many doctests depend on this
        parts = ["api"]
        if getattr(actor.model, "_meta", False):
            parts += [
                actor.model._meta.app_label,
                actor.model.get_default_table().__name__,
            ]
        else:
            parts += [actor.app_label, actor.__name__]
        parts.append(str(pk))
        parts += args
        return self.build_plain_url(*parts, **kw)
