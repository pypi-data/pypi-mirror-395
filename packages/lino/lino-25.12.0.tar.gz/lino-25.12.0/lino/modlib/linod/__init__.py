# Copyright 2022-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html
"""Defines ASGI runtime environment, log server, as well as background tasks.
See :doc:`/plugins/linod`.

"""

import re
from lino.api import ad, _

try:
    import daphne
    import channels
except ImportError:
    daphne = None


class Plugin(ad.Plugin):
    verbose_name = _("Lino daemon")
    use_channels = False
    background_sleep_time = 5  # in seconds
    daemon_user = "robin"  # TODO: find a better solution

    def on_plugins_loaded(self, site):
        assert self.site is site
        if self.use_channels:
            sd = site.django_settings
            # the dict that will be used to create settings
            cld = {}
            sd["CHANNEL_LAYERS"] = {"default": cld}
            sd["ASGI_APPLICATION"] = "lino.modlib.linod.routing.application"
            cld["BACKEND"] = "channels_redis.core.RedisChannelLayer"
            cld["CONFIG"] = {
                "hosts": [("localhost", 6379)],
                "channel_capacity": {
                    "http.request": 200,
                    "http.response!*": 10,
                    re.compile(r"^websocket.send\!.+"): 80,
                },
            }

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("linod.SystemTasks")

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("linod.Procedures")

    def get_needed_plugins(self):
        # We don't use needs_plugins because it depends on use_channels. We must
        # not install the plugin when the Python package isn't installed because
        # otherwise `pm install` fails with ModuleNotFoundError: No module named
        # 'daphne'.
        if self.use_channels and daphne is not None:
            yield "channels"
            yield "daphne"

    def get_requirements(self, site):
        if self.use_channels:
            yield "channels"
            yield "channels_redis"
            yield "daphne"

    def get_used_libs(self, html=None):
        if self.use_channels:
            import channels

            # if channels is None:
            #     version = self.site.not_found_msg
            # else:
            #     version = channels.__version__
            yield (
                "Channels",
                channels.__version__,
                "https://github.com/django/channels",
            )
