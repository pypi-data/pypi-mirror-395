# -*- coding: UTF-8 -*-
# Copyright 2023-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
from typing import Callable
from asgiref.sync import sync_to_async
from django.conf import settings
from lino.api import dd, rt, _
from lino.core.roles import SiteStaff


class Procedure(dd.Choice):
    func: Callable
    kwargs: dict
    class_name: str
    run_after: Callable | None
    during_initdb: bool

    def __init__(
        self, func, class_name=None, run_after=None, during_initdb=True, **kwargs
    ):
        name = func.__name__
        super().__init__(name, name, name)
        self.func = func
        self.class_name = class_name
        self.run_after = run_after
        self.during_initdb = during_initdb
        self.kwargs = kwargs

    async def install_if_needed(self, ar):
        if self.class_name == "linod.SystemTask":
            SystemTask = rt.models.linod.SystemTask
            if not await SystemTask.objects.filter(procedure=self).aexists():
                await ar.adebug("Create background task for %r", self)
                # Without a value for start_date and end_date, Django would
                # dd.today(), which does a database lookup to find
                # SiteConfig.simulate_today, which would raise a "cannot call
                # this from an async context" exception.
                # self.kwargs.update(start_date=None, end_date=None)
                self.kwargs.setdefault('start_date', await settings.SITE.atoday())
                # self.kwargs.setdefault('end_date', None)
                obj = SystemTask(procedure=self, **self.kwargs)
                # every_unit=proc.every_unit, every=proc.every_value)
                if obj.every_unit == "secondly":
                    obj.log_level = "WARNING"
                await sync_to_async(obj.full_clean)()
                await obj.asave()

    def run(self, ar):
        return self.func(ar)

    def __repr__(self):
        return f"Procedures.{self.value}"


class Procedures(dd.ChoiceList):
    verbose_name = _("Background procedure")
    verbose_name_plural = _("Background procedures")
    max_length = 100
    item_class = Procedure
    column_names = "value name text class_name kwargs"
    required_roles = dd.login_required(SiteStaff)

    # task_classes = []

    # @classmethod
    # def sort_for_runner(cls):

    @classmethod
    def add_item(cls, *args, **kwargs):
        rv = super().add_item(*args, **kwargs)
        newchoices = []
        collected_funcs = set()
        todo = cls.choices
        while len(todo):
            later = []
            for p_text in todo:
                p, text = p_text
                if p.run_after is None or p.run_after in collected_funcs:
                    newchoices.append(p_text)
                    collected_funcs.add(p.name)
                else:
                    later.append(p_text)
            if len(later) == len(todo):
                # raise Exception(f"No {p.run_after} in {collected_funcs}")
                newchoices += todo
                break
            todo = later
        cls.choices = newchoices
        return rv

    @classmethod
    def task_classes(cls):
        return [
            dd.resolve_model(spec) for spec in {c.class_name for c, _ in cls.choices}
        ]

    @dd.virtualfield(dd.CharField(_("Task class")))
    def class_name(cls, choice, ar):
        return choice.class_name

    @dd.virtualfield(dd.CharField(_("Suggested recurrency")))
    def kwargs(cls, choice, ar):
        return ", ".join(["{}={}".format(*i) for i in sorted(choice.kwargs.items())])


class LogLevel(dd.Choice):
    num_value = logging.NOTSET

    def __init__(self, name):
        self.num_value = getattr(logging, name)
        super().__init__(name, name, name)


class LogLevels(dd.ChoiceList):
    verbose_name = _("Logging level")
    verbose_name_plural = _("Logging levels")
    item_class = LogLevel
    column_names = "value text num_value"

    @dd.virtualfield(dd.IntegerField(_("Numeric value")))
    def num_value(cls, choice, ar):
        return choice.num_value


LogLevel.set_widget_options("num_value", hide_sum=True)

add = LogLevels.add_item
add("DEBUG")
add("INFO")
add("WARNING")
add("ERROR")
add("CRITICAL")


def background_task(**kwargs):
    if "class_name" not in kwargs:
        kwargs["class_name"] = "linod.SystemTask"

    def decorator(func):
        Procedures.add_item(func, **kwargs)
        return func

    return decorator


def schedule_often(every=10, **kwargs):
    kwargs.update(every_unit="secondly", every=every)
    return background_task(**kwargs)


def schedule_daily(**kwargs):
    kwargs.update(every_unit="daily", every=1)
    return background_task(**kwargs)
