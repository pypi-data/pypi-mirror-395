# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing :term:`notification messages <notification
message>`.

See :doc:`/specs/notify`.

"""

import re
from lino.api import ad, _
from lino.core.utils import is_devserver


class Plugin(ad.Plugin):
    verbose_name = _("Messages")
    needs_plugins = ["lino.modlib.users", "lino.modlib.memo", "lino.modlib.linod"]
    media_name = "js"

    use_push_api = False
    # Beware: The key pair used here are supposed to be used only in a
    # development environment and the keys are publicly available on the
    # internet and are not to be used in a production environment.
    vapid_private_key = "3W2nQ-o07lGlP8qs-STuUrTioCC7KxPVG7SNOSy2A4Y"
    vapid_public_key = "BCPMIR93gv_Di_AHL4i-zew3hB9I5ebPXihpKX44dgsxYxVymMZ79EK4_LIO7fN6d_UwUbz611Uiz7amJN1q2Wg"
    vapid_admin_email = "sharifmehedi24@gmail.com"

    remove_after = 2 * 7  # two weeks
    keep_unseen = True
    mark_seen_when_sent = False

    def get_requirements(self, site):
        if self.use_push_api:
            yield "pywebpush"

    def get_patterns(self):
        if self.use_push_api:
            from django.urls import re_path as url
            from . import views

            yield url(r"pushsubscription", views.PushSubscription.as_view())
            # yield url(r'testpush', views.TestPush.as_view())

    def get_js_includes(self, settings, language):
        if self.use_push_api:
            if settings.DEBUG:
                yield self.build_lib_url(("push.js/push.min.js"))
            else:
                yield self.build_lib_url(("push.js/push.js"))

    def setup_main_menu(self, site, user_type, m, ar=None):
        p = site.plugins.office
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action("notify.MyMessages")

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action("notify.AllMessages")

    def get_head_lines(self, site, request):
        if not self.use_push_api:
            return

        yield """\
            <script type="text/javascript">
            window.addEventListener('click', () => {
                Notification.requestPermission((status) => {
                    // console.log('Notification Permission Status: ', status);
                    if (status === 'granted' && !window.subscribed
                        && 'serviceWorker' in navigator) {
                        navigator.serviceWorker.ready.then((reg) => {
                            reg.pushManager.getSubscription().then((sub) => {
                                if (sub === null) {
                                    reg.pushManager.subscribe({
                                        userVisibleOnly: true,
                                        applicationServerKey: \"""" + self.vapid_public_key + """\",
                                    }).then((sub) => {
                                        fetch(`pushsubscription?sub=${
                                            JSON.stringify(sub)}&lang=${
                                            navigator.userLanguage
                                            || navigator.language}&userAgent=${
                                            navigator.userAgent}`);
                                        window.subscribed = true;
                                    });
                                }
                            });
                        });
                    }
                });
            });
            </script>"""

        # if not self.site.use_linod:
        #     return
        # from lino.utils.jsgen import py2js
        # user_name = "anony"
        # if request.user.is_authenticated:
        #     user_name = request.user.username
        site_title = site.title or "Lino-framework"
        if self.site.default_ui == "lino_react.react":
            js_to_add = """
        <script type="text/javascript">
            window.Lino = window.Lino || {}
            window.Lino.useWebSockets = true;
        </script>
            """
        else:
            # 2024-02-20  disabled the call to Ext.onReady() because I had the
            # feeling that it caused notable performance degradation.
            return

            js_to_add = """
        <script type="text/javascript">
        Ext.onReady(function() {
            // Note that the path doesn't matter for routing; any WebSocket
            // connection gets bumped over to WebSocket consumers
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = "/WS/";
            let webSocket;
            console.log("Connecting to " + ws_path);
            function connect() {
                webSocket = new WebSocket(ws_scheme + "://" + window.location.host + ws_path);
                webSocket.addEventListener('open', (event) => {
                    console.log(event);
                });
                webSocket.addEventListener('message', (event) => {
                    let data = JSON.parse(event.data);
                    if (data.type === "NOTIFICATION") {
                        let onGranted = () => console.log("onGranted");
                        let onDenied = () => console.log("onDenied");
                        // Ask for permission if it's not already granted
                        Push.Permission.request(onGranted, onDenied);
                        let {body, subject, action_url} = data;
                        try {
                            Push.create(subject, {
                                body: body,
                                icon: '/static/img/lino-logo.png',
                                onClick: function () {
                                    window.open(action_url);
                                }
                            });
                        }
                        catch (err) {
                            console.log(err.message);
                        }
                    }
                });
                webSocket.addEventListener('close', (event) => {
                    setTimeout(function() {
                      connect();
                    }, 1000);
                });
                webSocket.addEventListener('error', (event) => {
                    setTimeout(function() {
                      connect();
                    }, 1000);
                });
            }
            connect();
        });
        </script>
            """  # % (user_name, py2js(site_title))
        yield js_to_add

    # def get_dashboard_items(self, user):
    #     if user.is_authenticated:
    #         # yield ActorItem(
    #         #     self.models.notify.MyMessages, header_level=None)
    #         yield self.site.models.notify.MyMessages
