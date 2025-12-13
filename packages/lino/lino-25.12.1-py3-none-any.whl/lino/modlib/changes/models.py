# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger

import datetime

from django.conf import settings
from django.apps import apps

from django.db import models
from django.utils import timezone

from lino.api import dd, _
from lino.utils.html import E, tostring
from .utils import get_master

from lino.core.roles import SiteStaff
from lino.core.signals import pre_ui_delete, on_ui_created, on_ui_updated
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child, pre_remove_child
from lino.core.signals import receiver

from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField
from lino.modlib.users.mixins import UserAuthored


class ChangeTypes(dd.ChoiceList):
    # app_label = 'lino'
    verbose_name = _("Change Type")
    verbose_name_plural = _("Change Types")


add = ChangeTypes.add_item
add("C", _("Create"), "create")
add("U", _("Update"), "update")
add("D", _("Delete"), "delete")
add("R", _("Remove child"), "remove_child")
add("A", _("Add child"), "add_child")
add("M", _("Merge"), "merge")


class Change(UserAuthored):
    class Meta(object):
        verbose_name = _("Change")
        verbose_name_plural = _("Changes")

    # allow_cascaded_delete = 'master'
    quick_search_fields = "changed_fields diff"
    show_in_site_search = False

    time = models.DateTimeField()
    type = ChangeTypes.field()
    # if settings.SITE.user_model:
    #     user = dd.ForeignKey(settings.SITE.user_model)
    # else:
    #     user = dd.DummyField()

    object_type = dd.ForeignKey(
        "contenttypes.ContentType",
        blank=True,
        null=True,
        verbose_name=_("Object type"),
        related_name="changes_by_object",
    )
    object_id = GenericForeignKeyIdField(object_type, blank=True, null=True)
    object = GenericForeignKey(
        "object_type", "object_id", verbose_name=_("Object"))

    master_type = dd.ForeignKey(
        "contenttypes.ContentType",
        blank=True,
        null=True,
        verbose_name=_("Master type"),
        related_name="changes_by_master",
    )
    master_id = GenericForeignKeyIdField(master_type, blank=True, null=True)
    master = GenericForeignKey(
        "master_type", "master_id", verbose_name=_("Master"))

    diff = dd.RichTextField(_("Changes"), format="plain",
                            blank=True, editable=False)
    changed_fields = dd.CharField(_("Fields"), max_length=250, blank=True)

    def __str__(self):
        # ~ return "#%s - %s" % (self.id,self.time)
        return "#%s" % self.id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # print("20240516", self, self.type, self.diff)


class Changes(dd.Table):
    param_object_type = dd.ForeignKey(
        "contenttypes.ContentType", verbose_name=_("Object type"), blank=True
    )
    parameters = {
        "change_type": ChangeTypes.field(force_selection=False, blank=True),
        "date": models.DateField(_("Only changes from"), blank=True),
        "object_type": param_object_type,
        "object_id": models.PositiveIntegerField("Object ID", blank=True),
    }
    # no longer needed because user is a simple parameter
    # if settings.SITE.user_model:
    #     parameters['user'] = dd.ForeignKey(
    #         settings.SITE.user_model,
    #         blank=True)

    required_roles = dd.login_required(SiteStaff)

    editable = False
    model = "changes.Change"
    order_by = ["-time"]

    detail_layout = """
    time user type master object id
    diff
    """

    params_layout = """
    date user change_type object_type object_id
    """

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        # print("20230620", ar.master_instance)
        qs = super().get_request_queryset(ar, **filter)
        if (pv := ar.param_values) is None:
            return qs
        if not isinstance(qs, list):
            if pv.change_type:
                qs = qs.filter(type=pv.change_type)
            if pv.date:
                qs = qs.filter(time__range=(
                    pv.date, pv.date + datetime.timedelta(1)))
            # if settings.SITE.user_model and ar.param_values.user:
            #     qs = qs.filter(user=ar.param_values.user)
            if pv.object_type:
                qs = qs.filter(object_type=pv.object_type)
            if pv.object_id:
                qs = qs.filter(object_id=pv.object_id)
            # print("20230620", qs.query)
        return qs


class ChangesByObject(Changes):
    required_roles = dd.login_required(SiteStaff)
    master_key = "object"
    column_names = "time user type changed_fields master master_type master_id *"


