# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See src/core/actions.rst

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext
from lino.core import constants
from lino.core import keyboard
# from lino.core.exceptions import ChangedAPI
from .utils import traverse_ddh_fklist
from .utils import navinfo
from .utils import obj2unicode
# from .action import Action


from .base import Action


class TableAction(Action):
    pass


class ShowTable(TableAction):
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True
    window_type = constants.WINDOW_TYPE_TABLE
    action_name = "grid"
    select_rows = False
    callable_from = None

    def get_label(self):
        return self.label or self.defining_actor.label

    def get_window_layout(self, actor):
        return None

    def get_window_size(self, actor):
        return actor.window_size


class ShowDetail(Action):
    help_text = _("Open a detail window on this record.")
    action_name = "detail"
    label = _("Detail")
    # icon_name = "application_form"
    ui5_icon_name = "sap-icon://detail-view"
    opens_a_window = True
    window_type = constants.WINDOW_TYPE_DETAIL
    show_in_toolbar = False
    show_in_workflow = False
    save_action_name = "submit_detail"
    callable_from = "t"
    sort_index = 20

    def __init__(self, dl, label=None, **kwargs):
        self.owner = dl
        super().__init__(label, **kwargs)

    # def get_help_text(self, ba):
    #     return _("Open a detail window on records of {}.").format(
    #         ba.actor.app_label)

    def attach_to_actor(self, actor, name):
        self.help_text = _(
            "Open a detail window on records of " + actor.app_label + "."
        )
        return super().attach_to_actor(actor, name)

    def get_required_roles(self, actor):
        if self.owner.required_roles is None:
            return actor.required_roles
        return self.owner.required_roles

    def get_window_layout(self, actor):
        # if actor.detail_layout is None:
        #     return actor.extra_layouts[0]
        return actor.detail_layout

    # def get_help_text(self, ba):
    #     if self.default_record_id is not None:
    #         return ba.actor.help_text
    #     return super().get_help_text(ba)

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        if wl is not None:
            return wl.window_size


class ShowEmptyTable(ShowDetail):

    use_param_panel = True
    action_name = "show"
    default_format = "html"
    icon_name = None
    # callable_from = 't'
    hide_navigator = True  # 20210509

    # def attach_to_actor(self, actor, name):
    #     self.label = actor.label
    #     return super().attach_to_actor(actor, name)

    def get_label(self):
        return self.label or self.defining_actor.label

    def as_bootstrap_html(self, ar):
        return super().as_bootstrap_html(ar, "-99998")


class ShowExtraDetail(ShowEmptyTable):
    # label = None
    # def get_label(self):
    #     return None

    def get_window_layout(self, actor):
        return self.owner


class ShowInsert(TableAction):
    save_action_name = "submit_insert"
    show_in_plain = True
    disable_primary_key = False
    default_record_id = -99999

    label = _("New")
    if True:  # settings.SITE.use_silk_icons:
        icon_name = "add"  # if action rendered as toolbar button
    else:
        # button_text = u"❏"  # 274F Lower right drop-shadowed white square
        # button_text = u"⊞"  # 229e SQUARED PLUS
        button_text = "⊕"  # 2295 circled plus

    ui5_icon_name = "sap-icon://add"
    # help_text = _("Insert a new record")

    show_in_workflow = False
    show_in_side_toolbar = True
    opens_a_window = True
    window_type = constants.WINDOW_TYPE_INSERT
    hide_navigator = True  # 20210509
    hide_top_toolbar = True  # 20210509
    sort_index = 10
    # required_roles = set([SiteUser])
    action_name = "insert"
    hotkey = keyboard.INSERT  # (ctrl=True)
    hide_virtual_fields = True
    readonly = False  # 20251019
    select_rows = False
    http_method = "POST"

    def get_help_text(self, ba):
        return format_lazy(
            _("Insert a new {}."), ba.actor.model._meta.verbose_name)
    # def attach_to_actor(self, owner, name):
    #     if owner.model is not None:
    #         self.help_text = format_lazy(
    #             _("Insert a new {}."), owner.model._meta.verbose_name
    #         )
    #     return super().attach_to_actor(owner, name)

    def get_action_title(self, ar):
        # return _("Insert into %s") % force_str(ar.get_title())
        if ar.actor.model is None:
            return _("Insert into %s") % force_str(ar.get_title())
        return format_lazy(_("Insert a new {}"), ar.actor.model._meta.verbose_name)

    def get_window_layout(self, actor):
        return self.params_layout or actor.insert_layout or actor.detail_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        if wl is not None:
            return wl.window_size

    def get_action_view_permission(self, actor, user_type):
        # The action is readonly because it doesn't write to the current object,
        # but we DO want to hide it for readonly users because it modifies the
        # database.
        if not actor.allow_create:
            return False
        if user_type and user_type.readonly:
            # if user_type is None or user_type.readonly:
            return False
        return super().get_action_view_permission(actor, user_type)

    def create_instance(self, ar):
        """
        Create a temporary instance that will not be saved, used only to
        build the button.
        """
        return ar.create_instance()

    def get_status(self, ar, **kw):
        kw = super().get_status(ar, **kw)
        if "record_id" in kw:
            return kw
        if "data_record" in kw:
            return kw
        if ar.ah.store is None:  # can happen when async
            return kw
        # raise Exception("20150218 %s" % ar.get_user())
        elem = self.create_instance(ar)
        rec = ar.elem2rec_insert(ar.ah, elem)
        kw.update(data_record=rec)
        return kw


