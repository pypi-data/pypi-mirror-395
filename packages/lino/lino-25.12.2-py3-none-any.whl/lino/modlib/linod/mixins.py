# -*- coding: UTF-8 -*-
# Copyright 2023-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import traceback
import asyncio
from datetime import timedelta
from django.db import models
from django.utils import timezone
# from django.core.exceptions import ValidationError
from asgiref.sync import sync_to_async, async_to_sync

from lino.api import dd, _
from lino.mixins import Sequenced
from lino.modlib.system.mixins import RecurrenceSet
from lino.modlib.system.choicelists import Recurrences
from .choicelists import LogLevels, Procedures

# if dd.plugins.linod.use_channels:
#     from channels.db import database_sync_to_async


def astr(self):
    return str(self)
    # return sync_to_async(self.__str__)()


class RunNow(dd.Action):
    label = _("Run now")
    help_text = _("Mark the task as to be executed asap by linod.")
    select_rows = True
    button_text = "▶"
    # icon_name = 'bell'
    # icon_name = 'lightning'

    # def get_action_permission(self, ar, obj, state):
    #     if obj.requested_at or obj.is_running():
    #         return False
    #     return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kwargs):
        # print("20231102 RunNow", ar.selected_rows)
        # now = dd.now()
        now = timezone.now()
        for obj in ar.selected_rows:
            assert issubclass(obj.__class__, Runnable)
            if True:  # dd.plugins.linod.use_channels:
                obj.last_start_time = None
                obj.last_end_time = None
                obj.requested_at = now
                tpl = _("{0} requested to run this task at {1}.")
                obj.message = tpl.format(ar.get_user(), dd.fdtl(now))
                # obj.disabled = False
                obj.full_clean()
                obj.save()
            else:
                # Run the task myself (not in background).
                async_to_sync(obj.start_task)(ar)
        ar.set_response(refresh=True)


class CancelRun(dd.Action):
    label = _("Cancel request")
    help_text = _("Cancel the request to run this task asap.")
    select_rows = True
    button_text = "🗙"  # ⛒
    # icon_name = 'bell'
    # icon_name = 'lightning'

    # def get_action_permission(self, ar, obj, state):
    #     if obj.requested_at is None:
    #         return False
    #     return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kwargs):
        for obj in ar.selected_rows:
            assert issubclass(obj.__class__, Runnable)
            obj.requested_at = None
            obj.message = "{} cancelled the request to run this task.".format(
                ar.get_user())
            obj.full_clean()
            obj.save()
        ar.set_response(refresh=True)


class Runnable(Sequenced, RecurrenceSet):
    class Meta:
        abstract = True

    log_level = LogLevels.field(default="INFO")
    disabled = dd.BooleanField(_("Disabled"), default=False)
    last_start_time = dd.DateTimeField(
        _("Started at"), null=True, editable=False)
    last_end_time = dd.DateTimeField(_("Ended at"), null=True, editable=False)
    requested_at = dd.DateTimeField(_("Requested at"), null=True, editable=False)
    message = dd.RichTextField(
        _("Logged messages"), format="plain", editable=False)

    # procedure = Procedures.field(strict=False, unique=True, editable=False)
    procedure = Procedures.field(strict=False)
    name = models.CharField(_("Name"), max_length=200, blank=True)

    run_now = RunNow()
    cancel_run = CancelRun()

    def __str__(self):
        # r = "{} ({} #{})".format(
        #     self.name, self._meta.verbose_name, self.seqno)
        r = "{} #{} ({})".format(
            self._meta.verbose_name, self.seqno, self.name)
        return r

    def disabled_fields(self, ar):
        rv = super().disabled_fields(ar)
        if self.requested_at is None:
            rv.add('cancel_run')
        else:
            rv.add('run_now')
        return rv

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        # 20250213 The following caused 'Invalid procedure invoicing.Task for
        # linod.SystemTask' during restore.py:
        # class_name = dd.full_model_name(self.__class__)
        # if self.procedure.class_name != class_name:
        #     raise ValidationError(f"Invalid procedure {self.procedure.class_name} for {class_name}")
        if self.every_unit is None:
            self.every_unit = Recurrences.never
        if not self.name:
            self.name = str(self.procedure.value)

    def is_running(self):
        return self.last_end_time is None and self.last_start_time is not None

    def run_task(self, ar):
        raise NotImplementedError()

    @dd.chooser()
    def procedure_choices(cls):
        # print([p.class_name for p in Procedures.get_list_items()])
        return Procedures.filter(class_name=dd.full_model_name(cls))

    async def start_task(self, ar):
        # print("20231102 start_task", self)
        if self.is_running():
            raise Warning(_("{} is already running").format(astr(self)))
            # return
        # Start and Terminated messages are logged with debug, not info, because
        # e.g. send_pending_emails_often runs every 5 seconds
        await ar.adebug("Start %s with logging level %s", self, self.log_level)
        # ar.info("Start %s with logging level %s", astr(self), self.log_level)
        # forget about any previous run:
        # now = await sync_to_async(dd.now)()
        now = timezone.now()
        self.last_start_time = now
        self.requested_at = None
        self.last_end_time = None
        self.message = f"Started at {self.last_start_time} " \
            f"with logging level {self.log_level}"
        # print("20231102 full_clean")
        await sync_to_async(self.full_clean)()
        # self.full_clean()
        # print("20231102 save")
        await self.asave()
        with ar.capture_logger(self.log_level.num_value) as out:
            # await ar.ainfo("Start %s using %s...", self, self.log_level)
            # print("20231021", ar.logger)
            try:
                # self.run_task(ar)
                # await database_sync_to_async(self.run_task)(ar)
                await sync_to_async(self.run_task)(ar)
                # job.message = ar.response.get('info_message', '')
                await ar.adebug("Successfully terminated %s", self)
                # ar.info("Successfully terminated %s", astr(self))
                self.message = out.getvalue()
            except Warning as e:
                await ar.adebug("Terminated %s with warning %s", self, str(e))
                self.message = out.getvalue()
            except Exception as e:
                tb = "".join(traceback.format_exception(e))
                self.message = out.getvalue()
                self.message += "\n" + tb
                self.disabled = True
                await ar.awarning("Disabled %s after exception:\n%s", self, tb)
                # ar.warning("Disabled %s after exception %s", astr(self), e)
        # now = await sync_to_async(dd.now)()
        self.last_end_time = timezone.now()
        self.message = "<pre>" + self.message + "</pre>"
        await sync_to_async(self.full_clean)()
        # self.full_clean()
        await self.asave()
        await sync_to_async(dd.post_ui_save.send)(sender=self.__class__, instance=self)

    @dd.displayfield("Status")
    def status(self, ar=None):
        if self.is_running():
            return _("Running since {}").format(dd.fdtf(self.last_start_time))
        if self.requested_at is not None:
            return _("Requested to run asap (since {})").format(
                dd.fdtf(self.requested_at))
        if self.disabled:
            return _("Disabled")
        if self.last_start_time is None or self.last_end_time is None:
            if self.every_unit in {Recurrences.never, None}:
                return _("Not scheduled")
            return _("Scheduled to run asap")
        next_time = self.get_next_suggested_date(self.last_end_time)
        if next_time is None:
            return _("Not scheduled")
        return _("Scheduled to run at {}").format(dd.fdtf(next_time))


