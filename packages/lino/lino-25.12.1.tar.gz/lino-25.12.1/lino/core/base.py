# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See src/core/actions.rst

from typing import Any
from django.conf import settings
from lino.core import constants
# from lino.core.exceptions import ChangedAPI

from django.core.exceptions import BadRequest

from .permissions import Permittable
from lino.core.params import Parametrizable
from lino.utils import choosers
from lino.core.resolve import register_params, make_params_layout_handle


class InstanceAction:
    """
    Volatile object that wraps a given action to be run on a given
    model instance.

    .. attribute:: bound_action

        The bound action that will run.

    .. attribute:: instance

        The database object on which the action will run.

    .. attribute:: owner


    """

    def __init__(self, action, actor, instance, owner):
        # ~ print "Bar"
        # ~ self.action = action
        if actor is None:
            actor = instance.get_default_table()
        self.bound_action = actor.get_action_by_name(action.action_name)
        if self.bound_action is None:
            raise Exception("%s has not action %r" % (actor, action))
            # Happened 20131020 from lino_xl.lib.beid.eid_info() :
            # When `use_eid_jslib` was False, then
            # `Action.attach_to_actor` returned False.
        self.instance = instance
        self.owner = owner

    def __str__(self):
        return "{0} on {1}".format(self.bound_action, obj2str(self.instance))

    def run_from_code(self, ar, *args, **kw):
        """
        Probably to be deprecated.
        Run this action on this instance in the given session, updating
        the response of the session.  Returns the return value of the
        action.
        """
        # raise Exception("20170129 is this still used?")
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_code(ar, *args, **kw)

    def run_from_ui(self, ar, *args, **kwargs):
        """
        Run this action on this instance in the given session, updating
        the response of the session.  Returns nothing.
        """
        # raise Exception("20170129 is this still used?")
        # kw.update(selected_rows=[self.instance])
        ar.selected_rows = [self.instance]
        self.bound_action.action.run_from_ui(ar, *args, **kwargs)

    def request_from(self, ses, **kwargs):
        """
        Create an action request on this instance action without running
        the action.
        """
        kwargs.update(selected_rows=[self.instance])
        kwargs.update(parent=ses)
        ar = self.bound_action.create_request(**kwargs)
        return ar

    def run_from_session(self, ses, **kwargs):
        """
        Run this instance action in a child request of given session.

        Additional arguments are forwarded to the action.
        Returns the response of the child request.
        Doesn't modify response of parent request.
        """
        ar = self.request_from(ses, **kwargs)
        self.bound_action.action.run_from_code(ar)
        return ar.response

    def __call__(self, *args, **kwargs):
        """
        Run this instance action in an anonymous base request.

        Additional arguments are forwarded to the action.
        Returns the response of the base request.
        """
        if len(args) and isinstance(args[0], BaseRequest):
            raise ChangedAPI("20181004")
        ar = self.bound_action.create_request(
            renderer=settings.SITE.kernel.text_renderer)
        self.run_from_code(ar, *args, **kwargs)
        return ar.response

    def as_button_elem(self, ar, label=None, **kwargs):
        return settings.SITE.kernel.row_action_button(
            self.instance, ar, self.bound_action, label, **kwargs
        )

    def as_button(self, *args, **kwargs):
        """Return a HTML chunk with a "button" which, when clicked, will
        execute this action on this instance.  This is being used in
        the :ref:`lino.tutorial.polls`.

        """
        return tostring(self.as_button_elem(*args, **kwargs))

    def get_row_permission(self, ar):
        state = self.bound_action.actor.get_row_state(self.instance)
        # logger.info("20150202 ia.get_row_permission() %s using %s",
        #             self, state)
        return self.bound_action.get_row_permission(ar, self.instance, state)


