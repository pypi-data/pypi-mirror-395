# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.html import E, tostring, format_html, mark_safe
from lino.core.utils import full_model_name as fmn
from lino.api import dd, rt, _

# PUBLIC_GROUP = "all_users_channel"


def get_updatables(instance, ar=None):
    data = {
        "actorIDs": instance.updatable_panels,
        "pk": instance.pk,
        "model": f"{fmn(instance)}",
        "mk": None, "master_model": None
    }
    if ar is None:
        return data
    if mi := ar.master_instance:
        data.update(mk=mi.pk, master_model=f"{fmn(mi)}")
    return data


class ChangeNotifier(dd.Model):

    class Meta:
        abstract = True

    def get_change_subject(self, ar, cw):
        ctx = dict(user=ar.user, what=str(self))
        if cw is None:
            return _("{user} created {what}").format(**ctx)
            # msg = _("has been created by {user}").format(**ctx)
            # return "{} {}".format(self, msg)
        if len(list(cw.get_updates())) == 0:
            return
        return _("{user} modified {what}").format(**ctx)
        # msg = _("has been modified by {user}").format(**ctx)
        # return "{} {}".format(self, msg)

    def get_change_body(self, ar, cw):
        ctx = dict(user=ar.user, what=ar.obj2htmls(self))
        if cw is None:
            html = format_html(_("{user} created {what}"), **ctx)
            html += self.get_change_info(ar, cw)
            html = format_html("<p>{}</p>.", html)
        else:
            items = list(cw.get_updates_html(["_user_cache"]))
            if len(items) == 0:
                return
            txt = format_html(_("{user} modified {what}"), **ctx)
            html = format_html("<p>{}:</p>", txt)
            html += tostring(E.ul(*items))
            html += self.get_change_info(ar, cw)
        return format_html("<div>{}</div>", html)

    def get_change_info(self, ar, cw):
        return mark_safe("")

    if dd.is_installed("notify"):

        def add_change_watcher(self, user):
            pass
            # raise NotImplementedError()

        def get_change_owner(self):
            return self

        def get_change_observers(self, ar=None):
            """
            Return or yield a list of `(user, mail_mode)` tuples who are
            observing changes on this object.  Returning an empty list
            means that nobody gets notified.

            Subclasses may override this. The default implementation
            forwards the question to the owner if the owner is
            ChangeNotifier and otherwise returns an empty list.
            """
            owner = self.get_change_owner()
            if owner is self:
                return []
            if not isinstance(owner, ChangeNotifier):
                return []
            return owner.get_change_observers(ar)

        def get_notify_options(self):
            return dict()

        def get_notify_message_type(self):
            return rt.models.notify.MessageTypes.change

        def after_ui_save(self, ar, cw):
            # Emits notification about the change to every observer.
            super().after_ui_save(ar, cw)
            if cw and not cw.is_dirty():
                return
            if (mt := self.get_notify_message_type()) is None:
                return

            def msg():
                with ar.override_attrs(permalink_uris=True):
                    subject = self.get_change_subject(ar, cw)
                    if not subject:
                        return None
                    body = self.get_change_body(ar, cw)
                    return (subject, body)

            owner = self.get_change_owner()
            kwargs = self.get_notify_options()
            rt.models.notify.Message.emit_notification(
                ar, owner, mt, msg, self.get_change_observers(ar), **kwargs)
