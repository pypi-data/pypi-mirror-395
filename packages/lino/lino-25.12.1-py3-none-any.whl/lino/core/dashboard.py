# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the :class:`DashboardItem` class.

"""

# from django.conf import settings
# from lino.api import _
from lino.core.permissions import Permittable
from lino.core.requests import ActionRequest
from lino.core.atable import AbstractTable
# from lino.core.actions import ShowTable
from lino.utils.html import E, tostring, assert_safe
from django.utils.html import mark_safe


class DashboardItem(Permittable):
    """Base class for all dashboard items.

    .. attribute:: name

        The name used to reference this item in
        :attr:`Widget.item_name`.

    .. attribute:: width

        The width in percent of total available width.

    .. attribute:: min_count

        Hide this item if there are less than min_count rows.

    """

    width = None
    header_level = None
    min_count = None

    def __init__(self, name, header_level=2, min_count=1):
        self.name = name
        self.header_level = header_level
        self.min_count = min_count

    def render(self, ar, **kwargs):
        """Yield a list of html chunks."""
        return []

    def render_request(self, ar, sar, **kwargs):
        """
        Render the given table action
        request. `ar` is the incoming request (the one which displays
        the dashboard), `sar` is the table we want to show (a child of
        `ar`).

        This is a helper function for shared use by :class:`ActorItem`
        and :class:`RequestItem`.
        """
        assert ar.user is sar.user
        # T = sar.actor
        # print("20210112 render_request()", sar.actor, sar)
        if self.min_count is not None:
            if sar.get_total_count() < self.min_count:
                # print("20180212 render no rows in ", sar)
                return
        yield mark_safe('<div class="dashboard-item">')
        if self.header_level is not None:
            buttons = sar.plain_toolbar_buttons()
            # 20250713 Maybe add the ⏏ button already in plain_toolbar_buttons()
            # buttons.append(sar.open_in_own_window_button())
            elems = []
            for b in buttons:
                elems.append(b)
                elems.append(" ")
            yield tostring(E.h2(str(sar.actor.get_title_base(sar)), " ", *elems))

        assert sar.renderer is not None
        if isinstance(sar, ActionRequest):
            # TODO 20220930 until now, dashboard was always acting as if
            # display_mode was DISPLAY_MODE_GRID
            if issubclass(sar.actor, AbstractTable):
                # if isinstance(sar.bound_action.action, ShowTable):
                for e in sar.renderer.table2story(sar, **kwargs):
                    # assert_safe(tostring(e))
                    yield tostring(e)
            else:
                # example : courses.StatusReport in dashboard
                yield sar.renderer.show_story(
                    ar, sar.actor.get_story(None, ar), **kwargs)
                # for e in sar.renderer.show_story(
                #     ar, sar.actor.get_story(None, ar), **kwargs):
                #     # assert_safe(tostring(e))
                #     yield tostring(e)
        else:
            raise Exception("20240908 Cannot render {}".format(sar))
            # yield "Cannot render {}".format(sar)
        yield mark_safe("</div>")

    def serialize(self):
        return dict(name=self.name, header_level=self.header_level)

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}({self.name},header_level={self.header_level},min_count={self.min_count})"


class ActorItem(DashboardItem):
    """A dashboard item that simply renders a given actor.
    The actor should be a table, other usage is untested.

    Usage examples:
    - :mod:`lino_xl.lib.blogs`
    - :mod:`lino_book.projects.events`

    .. attribute:: header_level

        The header level.

    """

    def __init__(self, actor, **kwargs):
        self.actor = actor
        super().__init__(str(actor), **kwargs)

    def get_view_permission(self, user_type):
        # if settings.SITE.is_hidden_plugin(self.actor.app_label):
        if self.actor.abstract:
            return False
        return self.actor.default_action.get_view_permission(user_type)
        # rv = self.actor.default_action.get_view_permission(user_type)
        # print("20210112 get_view_permission", self.actor, rv)
        # return rv

    def get_story(self, ar):
        yield self.actor

    def render(self, ar, **kwargs):
        """Render this table to the dashboard.

        - Do nothing if there is no data.

        - If :attr:`header_level` is not None, add a header

        - Render the table itself by calling
          :meth:`lino.core.requests.BaseRequest.show`

        """

        # if ar.subst_user:
        #     raise(Exception("20230331 {}".format(ar.subst_user)))
        # from lino.core.atable import AbstractTable
        T = self.actor
        # if isinstance(T, AbstractTable):
        # , renderer=settings.SITE.kernel.default_renderer)
        sar = T.create_request(limit=T.preview_limit, parent=ar)
        # sar = ar.spawn(T, limit=T.preview_limit)
        # sar = ar.spawn_request(actor=T, limit=T.preview_limit)
        # raise Exception("20230331 {}".format(ar.subst_user))

        # print("20250714 render()", sar.limit)
        # print("20210112 render()", ar, sar, ar.get_user(), sar.get_user())

        for i in self.render_request(ar, sar, **kwargs):
            yield i

    def serialize(self):
        d = super().serialize()
        d.update(actor=self.actor.actor_id)
        return d


# class RequestItem(DashboardItem):
class RequestItem(ActorItem):
    """
    Experimentally used in `lino_book.projects.events`.
    """

    def __init__(self, sar, **kwargs):
        self.sar = sar
        super().__init__(sar.actor, **kwargs)

    def get_view_permission(self, user_type):
        return self.sar.get_permission()
        # rv = self.sar.get_permission()
        # print("20210112 get_view_permission", self.sar, rv)
        # return rv

    def get_story(self, ar):
        yield self.sar

    def render(self, ar, **kwargs):
        for i in self.render_request(ar, self.sar, **kwargs):
            yield i


# class CustomItem(DashboardItem):
#     """Won't work. Not used and not tested."""
#     def __init__(self, name, func, *args, **kwargs):
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         super(CustomItem, self).__init__(name)

#     def render(self, ar):
#         return self.func(ar, *self.args, **self.kwargs)