# class UpdateRowAction(Action):
#     show_in_workflow = False
#     readonly = False
#     # required_roles = set([SiteUser])

# this is a first attempt to solve the "cannot use active fields in
# insert window" problem.  not yet ready for use. the idea is that
# active fields should not send a real "save" request (either POST or
# PUT) in the background but a "validate_form" request which creates a
# dummy instance from form content, calls it's full_clean() method to
# have other fields filled in, and then return the modified form
# content. Fails because the Record.phantom in ExtJS then still gets
# lost.


class ValidateForm(Action):
    # called by active_fields
    show_in_workflow = False
    action_name = "validate"
    readonly = False
    auto_save = False
    callable_from = None

    def run_from_ui(self, ar, **kwargs):
        elem = ar.create_instance_from_request(**kwargs)
        ar.ah.store.form2obj(ar, ar.rqdata, elem, False)
        elem.full_clean()
        ar.success()
        # ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
        ar.goto_instance(elem)


class SaveGridCell(Action):

    sort_index = 10
    show_in_workflow = False
    action_name = "grid_put"
    http_method = "PUT"
    readonly = False
    auto_save = False
    callable_from = None

    def run_from_ui(self, ar, **kw):
        # logger.info("20140423 SubmitDetail")
        elem = ar.selected_rows[0]
        elem.save_existing_instance(ar)
        ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])

        # We also need *either* `rows` (when this was called from a
        # Grid) *or* `goto_instance` (when this was called from a
        # form).


class SubmitDetail(SaveGridCell):

    sort_index = 100
    icon_name = "disk"
    help_text = _("Save changes in this form")
    label = _("Save")
    action_name = ShowDetail.save_action_name
    callable_from = "d"

    def run_from_ui(self, ar, **kw):
        # logger.info("20210213a SubmitDetail")
        for elem in ar.selected_rows:
            # logger.info("20210213b SubmitDetail %s", elem)
            elem.save_existing_instance(ar)
            if ar.renderer.front_end.app_label != "react":
                # No point in clos
                if ar.actor.stay_in_grid:
                    ar.close_window()
                else:
                    ar.goto_instance(elem)
            else:
                if len(ar.selected_rows) == 1:
                    ar.success(data_record=ar.elem2rec_detailed(elem))


