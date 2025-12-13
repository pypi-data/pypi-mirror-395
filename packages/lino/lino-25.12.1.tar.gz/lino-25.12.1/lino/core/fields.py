# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines extended database field classes and utility functions
related to fields.
"""

#fmt: off

import datetime
from decimal import Decimal

from django import http
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.core.exceptions import ValidationError
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import NOT_PROVIDED
from django.utils.functional import cached_property

from lino import logger
from lino.utils.html import tostring, SafeString, escape, mark_safe, format_html

from lino.core.exceptions import ChangedAPI
from lino.core.diff import ChangeWatcher
from lino.core import constants

from lino.utils import isiterable
from lino.utils import IncompleteDate
from lino.utils import quantities
from lino.utils.quantities import Duration

from .signals import pre_ui_save
from .utils import use_as_wildcard
# from .fields import (
#     set_default_verbose_name, validate_incomplete_date,  PasswordField,
#     RichTextField, PreviewTextField, PercentageField, TimeField,
#     DatePickerField, MonthField, PriceField, CharField, QuantityField, DurationField,
#     IncompleteDateField, RecurrenceField,
#     OneToOneField, ForeignKey, CustomField
# )
from .vfields import Dummy, DummyField, ForeignKey, OneToOneField, Constant, constant
from .vfields import (
    RemoteField,
    VirtualField, virtualfield, DisplayField, displayfield,
    HtmlBox, htmlbox, DelayedHtmlBox, delayedhtmlbox,
    VirtualBooleanField, RequestField, requestfield,
    TableRow, wildcard_data_elems,
    fields_list, TableRow, ImportedFields)

from .params import ParameterPanel


def validate_incomplete_date(value):
    """Raise ValidationError if user enters e.g. a date 30.02.2009."""
    try:
        value.as_date()
    except ValueError:
        raise ValidationError(_("Invalid date"))


class PasswordField(models.CharField):
    """Stored as plain text in database, but not displayed in user
    interface.

    """

    pass


class RichTextField(models.TextField):
    # See :doc:`/dev/textfield`.

    def __init__(self, *args, **kw):
        # textfield_format was still accepted for backward compatibility
        # self.format = kw.pop('format', kw.pop('textfield_format', None))
        self.format = kw.pop("format", None)
        self.bleached = kw.pop("bleached", None)
        super().__init__(*args, **kw)

    def set_format(self, fmt):
        self.format = fmt


class PreviewTextField(RichTextField):
    pass


class PercentageField(models.DecimalField):
    """
    A field to express a percentage.
    The database stores this like a DecimalField.
    Plain HTML adds a "%".
    """

    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=0,
        )
        defaults.update(kwargs)
        super().__init__(*args, **defaults)


class TimeField(models.TimeField):
    """
    Like a TimeField, but allowed values are between
    :attr:`calendar_start_hour
    <lino.core.site.Site.calendar_start_hour>` and
    :attr:`calendar_end_hour <lino.core.site.Site.calendar_end_hour>`.
    """

    pass


class DatePickerField(models.DateField):
    """
    A DateField that uses a DatePicker instead of a normal DateWidget.
    Doesn't yet work.
    """

    pass


class MonthField(models.DateField):
    """
    A DateField that uses a MonthPicker instead of a normal DateWidget
    """

    pass
    # def __init__(self, *args, **kw):
    #     models.DateField.__init__(self, *args, **kw)


# def PriceField(*args, **kwargs):
#     defaults = dict(
#         max_length=10,
#         max_digits=10,
#         decimal_places=2,
#     )
#     defaults.update(kwargs)
#     return models.DecimalField(*args, **defaults)


class PriceField(models.DecimalField):
    """
    A thin wrapper around Django's `DecimalField
    <https://docs.djangoproject.com/en/5.2/ref/models/fields/#decimalfield>`_
    with price-like default values for `decimal_places`, `max_length` and
    `max_digits`.
    """

    # def __init__(self, verbose_name=None, max_digits=10, **kwargs):
    #     defaults = dict(
    #         max_length=max_digits,
    #         max_digits=max_digits,
    #         decimal_places=2,
    #     )
    #     defaults.update(kwargs)
    #     super().__init__(verbose_name, **defaults)

    def __init__(self, verbose_name=None, max_digits=10, **kwargs):
        defaults = dict(
            max_digits=max_digits,
            decimal_places=2,
        )
        defaults.update(kwargs)
        super().__init__(verbose_name, **defaults)




# ~ class MyDateField(models.DateField):

# ~ def formfield(self, **kwargs):
# ~ fld = super(MyDateField, self).formfield(**kwargs)
# ~ # display size is smaller than full size:
# ~ fld.widget.attrs['size'] = "8"
# ~ return fld
"""
https://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
answer Dec 20 '09 at 3:40 by mightyhal
https://stackoverflow.com/a/1934764
"""

# class NullCharField(models.CharField):  # subclass the CharField
#     description = "CharField that stores empty strings as NULL instead of ''."

#     def __init__(self, *args, **kwargs):
#         defaults = dict(blank=True, null=True)
#         defaults.update(kwargs)
#         super(NullCharField, self).__init__(*args, **defaults)

#     # this is the value right out of the db, or an instance
#     def to_python(self, value):
#         # ~ if isinstance(value, models.CharField): #if an instance, just return the instance
#         if isinstance(value, six.string_types):  # if a string, just return the value
#             return value
#         if value is None:  # if the db has a NULL (==None in Python)
#             return ''  # convert it into the Django-friendly '' string
#         else:
#             return value  # otherwise, return just the value

#     def get_db_prep_value(self, value, connection, prepared=False):
#         # catches value right before sending to db
#         # if Django tries to save '' string, send the db None (NULL)
#         if value == '':
#             return None
#         else:
#             return value  # otherwise, just pass the value


class CharField(models.CharField):
    """
    An extension of Django's `models.CharField`.

    Adds two keywords `mask_re` and `strip_chars_re` which, when using
    the ExtJS front end, will be rendered as the `maskRe` and `stripCharsRe`
    config options of `TextField` as described in the `ExtJS
    documentation
    <https://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.TextField>`__,
    converting naming conventions as follows:

    =============== ============ ==========================
    regex           regex        A JavaScript RegExp object to be tested against the field value during validation (defaults to null). If the test fails, the field will be marked invalid using regexText.
    mask_re         maskRe       An input mask regular expression that will be used to filter keystrokes that do not match (defaults to null). The maskRe will not operate on any paste events.
    strip_chars_re  stripCharsRe A JavaScript RegExp object used to strip unwanted content from the value before validation (defaults to null).
    =============== ============ ==========================

    Example usage::

      belgian_phone_no = dd.CharField(max_length=15, strip_chars_re='')

    """

    def __init__(self, *args, **kw):
        self.strip_chars_re = kw.pop("strip_chars_re", None)
        self.mask_re = kw.pop("mask_re", None)
        self.regex = kw.pop("regex", None)
        super().__init__(*args, **kw)


class QuantityField(models.CharField):
    """
    A field that accepts :class:`Quantity
    <lino.utils.quantities.Quantity>`, :class:`Percentage
    <lino.utils.quantities.Percentage>` and :class:`Duration
    <lino.utils.quantities.Duration>` values.

    Implemented as a CharField, which means that
    sorting or filter ranges may not work as expected,
    and you cannot use SUM or AVG agregators on quantity fields
    since the database does not know how to calculate sums from them.

    When you set `blank=True`, then you should also set `null=True`.

    """

    description = _("Quantity (Decimal or Duration)")
    # overflow_value = None

    def __init__(self, *args, **kw):
        kw.setdefault("max_length", settings.SITE.quantity_max_length)
        super().__init__(*args, **kw)
        if self.blank and not self.null:
            raise ChangedAPI(
                "When `blank` is True, `null` must be True as well.")

    # ~ def get_internal_type(self):
    # ~ return "CharField"

    def to_python(self, value):
        """
        Excerpt from `Django docs
        <https://docs.djangoproject.com/en/5.2/howto/custom-model-fields/#converting-values-to-python-objects>`__:

            As a general rule, :meth:`to_python` should deal gracefully with
            any of the following arguments:

            - An instance of the correct type (e.g., `Hand` in our ongoing example).
            - A string (e.g., from a deserializer).
            - `None` (if the field allows `null=True`)

        I'd add "Any value allowed for this field when instantiating a model."

        """
        if isinstance(value, quantities.Quantity):
            return value
        elif isinstance(value, Decimal):
            return quantities.Quantity(value)
        elif isinstance(value, str):
            return quantities.parse(value)
        elif value:
            # try:
            return quantities.Quantity(value)
            # except Exception as e:
            #     raise ValidationError(
            #         "Invalid value {} for {} : {}".format(value, self, e))
        return None

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)
        # if value is None or value == '':
        #     return self.get_default()
        # return quantities.parse(value)

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     return str(value) if value else ''

    def get_prep_value(self, value):
        if value is None:
            return ""
        return str(value)  # if value is None else ''

    def clean(self, raw_value, obj):
        # if isinstance(raw_value, quantities.Quantity):
        raw_value = self.to_python(raw_value)
        if raw_value is not None:
            raw_value = raw_value.limit_length(self.max_length, ValidationError)
        # if len(str(raw_value)) > self.max_length:
        #     if self.overflow_value:
        #         return self.overflow_value
        #     raise ValidationError(
        #         f"Cannot accept quantity {raw_value} "
        #         + f"because max_length is {self.max_length}")
        #     # print("20230129 Can't store {}={} in {}".format(self.name, raw_value, obj))
        #     # return -1
        return super().clean(raw_value, obj)


class DurationField(QuantityField):
    """
    A field that stores :class:`Duration
    <lino.utils.quantities.Duration>` values as CHAR.

    """

    def from_db_value(self, value, expression, connection, context=None):
        if value is None or value == "":
            return self.get_default()
        return Duration(value)

    def to_python(self, value):
        if isinstance(value, Duration):
            return value
        if value:
            # if isinstance(value, six.string_types):
            #     return Duration(value)
            return Duration(value)
        return None


class IncompleteDateField(models.CharField):
    """
    A field that behaves like a DateField, but accepts incomplete
    dates represented using
    :class:`lino.utils.format_date.IncompleteDate`.
    """

    default_validators = [validate_incomplete_date]

    def __init__(self, *args, **kw):
        kw.update(max_length=11)
        # msgkw = dict()
        # msgkw.update(ex1=IncompleteDate(1980, 0, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex2=IncompleteDate(1980, 7, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex3=IncompleteDate(0, 7, 23)
        #              .strftime(settings.SITE.date_format_strftime))
        kw.setdefault(
            "help_text",
            _(
                """\
