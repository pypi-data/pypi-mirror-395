# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _


class EditRow(dd.Action):
    """
    Available on :class:`EditSafe <lino.modlib.system.mixins.EditSafe>` mixin.
    Runs when a user clicks the edit button.
    """

    select_rows = True
    action_name = "edit_row"
    react_icon_name = "pi-pencil"
    label = _("Edit")
    sort_index = 999

    def run_from_ui(self, ar, **kwargs):
        for row in ar.selected_rows:
            row.before_ui_edit(ar, **kwargs)
        ar.success(editing_mode=True)


class AbortEdit(dd.Action):
    """
    Available on :class:`EditSafe <lino.modlib.system.mixins.EditSafe>` mixin.
    Runs when a user clicks the abort button to discard changes in an editing window.
    """

    select_rows = True
    action_name = "abort_edit"
    react_icon_name = "pi-times"
    label = _("Abort")
    sort_index = 999

    def run_from_ui(self, ar, **kwargs):
        for row in ar.selected_rows:
            row.on_ui_abort(ar, **kwargs)
        ar.success(editing_mode=False)