class CreateRow(Action):

    sort_index = 10
    auto_save = False
    show_in_workflow = False
    readonly = False
    callable_from = None
    http_method = "POST"

    # select_rows = False
    def run_from_ui(self, ar, **kwargs):
        if (msg := ar.actor.model.disable_create(ar)) is not None:
            ar.error(msg)
            return
        elem = ar.create_instance_from_request(**kwargs)
        self.save_new_instance(ar, elem)

    def save_new_instance(self, ar, elem):
        elem.full_clean()
        elem.save_new_instance(ar)
        ar.success(_("%s has been created.") % obj2unicode(elem))

        # print(19062017, "Ticket 1910")
        if ar.actor.handle_uploaded_files is None:
            # The `rows` can contain complex strings which cause
            # decoding problems on the client when responding to a
            # file upload
            ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
            ar.set_response(navinfo=navinfo(ar.data_iterator, elem))

        # if ar.actor.stay_in_grid and ar.requesting_panel:
        if ar.actor.stay_in_grid:
            # do not open a detail window on the new instance
            ar.set_response(refresh_all=True)
            return

        ar.goto_instance(elem)
        # print(f"20250121d eval_js response for {ar} is {ar.response['eval_js']}")

        # No need to ask refresh_all since closing the window will
        # automatically refresh the underlying window.

    def save_new_instances(self, ar, elems):
        """Currently only used for file uploads."""
        for e in elems:
            e.save_new_instance(ar)

        ar.success(
            _("%s files have been uploaded: %s")
            % (len(elems), "\n".join([obj2unicode(elem) for elem in elems]))
        )

        # print(19062017, "Ticket 1910")
        if ar.actor.handle_uploaded_files is None:
            ar.set_response(rows=[ar.ah.store.row2list(ar, elems[0])])
            ar.set_response(navinfo=navinfo(ar.data_iterator, elems[0]))
        else:
            # Must set text/html for file uploads, otherwise the
            # browser adds a <PRE></PRE> tag around the AJAX response.
            ar.set_content_type("text/html")

        # if ar.actor.stay_in_grid and ar.requesting_panel:
        if ar.actor.stay_in_grid:
            # do not open a detail window on the new instance
            return

        ar.goto_instance(elems[0])

        # No need to ask refresh_all since closing the detail window will
        # automatically refresh the underlying window.


class SubmitInsert(CreateRow):
    label = _("Create")
    action_name = None  # 'post'
    help_text = _("Create the record and open a detail window on it")
    http_method = "POST"

    callable_from = "i"

    def run_from_ui(self, ar, **kwargs):
        # must set requesting_panel to None, otherwise javascript
        # button actions would try to refer the requesting panel which
        # is going to be closed (this disturbs at least in ticket
        # #219)
        if (msg := ar.actor.model.disable_create(ar)) is not None:
            ar.error(msg)
            return
        ar.requesting_panel = None

        if ar.actor.handle_uploaded_files is not None:
            # Must set text/html for file uploads, otherwise the
            # browser adds a <PRE></PRE> tag around the AJAX response.
            # 20210217 And this is true also in case of a ValidationError
            ar.set_content_type("text/html")

        # print("20201230 SubmitInsert.run_from_ui", ar)
        if (
            ar.actor.handle_uploaded_files is not None
            and len(ar.request.FILES.getlist("file")) > 1
        ):
            # Multiple uploads possible, note plural method names.
            elems = ar.create_instances_from_request(**kwargs)
            self.save_new_instances(ar, elems)
        else:
            elem = ar.create_instance_from_request(**kwargs)
            self.save_new_instance(ar, elem)

        ar.set_response(close_window=True)
        ar.set_response(refresh=True)
        # if settings.SITE.is_installed("react"):
        #     ar.goto_instance(elem)

        # ar.set_response(
        #     eval_js=ar.renderer.obj2url(ar, elem).replace('javascript:', '', 1)
        # )


# class SubmitInsertAndStay(SubmitInsert):
#     sort_index = 11
#     switch_to_detail = False
#     action_name = 'poststay'
#     label = _("Create without detail")
#     help_text = _("Don't open a detail window on the new record")


class ExplicitRefresh(Action):  # experimental 20170929
    label = _("Go")
    show_in_toolbar = False
    # js_handler = 'function(panel) {panel.refresh()}'
    js_handler = 'function(btn, evt) {console.log("20170928", this); this.refresh()}'
    # def run_from_ui(self, ar, **kw):
    #     ar.set_response(refresh_all=True)


