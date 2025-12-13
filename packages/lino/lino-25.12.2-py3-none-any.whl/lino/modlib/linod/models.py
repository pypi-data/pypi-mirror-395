# -*- coding: UTF-8 -*-
# Copyright 2023-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

from lino.api import dd, _
from lino.core.roles import SiteStaff
from lino import logger
# from lino.modlib.checkdata.choicelists import Checker
from .choicelists import Procedures, LogLevels

# if dd.plugins.linod.use_channels:
#     from channels.db import database_sync_to_async

from .mixins import Runnable


class SystemTask(Runnable):
    class Meta:
        abstract = dd.is_abstract_model(__name__, "SystemTask")
        app_label = "linod"
        verbose_name = _("System task")
        verbose_name_plural = _("System tasks")

    def run_task(self, ar):
        return self.procedure.run(ar)


class SystemTasks(dd.Table):
    # label = _("System tasks")
    model = "linod.SystemTask"
    order_by = ['seqno']
    required_roles = dd.login_required(SiteStaff)
    column_names = "seqno name log_level disabled status procedure dndreorder *"
    detail_layout = """
    seqno procedure
    name
    every every_unit
    log_level disabled status
    requested_at last_start_time last_end_time
    message
    """
    insert_layout = """
    procedure
    every every_unit
    """


# class SystemTaskChecker(Checker):
#     """
#     Checks for procedures that do not yet have a background task.
#     """
#
#     verbose_name = _("Check for missing system tasks")
#     model = None
#
#     def get_checkdata_problems(self, ar, obj, fix=False):
#         for proc in Procedures.get_list_items():
#             if proc.class_name == "linod.SystemTask":
#                 if SystemTask.objects.filter(procedure=proc).count() == 0:
#                     msg = _("No {} for {}").format(
#                         SystemTask._meta.verbose_name, proc)
#                     yield (True, msg)
#                     if fix:
#                         logger.debug("Create background task for %r", proc)
#                         jr = SystemTask(procedure=proc, **proc.kwargs)
#                         # every_unit=proc.every_unit, every=proc.every_value)
#                         if jr.every_unit == "secondly":
#                             jr.log_level = "WARNING"
#                         jr.full_clean()
#                         jr.save()
#
#
# SystemTaskChecker.activate()
