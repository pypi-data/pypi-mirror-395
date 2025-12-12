# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/plugins/changes`.

"""
from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Changes")

    needs_plugins = ["lino.modlib.users", "lino.modlib.gfks"]

    # remove_after = None
    remove_after = 30

    def setup_explorer_menu(config, site, user_type, m, ar=None):
        menu_group = site.plugins.system
        m = m.add_menu(menu_group.app_label, menu_group.verbose_name)
        m.add_action("changes.Changes")

    def before_actors_discover(self):
        super().before_actors_discover()
        from django.apps import apps
        from lino.core.actions import ShowSlaveTable

        for m in apps.get_models():
            if (cs := m.change_watcher_spec) is not None:
                # print("20240328", m)
                if cs.master_key is None:
                    m.define_action(
                        show_changes=ShowSlaveTable(
                            "changes.ChangesByMaster", button_text="≅"
                        )
                    )  # 2245 approximately equal to
                else:
                    m.define_action(
                        show_changes=ShowSlaveTable(
                            "changes.ChangesByObject", button_text="≈"
                        )
                    )  # 2248 almost equal to