class ShowSlaveTable(Action):

    TABLE2ACTION_ATTRS = (
        "icon_name",
        "react_icon_name",
        "_label",
        "sort_index",
        "required_roles",
        "button_text",
    )  # 'help_text',
    show_in_toolbar = True
    _defined_help_text = None

    def __init__(self, slave_table, help_text=None, **kw):
        self.slave_table = slave_table
        self.explicit_attribs = set(kw.keys())
        if help_text is not None:
            self._defined_help_text = help_text
        super().__init__(**kw)

    # Removed 20250521 because I don't see why it is needed
    # @classmethod
    # def get_actor_label(self):
    #     return self.get_label() or self.slave_table.label

    def attach_to_actor(self, actor, name):
        if isinstance(self.slave_table, str):
            T = settings.SITE.models.resolve(self.slave_table)
            if T is None:
                msg = "Invalid action {} on actor {!r}: no table named {}".format(
                    name, actor, self.slave_table
                )
                raise Exception(msg)
            self.slave_table = T

        for k in self.TABLE2ACTION_ATTRS:
            if k not in self.explicit_attribs:
                attr = getattr(self.slave_table, k, None)
                setattr(self, k, attr)
        # if self.help_text is None:
        #     self.help_text = self.slave_table.help_text
        return super().attach_to_actor(actor, name)

    def get_help_text(self, ba):
        return self._defined_help_text or self.slave_table.help_text

    # @property
    # def help_text(self):
    #     return self._defined_help_text or self.slave_table.help_text

    # @help_text.setter
    # def help_text(self, help_text):
    #     self._help_text = help_text

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        sar = ar.spawn(self.slave_table, master_instance=obj)
        js = ar.renderer.request_handler(sar)
        ar.set_response(eval_js=js)


class WrappedAction(Action):

    instance = None  # for Renderer.menu_item_button()
    show_in_toolbar = True
    callable_from = "d"

    WRAPPED_ATTRS = (
        "help_text",
        "icon_name",
        "react_icon_name",
        "label",
        "sort_index",
        "required_roles",
        "button_text",
        "window_type",
        "opens_a_window",
        "parameters",
        "no_params_window",
    )

    def __init__(self, bound_action, **kwargs):
        self.bound_action = bound_action
        if "action_name" not in kwargs and self.action_name is None:
            kwargs.update(
                action_name=(
                    str(bound_action.actor).replace(".", "_")
                    + "_"
                    + bound_action.action.action_name
                )
            )
        for k in self.WRAPPED_ATTRS:
            if k not in kwargs:
                kwargs[k] = getattr(bound_action.action, k)
        super().__init__(**kwargs)
        # print("20230501 WrappedAction()", kwargs)

    def get_required_roles(self, actor):
        # print(self.bound_action, actor.required_roles | self.bound_action.required)
        return actor.required_roles | self.bound_action.required

    @ classmethod
    def get_actor_label(self):
        return self.get_label() or self.bound_action.label

    def get_label(self):
        return self.label or str(self.bound_action.action)

    def run_from_ui(self, ar, **kw):
        sar = self.bound_action.request_from(ar)
        js = ar.renderer.request_handler(sar)
        ar.set_response(eval_js=js)


class MultipleRowAction(Action):

    custom_handler = True

    def run_on_row(self, obj, ar):
        """This is being called on every selected row."""
        raise NotImplementedError()

    def run_from_ui(self, ar, **kw):
        ar.success(**kw)
        n = 0
        for obj in ar.selected_rows:
            if not ar.response.get("success"):
                ar.debug("Aborting remaining rows")
                break
            ar.debug("Run %s for %s...", self.label, obj)
            n += self.run_on_row(obj, ar)
            ar.set_response(refresh_all=True)

        msg = _("%d row(s) have been updated.") % n
        ar.debug(msg)
        # ~ ar.success(msg,**kw)


