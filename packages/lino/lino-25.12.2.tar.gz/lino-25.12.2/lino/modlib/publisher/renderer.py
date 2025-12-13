# -*- coding: UTF-8 -*-
# Copyright 2023-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd
from lino.core.renderer import add_user_language
from lino.core.renderer import HtmlRenderer
from lino.core.kernel import is_candidate
from lino.modlib.publisher.mixins import Publishable


class Renderer(HtmlRenderer):

    tableattrs = {"class": "table table-hover table-striped table-condensed"}
    cellattrs = dict(align="left", valign="top")
    readonly = True

    can_auth = False

    def __init__(self, front_end):
        super().__init__(front_end)
        dr = front_end.site.kernel.default_renderer
        for k in ("row_action_button", "get_detail_url"):
            setattr(self, k, getattr(dr, k))

    def obj2url(self, ar, obj, **kwargs):
        if not isinstance(obj, Publishable):
            # print(f"20251023 {obj} is not publishable")
            return super().obj2url(ar, obj, **kwargs)
        # print(f"20251023 {obj} is publishable")
        # if ar.actor is None or not isinstance(obj, ar.actor.model):
        add_user_language(kwargs, ar)
        # if dd.plugins.publisher.with_trees:
        # if isinstance(obj, self.front_end.site.models.publisher.Page) and obj.ref == 'index':
        #     if isinstance(obj, self.front_end.site.models.publisher.Page) and obj.parent is None:
        #         if obj.publisher_tree.ref is not None:
        #             if obj.publisher_tree.ref == 'index':
        #                 return self.front_end.buildurl(**kwargs)
        #             return self.front_end.buildurl(obj.publisher_tree.ref, **kwargs)
        # if obj.ref:
        #     return self.front_end.buildurl(obj.ref, **kwargs)
        # a = ar.actor
        # if a and a.model is obj.__class__ and a._lino_publisher_location:
        #     # if not is_candidate(a):
        #     #     print(f"20251023 {a} is not a candidate")
        #     loc = a._lino_publisher_location
        # else:
        #     # print(f"20251019 the actor of {ar} is None")
        #     a = obj.__class__.get_default_table()
        #     loc = a._lino_publisher_location
        a = obj.__class__.get_default_table()
        loc = a._lino_publisher_location
        if loc is None:
            if (found := self.front_end.find_location_for(obj)):
                loc, a = found
            # leave the author of a blog entry unclickable when there is no
            # publisher view,
            # print(f"20251023 No location for {obj}")
            # # dd.logger.warning("No location for %s", obj.__class__)
            # return None
        # print(f"20251023 Location for {obj} is {repr(loc)}")
        if loc is not None:
            pk = obj.get_publisher_pk()
            if a.master is None:
                return self.front_end.buildurl(loc, pk, **kwargs)
            return self.front_end.buildurl(
                loc, str(ar.master_instance.pk), pk, **kwargs)
        # print(f"20251023 No location for {obj}")
        # if True:
        #     return None
        # return self.front_end.site.kernel.default_renderer.obj2url(ar, obj, **kwargs)

    def get_home_url(self, ar, *args, **kw):
        add_user_language(kw, ar)
        return self.front_end.build_plain_url(*args, **kw)

    def get_request_url(self, ar, *args, **kwargs):
        if len(ar.selected_rows) == 0:
            add_user_language(kwargs, ar)
            kernel = self.front_end.site.kernel
            if False:
                for loc, actor in self.front_end.locations:
                    if issubclass(ar.actor, actor):
                        return self.front_end.build_plain_url(loc, *args, **kwargs)
                return kernel.default_renderer.get_request_url(ar, *args, **kwargs)
            try:
                location = self.front_end.cls2loc[ar.actor]
            except KeyError:
                # print(f"20251006 No location for actor {ar.actor}")
                return kernel.default_renderer.get_request_url(ar, *args, **kwargs)
            if ar.actor.master is None:
                return self.front_end.build_plain_url(location, *args, **kwargs)
            else:
                mk = str(ar.master_instance.pk)
                return self.front_end.build_plain_url(location, mk, *args, **kwargs)
        obj = ar.selected_rows[0]
        return self.obj2url(ar, obj, **kwargs)
        # return obj.publisher_url(ar, **kwargs)

    def action_call(self, ar, bound_action, status):
        # a = bound_action.action
        # if a.opens_a_window or (a.parameters and not a.no_params_window):
        #     return "#"
        sar = bound_action.request_from(ar)
        return self.get_request_url(sar)
