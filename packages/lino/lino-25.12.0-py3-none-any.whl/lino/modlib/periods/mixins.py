# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.api import dd, rt
from lino import mixins
from lino.mixins import Referrable
from lino.utils import ONE_DAY

from lino.modlib.office.roles import OfficeStaff


class PeriodRange(dd.Model):

    class Meta:
        abstract = True

    start_period = dd.ForeignKey(
        'periods.StoredPeriod',
        blank=True,
        verbose_name=_("Start period"),
        related_name="%(app_label)s_%(class)s_set_by_start_period")

    end_period = dd.ForeignKey(
        'periods.StoredPeriod',
        blank=True,
        null=True,
        verbose_name=_("End period"),
        related_name="%(app_label)s_%(class)s_set_by_end_period")

    def get_period_filter(self, fieldname, **kwargs):
        return rt.models.periods.StoredPeriod.get_period_filter(
            fieldname, self.start_period, self.end_period, **kwargs)


class PeriodRangeObservable(dd.Model):

    class Meta:
        abstract = True

    observable_period_prefix = ''

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(start_period=dd.ForeignKey(
            'periods.StoredPeriod',
            blank=True,
            null=True,
            help_text=_("Start of observed period range."),
            verbose_name=_("Period from")))
        fields.update(end_period=dd.ForeignKey(
            'periods.StoredPeriod',
            blank=True,
            null=True,
            help_text=_("Optional end of observed period range. "
                        "Leave empty to observe only the start period."),
            verbose_name=_("Period until")))
        super().setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super().get_request_queryset(ar, **kwargs)
        if (pv := ar.param_values) is None: return qs
        if pv.start_period is not None:
            fkw = dict()
            fkw[cls.observable_period_prefix + "journal__preliminary"] = False
            flt = rt.models.periods.StoredPeriod.get_period_filter(
                cls.observable_period_prefix + "accounting_period",
                pv.start_period, pv.end_period, **fkw)
            qs = qs.filter(**flt)
        return qs

    @classmethod
    def get_title_tags(cls, ar):
        for t in super().get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_period is not None:
            if pv.end_period is None:
                yield str(pv.start_period)
            else:
                yield "{}..{}".format(pv.start_period, pv.end_period)


class PeriodRangeParameters(dd.ParameterPanel):

    def __init__(self,
                 verbose_name_start=_("Period from"),
                 verbose_name_end=_("until"),
                 **kwargs):
        kwargs.update(
            start_period=dd.ForeignKey(
                'periods.StoredPeriod',
                blank=True,
                null=True,
                help_text=_("Start of observed period range"),
                verbose_name=verbose_name_start),
            end_period=dd.ForeignKey(
                'periods.StoredPeriod',
                blank=True,
                null=True,
                help_text=_("Optional end of observed period range. "
                            "Leave empty to consider only the Start period."),
                verbose_name=verbose_name_end))
        super().__init__(**kwargs)

    def check_values(self, pv):
        if not pv.start_period:
            raise Warning(_("Select at least a start period"))
        if pv.end_period:
            if str(pv.start_period) > str(pv.end_period):
                raise Warning(_("End period must be after start period"))

    def get_title_tags(self, ar):
        pv = ar.param_values
        if pv.start_period:
            if pv.end_period:
                yield _("Periods {}...{}").format(pv.start_period,
                                                  pv.end_period)
            else:
                yield _("Period {}").format(pv.start_period)
        else:
            yield str(_("All periods"))