class DeleteSelected(MultipleRowAction):

    action_name = "delete_selected"  # because...
    if True:  # settings.SITE.use_silk_icons:
        icon_name = "delete"
    else:
        button_text = "⊖"  # 2296 CIRCLED MINUS
        # button_text = u"⊟"  # 229F SQUARED MINUS

    show_in_side_toolbar = True

    ui5_icon_name = "sap-icon://less"
    help_text = _("Delete this record")
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    label = _("Delete")
    hotkey = keyboard.DELETE  # (ctrl=True)

    # ~ client_side = True

    def run_from_ui(self, ar, **kw):
        objects = []
        for obj in ar.selected_rows:
            objects.append(str(obj))
            msg = ar.actor.disable_delete(obj, ar)
            if msg is not None:
                ar.error(None, msg, alert=True)
                return

        # build a list of volatile related objects that will be deleted together
        # with this one
        cascaded_objects = {}
        kernel = settings.SITE.kernel
        for obj in ar.selected_rows:
            # print(20201229, "selected:", obj)
            for m, fk in traverse_ddh_fklist(obj.__class__):
                if fk.name in m.allow_cascaded_delete:
                    qs = m.objects.filter(**{fk.name: obj})
                    n = qs.count()
                    if n:
                        # print(20201229, n, fk, m, qs)
                        if m in cascaded_objects:
                            cascaded_objects[m] += n
                        else:
                            cascaded_objects[m] = n

            # print "20141208 generic related objects for %s:" % obj
            for gfk, fk_field, qs in kernel.get_generic_related(obj):
                if gfk.name in qs.model.allow_cascaded_delete:
                    n = qs.count()
                    if n:
                        cascaded_objects[qs.model] = n

        def ok(ar2):
            super(DeleteSelected, self).run_from_ui(ar, **kw)
            # refresh_all must be True e.g. for when user deletes an item of a
            # bank statement
            ar2.success(record_deleted=True, refresh_all=True)
            # hack required for extjs:
            if ar2.actor.detail_action:
                ar2.set_response(
                    detail_handler_name=ar2.actor.detail_action.full_name()
                )

        d = dict(num=len(objects), targets=", ".join(objects))
        if len(objects) == 1:
            d.update(type=ar.actor.model._meta.verbose_name)
        else:
            d.update(type=ar.actor.model._meta.verbose_name_plural)
            if len(objects) > 10:
                objects = objects[:9] + ["..."]
        msg = gettext(
            "You are about to delete %(num)d %(type)s\n(%(targets)s)") % d

        if len(cascaded_objects):
            lst = [
                "{} {}".format(
                    n, m._meta.verbose_name if n == 1 else m._meta.verbose_name_plural
                )
                for m, n in cascaded_objects.items()
            ]
            msg += "\n" + gettext(
                "as well as all related volatile records ({})"
            ).format(", ".join(lst))

        ar.confirm(
            ok,
            "{}. {}".format(msg, gettext("Are you sure?")),
            uid="deleting %(num)d %(type)s pks=" % d
            + "".join([str(t.pk) for t in ar.selected_rows]),
        )

    def run_on_row(self, obj, ar):
        obj.delete_instance(ar)
        return 1


class ShowEditor(Action):
    select_rows = True
    button_text = settings.SITE.expand_panel_symbol
    show_in_toolbar = False
    readonly = False

    def __init__(self, fieldname, *args, **kwargs):
        self.buddy_name = fieldname
        super().__init__(*args, **kwargs)

    def run_from_ui(self, ar, **kwargs):
        kw = dict()
        if ar.master_instance:
            kw.update({
                constants.URL_PARAM_MASTER_PK: ar.master_instance.pk,
                constants.URL_PARAM_MASTER_TYPE: settings.SITE.models.gfks.ContentType.objects.get_for_model(
                    ar.master_instance.__class__).pk
            })
        ar.set_response(goto_url=ar.renderer.front_end.build_plain_url(
            "#", "api", *ar.actor.actor_id.split("."), str(ar.selected_rows[0].pk), self.buddy_name, **kw))

# Some actions are described by a single action instance used by most actors:

# SHOW_TABLE = ShowTable()
# SUBMIT_DETAIL = SubmitDetail()
# DELETE_ACTION = DeleteSelected()
# UPDATE_ACTION = SaveGridCell()
# VALIDATE_FORM = ValidateForm()
