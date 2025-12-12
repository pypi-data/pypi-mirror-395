# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the classes :class:`AbstractTable` and
:class:`VirtualTable`.

"""

# import os
import yaml

from django.db import models
from django.db.utils import OperationalError, ProgrammingError
# from django.conf import settings
from django.utils.translation import gettext_lazy as _
# from django.core.exceptions import BadRequest

from lino import logger
# from lino.core import constants
# from lino.core import actors
from lino.core import vfields
# from lino.core import layouts
# from lino.core.utils import resolve_fields_list
from .atable import AbstractTable

# class InvalidRequest(Exception):
#     pass

if False:  # 20130710
    from lino.utils.config import Configured

    class GridConfig(Configured):
        def __init__(self, report, data, *args, **kw):
            self.report = report
            self.data = data
            self.label_en = data.get("label")
            self.data.update(label=_(self.label_en))
            super(GridConfig, self).__init__(*args, **kw)
            must_save = self.validate()
            if must_save:
                msg = self.save_config()
                # ~ msg = self.save_grid_config()
                logger.debug(msg)

        def validate(self):
            """
            Removes unknown columns
            """
            must_save = False
            gc = self.data
            columns = gc["columns"]
            col_count = len(columns)
            widths = gc.get("widths", None)
            hiddens = gc.get("hiddens", None)
            if widths is None:
                widths = [None for x in columns]
                gc.update(widths=widths)
            elif col_count != len(widths):
                raise Exception("%d columns, but %d widths" % (col_count, len(widths)))
            if hiddens is None:
                hiddens = [False for x in columns]
                gc.update(hiddens=hiddens)
            elif col_count != len(hiddens):
                raise Exception(
                    "%d columns, but %d hiddens" % (col_count, len(hiddens))
                )

            valid_columns = []
            valid_widths = []
            valid_hiddens = []
            for i, colname in enumerate(gc["columns"]):
                f = self.report.get_data_elem(colname)
                if f is None:
                    logger.debug(
                        "Removed unknown column %d (%r). Must save.", i, colname
                    )
                    must_save = True
                else:
                    valid_columns.append(colname)
                    valid_widths.append(widths[i])
                    valid_hiddens.append(hiddens[i])
            gc.update(widths=valid_widths)
            gc.update(hiddens=valid_hiddens)
            gc.update(columns=valid_columns)
            return must_save

        def unused_write_content(self, f):
            self.data.update(label=self.label_en)
            f.write(yaml.dump(self.data))
            self.data.update(label=_(self.label_en))

        def write_content(self, f):
            f.write(yaml.dump(self.data))


class VirtualTable(AbstractTable):
    """
    An :class:`AbstractTable` that works on an volatile (non
    persistent) list of rows.

    By nature it cannot have database fields, only virtual fields.

    Subclasses must define a :meth:`get_data_rows` method.

    """

    abstract = True


class VentilatedColumns(VirtualTable):
    """
    A mixin for tables that have a series of automatically generated
    columns.  TODO: rename this to DynamicColumns.
    """

    ventilated_column_suffix = ":5"

    column_names_template = ""
    """
    The template to use for :attr:`column_names`.   It should contain a string
    ``{vcolumns}``, which will be replaced by a space-separated list of the column
    names given by :meth:`get_ventilated_columns`.
    """

    abstract = True

    @classmethod
    def setup_columns(self):
        # if not "{vcolumns}" in self.column_names_template:
        #     return
        # self.column_names = 'description '
        names = ""
        try:
            for i, vf in enumerate(self.get_ventilated_columns()):
                self.add_virtual_field("vc" + str(i), vf)
                names += " " + vf.name + self.ventilated_column_suffix
        except (OperationalError, ProgrammingError) as e:
            # Error can differ depending on the database engine.
            logger.debug("Failed to load ventilated columns : %s", e)
        self.column_names = self.column_names_template.format(vcolumns=names)

        # ~ logger.info("20131114 setup_columns() --> %s",self.column_names)

    @classmethod
    def get_ventilated_columns(self):
        return []


class VentilatingTable(VentilatedColumns):
    abstract = True
    column_names_template = "description {vcolumns}"

    @vfields.virtualfield(models.CharField(_("Description"), max_length=30))
    def description(self, obj, ar):
        return str(obj)


class ButtonsTable(VirtualTable):
    """

    Probably deprecated. Might not work as expected in React (because of
    hide_top_toolbar).

    An abstract :class:`VirtualTable` with only one column and whose rows are
    action buttons.

    Subclasses must implement `get_data_rows` to yield action buttons.

    Usage example
    `lino_welfare.modlib.reception.models.FindDateByClientTable`.

    """

    abstract = True
    column_names = "button"
    auto_fit_column_widths = True
    window_size = (60, 20)
    hide_top_toolbar = True

    @vfields.displayfield(_("Button"))
    def button(self, obj, ar):
        return obj


# from lino.core.signals import post_analyze
# from django.db.utils import DatabaseError

# @signals.receiver(post_analyze)
# def setup_ventilated_columns(sender, **kw):
#     # print("20170308 SETUP_VENTILATED_COLUMNS")
#     if actors.actors_list is not None:
#         for a in actors.actors_list:
#             if issubclass(a, AbstractTable) and not a.abstract:
#                 try:
#                     a.setup_columns()
#                 except DatabaseError:
#                     logger.debug(
#                         "Ignoring DatabaseError in %s.setup_ventilated_columns", a)
#     settings.SITE.resolve_virtual_fields()
