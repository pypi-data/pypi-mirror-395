# Copyright 2009-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the "store" and its "fields" .

During startup, Lino instantiates a "store" and its "fields" (aka
"atomizers") for every table.  These were used originally for dealing
with Sencha ExtJS GridPanels and FormPanels, but the concept turned
out useful for other features.

Some usages specific to Sencha ExtJS:

- for generating the JS code of the GridPanel definition
- for generating an "atomized" JSON representation when
  rendering data for that GridPanel
- for parsing the JSON sent by GridPanel and FormPanel

Other usages:

- remote fields (:class:`lino.core.fields.RemoteField`)

- render tables as text
  (:meth:`lino.core.renderer.TextRenderer.show_table` and
  :meth:`lino.core.requests.ActionRequest.row2text`)

"""

from lino import logger

# from django.db.models.fields import Field
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
# from lino import AFTER17

# from lino.utils.jsgen import py2js
# from lino.utils.quantities import parse_decimal
from lino.core.utils import getrqdata
from lino.core.utils import DelayedValue
# from lino.core.gfks import GenericForeignKey
from lino.core import constants
# from .vfields import DummyField
from lino.core import frames
from lino.core import atomizer
from lino.core.utils import PhantomRow
# from lino.utils import choosers

from .storefields import (
    RowClassStoreField, DisableEditingStoreField, DisabledFieldsStoreField,
    StoreField, VirtStoreField)


class BaseStore(object):
    pass


class ParameterStore(BaseStore):
    # Lazily instantiated in `lino.core.layouts`
    def __init__(self, params_layout_handle, url_param):
        param_fields = []

        holder = params_layout_handle.layout.get_chooser_holder()
        # print(f"20250121e {holder}")
        # debug = False
        for pf in params_layout_handle._data_elems:
            sf = atomizer.create_atomizer(holder, pf, pf.name)
            if sf is not None:
                # if "__" in pf.name:
                #     print("20200423 ParameterStore", pf.name, sf)
                #     debug  = True
                param_fields.append(sf)

        # if debug:
        #     print("20200423 ParameterStore2", self.param_fields)

        self.param_fields = tuple(param_fields)
        self.url_param = url_param
        self.params_layout_handle = params_layout_handle

    def __str__(self):
        return "%s of %s" % (self.__class__.__name__, self.params_layout_handle)

    def pv2dict(self, ar, pv, **d):
        # debug = False
        for fld in self.param_fields:
            #     debug = True
            if fld.delayed_value and len(ar.selected_rows) == 1:
                v = DelayedValue(ar, fld.name, ar.selected_rows[0])
            else:
                v = pv.get(fld.name, None)
            # if "__" in fld.name:
            #     print("20200430", fld, v)
            fld.value2dict(ar, fld.name, v, d, None)
            # try:
            #     v = pv.get(fld.name, None)
            #     fld.value2dict(ar, v, d, None)
            # except Exception as e:
            #     raise e.__class__("{} : {}".format(fld, e))
        # if debug:
        #     print("20200423", d)
        return d

    def pv2list(self, ar, apv):  # new since 20140930
        l = []
        for fld in self.param_fields:
            v = apv.get(fld.name, None)
            l.append(v)
        return l

    def parse_form_value(self, sf, form_value):
        """
        Convert a form value (string) into the corresponding
        Python object for the given StoreField `sf`.
        """
        if form_value == "" and not sf.field.empty_strings_allowed:
            return sf.form2obj_default
        elif form_value in (
            constants.CHOICES_BLANK_FILTER_VALUE,
            constants.CHOICES_NOT_BLANK_FILTER_VALUE,
        ):
            return form_value
        else:
            return sf.parse_form_value(form_value, None)

    def parse_prefixed_params(self, request, prefix, **kw):
        """
        Like :meth:`parse_params` but expects the parameters to be
        prefixed in the request data. E.g. for prefix 'pv' and
        field name 'status' it looks for 'pv-status' in the request
        data.
        """
        data = getrqdata(request)
        for f in self.param_fields:
            fv = data.get(f"{prefix}-{f.name}", "")
            kw[f.name] = self.parse_form_value(f, fv)
        return kw

    def parse_params(self, request, **kw):
        data = getrqdata(request)
        # print(20160329, data)
        # assert 'pv' in data
        pv = data.getlist(self.url_param)  # 'fv', 'pv', post[fn] post[fv][fn]

        # logger.info("20120221 ParameterStore.parse_params(%s) --> %s",self.url_param,pv)

        parse = self.parse_form_value

        # def parse(sf, form_value):
        #     if form_value == "" and not sf.field.empty_strings_allowed:
        #         return sf.form2obj_default
        #         # When a field has been posted with empty string, we
        #         # don't want it to get the field's default value
        #         # because otherwise checkboxes with default value True
        #         # can never be unset.  charfields have
        #         # empty_strings_allowed e.g. id field may be empty.
        #         # But don't do this for other cases.
        #     elif form_value in (
        #         constants.CHOICES_BLANK_FILTER_VALUE,
        #         constants.CHOICES_NOT_BLANK_FILTER_VALUE,
        #     ):
        #         return form_value
        #     else:
        #         return sf.parse_form_value(form_value, None)

        if len(pv) > 0:
            if len(self.param_fields) != len(pv):
                raise Exception(
                    "%s expects a list of %d values but got %d: %s"
                    % (self, len(self.param_fields), len(pv), pv)
                )
            for i, f in enumerate(self.param_fields):
                # kw[f.field.name] = parse(f, pv[i])
                kw[f.name] = parse(
                    f, pv[i]
                )  # 20200423 support remote fields in parameters
        elif self.url_param == "fv":
            # try to get data from dict style in main body of request
            for i, f in enumerate(self.param_fields):
                if f.name + "Hidden" in data:
                    kw[f.name] = parse(f, data[f.name + "Hidden"])
                elif f.name in data:
                    kw[f.name] = parse(f, data[f.name])
        # print(20160329, kw)
        return kw


class Store(BaseStore):
    """
    A Store is the collection of StoreFields for a given actor.
    Instantiated in kernel
    """

    pk = None
    _disabled_fields_storefield = None

    def __init__(self, rh, **options):
        self.rh = rh
        self.actor = rh.actor
        # temporary dict used by collect_fields and add_field_for
        # self.df2sf = {}
        self.all_fields = []
        self.grid_fields = []
        self.detail_fields = []
        self.card_fields = []
        self.item_fields = []
        self.primary_keys = set([])

    def init_store(self):

        rh = self.rh

        def addfield(sf):
            if not isinstance(sf, StoreField):
                raise Exception("20210623 {} is not a StoreField".format(sf))
            self.all_fields.append(sf)
            self.grid_fields.append(sf)
            self.detail_fields.append(sf)

        if not issubclass(rh.actor, frames.Frame):
            self.collect_fields(self.grid_fields, rh.get_grid_layout())

        form = rh.actor.detail_layout
        if form:
            dh = form.get_layout_handle()
            self.collect_fields(self.detail_fields, dh)

        for form in rh.actor.extra_layouts.values():
            dh = form.get_layout_handle()
            self.collect_fields(self.detail_fields, dh)

        form = rh.actor.insert_layout
        if form:
            if isinstance(form, str):
                raise Exception(f"20250306 insert_layout {repr(rh.actor)} is a str!")
            dh = form.get_layout_handle()
            self.collect_fields(self.detail_fields, dh)

        form = rh.actor.card_layout
        if form:
            dh = form.get_layout_handle()
            self.collect_fields(self.card_fields, dh)

        # form = rh.actor.list_layout
        # if form:
        #     dh = form.get_layout_handle()
        #     self.collect_fields(self.item_fields, dh)

        if self.pk is not None:
            self.pk_index = 0
            found = False
            for fld in self.grid_fields:
                """
                Django's Field.__cmp__() does::

                  return cmp(self.creation_counter, other.creation_counter)

                which causes an exception when trying to compare a field
                with an object of other type.
                """
                if (fld.field.__class__ is self.pk.__class__) and fld.field == self.pk:
                    # self.pk = fld.field
                    found = True
                    break
                self.pk_index += fld.list_values_count
            if not found:
                raise Exception(
                    "Primary key %r not found in grid_fields %s"
                    % (self.pk, [f.field for f in self.grid_fields])
                )

        actor_editable = True  # not rh.actor.hide_editing(None)
        if actor_editable:
            self._disabled_fields_storefield = DisabledFieldsStoreField(self)
            addfield(self._disabled_fields_storefield)
            # NB what about disabled actions on non-editable actor?

        if actor_editable:
            addfield(DisableEditingStoreField(self))

        if rh.actor.get_row_classes is not None:
            addfield(RowClassStoreField(self))

        # virtual fields must come last so that Store.form2obj()
        # processes "real" fields first.
        self.all_fields = [
            f for f in self.all_fields if not isinstance(f, VirtStoreField)
        ] + [f for f in self.all_fields if isinstance(f, VirtStoreField)]
        self.all_fields = tuple(self.all_fields)
        self.grid_fields = tuple(self.grid_fields)
        self.detail_fields = tuple(self.detail_fields)
        self.card_fields = tuple(self.card_fields)
        self.item_fields = tuple(self.item_fields)

    def collect_fields(self, fields, *layouts):
        """`fields` is a pointer to either `self.detail_fields` or
        `self.grid_fields`.  Each of these must contain a primary key
        field.

        """
        pk_found = False
        for layout in layouts:
            for df in layout._data_elems:
                assert df is not None
                self.add_field_for(fields, df)
                if df.primary_key:
                    self.primary_keys.add(df)
                    pk_found = True
                    if self.pk is None:
                        self.pk = df

        if self.pk is None:
            self.pk = self.actor.get_pk_field()
        if self.pk is not None:
            if not pk_found:
                self.add_field_for(fields, self.pk)

    def add_field_for(self, field_list, df):
        sf = atomizer.get_atomizer(self.actor, df, df.name)
        # if df.name == 'humanlinks_LinksByHuman':
        #     raise Exception("20181023 {} ({}) {}".format(
        #         self, df, sf))
        if sf is None:
            # if isinstance(df, DummyField):
            #     return
            return
            # raise Exception("20181023 No atomizer for {} in {}".format(
            #     repr(df), self.actor))
        if not isinstance(sf, StoreField):
            raise Exception("20210623 {} is not a StoreField".format(sf))
        # if not self.rh.actor.editable and isinstance(sf, ForeignKeyStoreField):
        #     sf = StoreField(df, df.name)
        #     raise Exception(20160907)
        if sf not in self.all_fields:
            self.all_fields.append(sf)

        # sf = self.df2sf.get(df,None)
        # if sf is None:
        # sf = self.create_atomizer(df,df.name)
        # self.all_fields.append(sf)
        # self.df2sf[df] = sf
        field_list.append(sf)

    def form2obj(self, ar, form_values, instance, is_new):
        """
        Store the `form_values` into the `instance` by calling
        :meth:`form2obj` for every store field.
        """
        disabled_fields = set(self.actor.get_disabled_fields(instance, ar))
        # logger.info("20210213 form2obj %s %s", disabled_fields, [f.name for f in self.all_fields])
        changed_triggers = []
        for f in self.all_fields:
            if f.name not in disabled_fields:
                try:
                    if f.form2obj(ar, instance, form_values, is_new):
                        # Check whether FOO_changed exists
                        m = getattr(instance, f.name + "_changed", None)
                        if m is not None:
                            changed_triggers.append(m)
                except exceptions.ValidationError as e:
                    # logger.warning("20150127 store (field %s) : %s",
                    #                f.name, e)
                    raise exceptions.ValidationError({f.name: e.messages})
                # except ValueError as e:
                #     # logger.warning("20150127 store (field %s) : %s",
                #     #                f.name, e)
                #     raise exceptions.ValidationError(
                #         {f.name: _("Invalid value for this field (%s).") % e})
                except Exception as e:
                    # Example: submit "31.02.2024" in a date field
                    if False:
                        logger.warning(
                            "Exception during Store.form2obj (field %s) : %s", f.name, e
                        )
                        logger.exception(e)
                    raise exceptions.ValidationError(
                        # {f.name: _("Invalid value (%s).") % e})
                        {f.name: str(e)}
                    )
                # logger.info("20120228 Store.form2obj %s -> %s",
                # f, dd.obj2str(instance))
        for m in changed_triggers:
            m(ar)

    def column_names(self):
        l = []
        for fld in self.grid_fields:
            l += fld.column_names()
        return l

    def column_index(self, name):
        """
        Used to set `disabled_actions_index`.
        Was used to write definition of Ext.ensible.cal.CalendarMappings
        and Ext.ensible.cal.EventMappings
        """
        # logger.info("20111214 column_names: %s",list(self.column_names()))
        return list(self.column_names()).index(name)

    def row2list(self, ar, row):
        # assert isinstance(ar, dbtables.AbstractTableRequest)
        # if not isinstance(ar, dbtables.ListActionRequest):
        # raise Exception()
        # logger.info("20120107 Store %s row2list(%s)", self.report.model, dd.obj2str(row))
        l = []
        if isinstance(row, PhantomRow):
            for fld in self.grid_fields:
                fld.value2list(ar, None, l, row)
            # instead of calling ar.scrap_row_meta, add independently the meta item
            l.append({'meta': True, 'phantom': True})
        else:
            for fld in self.grid_fields:
                if fld.delayed_value:
                    # self.actor.collect_extra_fields(fld)
                    v = DelayedValue(ar, fld.name, row)
                else:
                    v = fld.full_value_from_object(row, ar)
                fld.value2list(ar, v, l, row)

            ar.scrap_row_meta(row, l)
        # logger.info("20130611 Store row2list() --> %r", l)
        return l

    def row2dict(self, ar, row, fields=None, **d):
        # assert isinstance(ar,dbtables.AbstractTableRequest)
        # logger.info("20111209 Store.row2dict(%s)", dd.obj2str(row))
        if fields is None:
            fields = self.detail_fields
        for fld in fields:
            if fld is None:
                continue
            # logger.info("20241003 Store.row2dict %s", fld)
            if fld.delayed_value:
                # self.actor.collect_extra_fields(fld)
                v = DelayedValue(ar, fld.name, row)
            else:
                v = fld.full_value_from_object(row, ar)
            fld.value2dict(ar, fld.name, v, d, row)
            # logger.info("20140429 Store.row2dict %s -> %s", fld, v)
        #     if "households_" in fld.name:
        #         print("20181023 {}".format(fld))
        # print("20181023 row2dict {}".format(fields))
        return d

    # def file2url(self, ar, row):
    #     return settings.SITE.build_media_url(row.file.name)

    # def row2odt(self,request,fields,row,sums):
    # for i,fld in enumerate(fields):
    # if fld.field is not None:
    # v = fld.full_value_from_object(request,row)
    # if v is None:
    # yield ''
    # else:
    # sums[i] += fld.value2num(v)
    # yield fld.value2odt(request,v)
