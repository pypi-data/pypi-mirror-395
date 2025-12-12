# -*- coding: utf-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from asgiref.sync import async_to_sync
from lino.api import dd, rt
from lino.modlib.linod.mixins import start_task_runner

# import logging
# from lino import logger
# def getHandlerByName(name):
#     for l in logger.handlers:
#         if l.name == name:
#             return l


def objects():
    ar = rt.login(dd.plugins.users.demo_username)
    # logger.setLevel(logging.DEBUG)
    # getHandlerByName('console').setLevel(logging.DEBUG)
    # ar.debug("Coucou")
    async_to_sync(start_task_runner)(ar, max_count=1)
    return []