Uncomplete dates are allowed, e.g.
"00.00.1980" means "some day in 1980",
"00.07.1980" means "in July 1980"
or "23.07.0000" means "on a 23th of July"."""
            ),
        )
        models.CharField.__init__(self, *args, **kw)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    # def get_internal_type(self):
    #     return "CharField"

    def from_db_value(self, value, expression, connection, context=None):
        return IncompleteDate.parse(value) if value else self.get_default()
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''

    def to_python(self, value):
        if isinstance(value, IncompleteDate):
            return value
        if isinstance(value, datetime.date):
            # ~ return IncompleteDate(value.strftime("%Y-%m-%d"))
            # ~ return IncompleteDate(d2iso(value))
            return IncompleteDate.from_date(value)
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''
        return IncompleteDate.parse(value) if value else ""

    # def get_prep_value(self, value):
    #     return str(value)

    def get_prep_value(self, value):
        return str(value) if value else ""
        # if value:
        #     return str(value)
        #     # return '"' + str(value) + '"'
        #     #~ return value.format("%04d%02d%02d")
        # return ''

    # ~ def value_to_string(self, obj):
    # ~ value = self._get_val_from_obj(obj)
    # ~ return self.get_prep_value(value)


class RecurrenceField(models.CharField):
    """
    Deserves more documentation.
    """

    def __init__(self, *args, **kw):
        kw.setdefault("max_length", 200)
        models.CharField.__init__(self, *args, **kw)


class CustomField:
    """
    Mixin to create a custom field.

    It defines a single method :meth:`create_layout_elem`.
    """

    def create_layout_elem(self, base_class, layout_handle, field, **kw):
        """Return the widget to represent this field in the specified
        `layout_handle`.

        The widget must be an instance of the given `base_class`.

        `self` and `field` are identical unless `self` is a
        :class:`RemoteField` or a :class:`VirtualField`.

        """
        return None


class PriceRange(ParameterPanel):
    def __init__(self, field_name, verbose_name=_("Price"), **kwargs):
        self.field_name = field_name
        self.verbose_name = verbose_name
        kwargs["start_" + field_name] = PriceField(
            verbose_name=format_lazy(_("{} from"), verbose_name), blank=True, null=True
        )
        kwargs["end_" + field_name] = PriceField(
            verbose_name=_("to"), blank=True, null=True
        )
        super().__init__(**kwargs)

    def check_values(self, pv):
        start_value = getattr(pv, "start_" + self.field_name)
        if start_value is None:
            return
        end_value = getattr(pv, "end_" + self.field_name)
        if end_value is None:
            return
        if start_value > end_value:
            raise Warning(_("Invalid price range"))

    def get_title_tags(self, ar):
        pv = ar.param_values
        start_value = getattr(pv, "start_" + self.field_name)
        end_value = getattr(pv, "end_" + self.field_name)
        if start_value:
            if end_value:
                yield _("{} {}...{}").format(self.verbose_name, start_value, end_value)
            else:
                yield _("{} from {}").format(self.verbose_name, start_value)
        elif end_value:
            yield _("{} until {}").format(self.verbose_name, end_value)


def choices_for_field(ar, holder, field):
    """
    Return the choices for the given field and the given HTTP request
    whose `holder` is either a Model, an Actor or an Action.
    """
    if not holder.get_view_permission(ar.request.user.user_type):
        raise Exception(
            "{user} has no permission for {holder}".format(
                user=ar.request.user, holder=holder
            )
        )
    # model = holder.get_chooser_model()
    chooser = holder.get_chooser_for_field(field.name)
    # logger.info('20140822 choices_for_field(%s.%s) --> %s',
    #             holder, field.name, chooser)
    # print(f"20251124f {holder} {field} {chooser}")
    if chooser:
        qs = chooser.get_request_choices(ar, holder)
        if not isiterable(qs):
            raise Exception(
                "%s.%s_choices() returned non-iterable %r"
                % (holder.model, field.name, qs)
            )
        if chooser.simple_values:

            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                d[constants.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar, field)
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:  # values are (value, text) tuples
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
                return d

        return (qs, row2dict)

    if field.choices:
        qs = field.choices

        def row2dict(obj, d):
            if type(obj) is list or type(obj) is tuple:
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
            else:
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar, field)
                d[constants.CHOICES_VALUE_FIELD] = str(obj)
            return d

        return (qs, row2dict)

    if isinstance(field, VirtualField):
        field = field.return_type

    if isinstance(field, RemoteField):
        field = field.field
        if isinstance(field, VirtualField):  # 20200425
            field = field.return_type

    if isinstance(field, models.ForeignKey):
        m = field.remote_field.model
        t = m.get_default_table()
        # qs = t.create_request(request=ar.request).data_iterator
        qs = t.create_request(parent=ar).data_iterator
        # logger.info('20120710 choices_view(FK) %s --> %s', t, qs.query)

        def row2dict(obj, d):
            d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                obj, ar, field)
            d[constants.CHOICES_VALUE_FIELD] = obj.pk
            return d
    # elif isinstance(field, GenericForeignKeyIdField):
    #     ct = getattr(ar.selected_rows[0], field.type_field)
    #     m = ct.model_class()
    #     # print(f"20250511 {field.remote_field} {repr(field.type_field)}")
    #     t = m.get_default_table()
    #     qs = t.create_request(parent=ar).data_iterator
    #
    #     def row2dict(obj, d):
    #         d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
    #             obj, ar, field)
    #         d[constants.CHOICES_VALUE_FIELD] = obj.pk
    #         return d
    else:
        raise http.Http404("No choices for %s" % field)
    return (qs, row2dict)
