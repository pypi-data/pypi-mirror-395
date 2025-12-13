# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from dateutil.easter import easter
from dateutil.rrule import SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, YEARLY

from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.utils import isidentifier
from lino.core.choicelists import ChoiceList, Choice
from lino.core.roles import login_required, Explorer
from lino.core.fields import virtualfield
from lino.utils.dates import DateRangeValue
from lino.utils.format_date import day_and_month, fds
from lino.utils.html import mark_safe, format_html, escape


class YesNo(ChoiceList):
    verbose_name_plural = _("Yes or no")
    preferred_width = 12


add = YesNo.add_item
add("y", _("Yes"), "yes")
add("n", _("No"), "no")


class Genders(ChoiceList):
    verbose_name = _("Gender")
    verbose_name_plural = _("Genders")


add = Genders.add_item
add("M", _("Male"), "male")
add("F", _("Female"), "female")
add("N", _("Nonbinary"), "nonbinary")


class ObservedEvent(Choice):
    def __init__(self, value, name=None, **kwargs):
        if name is None and isidentifier(value):
            name = value
        super(ObservedEvent, self).__init__(value, names=name, **kwargs)

    def add_filter(self, qs, pv):
        return qs


class PeriodStarted(ObservedEvent):
    # name = 'started'
    text = _("Starts")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        qs = qs.filter(start_date__isnull=False)
        if obj.start_date:
            qs = qs.filter(start_date__gte=obj.start_date)
        if obj.end_date:
            qs = qs.filter(start_date__lte=obj.end_date)
        return qs


class PeriodActive(ObservedEvent):
    # name = 'active'
    text = _("Is active")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        if obj.end_date:
            qs = qs.filter(Q(start_date__isnull=True) | Q(start_date__lte=obj.end_date))
        if obj.start_date:
            qs = qs.filter(Q(end_date__isnull=True) | Q(end_date__gte=obj.start_date))
        return qs


class PeriodEnded(ObservedEvent):
    # name = 'ended'
    text = _("Ends")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        qs = qs.filter(end_date__isnull=False)
        if obj.start_date:
            qs = qs.filter(end_date__gte=obj.start_date)
        if obj.end_date:
            qs = qs.filter(end_date__lte=obj.end_date)
        return qs


# class PeriodEvent(ObservedEvent):
#     """Every item of :class:`PeriodEvents` is an instance of this."""
#     def add_filter(self, qs, obj):
#         elif self.name == 'ended':