class Action(Parametrizable, Permittable):
    # _params_layout_class = layouts.ActionParamsLayout
    label = None
    button_text: str = None
    button_color = None
    debug_permissions = False
    save_action_name = None
    disable_primary_key = True
    keep_user_values = False
    icon_name: str = None
    ui5_icon_name = None
    react_icon_name = None
    hidden_elements = frozenset()
    combo_group = None
    parameters: dict[str, Any] | None = None
    use_param_panel = False
    no_params_window = False
    sort_index = 90
    help_text = None
    auto_save = True
    extjs_main_panel = None
    js_handler = None
    action_name = None
    defining_actor = None
    hotkey = None
    default_format = "html"
    editable = True
    readonly = True
    opens_a_window = False
    hide_top_toolbar = False  # 20210509
    hide_navigator = False  # 20210509
    never_collapse = False
    show_in_side_toolbar = False
    show_in_plain = False
    show_in_toolbar = True
    show_in_workflow = False
    buddy_name: str = None
    custom_handler = False
    select_rows = True
    http_method = "GET"
    preprocessor = "null"  # None
    window_type = None
    callable_from = "td"
    hide_virtual_fields = False
    required_states = None
    default_record_id = None

    def __init__(self, label=None, **kwargs):
        # if hasattr(self, 'help_text'):
        #     raise ChangedAPI("Replace help_text on Action by help_text")
        if label is not None:
            self.label = label

        # if self.parameters is not None and self.select_rows:
        #     self.show_in_toolbar = False
        #     # see ticket #105

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("Invalid action keyword %s" % k)
            setattr(self, k, v)

        if self.show_in_workflow:
            self.custom_handler = True

        if self.icon_name:
            if self.icon_name not in constants.ICON_NAMES:
                raise Exception(
                    "Unkonwn icon_name '{0}'".format(self.icon_name))

        params = {}
        if self.parameters is not None:
            params.update(self.parameters)
        self.setup_parameters(params)
        if len(params):
            self.parameters = params

        register_params(self)

        if self.callable_from is not None:
            for c in self.callable_from:
                if c not in constants.WINDOW_TYPES:
                    raise Exception(f"Invalid window_type spec {c} in {self}")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return InstanceAction(self, None, instance, owner)

    # def get_django_form(self):
    #     """returns a django form object based on the params of this action"""
    #     from django import forms
    #
    #     mapping = {"PasswordField": "CharField"}
    #
    #     class LinoForm(forms.Form):
    #         pass
    #
    #     for name, field in self.parameters.items():
    #         setattr(
    #             LinoForm,
    #             name,
    #             getattr(
    #                 forms,
    #                 mapping.get(field.__class__.__name__,
    #                             field.__class__.__name__),
    #             )(),
    #         )
    #     return LinoForm

    @classmethod
    def decorate(cls, *args, help_text=None, **kw):

        def decorator(fn):
            assert "required" not in kw
            # print 20140422, fn.__name__
            kw.setdefault("custom_handler", True)
            if help_text is not None:
                kw.update(help_text=help_text)
            a = cls(*args, **kw)

            def wrapped(ar):
                obj = ar.selected_rows[0] if ar.selected_rows else ar.actor.model
                return fn(obj, ar)

            a.run_from_ui = wrapped
            return a

        return decorator

    def setup_parameters(self, params):
        pass

    def get_help_text(self, ba):
        if ba is ba.actor.default_action:
            if self.default_record_id is not None:
                return ba.actor.help_text or self.help_text
            return self.help_text or ba.actor.help_text
        return self.help_text

    def get_action_url(self, ar, obj=None):
        if self.js_handler:
            if callable(self.js_handler):
                js = self.js_handler(ar.bound_action.actor)
            else:
                js = self.js_handler
        else:
            js = ar.ar2js(obj, **ar._status)
        return ar.renderer.js2url(js)

    def get_required_roles(self, actor):
        return actor.required_roles

    def is_callable_from(self, caller):
        assert caller.window_type is not None
        if self.callable_from is None:
            return False
        return caller.window_type in self.callable_from
        # return isinstance(caller, self.callable_from)

    def is_window_action(self):
        return self.opens_a_window or (self.parameters and not self.no_params_window)

    def get_status(self, ar, **kw):
        if self.parameters is not None:
            if self.keep_user_values:
                kw.update(field_values={})
            else:
                defaults = kw.get("field_values", {})
                pv = self.params_layout.params_store.pv2dict(
                    ar, ar.action_param_values, **defaults
                )
                kw.update(field_values=pv)
        return kw

    def get_chooser_for_field(self, fieldname):
        d = getattr(self, "_choosers_dict", {})
        return d.get(fieldname, None)

    def get_choices_text(self, obj, ar, field):
        return obj.get_choices_text(ar, self, field)

    def make_params_layout_handle(self):
        return make_params_layout_handle(self)

    def get_data_elem(self, name):
        # same as in Actor but here it is an instance method
        return self.defining_actor.get_data_elem(name)

    def get_param_elem(self, name):
        # same as in Actor but here it is an instance method
        if self.parameters:
            return self.parameters.get(name, None)
        return None

    def get_widget_options(self, name, **options):
        # same as in Actor but here it is an instance method
        return options

    def get_label(self):
        return self.label or self.action_name

    def get_button_label(self, actor):
        if self.button_text is not None:
            return self.button_text
        if actor is None or actor.default_action is None:
            return self.label
        if self is actor.default_action.action:
            return actor.label
            # return actor.get_actor_label()  # 20200307
        else:
            return self.button_text or self.label

    def full_name(self, actor=None):
        if self.action_name is None:
            raise Exception(f"Tried to full_name() on {repr(self)}")
            # ~ return repr(self)
        if actor is None or (self.parameters and not self.no_params_window):
            return self.defining_actor.actor_id + "." + self.action_name
        return str(actor) + "." + self.action_name

    def get_action_title(self, ar):
        return ar.get_title()

    def __repr__(self):
        if self.label is None:
            name = self.action_name
        else:
            label_repr = repr(str(self.label))
            name = "{} ({})".format(self.action_name, label_repr)
        # if self.button_text:
        #     name = repr(str(self.button_text)) + " " + name
        return "<{}.{} {}>".format(
            self.__class__.__module__, self.__class__.__name__, name
        )

    def __str__(self):
        # return force_str(self.label)
        # return str(self.get_label())
        return str(self.get_label())

    def attach_to_workflow(self, wf, name):
        if self.action_name is not None:
            assert self.action_name == name
        self.action_name = name
        self.defining_actor = wf
        choosers.setup_params_choosers(self)

    def attach_to_actor(self, owner, name):
        if not owner.editable and not self.readonly:
            return False
        # if not actor.editable and not self.readonly:
        #     return False
        if self.defining_actor is not None:
            # already defined by another actor
            return True
        self.defining_actor = owner
        # if self.label is None:
        #     self.label = name
        # if self.__class__.__name__ == "CreateExamByCourse":
        #     print(f"20250608 {self} attach_to_actor({owner})")
        choosers.setup_params_choosers(self)
        if self.action_name is not None:
            return True
            # if name == self.action_name:
            #     return True
            # raise Exception(
            #     f"Can't attach named action {self.action_name} "
            #     f"as {name} to {owner}")
        self.action_name = name
        return True

    def get_action_permission(self, ar, obj, state):
        return True

    def get_view_permission(self, user_type):
        return self.get_action_view_permission(self.defining_actor, user_type)
        # raise Exception("20250323 replaced by get_action_view_permission()")

    def get_action_view_permission(self, actor, user_type):
        return True

    def run_from_ui(self, ar, **kwargs):
        raise BadRequest("{} has no run_from_ui() method".format(
            self.__class__.__name__))

    def run_from_code(self, ar=None, *args, **kwargs):
        self.run_from_ui(ar, *args, **kwargs)

    def run_from_session(self, ses, *args, **kw):  # 20130820
        if len(args):
            obj = args[0]
        else:
            obj = None
        ia = InstanceAction(self, self.defining_actor, obj, None)
        return ia.run_from_session(ses, **kw)

    def action_param_defaults(self, ar, obj, **kw):
        for k, pf in self.parameters.items():
            # print 20151203, pf.name, repr(pf.rel.to)
            kw[k] = pf.get_default()
        return kw

    def setup_action_request(self, actor, ar):
        pass

    def get_layout_aliases(self):
        return []