async def start_task_runner(ar=None, max_count=None):
    # called from consumers.LinoConsumer.run_background_tasks()
    await ar.ainfo("Start task runner using %s...", ar.logger)
    # ar.info("Start task runner using %s...", ar.logger)
    # await sync_to_async(tasks.setup)()
    # print("20240109", ar.logger.handlers)

    # Procedures.sort_for_runner()
    for proc in Procedures.get_list_items():
        await proc.install_if_needed(ar)

    count = 0
    while True:
        await ar.adebug("Start next task runner loop.")
        # now = await sync_to_async(dd.now)()
        now = timezone.now()
        next_time = now + \
            timedelta(seconds=dd.plugins.linod.background_sleep_time)

        tasks = []
        for cls in Procedures.task_classes():
            # asyncio.ensure_future(m.start_task_runner(ar.spawn_request()))
            # print("20240424b")
            async for obj in cls.objects.filter(
                    requested_at__isnull=False).order_by("requested_at"):
                tasks.append(obj)
        for cls in Procedures.task_classes():
            async for obj in cls.objects.filter(
                    requested_at__isnull=True, disabled=False).order_by("seqno"):
                tasks.append(obj)
            # print("20240424c")
            # async for self in tasks:
        for self in tasks:
            # print("20240424d")
            # raise Warning("20231230")
            if max_count is not None and not self.procedure.during_initdb:
                # print(f"20250621 skip {self} during initdb")
                continue
            if self.last_end_time is None and self.last_start_time is not None:
                run_duration = now - self.last_start_time
                if run_duration > timedelta(hours=2):
                    msg = "Killed {} because running more than 2 hours".format(
                        astr(self)
                    )
                    await ar.adebug(msg)
                    self.last_end_time = now
                    self.message = msg
                    await sync_to_async(self.full_clean)()
                    # self.full_clean()
                    await self.asave()
                    # self.disabled = True
                else:
                    await ar.adebug("Skip running task %s", astr(self))
                continue

            if self.requested_at is None and self.last_end_time is not None:
                nst = await sync_to_async(self.get_next_suggested_date)(
                    self.last_end_time, ar.logger
                )
                if nst is None:
                    await ar.adebug("No time suggested to start %s", astr(self))
                    continue
                if nst > now:
                    await ar.adebug("Too early to start %s", astr(self))
                    next_time = min(next_time, nst)
                    continue

            # await ar.adebug("Start %s", self)
            # print("20231021 1 gonna start", self)
            await self.start_task(ar)
            assert self.last_end_time is not None
            nst = await sync_to_async(self.get_next_suggested_date)(
                self.last_end_time, ar.logger
            )
            if nst is not None:
                next_time = min(next_time, nst)

        count += 1
        if max_count is not None and count >= max_count:
            await ar.ainfo("Stop after %s loops.", max_count)
            return next_time
        # now = await sync_to_async(dd.now)()
        now = timezone.now()
        if (to_sleep := (next_time - now).total_seconds()) <= 0:
            continue
        await ar.adebug("Let task runner sleep for %s seconds.", to_sleep)
        await asyncio.sleep(to_sleep)
