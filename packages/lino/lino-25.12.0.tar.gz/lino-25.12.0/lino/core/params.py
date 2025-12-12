# -*- coding: UTF-8 -*-
# Copyright 2010-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils.translation import gettext as _


class ParameterPanel:
    """
    A utility class for defining reusable definitions for
    :attr:`parameters <lino.core.actors.Actor.parameters>`.

    Subclassed e.g. by
    :class:`lino.mixins.periods.ObservedDateRange`.
    :class:`lino_xl.lib.accounting.PeriodRangeParameters`.
    """

    def __init__(self, **kw):
        self.fields = kw

    def get(self, *args, **kw):
        return self.fields.get(*args, **kw)

    def values(self, *args, **kw):
        return self.fields.values(*args, **kw)

    def keys(self, *args, **kw):
        return self.fields.keys(*args, **kw)

    def items(self, *args, **kw):
        return self.fields.items(*args, **kw)

    def update(self, *args, **kw):
        return self.fields.update(*args, **kw)

    def setdefault(self, *args, **kw):
        return self.fields.setdefault(*args, **kw)

    def __iter__(self, *args, **kw):
        return self.fields.__iter__(*args, **kw)

    def __len__(self, *args, **kw):
        return self.fields.__len__(*args, **kw)

    def __getitem__(self, *args, **kw):
        return self.fields.__getitem__(*args, **kw)

    def __setitem__(self, *args, **kw):
        return self.fields.__setitem__(*args, **kw)

    def get_title_tags(self, ar):
        """A hook for specifying title tags for the actor which uses this
        parameter panel.

        See :meth:`lino.core.actor.Actor.get_title_tags`.

        """
        return []

    def check_values(self, pv):
        """
        Return an error message if the specified parameter values are
        invalid.
        """
        pass


# from lino.core.utils import resolve_field
#
# class FieldRange(ParameterPanel):
#
#     def __init__(self, fldspec, **kwargs):
#         fld = resolve_field(fldspec)
#         self.start_field = dbfield2params_field(fld)
#         self.end_field = dbfield2params_field(fld)


class Parametrizable:
    """
    Base class for both Actors and Actions.  See :doc:`/dev/parameters`.

    This is a pseudo-mixins that groups the common functionality for both actors
    and actions. It's not a real mixin because :class:`Actor` must override
    every method as a class method (because actors are class objects while
    actions are class instances).

    .. method:: FOO_choices

        For every parameter field named "FOO", if the action has a method
        called "FOO_choices" (which must be decorated by
        :func:`dd.chooser`), then this method will be installed as a
        chooser for this parameter field.
    """

    active_fields = None  # 20121006
    master_field = None
    known_values = None
    parameters = None
    params_layout = None
    params_panel_hidden = True
    params_panel_pos = "bottom"  # allowed values "top", "bottom", "left" and "right"
    use_detail_param_panel = False

    # _params_layout_class = NotImplementedError
    _field_actions = dict()

    def get_window_layout(self, actor):
        return self.params_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        if wl is not None:
            return wl.window_size

    def check_params(self, pv):
        """Called when a request comes in."""
        if isinstance(self.parameters, ParameterPanel):
            self.parameters.check_values(pv)

    def hide_editing(cls, user_type):
        return False