class ChangesByMaster(Changes):
    required_roles = dd.login_required()
    master_key = "master"
    column_names = "time user type changed_fields object *"


def log_change(type, request, master, obj, msg="", changed_fields=""):
    Change(
        type=type,
        time=dd.now(),
        master=master,
        user=request.user,
        object=obj,
        changed_fields=changed_fields,
        diff=msg,
    ).save()


remove_after = dd.plugins.changes.remove_after
if remove_after:

    from lino.modlib.linod.choicelists import schedule_daily

    @schedule_daily()
    def delete_older_changes(ar):
        days = datetime.timedelta(days=remove_after)
        # django.core.exceptions.FieldError: Cannot resolve keyword 'time_lt' into field. Choices are: changed_fields, diff, id, list_item, master, master_id, master_type, master_type_id, name_column, navigation_panel, object, object_id, object_type, object_type_id, overview, time, type, user, user_id, workflow_buttons
        qs = Change.objects.filter(time__lt=dd.now() - days)
        if qs.count() > 0:
            ar.logger.info(
                "Removing %d changes older than %d days.", qs.count(), remove_after
            )
            qs.delete()


@receiver(on_ui_updated)
def on_update(sender=None, watcher=None, request=None, **kw):
    """
    Log a change if there is a `change_watcher_spec`.
    `watcher` is a :class:`lino.core.diff.ChangeWatcher` instance.
    """
    master = get_master(watcher.watched)
    if master is None:
        # No master, nothing to log
        return

    cs = watcher.watched.change_watcher_spec
    changed_fields = ""
    if False:  # I tried a html version, but it doesn't help to make
        # things more end-user friendly. And it caused
        # problems when being rendered in a grid.
        changes = list(watcher.get_updates_html(cs.ignored_fields))
        if len(changes) == 0:
            msg = "(no changes)"
        elif len(changes) == 1:
            msg = tostring(changes[0])
        else:
            msg = tostring(E.ul(*changes))
    else:
        changes = []
        for k, old, new in watcher.get_updates(cs.ignored_fields):
            changed_fields += k + " "
            changes.append("%s : %s --> %s" %
                           (k, dd.obj2str(old), dd.obj2str(new)))
        if len(changes) == 0:
            msg = "(no changes)"
        elif len(changes) == 1:
            msg = changes[0]
        else:
            msg = "- " + ("\n- ".join(changes))
    log_change(
        ChangeTypes.update, request, master, watcher.watched, msg, changed_fields
    )


@receiver(pre_ui_delete)
def on_delete(sender=None, request=None, **kw):
    """Calls :func:`log_change` with `ChangeTypes.delete`.

    Note that you must call this before actually deleting the object, otherwise
    mysql (not sqlite) says ERROR: (1048, "Column 'object_id' cannot be null")

    """
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.delete, request, master,
               sender, dd.obj2str(sender, True))


@receiver(on_ui_created)
def on_ui_created(sender=None, request=None, **kw):
    """To be called when a new instance has actually been created and saved."""
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.create, request, master,
               sender, dd.obj2str(sender, True))


@receiver(pre_add_child)
def on_add_child(sender=None, request=None, child=None, **kw):
    master = get_master(sender)
    if master is None:
        return
    log_change(
        ChangeTypes.add_child, request, master, sender, dd.full_model_name(
            child)
    )


@receiver(pre_remove_child)
def on_remove_child(sender=None, request=None, child=None, **kw):
    master = get_master(sender)
    if master is None:
        return
    log_change(
        ChangeTypes.remove_child, request, master, sender, dd.full_model_name(
            child)
    )


@receiver(pre_merge)
def on_merge(sender=None, request=None, **kw):
    if request is None:
        return
    master = get_master(sender.obj)
    if master is None:
        return
    log_change(ChangeTypes.merge, request, master, sender.obj, sender.logmsg())


# @dd.receiver(dd.pre_analyze)
# def define_actions(sender, **kw):
#     for m in apps.get_models():
#         if (cs := m.change_watcher_spec) is not None:
#             # print("20240328", m)
#             if cs.master_key is None:
#                 m.define_action(show_changes=dd.ShowSlaveTable(
#                     ChangesByMaster, button_text='≅'))  # 2245 approximately equal to
#             else:
#                 m.define_action(show_changes=dd.ShowSlaveTable(
#
#                     ChangesByObject, button_text='≈'))  # 2248 almost equal to
