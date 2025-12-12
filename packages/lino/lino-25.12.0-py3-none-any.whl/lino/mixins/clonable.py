# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"See :doc:`/dev/duplicate`."

from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from lino import logger
from lino.core import actions
from lino.core import model
from lino.core.diff import ChangeWatcher
# from lino.core.roles import Expert


class CloneRow(actions.Action):
    "See :doc:`/dev/duplicate`."

    # button_text = "⚇"  # \u2687 "white circle with two dots"
    button_text = "🗗"  # OVERLAP (U+1F5D7)
    label = _("Duplicate")
    # icon_name = 'arrow_divide'
    sort_index = 11
    show_in_workflow = False
    # readonly = False  # like ShowInsert. See docs/blog/2012/0726
    callable_from = "td"

    # required_roles = set([Expert])

    def get_help_text(self, ba):
        return format_lazy(
            _("Insert a new {} as a copy of this."),
            ba.actor.model._meta.verbose_name)

    def get_action_view_permission(self, actor, user_type):
        # the action is readonly because it doesn't write to the
        # current object, but since it does modify the database we
        # want to hide it for readonly users.
        if not actor.allow_create:
            return False
        if user_type:
            if user_type.readonly:
                return False
            # if not user_type.has_required_roles([Expert]):
            #     return False
        return super().get_action_view_permission(actor, user_type)

    def run_from_code(self, ar, **known_values):
        # CloneSequenced uses known_values to set seqno to seqno + 1
        obj = ar.selected_rows[0]
        new, related = obj.duplication_plan(**known_values)
        new.on_duplicate(ar, None)
        new.full_clean()
        new.save(force_insert=True)
        cw = ChangeWatcher(new)
        relcount = 0

        for fk, qs in related:
            for relobj in qs:
                relobj.pk = None  # causes Django to save a copy
                setattr(relobj, fk.name, new)
                relobj.on_duplicate(ar, new)
                relobj.save(force_insert=True)
                relcount += 1

        new.after_duplicate(ar, obj)

        if cw.is_dirty():
            new.full_clean()
            new.save()

        logger.info("%s has been duplicated to %s (%d related rows)",
                    obj, new, relcount)
        return new

    def run_from_ui(self, ar, **kw):

        if (msg := ar.actor.model.disable_create(ar)) is not None:
            ar.error(msg)
            return

        def ok(ar2):
            new = self.run_from_code(ar)
            kw = dict()
            # kw.update(refresh=True)
            kw.update(
                message=_("Duplicated %(old)s to %(new)s.") % dict(
                    old=obj, new=new)
            )
            # ~ kw.update(new_status=dict(record_id=new.pk))
            ar2.success(**kw)
            if ar.actor.detail_action is None or ar.actor.stay_in_grid:
                ar2.set_response(refresh_all=True)
            else:
                ar2.goto_instance(new)

        obj = ar.selected_rows[0]
        ar.confirm(
            ok, _("This will create a copy of {}.").format(
                obj), _("Are you sure?")
        )


class Clonable(model.Model):
    "See :doc:`/dev/duplicate`."

    class Meta:
        abstract = True

    clone_row = CloneRow()

    def duplication_plan(obj, **known_values):
        related = []
        for m, fk in obj._lino_ddh.fklist:
            # if fk.name in m.suppress_cascaded_copy:
            #     continue
            # print(fk.name, m.allow_cascaded_delete, m.allow_cascaded_copy, obj)
            # if fk.name in m.allow_cascaded_delete or fk.name in m.allow_cascaded_copy:
            if fk.name in m.allow_cascaded_copy:
                related.append((fk, m.objects.filter(**{fk.name: obj})))

        fields_list = obj._meta.concrete_fields
        if True:
            for f in fields_list:
                if not f.primary_key:
                    if f.name not in known_values:
                        known_values[f.name] = getattr(obj, f.name)
            new = obj.__class__(**known_values)
            # 20120704 create_instances causes fill_from_person() on a
            # CBSS request.
        else:
            # doesn't seem to want to work
            new = obj
            for f in fields_list:
                if f.primary_key:
                    # causes Django to consider this an unsaved instance
                    setattr(new, f.name, None)
        return new, related
