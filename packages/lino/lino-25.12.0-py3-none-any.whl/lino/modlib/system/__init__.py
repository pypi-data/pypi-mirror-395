# Copyright 2014-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines some "system features", especially the :class:`SiteConfig` model.
See :doc:`/specs/system`.

"""

from lino import ad, _
from django.utils.translation import gettext
from lino.utils.html import E, join_elems


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("System")
    needs_plugins = ["lino.modlib.printing"]

    def setup_config_menu(self, site, user_type, m, ar=None):
        system = m.add_menu(self.app_label, self.verbose_name)
        system.add_instance_action(site.site_config)

    def pre_site_startup(self, site):
        super().pre_site_startup(site)

        from lino.modlib.system.mixins import Lockable

        if len(list(Lockable.get_lockables())):

            def welcome_messages(ar):
                locked_rows = list(Lockable.get_lockable_rows(ar.get_user()))
                if len(locked_rows) > 0:
                    chunks = [gettext("You have a dangling edit lock on"), " "]
                    chunks += join_elems(
                        [ar.obj2html(obj) for obj in locked_rows], ", "
                    )
                    chunks.append(".")
                    yield E.div(*chunks)

            site.add_welcome_handler(welcome_messages)

    def get_requirements(self, site):
        yield "num2words"
