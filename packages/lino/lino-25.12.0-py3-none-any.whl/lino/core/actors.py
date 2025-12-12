# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This defines :class:`Actor` and related classes.

Introduction see :doc:`/dev/actors`.
Class reference see :doc:`/src/lino/core/actors`.

"""

import os
import warnings
import copy
from inspect import getmro
from types import GeneratorType
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from lino.utils.html import E, escape, tostring, Grouper, SAFE_EMPTY
from lino.utils import curry, AttrDict, is_string
from lino.core.utils import navinfo, dbfield2params_field
from lino.core.params import ParameterPanel
from lino.utils.html import qs2summary
from lino.core.utils import resolve_model
from lino.core.permissions import add_requirements, Permittable
from lino.core.params import Parametrizable
from lino.core.constants import _handle_attr_name
from lino.core.exceptions import ChangedAPI
from lino.core.boundaction import BoundAction
from lino.core import constants
from lino.core import actions
from lino.core import vfields
# from lino.core import fields
from lino.utils import MissingRow
from lino.utils.choosers import setup_params_choosers, check_for_chooser
from lino import logger
from .base import Action
from .roles import SiteUser
from .layouts import DetailLayout, InsertLayout


from .resolve import install_layout, resolve_layout, make_params_layout_handle, register_params
# from lino.core.utils import make_params_layout_handle, register_params
# from lino.utils.html import assert_safe


ACTOR_SEP = "."
DIVTPL = '<div class="htmlText">{}</div>'
btn_sep = mark_safe(" ")


# actors are automatically discovered at startup.

actor_classes = []
actors_dict = None
actors_list = None


def discover():
    global actor_classes
    global actors_list
    global actors_dict

    assert actors_list is None
    assert actors_dict is None

    actors_list = []
    actors_dict = AttrDict()

    logger.debug("actors.discover() : registering %d actors",
                 len(actor_classes))
    for cls in actor_classes:
        register_actor(cls)
    actor_classes = None


def register_actor(a):
    """

    Called during startup process to insert an
    actor class in the global actors_list and actors_dict.

    Special attention is given to the case when a plugin extends another plugin
    and redefines an actor of same name.  In that case we want the ordering to
    remain as it was from the beginning. Actor overrides are not appended to the
    end but replaced, in order to not disturb the finding of
    `_lino_default_table`.


    """
    # ~ logger.debug("register_actor %s",a)
    if not a.abstract:
        # if not settings.SITE.is_installed(a.app_label):
        p = settings.SITE.plugins.get(a.app_label, None)
        if p is None or p.is_hidden():
            # avoid registering choicelists of non-installed plugins
            # logger.info("20190107 skip register_actor for %s", a)
            a.abstract = True
            return
    old = actors_dict.define(a.app_label, a.__name__, a)
    if old is not None:
        # For example lino_voga.lib.courses.EnrolmentsByCourse replaces class of
        # same name from lino_xl
        # print(f"20250523 {repr(a)} replaces {repr(old)} ({old.abstract} {a.abstract})")
        # if not issubclass(a, old):
        #     raise Exception(f"20250523 {a} is not subclass of {old}")
        # if not a.abstract:
        #     old.abstract = True
        #     a.abstract = False
        i = actors_list.index(old)
        actors_list[i] = a
        # actors_list.remove(old)
    else:
        actors_list.append(a)
    return a


def field_getter(name):
    def func(cls, obj, ar):
        # ~ print 20130910, repr(obj),name
        return getattr(obj, name)

    return func


class ActorMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        # ~ if not classDict.has_key('app_label'):
        # ~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        attributes that are never inherited from base classes:
        """
        # classDict.setdefault('name',classname)
        # ~ classDict.setdefault('label',None) # 20130906
        # ~ classDict.setdefault('related_name',None)
        # ~ classDict.setdefault('button_label',None)
        classDict.setdefault("title", None)
        classDict.setdefault("help_text", None)
        classDict.setdefault("abstract", False)

        declared_label = classDict.pop("label", None)
        if declared_label is not None:
            classDict.update(_label=declared_label)
        declared_known_values = classDict.pop("known_values", None)
        if declared_known_values is not None:
            classDict.update(_known_values=declared_known_values)
        #         if 'editable' in classDict:
        #             raise ChangedAPI("""
        # 20210512 {} : replace 'editable = False' by "
        # @classmethod
        # def hide_editing(cls, user_type):
        #     return True
        # """.format(classname))
        declared_editable = classDict.pop("editable", None)
        if declared_editable is not None:
            classDict.update(_editable=declared_editable)

        if classDict.get("default_record_id", None) is not None:
            classDict.update(hide_navigator=True)
            classDict.update(allow_create=False)
            classDict.update(allow_delete=False)
            # classDict.update(display_mode=(
            #     (None, constants.DISPLAY_MODE_DETAIL)))

        cls = super().__new__(meta, classname, bases, classDict)

        # On 20110822 I thought "A Table always gets the app_label of its model,
        # you cannot set this yourself in a subclass
        # because otherwise it gets complex when inheriting reports from other
        # app_labels."
        # On 20110912 I cancelled change 20110822 because PersonsByOffer
        # should clearly get app_label 'jobs' and not 'contacts'.
        if classDict.get("app_label", None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            x = cls.__module__.split(".")
            if len(x) > 1:
                cls.app_label = x[-2]

        cls.actor_id = cls.app_label + "." + cls.__name__
        cls._setup_done = False
        cls._setup_doing = False
        cls.virtual_fields = {}
        cls._constants = {}
        cls._actions_dict = {}  # AttrDict()
        cls._actions_list = []  # 20121129

        cls.collect_virtual_fields()

        if actor_classes is not None:
            actor_classes.append(cls)
        # else:
        #     print(f"20250523 found {cls} but actor_classes is None")
        return cls

    def __str__(cls):
        return cls.actor_id

    def __repr__(cls):
        return cls.__module__ + "." + cls.__name__

    @property
    def label(cls):
        # return cls.get_label()  # 20200307
        return cls.get_actor_label()

    @property
    def known_values(cls):
        return cls.get_known_values()

    @property
    def editable(cls):
        # See docs/dev/disable.rst
        return cls.get_actor_editable()


# class Actor(metaclass=ActorMetaClass, type('NewBase', (actions.Parametrizable, Permittable), {}))):
class Actor(Parametrizable, Permittable, metaclass=ActorMetaClass):
    """
    """

    _detail_action_class = None

    obvious_fields = set()
    required_roles = set([SiteUser])
    model = None
    only_fields = None
    default_display_modes = None
    # extra_display_modes = set()
    # extra_display_modes = {constants.DISPLAY_MODE_SUMMARY}
    extra_display_modes = {constants.DISPLAY_MODE_HTML}
    app_label = None
    master = None
    master_key = None
    details_of_master_template = _("%(details)s of %(master)s")

    parameters = None
    # See :attr:`lino.core.utils.Parametrizable.parameters`.

    # _params_layout_class = None
    _state_to_disabled_actions = None
    _lino_publisher_location = None

    ignore_required_states = False
    """
    Whether to ignore the required states of workflow actions.

    Set this to `True` on a workflow if you want to disable workflow
    control based on the state of the object.

    Note that you must set this to True *before* importing any library workflows
    because permission handlers are defined when a workflow is imported. """

    sort_index = 60
    """The :attr:`sort_index <lino.core.actions.Action.sort_index>` to be
    used when this table is being used by a :class:`ShowSlaveTable
    <lino.core.actions.ShowSlaveTable>`.

    """

    icon_name = None
    """The :attr:`lino.core.actions.Action.icon_name` to be used for a
    :class:`lino.core.actions.ShowSlaveTable` action on this actor.

    """

    simple_parameters = None

    hidden_elements = frozenset()

    detail_html_template = "bootstrap5/detail.html"
    """The template to be used for rendering a row of this actor as a
    detail html page.

    """
    list_html_template = "bootstrap5/table.html"
    """The template to be used for rendering a collection of rows of this
    actor as a table html page.

    """
    welcome_message_when_count = None
    get_welcome_messages = None
    get_row_classes = None
    window_size = None

    # 20240404 default_list_action_name = 'grid'
    # default_elem_action_name = 'detail'

    # editable = None

    auto_apply_params = True
    """Whether the parameter values of the parameter panel should be
    applied automatically when some value has been changed.

    """

    enable_slave_params = False
    """Whether the parameter panel could be shown in a slave panel"""

    insert_layout_width = 60
    hide_window_title = False
    allow_create = True
    allow_delete = True
    hide_headers = False

    toolbar_location = "top"
    """Not yet implemented.
    Should be one of 'top' (default), 'bottom', 'right', 'left'
    """

    hide_top_toolbar = False  # 20210509
    """See :ref:`dev.actor_config.hide_top_toolbar`."""

    hide_navigator = False  # 20210509
    """See :ref:`dev.actor_config.hide_navigator`."""

    simple_slavegrid_header = False

    paginator_template = None

    _label = None
    _editable = None
    _known_values = {}
    title = None
    button_text = None
    label = None
    default_action = None
    actor_id = None

    grid_layout = None
    detail_layout = None
    insert_layout = None
    card_layout = None
    list_layout = None  # no longer used

    detail_template = None  # deprecated: use insert_layout instead
    insert_template = None  # deprecated: use detail_layout instead
    row_template = None   # "{row}"

    help_text = None
    detail_action = None
    update_action = None
    insert_action = None
    # create_action = None
    delete_action = None
    _handle_class = None  # For internal use.
    get_handle_name = None

    abstract = True
    sum_text_column = 0

    preview_limit = None

    handle_uploaded_files = None
    default_record_id = None

    def __init__(self, *args, **kw):
        raise Exception("Actors should never get instantiated")

    @classmethod
    def apply_cell_format(self, ar, row, col, recno, td):
        """
        Actor-level hook for overriding the formating when rendering
        this table as plain html.

        For example :class:`lino_xl.lib.cal.Events` overrides this.
        """
        pass

    @classmethod
    def actor_url(self):
        return "/" + self.app_label + "/" + self.__name__

    @classmethod
    def is_installed(self):
        return settings.SITE.is_installed(self.app_label)

    @classmethod
    def before_group_change(cls, gh, row):
        return SAFE_EMPTY

    @classmethod
    def after_group_change(cls, gh, row):
        return SAFE_EMPTY

    @classmethod
    def is_hidden(self):
        return settings.SITE.is_hidden_plugin(self.app_label)

    @classmethod
    def get_widget_options(cls, name, **options):
        if cls.model is None:
            return options
        return cls.model.get_widget_options(name, **options)

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, "_choosers_dict", {})
        ch = d.get(fieldname, None)
        if ch is not None:
            # print(f"20251124g {cls} {fieldname} {ch}")
            return ch
        if cls.model is not None:
            return cls.model.get_chooser_for_field(fieldname)

    # @classmethod
    # def inject_field(cls, name, fld):
    #     # called from auth.add_user_group()
    #     setattr(cls, name, fld)
    #     cls.register_class_attribute(name, fld)

    @classmethod
    def get_pk_field(self):
        """Return the Django field used to represent the primary key
        when filling `selected_pks`.

        """
        return None

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """Return the data row identified by the given primary key."""
        raise NotImplementedError()

    @classmethod
    def get_master_instance(cls, ar, model, pk):
        """Return the `master_instance` corresponding to the specified primary
        key.

        You need to override this on slave actors whose
        :attr:`master` is not a database model,
        e.g. the :class:`MessagesByChecker
        <lino.modlib.checkdata.MessagesByChecker>` table.

        `ar` is the action request on this actor. `model` is the
        :attr:`master`, except if :attr:`master` is `ContentType` (in
        which case `model` is the *requested* master).

        """
        if not pk:
            return None
        # if not issubclass(model, models.Model):
        #     msg = "{0} must override get_master_instance"
        #     msg = msg.format(self)
        #     raise Exception(msg)
        try:
            # print(20240804, model, ar)
            return model.get_request_queryset(ar).get(pk=pk)
            # Why not simply return model.objects.get(pk=pk)? Because a
            # confidential master instance should get hidden.

            # if obj is not None:
            #     obj = cls.cast_master_instance(obj)
            # return obj
        except Exception as e:
            # logger.error(e)
            # raise Exception("20240804 {}\n{}\n{}".format(e, model, ar))
            return MissingRow("{} (pk={})".format(e, pk))

    @classmethod
    def cast_master_instance(cls, obj):
        return obj

    @classmethod
    def get_disabled_fields(cls, obj, ar):
        """
        Return the cached set of disabled fields for this `obj` and `ar`.

        """
        df = getattr(obj, "_disabled_fields", None)
        if df is None:
            df = cls.make_disabled_fields(obj, ar)
            setattr(obj, "_disabled_fields", df)
        return df

    @classmethod
    def make_disabled_fields(cls, obj, ar):
        """
        Used internally. Return a set of disabled fields for the specified
        object and request. See :doc:`/dev/disable`.
        """

        s = set()
        state = cls.get_row_state(obj)
        if state is not None:
            s |= cls._state_to_disabled_actions.get(state.name, set())
        return s

    @classmethod
    def get_handle(self):
        """
        Return a static handle for this actor.
        """
        # ~ assert ar is None or isinstance(ui,UI), \
        # ~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        if self.get_handle_name is not None:
            raise Exception(
                "Tried to get static handle for %s (get_handle_name is %r)"
                % (self, self.get_handle_name)
            )
        return self._get_handle(None, _handle_attr_name)

    @classmethod
    def _get_handle(self, ar, hname):
        # don't inherit from parent!
        h = self.__dict__.get(hname, None)
        # logger.info("18072017, h:|%s|, hname:|%s| #1955"%(h, hname))
        if h is None:
            h = self._handle_class(self)
            # don't store the handle instance when an exception occurs during
            # setup_handle. Because if the exception is caught by calling code,
            # the unfinished handle would remain in memory and get used by
            # subsequent calls, causing tracebacks like "AttributeError:
            # 'TableHandle' object has no attribute 'store'"
            setattr(self, hname, h)

            # In released versions the following should be True. We might want
            # to catch exceptions only for debugging purposes.

            if True:
                settings.SITE.kernel.setup_handle(h, ar)
            else:
                try:
                    settings.SITE.kernel.setup_handle(h, ar)
                except Exception as e:
                    logger.warning(
                        "%s setup_handle failed with %s (change actors.py to see more)",
                        self,
                        e,
                    )
                    delattr(self, hname)
                    # raise

        # logger.info("18072017, h:|%s|, h.store:|%s|, #1955"%(h, getattr(h,'store',None)))
        return h

    @classmethod
    def get_request_handle(self, ar):
        """
        Return the dynamic (per-request) handle for this actor for the
        renderer used by specified action request.
        """
        # logger.info("18072017, self.get_handle_name:|%s| #1955"%(self.get_handle_name),)
        if self.get_handle_name is None:
            return self._get_handle(ar, _handle_attr_name)
        return self._get_handle(ar, self.get_handle_name(ar))

    @classmethod
    def has_handle(self, ui):
        return self.__dict__.get(_handle_attr_name, False)

    @classmethod
    def clear_handle(self):
        """
        When an actor has dynamic columns which depend on database
        content, then its layout handle may not persist between
        different Django test cases because a handle from a first
        test case may refer to elements which no longer exist in a
        second test case.
        """
        setattr(self, _handle_attr_name, None)

    @classmethod
    def get_navinfo(cls, ar, obj):
        """
        Return navigation info for the given obj in the given ar.

        The default implementation assumes that you navigate on the
        :attr:`data_iterator`.

        :class:`lino_xl.lib.calview.DayNavigator` overrides this.

        """
        return navinfo(ar.data_iterator, obj, ar.limit)

    @classmethod
    def is_valid_row(self, row):
        return False

    @classmethod
    def make_params_layout_handle(cls):
        if cls.is_abstract():
            raise Exception(f"{repr(cls)} is abstract")
        return make_params_layout_handle(cls)

    @classmethod
    def is_abstract(cls):
        return cls.abstract

    @classmethod
    def on_analyze(self, site):
        pass

    @classmethod
    def do_setup(self):
        pass

    # @classmethod
    # def update_field(cls, name, **kwargs):
    #     cls._pending_field_updates.append((name, kwargs)) xxx
    #     de = getattr(cls, name)
    #     if de.model is not cls:
    #         de = copy.deepcopy(de)
    #         de.model = cls
    #         setattr(cls, name, de)
    #     for k, v in kwargs.items():
    #         setattr(de, k, v)

    @classmethod
    def class_init(cls):
        """Called internally at site startup."""
        # logger.info("20180201 class_init", cls)

        if hasattr(cls, "required"):
            raise ChangedAPI(
                f"{cls} must convert `required` to `required_roles`"
            )
        if hasattr(cls, "display_mode"):
            # cls.default_display_modes = {k:v for k, v in cls.display_mode}
            # logger.info(f"{cls} uses deprecated `display_mode`, please convert to `default_display_modes`.")
            raise ChangedAPI(
                f"{cls} must convert `display_mode` to `default_display_modes`")

        master = getattr(cls, "master", None)
        if isinstance(master, str):
            # if isinstance(master, string_types):
            cls.master = resolve_model(master)

        model = getattr(cls, "model", None)
        if isinstance(model, str):
            model = cls.model = resolve_model(model)

        cls.collect_virtual_fields()

        # set the verbose_name of the detail_link field
        # model = cls.model
        if isinstance(model, type) and issubclass(model, models.Model):
            de = cls.detail_link
            assert de.model is not None
            # only if it hasn't been overridden by a parent actor
            if de.model is Actor:
                if de.return_type.verbose_name != model._meta.verbose_name:
                    de = copy.deepcopy(de)
                    de.model = de.return_type.model = cls
                    de.return_type.verbose_name = model._meta.verbose_name
                    de.lino_resolve_type()
                    cls.detail_link = de
                    cls.virtual_fields["detail_link"] = de
                    # cls.add_virtual_field('detail_link', de)

        if cls.abstract:
            return

        edm = set()  # extra display modes to add automatically
        if cls.default_display_modes is not None:
            for v in cls.default_display_modes.values():
                if v not in constants.DISPLAY_MODES:
                    raise Exception(f"Invalid display mode {v} in {cls}")
                if v not in constants.BASIC_DISPLAY_MODES:
                    # be sure to have our copy the extra_display_modes set
                    # if str(cls) == "comments.Comments":
                    #     print(f"20240929 extra_display_modes is {cls.extra_display_modes}, we add {v}")
                    # cls.extra_display_modes = cls.extra_display_modes | {v}
                    edm.add(v)

        if cls.hide_navigator:
            return

        if cls.card_layout is not None:
            edm.add(constants.DISPLAY_MODE_CARDS)
        if 'row_as_paragraph' in cls.__dict__:
            edm.add(constants.DISPLAY_MODE_LIST)
        # if 'row_as_page' in cls.__dict__:
        #     edm.add(constants.DISPLAY_MODE_STORY)
        if model is not None:
            if model.extra_display_modes is not None:
                for v in model.extra_display_modes:
                    if v not in constants.DISPLAY_MODES:
                        raise Exception(
                            f"Invalid extra_display_modes mode {v} in {model}")
                edm |= model.extra_display_modes
            if 'as_paragraph' in model.__dict__:
                edm.add(constants.DISPLAY_MODE_LIST)
            if 'as_page' in model.__dict__:
                edm.add(constants.DISPLAY_MODE_STORY)
            if 'as_tile' in model.__dict__:
                edm.add(constants.DISPLAY_MODE_TILES)
            # no need to automatically add summary because it's in default_display_modes of every table
            # if 'as_summary_item' in model.__dict__:
            #     edm.add(constants.DISPLAY_MODE_SUMMARY)
        if len(edm) > 0:
            # if str(cls) == "comments.Comments":
            #     print(f"20240929 {cls} extra_display_modes add {edm}")
            cls.extra_display_modes = cls.extra_display_modes | edm

    @classmethod
    def init_layouts(cls):
        # 20200430 this was previously part of class_init, but is now called in
        # a second loop. Because calview.EventsParams copies parameters from Events.

        install_layout(cls, "detail_layout", DetailLayout)
        install_layout(
            cls,
            "insert_layout",
            InsertLayout,
            window_size=(cls.insert_layout_width, "auto"),
        )
        install_layout(cls, "card_layout", DetailLayout)
        # layouts.install_layout(cls, "list_layout", layouts.DetailLayout)

        cls.extra_layouts = dict()
        for name, main in cls.get_extra_layouts():
            layout_instance = resolve_layout(
                cls, "extra_layout", main, DetailLayout
            )
            cls.extra_layouts.update({name: layout_instance})
            a = actions.ShowExtraDetail(layout_instance)
            cls._bind_action("extra_" + name, a, False)
            if cls.detail_action is None:
                cls.detail_action = cls._bind_action("detail_action", a, True)

        if cls.abstract:
            return

        if "parameters" in cls.__dict__:
            cls.setup_parameters(cls.parameters)
        else:
            params = {}
            if cls.parameters is not None:
                params.update(cls.parameters)
            cls.setup_parameters(params)
            if len(params):
                cls.parameters = params

        lst = []

        def append(n):
            if isinstance(n, (GeneratorType, list, tuple)):
                for i in n:
                    append(i)
            elif n in lst:
                logger.warning(
                    "Removed duplicate name %s returned by %s.get_simple_parameters()",
                    n,
                    cls,
                )
            else:
                lst.append(n)

        for n in cls.get_simple_parameters():
            # if cls.master_key is not None:
            #     print(repr(n), "!=", repr(cls.master_key))
            if n != cls.master_key:
                append(n)

        cls.simple_parameters = tuple(lst)

        if len(cls.simple_parameters) > 0:
            if cls.parameters is None:
                cls.parameters = {}
            for name in cls.simple_parameters:
                if name not in cls.parameters:
                    db_field = cls.get_data_elem(name)
                    if db_field is None:
                        raise Exception(
                            "{}.get_simple_parameters() returned invalid name '{}'".format(
                                cls, name
                            )
                        )
                    fld = dbfield2params_field(db_field)
                    cls.parameters[name] = fld
                    ch = check_for_chooser(cls, fld, name)
                    if ch is None and cls.model is not None:
                        ch = check_for_chooser(cls.model, fld, name)
                    # if name == 'exam__challenge__skill':
                    #     print(f"20251124h init_layouts {cls} {fld} -> {ch}")

                    # if "__" in name:
                    #     print("20200423", cls.parameters)
            if len(cls.parameters) == 0:
                raise Exception("20200825")
                # cls.parameters = None # backwards compatibility
        # if cls.__name__.endswith("Users"):
        #     print("20200825 {}.register_params {} {}".format(
        #         cls, cls.parameters, cls.params_layout))

    # @classmethod
    # def collect_extra_fields(cls, fld):
    #     cls.extra_fields[fld.name] = fld

    @classmethod
    def collect_virtual_fields(cls):
        """Collect virtual fields from class attributes and register them as
        virtual fields."""
        # print("20190201 collect_virtual_fields {}".format(cls))
        for b in reversed(cls.__mro__):
            for k, v in b.__dict__.items():
                # for k in b.__dict__.keys():
                #     v = getattr(cls, k)
                if isinstance(v, vfields.Constant):
                    cls.add_constant(k, v)
                elif isinstance(v, vfields.VirtualField):  # 20120903b
                    cls.add_virtual_field(k, v)
                elif isinstance(v, models.Field):  # 20130910
                    # ~ print "20130910 add virtual field " ,k, cls
                    vf = vfields.VirtualField(v, field_getter(k))
                    cls.add_virtual_field(k, vf)

    @classmethod
    def get_known_values(cls):
        return cls._known_values

    @classmethod
    def hide_editing(cls, user_type):
        """
        Whether users of the given :term:`user type` can edit in this
        :term:`data window`.

        Returns `False` by default: a user who has view permission also has
        permission to edit the data they see.

        If this returns `True`, then Lino won't even call :meth:`disable_delete`
        or :meth:`disabled_fields`.

        This is similar to :attr:`editable`, but it allows you to keep editing
        functionality for certain user types.

        Usage examples see :ref:`dev.actor_config.editing`.

        """
        return not cls.editable

    @classmethod
    def get_actor_editable(cls):
        return cls._editable

    @classmethod
    def hide_elements(self, *names):
        for name in names:
            if self.get_data_elem(name) is None:
                raise Exception("%s has no element '%s'" % self, name)
        self.hidden_elements = self.hidden_elements | set(names)

    @classmethod
    def add_view_requirements(cls, *args):
        return add_requirements(cls, *args)

    @classmethod
    def get_view_permission(self, user_type):
        """Return True if this actor as a whole is visible for users with the
        given user_type.

        """
        # return isinstance(user_type, tuple(self.required_roles))
        return True

    @classmethod
    def get_create_permission(self, ar):
        if not self.allow_create:
            return False
        if settings.SITE.readonly:
            return False
        if settings.SITE.user_types_module:
            user = ar.get_user()
            if user.user_type.readonly:
                return False
            if self.hide_editing(user.user_type):
                return False
        return True

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        """
        Whether to allow the given action request `ar` on the given
        :term:`database row` `row`.
        """

        if ba.action.readonly:
            return True
        user_type = ar.get_user().user_type
        if user_type.readonly:
            return False
        return not cls.hide_editing(user_type)

    @classmethod
    def get_request_detail_action(cls, ar):
        """
        Return the detail action of this actor, respecting the user's view
        permissions.

        This is equivalent to the actors's :attr:`detail_action`, except when
        the model's :meth:`get_detail_action` method returns a table for which
        the user has no view permission.  In that case we don't want Lino to
        give up too quickly because there is still a possibility that the same
        layout is used on other tables, to which the user does have permission.

        An example is described in :ref:`avanti.specs.get_request_detail_action`

        """
        if (ba := cls.detail_action) is None:
            return None
        if ar is None:
            return ba
        ut = ar.get_user().user_type
        if (
            ar.actor is not None
            and ar.actor.detail_action is not None
            and ba.action is ar.actor.detail_action.action
        ):
            # 20210223 When this actor uses the same action, don't return
            # the default area actor because the user might not have
            # permission to see the defining actor. See
            # specs/avanti/courses.rst
            # return ar.actor.detail_action
            ba = ar.actor.detail_action
            if ba.allow_view(ut):
                # if ba.get_view_permission(ut):
                # print("20210223", ba, "is allowed for", ut)
                return ba
        # e.g. the owner of a cal.Event
        # wl = table.get_detail_layout()
        # for ds in wl.layout.get_datasources():
        for ds in ba.action.owner.get_datasources():
            if ds.default_action is None:
                # print("20210224", ds)
                continue
            if ds.default_action.get_view_permission(ut):
                ba = ds.detail_action
                # if ba.allow_view(ut):
                if ba.get_view_permission(ut):
                    # print("20210223", ba, "is allowed for", ut)
                    return ba
        return None

    @classmethod
    def _collect_actions(cls):
        """
        Loops through the class dict and collects all Action instances,
        calling :meth:`_attach_action`, which will set their `actor` attribute.
        Before this we create `insert_action` and `detail_action` if necessary.
        Also fill :attr:`_actions_list`.
        """
        from lino.core import actions
        from lino.core import sai

        if cls.detail_layout:
            if (
                cls.detail_action
                and cls.detail_action.action.owner == cls.detail_layout
            ):
                dtla = cls.detail_action.action
            else:
                dtla = cls._detail_action_class(cls.detail_layout)
            cls.detail_action = cls._bind_action("detail_action", dtla, True)
            if cls.use_detail_param_panel:
                cls.detail_action.action.use_param_panel = True
            # if str(cls).endswith("Days"):
            #     logger.info("20181230 %r detail_action is %r", cls, cls.detail_action)
            if cls.editable:
                cls.submit_detail = cls._bind_action(
                    "submit_detail", sai.SUBMIT_DETAIL, True
                )

        # avoid inheriting the following actions from parent:
        cls.insert_action = None
        cls.delete_action = None
        cls.update_action = None
        cls.validate_form = None

        if cls.editable:
            if cls.allow_create:
                # if cls.detail_action and not cls.hide_top_toolbar:
                # if cls.insert_layout and not cls.hide_top_toolbar:
                # NB polls.AnswerRemarksByAnswer has hide_top_toolbar but we need its insert_action.
                if (ia := cls.get_insert_action()) is not None:
                    cls.insert_action = cls._bind_action(
                        "insert_action", ia, True)
            if cls.allow_delete:
                if (ia := cls.get_delete_action()) is not None:
                    cls.delete_action = cls._bind_action(
                        "delete_action", ia, True)
            cls.update_action = cls._bind_action(
                "update_action", sai.UPDATE_ACTION, True)
            if cls.detail_layout:
                cls.validate_form = cls._bind_action(
                    "validate_form", sai.VALIDATE_FORM, True)

        if is_string(cls.workflow_owner_field):
            cls.workflow_owner_field = cls.get_data_elem(
                cls.workflow_owner_field)
        if is_string(cls.workflow_state_field):
            # if isinstance(cls.workflow_state_field, string_types):
            fld = cls.get_data_elem(cls.workflow_state_field)
            if fld is None:
                raise Exception(
                    "Failed to resolve {}.workflow_state_field {}".format(
                        cls, cls.workflow_state_field
                    )
                )
            cls.workflow_state_field = fld

        # note that the fld may be None e.g. cal.Component
        if cls.workflow_state_field is not None:
            for a in cls.workflow_state_field.choicelist.workflow_actions:
                setattr(cls, a.action_name, a)

        # Bind all custom actions, including those inherited from parent actors.

        # NB is it still true that an actor can refuse to inherit some action
        # from a parent by defining a class attribute of same name that contains
        # something else?

        for b in cls.mro():
            for k, v in b.__dict__.items():
                v = cls.__dict__.get(k, v)
                if isinstance(v, Action):
                    cls._bind_action(k, v, False)

        if cls.default_record_id is None:
            if (da := cls.get_default_action()) is not None:
                if isinstance(da, Action):
                    cls.default_action = cls._bind_action(
                        "default_action", da, True)
                else:
                    # raise Exception(f"20250913 {cls}")
                    cls.default_action = da
        else:
            assert cls.detail_action is not None
            da = cls.detail_action.action
            da = da.__class__(
                da.owner, label=cls.label, help_text=cls.help_text,
                default_record_id=cls.default_record_id)
            da = cls._bind_action("default_action", da, True)
            cls.default_action = cls.detail_action = da

        cls._actions_list.sort(
            key=lambda a: (a.action.sort_index, a.action.action_name)
        )
        # cls._actions_list = tuple(cls._actions_list)

        # build a dict which maps state.name to a set of action names
        # to be disabled on objects having that state:
        cls._state_to_disabled_actions = {}
        wsf = cls.workflow_state_field
        if wsf is not None:
            st2da = cls._state_to_disabled_actions
            for state in wsf.choicelist.get_list_items():
                st2da[state.name] = set()
            for a in wsf.choicelist.workflow_actions:
                st2da[a.target_state.name].add(a.action_name)
            if wsf.choicelist.ignore_required_states:
                # raise Exception("20181107")
                # logger.info("20181107 %s", st2da)
                # from pprint import pprint
                # pprint(st2da)
                return
            for ba in cls._actions_list:
                # st2da[ba] = 1
                if ba.action.action_name:
                    required_states = ba.action.required_states
                    if required_states:
                        # if an action has required states, then it must
                        # get disabled for all other states:
                        if is_string(required_states):
                            required_states = set(required_states.split())
                        for k in st2da.keys():
                            if k not in required_states:
                                st2da[k].add(ba.action.action_name)

    @classmethod
    def collect_extra_actions(cls):
        return []

    @classmethod
    def _bind_action(cls, k, a, override):
        # Only for internal use during _collect_actions().
        # This is used in two different kinds of contexts: (a) when binding the
        # action shortcuts (defaul_action, insert_actions etc) to every actor
        # and (b) when discovering custom actions.
        # The `override` argument says what to do when an action of that name
        # has already been bound to this actor.
        # An example for (b) is finan.SuggestionsByVoucherItem which overrides
        # the `do_fill` action defined by its parent finan.SuggestionsByVoucher.

        if not a.attach_to_actor(cls, k):
            return
        # if str(cls) == "finan.SuggestionsByPaymentOrderItem": # and a.__class__.__name__ == "ShowDetail":
        #     print("20210106", k, a.action_name, a.__class__)

        names = [k]
        if a.action_name and a.action_name != k:
            names.append(a.action_name)

        for name in names:
            if name in cls._actions_dict:
                old = cls._actions_dict[name]
                # if old.actor is cls:
                #     return old
                # if str(cls) == "system.SiteConfigs": # and a.__class__.__name__ == "ShowDetail":
                #     print("20210106 ignore {} {} because {} exists".format(k, a.__class__, old))
                if override:
                    # if name == "update_guests":
                    #     print(f"20250622 override {old} on {cls}")
                    cls._actions_list.remove(old)
                else:
                    return old

        ba = BoundAction(cls, a)
        # if name == "update_guests":
        #     print(f"20250622 create {hash(ba)} on {cls}")
        # try:
        #     ba = BoundAction(cls, a)
        # except Exception as e:
        #     raise Exception("Cannot bind {!r} to {!r} : {}".format(a, cls, e))

        for name in names:
            cls._actions_dict[name] = ba
        cls._actions_list.append(ba)

        # setattr(cls, k, ba)
        return ba

    @classmethod
    def get_default_action(cls):
        pass

    @classmethod
    def get_insert_action(cls):
        from lino.core import sai
        if cls.insert_layout:
            return sai.SHOW_INSERT

    @classmethod
    def get_delete_action(cls):
        from lino.core import sai
        return sai.DELETE_ACTION

    @classmethod
    def get_label(self):
        return self.label
        # return self._label  # 20200307

    @classmethod
    def get_actor_label(self):
        return self._label or self.__name__

    @classmethod
    def get_detail_title(self, ar, obj):
        """Return the string to use when building the title of a detail
        window on a given row of this actor.

        """
        return obj.as_str(ar)

    @classmethod
    def get_card_title(self, ar, obj):
        return self.get_detail_title(ar, obj)

    @classmethod
    def get_main_card(
        self,
        ar,
    ):
        return None

    @classmethod
    def row_as_summary(cls, ar, obj, text=None, **kwargs):
        if ar is None:
            return text or str(obj)
        return obj.as_summary_item(ar, text, **kwargs)

    @classmethod
    def row_as_paragraph(cls, ar, row):
        """Return an HTML string that represents the given row as a single
        paragraph.

        See :ref:`dev.as_paragraph`.
        """
        return row.as_paragraph(ar)

    # @classmethod
    # def row_as_page(cls, ar, row, **kwargs):
    #     """
    #     Yield a list of safe HTML strings that represent the given row as a plain page.
    #     """
    #     return row.as_page(ar, **kwargs)

    @classmethod
    def get_choices_text(self, obj, ar, field):
        """
        Return the text to be displayed in a combo box
        for the field `field` of this actor to represent
        the choice `obj`.
        Override this if you want a customized representation.
        For example :class:`lino_voga.models.InvoiceItems`

        """
        return obj.get_choices_text(ar, self, field)

    @classmethod
    def has_db_model(cls):
        if cls.model is None:
            return False
        if not isinstance(cls.model, type):
            raise Exception(
                "{}.model is {!r} (must be a class)".format(cls, cls.model))
        return issubclass(cls.model, vfields.TableRow)

    @classmethod
    def get_breadcrumbs(cls, ar, elem=None):
        if cls.default_record_id is not None:
            yield ar.get_title()
            return
        if elem is not None:
            for pl in elem.get_parent_links(ar):
                yield pl
        sar = ar.spawn_request(actor=cls)
        yield tostring(sar.href_to_request(
            sar, ar.get_title(), icon_name=None))
        # if elem is not None:
        #     yield escape(ar.get_detail_title(elem))

    @classmethod
    def get_title(self, ar):
        title = self.get_title_base(ar)
        tags = [str(t) for t in self.get_title_tags(ar)]
        if len(tags):
            title += " (%s)" % (", ".join(tags))
        return title

    @classmethod
    def get_title_base(self, ar):
        title = self.title or self.label
        # if self.master is not None:
        if ar.master_instance is not None:
            title = self.details_of_master_template % dict(
                details=title, master=ar.master_instance
            )
        return title

    @classmethod
    def get_title_tags(self, ar):
        if isinstance(self.parameters, ParameterPanel):
            for t in self.parameters.get_title_tags(ar):
                yield t
        for k in self.simple_parameters:
            v = getattr(ar.param_values, k)
            if v and v != constants.CHOICES_BLANK_FILTER_VALUE:
                if v is True:
                    # For BooleanField no need to add "True" in the title
                    yield str(self.parameters[k].verbose_name)
                else:
                    yield str(self.parameters[k].verbose_name) + " " + str(v)
        if self.has_db_model():
            for s in self.model.get_title_tags(ar):
                yield s

    @classmethod
    def setup_request(self, ar):
        """Customized versions may e.g. set `master_instance` before calling
        super().

        Used e.g. by :class:`lino_xl.lib.outbox.models.MyOutbox` or
        :class:`lino.modlib.users.ByUser`.

        Other usages are more hackerish:

        - :class:`lino_xl.lib.households.models.SiblingsByPerson`
        - :class:`lino_welfare.modlib.cal.EntriesByClient`
        - :class:`lino_welfare.pcsw.models.Home`,
        - :class:`lino.modlib.users.MySettings`.

        """
        pass

    @classmethod
    def setup_parameters(cls, params):
        """Inheritable hook for defining parameters. Called once per actor at
        site startup.  The default implementation just calls
        :meth:`setup_parameters
        <lino.core.model.Model.setup_parameters>` of the
        :attr:`model` (if a :attr:`model` is set).

        """
        if cls.has_db_model():
            cls.model.setup_parameters(params)

    @classmethod
    def get_simple_parameters(cls):
        if cls.has_db_model():
            return cls.model.get_simple_parameters()
        return []

    @classmethod
    def get_param_elem(self, name):
        # same as in Parametrizable, but here it is a class method
        if self.parameters:
            return self.parameters.get(name, None)
        return None

    @classmethod
    def check_params(cls, pv):
        # same as in Parametrizable, but here it is a class method
        if isinstance(cls.parameters, ParameterPanel):
            return cls.parameters.check_values(pv)

    @classmethod
    def get_row_state(self, obj):
        if self.workflow_state_field is not None:
            return getattr(obj, self.workflow_state_field.name)
            # ~ if isinstance(state,choicelists.Choice):
            # ~ state = state.value

    @vfields.displayfield(_("Description"))
    def detail_link(cls, obj, ar):
        """
        A single-paragraph of formatted text that describes this :term:`database
        row`.

        It should begin with a clickable link that opens the :term:`detail
        window`.

        This is a :term:`htmlbox`. We don't recommend to override this field
        directly.
        """

        if False:  # until 20240504
            text = ar.obj2htmls(obj)
        else:
            # text = obj.as_paragraph(ar)
            text = cls.row_as_paragraph(ar, obj)
            # text = tostring(obj.as_summary_item(ar))
            # assert_safe(text)
            # return text
        return format_html("<div>{}</div>", text)

    @classmethod
    def override_column_headers(self, ar, **headers):
        """A hook to dynamically override the column headers. This has no
        effect on a GridPanel, only in printed documents or plain
        html.

        """
        if self.model is None:
            return headers
        return self.model.override_column_headers(ar, **headers)

    @classmethod
    def get_sum_text(self, ar, sums):
        return str(_("Total (%d rows)") % ar.get_total_count())

    @classmethod
    def get_layout_aliases(cls):
        """
        Yield a series of (ALIAS, repl) tuples that cause a name ALIAS in a
        layout based on this actor to be replaced by its replacement `repl`.
        """
        if cls.model is None:
            return []
        return cls.model.get_layout_aliases()

    @classmethod
    def set_detail_layout(self, *args, **kw):
        """Update the :attr:`detail_layout` of this actor, or create a new
        layout if there wasn't one before.

        This is maybe deprecated. See :ticket:`526`.

        The first argument can be either a string or a
        :class:`FormLayout <lino.core.layouts.FormLayout>` instance.
        If it is a string, it will replace the currently defined
        'main' panel.  With the special case that if the current `main`
        panel is horizontal (i.e. the layout has tabs), it replaces the
        'general' tab.

        Typical usage example::

            @dd.receiver(dd.post_analyze)
            def my_details(sender, **kw):
                contacts = sender.modules.contacts
                contacts.Partners.set_detail_layout(PartnerDetail())

        """
        return self.set_form_layout("detail_layout", DetailLayout, *args, **kw)

    @classmethod
    def set_insert_layout(self, *args, **kw):
        """
        Update the :attr:`insert_layout` of this actor,
        or create a new layout if there wasn't one before.

        Otherwise same usage as :meth:`set_detail_layout`.

        """
        return self.set_form_layout("insert_layout", InsertLayout, *args, **kw)

    @classmethod
    def set_form_layout(self, attname, lcl, dtl=None, **kw):
        if dtl is not None:
            existing = getattr(self, attname)  # 20120914c
            if is_string(dtl):
                # if isinstance(dtl, string_types):
                if existing is None:
                    setattr(self, attname, lcl(dtl, self, **kw))
                    # if existing is None or isinstance(existing, string_types):
                    #     if kw:
                    #         setattr(self, attname, layouts.FormLayout(
                    #             dtl, self, **kw))
                    #     else:
                    #         setattr(self, attname, dtl)
                    return
                if "\n" in dtl and "\n" not in existing.main:
                    name = "general"
                else:
                    name = "main"
                if name in kw:
                    raise Exception(
                        "set_form_layout() got two definitions for %r." % name)
                kw[name] = dtl
            else:
                if not isinstance(dtl, lcl):
                    msg = f"{repr(dtl)} is neither a string nor a layout"
                    raise Exception(msg)
                assert dtl._datasource is None

                # added for 20120914c but it wasn't the problem
                # if existing and not isinstance(existing, string_types):
                if existing and not is_string(existing):
                    if settings.SITE.strict_dependencies:
                        if not isinstance(dtl, existing.__class__):
                            raise Exception(
                                "Cannot replace existing %s %r by %r"
                                % (attname, existing, dtl)
                            )
                    if existing._added_panels:
                        if "\n" in dtl.main:
                            raise NotImplementedError(
                                "Cannot replace existing %s with added panels %s"
                                % (existing, existing._added_panels)
                            )
                        dtl.main += " " + (
                            " ".join(list(existing._added_panels.keys()))
                        )
                        # ~ logger.info('20120914 %s',dtl.main)
                        dtl._added_panels.update(existing._added_panels)
                    dtl._element_options.update(existing._element_options)
                dtl._datasource = self
                setattr(self, attname, dtl)

            # The following tests added for :ref:`book.changes.20250523`:
            if (kernel := settings.SITE.kernel) is not None:
                if (front_end := kernel.editing_front_end) is not None:
                    hname = front_end.ui_handle_attr_name
                    # we do not want any inherited handle
                    h = existing.__dict__.get(hname, None)
                    if h is not None:
                        raise Exception(
                            f"{existing} has already a layout handle {h.ui}")

            if kw:
                getattr(self, attname).update(**kw)

    @classmethod
    def add_detail_panel(self, *args, **kw):
        """
        Adds a panel to the Detail of this actor.
        Arguments: see :meth:`lino.core.layouts.BaseLayout.add_panel`

        This is deprecated. Use mixins instead.

        """
        self.detail_layout.add_panel(*args, **kw)

    @classmethod
    def add_detail_tab(self, *args, **kw):
        """
        Adds a tab panel to the Detail of this actor.
        See :meth:`lino.core.layouts.BaseLayout.add_tabpanel`

        This is deprecated. Use mixins instead.

        """
        if self.detail_layout is None:
            raise Exception("{} has no detail_layout".format(self))
        self.detail_layout.add_tabpanel(*args, **kw)

    @classmethod
    def add_virtual_field(cls, name, vf):
        if False:
            # disabled because UsersWithClients defines virtual fields
            # on connection_created
            if name in cls.virtual_fields:
                raise Exception(
                    "Duplicate add_virtual_field() %s.%s" % (cls, name))
        # assert vf.model is None
        # if vf.model is not None:
        #     # inherit from parent actor
        #     vf = copy.deepcopy(vf)
        # if name in cls.virtual_fields:
        #     old = cls.virtual_fields[name]
        #     if old is not vf:
        #         print("20190102 {} of {} replaces {} by {}".format(name, cls, old, vf))
        if vf.model is None:
            vf.model = cls
        elif not issubclass(cls, vf.model):
            msg = "20190201 Cannot add field {} defined in {} to {}"
            msg = msg.format(name, vf.model, cls)
            # print(msg)
            raise Exception(msg)
        vf.name = name
        # vf.attname = name
        cls.virtual_fields[name] = vf

        # ~ vf.lino_resolve_type(cls,name)
        # vf.get = vf.get
        # vf.get = curry(vf.get, cls)
        # vf.get = classmethod(vf.get)
        # vf.get = curry(classmethod(vf.get), cls)
        # ~ for k,v in self.virtual_fields.items():
        # ~ if isinstance(v,models.ForeignKey):
        # ~ v.rel.model = resolve_model(v.rel.model)

    @classmethod
    def add_constant(cls, name, vf):
        cls._constants[name] = vf
        vf.name = name

    @classmethod
    def after_site_setup(cls, site):
        # print(f"20250523 after_site_setup {cls}")
        self = cls
        # ~ raise "20100616"
        # ~ assert not self._setup_done, "%s.setup() called again" % self
        if self._setup_done:
            return True
        if self._setup_doing:
            if True:  # severe error handling
                raise Exception("%s.setup() called recursively" % self)
            else:
                logger.warning("%s.setup() called recursively" % self)
                return False
        self._setup_doing = True

        # logger.info("20181230 Actor.after_site_setup() %r", self)

        for vf in self.virtual_fields.values():
            if vf.model is self:
                vf.get = curry(vf.get, self)
                # settings.SITE.register_virtual_field(vf)

        if not self.is_abstract():
            register_params(self)
            # if self.parameters is not None:
            #     assert isinstance(self.params_layout, self._params_layout_class)
            #     print(f"20250523 params_layout ok for {repr(self)}")
            self._collect_actions()

        if not self.is_abstract():
            setup_params_choosers(self)

        # ~ logger.info("20130906 Gonna Actor.do_setup() on %s", self)
        self.do_setup()
        # ~ self.setup_permissions()
        self._setup_doing = False
        self._setup_done = True
        # ~ logger.info("20130906 Actor.after_site_setup() done: %s, default_action is %s",
        # ~ self.actor_id,self.default_action)
        return True

    @classmethod
    def get_action_by_name(self, name):
        return self._actions_dict.get(name, None)

    get_url_action = get_action_by_name

    @classmethod
    def get_url_action_names(self):
        return list(self._actions_dict.keys())

    @classmethod
    def get_toolbar_actions(self, parent, user_type):
        for ba in self.get_button_actions(parent):
            if ba.action.show_in_toolbar and ba.get_view_permission(user_type):
                if ba.action.readonly or not self.hide_editing(user_type):
                    yield ba

    # @classmethod
    # def get_cell_context_actions(self, cf):
    #     cca = dict()
    #     for col in self.columns:
    #         if it is a FK field::
    #             f = col.editor
    #             cca[f.name] = f.rel.to.detail_action
    #     return cca

    @classmethod
    def get_button_actions(self, parent):
        if not parent.opens_a_window:
            # return []
            raise Exception(
                "20180518 {} is not a windows action".format(parent.__class__)
            )
        return [ba for ba in self._actions_list if ba.action.is_callable_from(parent)]

    @classmethod
    def get_actions(self):
        return self._actions_list

    @classmethod
    def make_chooser(cls, wrapped):
        return classmethod(wrapped)

    @classmethod
    def get_detail_layout(cls):
        assert cls.detail_action is not None
        wl = cls.detail_action.get_window_layout()
        return wl.get_layout_handle()

    @classmethod
    def get_grid_layout(cls, *args):
        assert cls.default_action is not None
        ah = cls.get_handle()
        return ah.get_grid_layout()

    @classmethod
    def get_detail_elems(cls):
        """
        Return a list of the widgets (layout elements) that make up
        the detail layout.

        An optional first argument is the front end plugin, a
        :class:`Plugin` instance.  If this is None, use
        :attr:`settings.SITE.kernel.web_front_ends
        <lino.core.kernel.Kernel.web_front_ends>`.

        """
        lh = cls.get_detail_layout()
        return lh.main.elements

    @classmethod
    def get_extra_layouts(cls):
        return {}

    @classmethod
    def get_data_elem(self, name):
        """Find data element in this actor by name."""
        # Note that there are models with fields named 'master', 'app_label',
        # 'model' (i.e. a name that is also used as attribute of an actor.

        c = self._constants.get(name, None)
        if c is not None:
            return c
        # ~ return self.virtual_fields.get(name,None)

        for cls in getmro(self):
            if hasattr(cls, "virtual_fields"):
                vf = cls.virtual_fields.get(name, None)
                if vf is not None:
                    # ~ logger.info("20120202 Actor.get_data_elem found vf %r",vf)
                    return vf

        # Replacing above code block with the code below is theoretically the
        # same but in reality causes #5739 (Oops, get_atomizer(...) returned
        # None) to reappear in projects/noi1r/tests/test_notify.py:

        # vf = self.virtual_fields.get(name, None)
        # if vf is not None:
        #     # ~ logger.info("20120202 Actor.get_data_elem found vf %r",vf)
        #     return vf

        if self.model is not None:
            de = self.model.get_data_elem(name)
            if de is not None:
                return de

        # if len(self.extra_fields):
        #     ef = self.extra_fields.get(name)
        #     if ef:
        #         return ef

        a = getattr(self, name, None)
        if isinstance(a, Action):
            return a
        # if isinstance(a, fields.VirtualField):
        #     return a
        if isinstance(a, vfields.DummyField):
            return a

        # if a is not None:
        #     raise Exception("20240428 unhandled attribute {}={}".format(name, a))

        # cc = AbstractTable.get_data_elem(self,name)

        # ~ logger.info("20120307 lino.core.coretools.get_data_elem %r,%r",self,name)
        s = name.split(".")
        # site = settings.SITE
        if len(s) == 1:
            m = settings.SITE.models.get(self.app_label)
            if m is None:
                raise Exception(
                    "No plugin {} ({}.{})".format(self.app_label, self, name)
                )
                # return None
            rpt = getattr(m, name, None)
            # print("20240428a", name, rpt)
            # if rpt is None and name != name.lower():
            #     raise Exception("20140920 No %s in %s" % (name, m))
        elif len(s) == 2:
            m = settings.SITE.models.get(s[0])
            if m is None:
                # return fields.DummyField()
                # 20130422 Yes it was a nice idea to silently
                # ignore non installed app_labels, but mistakenly
                # specifying "person.first_name" instead of
                # "person__first_name" did not raise an error...
                # raise Exception("No plugin %s is installed" % s[0])
                # See docs/specs/welfare/xcourses.rst
                return None
            rpt = getattr(m, s[1], None)
            # print("20240428b", name, rpt)
        else:
            raise Exception("Invalid data element name %r" % name)
        return rpt

    @classmethod
    def param_defaults(self, ar, **kw):
        """
        Return a dict with default values for the :attr:`parameters`.
        This will be called per request.

        Usage example. The Clients table has a parameter `coached_since`
        whose default value is empty::

          class Clients(dd.Table):
              parameters = dd.ParameterPanel(
                ...
                coached_since=models.DateField(blank=True))

        But `NewClients` is a subclass of `Clients` with the only
        difference that the default value is `amonthago`::

          class NewClients(Clients):
              @classmethod
              def param_defaults(self, ar, **kw):
                  kw = super().param_defaults(ar, **kw)
                  kw.update(coached_since=amonthago())
                  return kw


        """
        if self.parameters:
            for k, pf in self.parameters.items():
                # if not isinstance(pf, fields.DummyField):
                kw[k] = pf.get_default()
        if self.model is not None:
            kw = self.model.param_defaults(ar, **kw)
        return kw

    # @classmethod
    # def get_parent_links(cls, ar):
    #     if cls.model is not None:
    #         for pl in cls.model.get_parent_links(ar):
    #             yield pl
    #     # if (mi := ar.master_instance) is not None:
    #     #     yield ar.obj2htmls(mi, str(mi))

    @classmethod
    def request(cls, *args, **kwargs):
        """
        Old name for :meth:`create_request`. Still does the same but with a
        deprecation warning.
        """
        warnings.warn(
            "Please call create_request() instead of request()", DeprecationWarning)
        return cls.create_request(*args, **kwargs)

    @classmethod
    def create_request(cls, master_instance=None, **kwargs):
        """Return a new :class:`ActionRequest
        <lino.core.requests.ActionRequest>` on this actor.

        The :attr:`master_instance
        <lino.core.requests.ActionRequest.master_instance>` can be
        specified as optional first positional argument.

        """
        from lino.core.requests import ActionRequest
        kwargs.update(actor=cls)
        kwargs.setdefault("action", cls.default_action)
        if master_instance is not None:
            kwargs.update(master_instance=master_instance)
        # kw.setdefault("renderer", settings.SITE.kernel.text_renderer)
        return ActionRequest(**kwargs)

    # @classmethod
    # def show(cls, master_instance=None, renderer=None, **kwargs):
    #     if renderer is None:
    #         renderer = settings.SITE.kernel.text_renderer
    #     ar = cls.request(master_instance, renderer=renderer)
    #     ar.show(**kwargs)

    @classmethod
    def to_html(self, **kw):
        return tostring(self.create_request(**kw).table2xhtml())

    @classmethod
    def get_screenshot_requests(self, language):
        """
        Return or yield a list of screenshots to generate for this actor.
        Not yet stable. Don't override this.
        """
        return []

    @classmethod
    def slave_as_html(cls, master, ar):
        """
        Execute this slave view on the given master and render it as plain html.
        Used when :attr:`display_mode` is ``DISPLAY_MODE_HTML``.
        """
        kwargs = dict(is_on_main_actor=False)
        if getattr(cls, "use_detail_params_value", False):
            kwargs.update(param_values=ar.param_values)
        # print(f"20240914 slave_as_html() {ar.request}")

        # 20240911 We don't want to re-parse the original request, especially
        # because it might contain disturbing things like selected_pks. But the
        # slave must at least inherit the user, as shown in
        # welfare/docs/specs/weleup/weleup1r.rst
        # kwargs.update(request=ar.request)
        kwargs.update(parent=ar)

        # 20251012 I removed the following line because tables in publisher
        # should have attrib filled from publisher, not from react:
        # kwargs.update(renderer=settings.SITE.kernel.default_renderer)

        try:
            ar = cls.create_request(master_instance=master, **kwargs)
            el = cls.table_as_html(ar)
        except Exception as e:
            msg = f"20241004 Error in {repr(ar)}: {e}"
            raise Exception(msg) from e
            logger.warning(msg)
            return msg
        return el

    # summary_sep = "<br/>"
    summary_sep = mark_safe(", ")

    @classmethod
    def get_table_as_list(cls, obj, ar):
        # raise Exception("20240316")
        sar = cls.create_request(parent=ar, master_instance=obj,
                                 is_on_main_actor=False)
        grp = Grouper(sar)
        html_text = grp.begin()
        limit = ar.limit or cls.preview_limit
        for i, obj in enumerate(sar.data_iterator):
            if i == limit:
                break
            par = sar.row_as_paragraph(obj)  # 20230207
            # assert_safe(par)  # temporary 20240506
            # 202405056 par = sar.add_detail_link(obj, par)
            par = format_html('<p class="clearfix">{}</p>', par)
            # url = sar.obj2url(obj)
            # if url is not None:
            #     url = html.escape(url)
            #     # par += ' <a href="{}">(Detail)</a>'.format(url)
            #     par = '<a href="{}">{}</a>'.format(url, par)
            # else:  # a funny way to debug:
            #     par = '<a href="{}">{}</a>'.format(str(sar.renderer), par)

            html_text += grp.before_row(obj)
            html_text += par
            html_text += grp.after_row(obj)
        html_text += grp.stop()

        # 20250713
        # if len(toolbar := sar.plain_toolbar_buttons()):
        #     p = mark_safe(btn_sep.join([tostring(b) for b in toolbar]))
        #     html_text = p + html_text

        # if cls.editable and cls.insert_action is not None:
        #     ir = cls.insert_action.request_from(sar)
        #     if ir.get_permission():
        #         # html_text = mark_safe(tostring(ir.ar2button()) + html_text)
        #         html_text = tostring(ir.ar2button()) + html_text

        # assert_safe(html_text)  # temporary 20240506
        return format_html(DIVTPL, html_text)

    @classmethod
    def get_table_as_tiles(cls, obj, ar):
        sar = cls.create_request(parent=ar, master_instance=obj,
                                 is_on_main_actor=False)
        tiles = SAFE_EMPTY
        prev = None
        limit = ar.limit or cls.preview_limit
        for i, obj in enumerate(sar.data_iterator):
            if i == limit:
                break
            tiles += obj.as_tile(sar, prev)
            prev = obj
        return format_html(constants.TILES_CONTAINER_TEMPLATE, tiles=tiles)
        # return mark_safe(tiles)

    @classmethod
    def get_table_story(cls, obj, ar):
        sar = cls.create_request(parent=ar, master_instance=obj,
                                 is_on_main_actor=False)
        html = SAFE_EMPTY
        limit = ar.limit or cls.preview_limit
        for i, obj in enumerate(sar.data_iterator):
            if i == limit:
                break
            s = obj.as_story_item(sar)
            # assert_safe(s)  # temporary 20240506
            html += s
        if cls.insert_action is not None:
            if not cls.editable:
                return html
            ir = cls.insert_action.request_from(sar)
            if ir.get_permission():
                html = tostring(ir.ar2button()) + html
        # assert_safe(html)  # temporary 20240506
        return html

    @classmethod
    def get_slave_summary(cls, obj, ar=None):
        """
        :param cls: Slave table
        :param obj: Master instance
        :param ar: Action request on master table
        """
        if ar is None:
            return ''
        sar = cls.create_request(parent=ar, master_instance=obj,
                                 is_on_main_actor=False)
        return cls.get_table_summary(sar)

    @classmethod
    def get_table_summary(cls, ar):
        """
        Return the HTML `<div>` to be displayed by
        :class:`lino.core.elems.TableSummaryPanel`.
        It basically just calls :meth:`table_as_summary`.

        """
        p = cls.table_as_summary(ar)
        # assert_safe(p)  # temporary 20240506
        # print("20240712", p)
        # return format_html(DIVTPL, p)
        return mark_safe(DIVTPL.format(p))

    @classmethod
    def table_as_summary(cls, ar):
        """
        Return a HTML-formatted text that summarizes this table in a few
        paragraphs.

        The default implementation return s a comma-separated list of the rows,
        followed by the `plain toolbar buttons`.

        Application developers can override this method to customize the summary
        view.

        See :ref:`dev.table_summaries`.

        """
        p = qs2summary(
            ar,
            ar.sliced_data_iterator,
            separator=cls.summary_sep,
            max_items=ar.limit or cls.preview_limit,
            wraptpl=None,
        )
        # assert isinstance(p, str)
        # assert_safe(p)  # temporary 20240506
        # assert not "&lt;" in p
        # No toolbar needed after 20250714 #6202 ("Tickets to work" has its
        # insert button (+) duplicated in the dashboard):
        # toolbar = ar.plain_toolbar_buttons()
        # if len(toolbar):
        #     # p += "<br/>"
        #     # p += " | "
        #     if p:
        #         p += cls.summary_sep
        #     for b in toolbar:
        #         p += tostring(b) + btn_sep
        return p

    @classmethod
    def table_as_html(cls, ar):
        """
        Return an ElementTree element that represents the given action
        request `ar` on this actor in :term:`display mode` "HTML".

        An :term:`application developer` may override this method. Usage example
        is :class:`lino_prima.lib.prima.PupilsAndProjects`.

        """
        el = ar.table2xhtml()
        if len(toolbar := ar.plain_toolbar_buttons()):
            el = E.div(el, E.p(*toolbar))
        return el

    @classmethod
    def columns_to_paragraph(cls, self, ar=None, fmt=None):
        """
        Represent the given row as a paragraph with a comma-separated list of
        the values of the fields in the column_names of this actor.
        """
        if ar is None:
            return str(self)
        # cols = ar.actor.get_detail_layout().main
        cols = cls.get_grid_layout().main.columns
        cols = [c for c in cols if not c.value.get("hidden")]
        if fmt is None:

            def fmt(obj, col):
                # return str(type(col))
                v = col.value_from_object(obj, ar)
                if v is None:
                    return None
                else:
                    try:
                        v = col.format_value(ar, v)
                    except Exception as e:
                        # v = "{} in {}".format(e, col.name)
                        return col.name + "?!"
                # return v
                return "{}:{}".format(col.get_label(), v)

        values = [fmt(self, c) for c in cols]
        values = [v for v in values if v is not None]
        s = ", ".join(values)
        # s = str(ar.actor)
        # print("20231218", s)  # self, ar.actor.get_grid_layout().main.columns)
        return s

    @classmethod
    def error2str(self, e):
        from lino.core.utils import error2str
        return error2str(self, e)
