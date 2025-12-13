# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, _

SUMMARY_PERIODS = ["yearly", "monthly", "weekly", "timeless"]


class ComputeResults(dd.Action):
    label = _("Update summary data")
    # icon_name = 'lightning'
    # button_text = "∑"  # "\u2211"  # N-ARY SUMMATION
    button_text = "Σ"  # "\u03A3"  # GREEK CAPITAL LETTER SIGMA

    # readonly = False

    def run_from_ui(self, ar, **kw):
        for obj in ar.selected_rows:
            obj.compute_summary_values()
        ar.success(refresh=True)


class UpdateSummariesByMaster(ComputeResults):
    def __init__(self, master_model, summary_models):
        self.master_model = master_model
        self.summary_models = summary_models
        super().__init__()

    def run_from_ui(self, ar, fix=None):
        for master in ar.selected_rows:
            assert isinstance(master, self.master_model)
            for sm in self.summary_models:
                sm.update_for_filter(master=master)
        ar.set_response(refresh=True)


class Summarized(dd.Model):

    class Meta:
        abstract = True

    compute_results = ComputeResults()
    delete_them_all = False

    @classmethod
    def check_all_summaries(cls):
        if cls.delete_them_all:
            cls.objects.all().delete()
        cls.update_for_filter()

    @classmethod
    def update_for_filter(cls, **flt):
        for obj in cls.get_for_filter(**flt):
            obj.compute_summary_values()

    # @classmethod
    # def get_summary_masters(cls):
    #     yield None

    @classmethod
    def get_for_filter(cls, **flt):
        qs = cls.objects.filter(**flt)
        if cls.delete_them_all:
            count = qs.count()
            if count > 1:
                # Theoretically this should never happen. There cannot be
                # more than one object for a given master and period.
                qs.delete()
                count = 0
            if count == 0:
                return [cls(**flt)]
        return qs

    def compute_summary_values(self):
        self.reset_summary_data()
        for collector, qs in self.get_summary_collectors():
            for obj in qs:
                collector(obj)
        self.full_clean()
        self.save()

    def reset_summary_data(self):
        pass

    def get_summary_collectors(self):
        raise NotImplementedError(
            f"{self.__class__} must define get_summary_collectors()"
        )


class SlaveSummarized(Summarized):

    class Meta:
        abstract = True

    allow_cascaded_delete = "master"
    allow_cascaded_copy = set()

    @classmethod
    def check_all_summaries(cls):
        if cls.delete_them_all:
            cls.objects.all().delete()
        for master in cls.get_summary_masters():
            cls.update_for_filter(master=master)

    @classmethod
    def get_summary_masters(cls):
        return cls.get_summary_master_model().objects.all()

    @classmethod
    def get_summary_master_model(cls):
        return cls._meta.get_field("master").remote_field.model

    # @classmethod
    # def get_for_filter(cls, master, **flt):
    #     flt.update(master=master)
    #     return super(SlaveSummarized, cls).get_for_filter(master, **flt)

    # @classmethod
    # def update_for_filter(cls, **flt):
    #     obj = cls.get_for_filter(**flt)
    #     obj.compute_summary_values()


class DateSummarized(Summarized):
    class Meta(object):
        abstract = True

    # summary_period = 'yearly'
    summary_period = "monthly"

    year = models.IntegerField(_("Year"), null=True, blank=True)
    month = models.IntegerField(_("Month"), null=True, blank=True)

    @classmethod
    def on_analyze(cls, site):
        if cls.summary_period not in SUMMARY_PERIODS:
            raise Exception(
                "Invalid summary_period {!r} for {}".format(cls.summary_period, cls)
            )
        if cls.summary_period == "weekly":
            cls._meta.get_field("month").verbose_name = _("Week")
        super().on_analyze(site)

    @classmethod
    def get_summary_periods(cls):
        config = dd.plugins.summaries
        if cls.summary_period == "timeless":
            yield None, None
            return
        for year in range(config.start_year, config.end_year + 1):
            if cls.summary_period == "yearly":
                yield year, None
            elif cls.summary_period == "monthly":
                for month in range(1, 13):
                    yield year, month
            elif cls.summary_period == "weekly":
                for week in range(1, 53):
                    yield year, week

    def add_date_filter(self, qs, fldname, **kwargs):
        if self.year is not None:
            kwargs[fldname + "__year"] = self.year
        if self.month is not None:
            if cls.summary_period == "monthly":
                kwargs[fldname + "__month"] = self.month
            elif cls.summary_period == "weekly":
                kwargs[fldname + "__week"] = self.month
        return qs.filter(**kwargs)

    # @classmethod
    # def get_widget_options(cls, name, **options):
    #     if name in ('year', 'month'):
    #         options.update(hide_sum=True)
    #     return super(Summary, cls).get_widget_options(name, **options)

    @classmethod
    def update_for_filter(cls, **flt):
        for year, period in cls.get_summary_periods():
            if period is not None:
                flt.update(month=period)
            if year is not None:
                flt.update(year=year)
            for obj in cls.get_for_filter(**flt):
                obj.compute_summary_values()


DateSummarized.set_widget_options("year", hide_sum=True)
DateSummarized.set_widget_options("month", hide_sum=True)
