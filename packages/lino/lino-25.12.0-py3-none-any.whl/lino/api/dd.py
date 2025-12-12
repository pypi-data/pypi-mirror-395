# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from lino.modlib.linod.choicelists import background_task, schedule_often, schedule_daily
import time
from importlib import import_module
from django.db.models import *
from django.utils import translation
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.dispatch import receiver
from django.db.backends.signals import connection_created
from django.db.models.signals import class_prepared
from django.db.models.signals import pre_init, post_init
from django.db.models.signals import pre_save, post_save

from lino.core.base import Action
from lino.core.tables import VentilatingTable
from lino.core.frames import Frame
from django.core.exceptions import FieldDoesNotExist
from lino.core.dbtables import Table
from lino.core.dbtables import has_fk
from lino.core.actors import Actor
from lino.core.merge import MergeAction
from lino.core.model import Model
from lino.core.utils import full_model_name
from lino.core.utils import overlap_range_filter
from lino.core.utils import inrange_filter
from lino.core.utils import range_filter
from lino.core.utils import obj2unicode
from lino.core.utils import obj2str
from lino.core.utils import resolve_field, get_field
from lino.core.utils import resolve_app
from lino.core.utils import resolve_model, UnresolvedModel
from lino.core.tables import VirtualTable
from lino import logger
from lino.utils.fieldutils import get_fields, fields_help
from lino.utils.format_date import fdl as dtosl
from lino.utils.mldbc.fields import BabelTextField
from lino.utils.mldbc.fields import BabelCharField, LanguageField
from lino.modlib.system.choicelists import Genders, PeriodEvents, YesNo
from lino.core.roles import SiteStaff, SiteUser, SiteAdmin, login_required
from lino.core.actions import WrappedAction
from lino.core.actions import MultipleRowAction
from lino.core.actions import ShowSlaveTable
from lino.core.actions import ShowTable, ShowDetail
from lino.core.actions import ShowInsert, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
from lino.core.actions import ShowEditor
from lino.core.choicelists import ChoiceList, Choice
from lino.core.workflows import State, Workflow, ChangeStateAction
from lino.core.fields import ImportedFields
from lino.core.fields import fields_list
from lino.core.fields import Dummy, DummyField
from lino.core.fields import TimeField
from lino.core.fields import TableRow
from lino.core.fields import CustomField
from lino.core.fields import RecurrenceField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DatePickerField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import PercentageField
from lino.core.fields import QuantityField
from lino.core.fields import DurationField
from lino.core.fields import HtmlBox, PriceField, RichTextField
from lino.core.fields import DisplayField, displayfield, htmlbox, delayedhtmlbox
from lino.core.fields import VirtualField, virtualfield
from lino.core.fields import VirtualBooleanField
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant, constant
from lino.utils.format_date import fdtl, fdtf
from lino.utils.format_date import fds as fds_
from lino.utils.format_date import fdm, fdl, fdf, fdmy
from lino.utils import IncompleteDate, read_exception
from lino.core.utils import PseudoRequest
from lino.core.params import ParameterPanel
from lino.core.inject import do_when_prepared, when_prepared
from lino.core.inject import inject_quick_add_buttons
from lino.core.inject import update_field
from lino.core.inject import update_model
from lino.core.inject import inject_field
from lino.core.inject import inject_action
from lino.core.signals import post_delete, pre_delete
from lino.core.signals import pre_ui_build
from lino.core.signals import post_ui_save
from lino.core.signals import pre_ui_save
from lino.core.signals import pre_remove_child
from lino.core.signals import pre_add_child
from lino.core.signals import pre_merge
from lino.core.signals import auto_create
from lino.core.signals import post_analyze
from lino.core.signals import pre_analyze
from lino.core.signals import pre_startup, post_startup
from lino.core.signals import on_ui_created, pre_ui_delete, on_ui_updated
from lino.core.layouts import DummyPanel
from lino.core.layouts import ParamsLayout, ActionParamsLayout
from lino.core.layouts import DetailLayout, InsertLayout
from lino.core.utils import Panel
from lino.utils.choosers import chooser, action_chooser
from lino.core.utils import babel_values
from lino.core.utils import babelkw
from lino.core.fields import CharField
from lino.core.vfields import ForeignKey, OneToOneField

# import types
# assert type(ForeignKey) is types.FunctionType  # 20251128
# print(20251128, Model)
# assert type(Model.collect_virtual_fields) is types.MethodType  # 20251128


# import logging ; logger = logging.getLogger(__name__)

# logger.info("20140227 dd.py a")

# from asgiref.sync import sync_to_async


action = Action.decorate


# 20140314 need a Dummy object to define a dummy module
# from lino.core.layouts import BaseLayout as Dummy  # 20140314
# from lino.core.actors import Actor as Dummy  # 20140314


# from lino.core.fields import NullCharField

# ~ from lino.core.fields import LinkedForeignKey


# from lino.core.fields import DisplayField, displayfield, htmlbox

# from lino_xl.lib.appypod.mixins import PrintTableAction


# from lino.core.utils import babelattr
# alias for babelkw for backward compat


# from lino.core.layouts import FormLayout


# from lino.core.signals import database_connected
# from lino.core.signals import post_ui_build


# ~ from lino.core import signals


def fds(d):
    if isinstance(d, IncompleteDate):
        return fds_(d.as_date())
    return fds_(d)


# backward compatibility
dtos = fds

babelitem = settings.SITE.babelitem
field2kw = settings.SITE.field2kw
# urlkwargs = settings.SITE.urlkwargs


decfmt = settings.SITE.decfmt
str2kw = settings.SITE.str2kw
str2dict = settings.SITE.str2dict
now = settings.SITE.now
# today = settings.SITE.today  # see below
strftime = settings.SITE.strftime
demo_date = settings.SITE.demo_date
is_abstract_model = settings.SITE.is_abstract_model
is_installed = settings.SITE.is_installed
is_hidden_plugin = settings.SITE.is_hidden_plugin
resolve_plugin = settings.SITE.resolve_plugin
get_plugin_setting = settings.SITE.get_plugin_setting
add_welcome_handler = settings.SITE.add_welcome_handler
build_media_url = settings.SITE.build_media_url
build_static_url = settings.SITE.build_static_url
get_default_language = settings.SITE.get_default_language
get_language_info = settings.SITE.get_language_info
resolve_languages = settings.SITE.resolve_languages
babelattr = settings.SITE.babelattr
plugins = settings.SITE.plugins
format_currency = settings.SITE.format_currency


def today(*args, **kwargs):
    # make it serializable for Django migrations
    return settings.SITE.today(*args, **kwargs)


get_language = translation.get_language


def auto_height(n):
    """
    When specifying a `window_size`, the `height` should often be ``'auto'``,
    but extjs dopesn't support auto  height with text editor widget.
    """
    if settings.SITE.default_ui == "lino_react.react":
        return "auto"
    else:
        return n
