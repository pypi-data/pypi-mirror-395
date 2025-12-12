# -*- coding: UTF-8 -*-
# Copyright 2022-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import asyncio
from django.conf import settings
from django.core.management import BaseCommand, call_command
from lino.api import dd
from lino.modlib.linod.mixins import start_task_runner
from lino.core.requests import BaseRequest

if dd.plugins.linod.use_channels:
    import threading
    from channels.layers import get_channel_layer
    from lino.modlib.linod.utils import CHANNEL_NAME


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not dd.plugins.linod.use_channels:
            # print("20240424 Run Lino daemon without channels")

            async def main():
                try:
                    u = await settings.SITE.user_model.objects.aget(
                        username=settings.SITE.plugins.linod.daemon_user)
                except settings.SITE.user_model.DoesNotExist:
                    u = None
                ar = BaseRequest(user=u)
                # await asyncio.gather(start_log_server(), start_task_runner(ar))
                await start_task_runner(ar)
                # t1 = asyncio.create_task(settings.SITE.start_log_server())
                # t2 = asyncio.create_task(start_task_runner(ar))
                # await t1
                # await t2

            asyncio.run(main())

        else:
            # print("20240424 Run Lino daemon using channels")

            def start_channels():
                try:
                    asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    # loop.set_debug(True)
                    asyncio.set_event_loop(loop)
                call_command("runworker", CHANNEL_NAME)

            worker_thread = threading.Thread(target=start_channels)
            worker_thread.start()

            async def initiate_linod():
                layer = get_channel_layer()
                # if log_sock_path is not None:
                # await layer.send(CHANNEL_NAME, {"type": "log.server"})
                # await asyncio.sleep(1)
                await layer.send(CHANNEL_NAME, {"type": "run.background.tasks"})

            # print("20240108 a")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(initiate_linod())
            # print("20240108 c")

            try:
                worker_thread.join()
            except KeyboardInterrupt:
                print("Finishing thread...")
                worker_thread.join(0)