class PeriodEvents(ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")


PeriodEvents.add_item_instance(PeriodStarted("10", "started"))
PeriodEvents.add_item_instance(PeriodActive("20", "active"))
PeriodEvents.add_item_instance(PeriodEnded("30", "ended"))

# add = PeriodEvents.add_item
# add('10', _("Starts"), 'started')
# add('20', _("Is active"), 'active')
# add('30', _("Ends"), 'ended')


class DurationUnit(Choice):
    du_freq = None  # dateutils frequency

    def add_duration(unit, orig, value):
        if orig is None:
            return None
        if unit.value == "N":
            return None
        if unit.value == "s":
            return orig + datetime.timedelta(seconds=value)
        if unit.value == "m":
            return orig + datetime.timedelta(minutes=value)
        if unit.value == "h":
            return orig + datetime.timedelta(hours=value)
        if unit.value == "D":
            return orig + datetime.timedelta(days=value)
        if unit.value == "W":
            return orig + datetime.timedelta(days=value * 7)
        day = orig.day
        while True:
            year = orig.year
            try:
                if unit.value == "M":
                    m = orig.month + value
                    while m > 12:
                        m -= 12
                        year += 1
                    while m < 1:
                        m += 12
                        year -= 1
                    return orig.replace(month=m, day=day, year=year)
                if unit.value == "Y":
                    return orig.replace(year=orig.year + value, day=day)
                if unit.value == "E":
                    offset = orig - easter(year)
                    return easter(year + value) + offset
                raise Exception("Invalid DurationUnit %s" % unit)
            except ValueError:
                if day > 28:
                    day -= 1
                else:
                    raise

    def get_date_formatter(self):
        if self.value in "YEM":
            return fds
        return day_and_month


class Weekdays(ChoiceList):
    verbose_name = _("Weekday")


add = Weekdays.add_item
add("1", _("Monday"), "monday")
add("2", _("Tuesday"), "tuesday")
add("3", _("Wednesday"), "wednesday")
add("4", _("Thursday"), "thursday")
add("5", _("Friday"), "friday")
add("6", _("Saturday"), "saturday")
add("7", _("Sunday"), "sunday")

WORKDAYS = frozenset(
    [
        Weekdays.get_by_name(k)
        for k in "monday tuesday wednesday thursday friday".split()
    ]
)


class DurationUnits(ChoiceList):
    verbose_name = _("Duration Unit")
    item_class = DurationUnit


add = DurationUnits.add_item
add("s", _("seconds"), "seconds")
add("m", _("minutes"), "minutes")
add("h", _("hours"), "hours")
add("D", _("days"), "days")
add("W", _("weeks"), "weeks")
add("M", _("months"), "months")
add("Y", _("years"), "years")


class Recurrences(ChoiceList):
    verbose_name = _("Recurrence")
    verbose_name_plural = _("Recurrences")
    item_class = DurationUnit
    preferred_foreignkey_width = 12


add = Recurrences.add_item
add("O", _("once"), "once")
add("N", _("never"), "never")
add("s", _("secondly"), "secondly", du_freq=SECONDLY)
add("m", _("minutely"), "minutely", du_freq=MINUTELY)
add("h", _("hourly"), "hourly", du_freq=HOURLY)
add("D", _("daily"), "daily", du_freq=DAILY)
add("W", _("weekly"), "weekly", du_freq=WEEKLY)
add("M", _("monthly"), "monthly", du_freq=MONTHLY)
add("Y", _("yearly"), "yearly", du_freq=YEARLY)
add("P", _("per weekday"), "per_weekday")  # deprecated
add("E", _("Relative to Easter"), "easter")


class DisplayColor(Choice):
    font_color = None

    def __init__(self, value, text, names, font_color="white"):
        super().__init__(value, text, names)
        self.font_color = font_color


class DisplayColors(ChoiceList):
    verbose_name = _("Display color")
    verbose_name_plural = _("Display colors")
    item_class = DisplayColor
    required_roles = login_required(Explorer)
    column_names = "value name text font_color"
    preferred_width = 10

    @virtualfield(models.CharField(_("Font color")))
    def font_color(cls, choice, ar):
        return choice.font_color

    @classmethod
    def display_text(cls, bc):
        # text = escape(bc.text)
        # txt = f"""<span style="background-color:{bc.name};color:{bc.font_color}">{text}</span>"""
        # txt = mark_safe(txt)
        sample = f"""<span style="padding:3pt;background-color:{
            bc.name};color:{bc.font_color}">(sample)</span>"""
        sample = mark_safe(sample)
        txt = format_html("{} {}", bc.text, sample)
        # raise Exception(f"20250118 {txt.__class__}")
        return txt


add = DisplayColors.add_item
# cssColors = 'White Silver Gray Black Red Maroon Yellow Olive Lime Green Aqua Teal Blue Navy Fuchsia Purple'
# cssColors = 'white silver gray black red maroon yellow olive lime green aqua teal blue navy fuchsia purple'
# for color in cssColors.split():
#     add(color, _(color), color, font_color="white")
#
# lightColors = 'White Silver Gray'
# # lightColors = 'white silver gray'
# for color in lightColors.split():
#     DisplayColors.get_by_value(color).font_color = "black"

# B&W
add("100",   _("White"), "white",  "black")
add("110",    _("Gray"), "gray",   "black")
add("120",   _("Black"), "black",  "white")

# Rainbow colors
add("210",     _("Red"), "red",    "white")
add("220",  _("Orange"), "orange", "white")
add("230",  _("Yellow"), "yellow", "black")
add("240",   _("Green"), "green",  "white")
add("250",    _("Blue"), "blue",   "white")
add("260", _("Magenta"), "magenta", "white")
add("270",  _("Violet"), "violet", "white")

# Other colors
add("300",     _("Silver"), "silver",     "black")
add("310",     _("Maroon"), "maroon",     "white")
add("311",       _("Peru"), "peru",       "white")
add("312",       _("Pink"), "pink",       "black")
add("320",      _("Olive"), "olive",      "white")
add("330",       _("Aqua"), "aqua",       "white")
add("340",       _("Navy"), "navy",       "white")
add("341", _("Aquamarine"), "aquamarine", "black")
add("342",  _("DarkGreen"), "darkgreen",  "white")
add("343",  _("PaleGreen"), "palegreen",  "black")
add("344", _("Chartreuse"), "chartreuse", "black")
add("345",       _("Lime"), "lime",       "black")
add("346",       _("Teal"), "teal",       "white")
add("350",    _("Fuchsia"), "fuchsia",    "white")
add("351",       _("Cyan"), "cyan",       "black")
add("361",     _("Purple"), "purple",     "white")

# List of all named colors: https://www.w3schools.com/colors/colors_names.asp
