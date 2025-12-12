# -*- coding: UTF-8 -*-
# Copyright 2015-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for handling checkdata messages.

See :doc:`/plugins/checkdata`.

.. autosummary::
   :toctree:

    roles
    fixtures.checkdata

"""

from lino.api import ad, _
from lino.core.exceptions import ChangedAPI


class Plugin(ad.Plugin):
    "The config descriptor for this plugin."

    verbose_name = _("Checkdata")
    needs_plugins = ["lino.modlib.users", "lino.modlib.gfks",
                     "lino.modlib.office", "lino.modlib.linod"]

    fix_in_background = True
    menu_group = "office"

    # plugin settings
    # responsible_user = None  # the username (a string)
    # """
    #
    # The :attr:`username <lino.modlib.users.User.username>`
    # of the **main checkdata responsible**, i.e. a designated
    # user who will be attributed to checkdata messages for which
    # no *specific responible* could be designated (returned by the
    # checker's :meth:`get_responsible_user
    # <lino.modlib.checkdata.Checker.get_responsible_user>`
    # method).
    #
    # The default value for this is `None`, except on a demo site
    # (i.e. which has :attr:`is_demo_site
    # <lino.core.site.Site.is_demo_site>` set to `True`) where it is
    # ``"'robin'``.
    #
    # """

    # _responsible_user = None  # the cached User object
    #
    # def get_responsible_user(self, checker, obj):
    #     if self.responsible_user is None:
    #         return None
    #     if self._responsible_user is None:
    #         User = self.site.models.users.User
    #         try:
    #             self._responsible_user = User.objects.get(
    #                 username=self.responsible_user)
    #         except User.DoesNotExist:
    #             msg = "Invalid username '{0}' in `responsible_user` "
    #             msg = msg.format(self.responsible_user)
    #             raise Exception(msg)
    #     return self._responsible_user

    def on_plugins_loaded(self, site):
        """Set :attr:`responsible_user` to ``"'robin'`` if this is a demo site
        (:attr:`is_demo_site <lino.core.site.Site.is_demo_site>`).

        """
        super().on_plugins_loaded(site)
        if hasattr(self, 'responsible_user'):
            raise ChangedAPI(
                "20250703 checkdata.responsible_user is replaced by users.demo_username")
        # if site.is_demo_site and self.responsible_user is None:
        #     self.configure(responsible_user="robin")

    def post_site_startup(self, site):
        super().post_site_startup(site)
        site.models.checkdata.Checkers.sort()

    def setup_main_menu(self, site, user_type, m, ar=None):
        g = self.get_menu_group()
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action("checkdata.MyMessages")

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        # g = self.get_menu_group()
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action("checkdata.Checkers")
        m.add_action("checkdata.AllMessages")
        # m.add_action('checkdata.Severities')
        # m.add_action('checkdata.Feedbacks')
