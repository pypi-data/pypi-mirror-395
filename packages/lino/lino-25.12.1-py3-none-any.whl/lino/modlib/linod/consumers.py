# -*- coding: UTF-8 -*-
# Copyright 2022-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import asyncio
import json
import os
import socket
import logging
import struct
import sys
from pathlib import Path

try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

# from asgiref.sync import sync_to_async
from django.conf import settings

# from django.utils import timezone
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer

# from lino.modlib.linod.tasks import Tasks
# from lino.utils.socks import send_through_socket, get_from_socket

from lino import logger

# from lino.api import dd
from .utils import BROADCAST_CHANNEL

# used for debugging, when no 'log' dir exists
# if not logger.handlers:
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.INFO)


def is_slave(actor): return actor.master is not None


match_master = (
    lambda ContentType, MasterModel, Master: Master == MasterModel
    or ContentType == Master
    or issubclass(Master, MasterModel)
)


class LinodConsumer(AsyncConsumer):
    # tasks: Tasks
    # clients = set()

    async def log_server(self, event=None):
        # 'log.server' in `pm linod`
        from lino.modlib.linod.mixins import start_log_server

        asyncio.ensure_future(start_log_server())

    async def run_background_tasks(self, event: dict):
        # 'run.background.tasks' in `pm linod`
        from lino.modlib.linod.mixins import start_task_runner
        # from lino.core.utils import login
        # ar = login(settings.SITE.plugins.linod.daemon_user)
        from lino.core.requests import BaseRequest
        u = await settings.SITE.user_model.objects.aget(
            username=settings.SITE.plugins.linod.daemon_user)
        ar = BaseRequest(user=u)
        asyncio.ensure_future(start_task_runner(ar))

    async def send_push(self, event):
        # 'send.push' in notify.send_notification()
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event["data"]
        user = event["user_id"]
        if user is not None:
            user = await database_sync_to_async(
                settings.SITE.models.users.User.objects.get
            )(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=settings.SITE.plugins.notify.vapid_private_key,
            vapid_claims={
                "sub": "mailto:{}".format(
                    settings.SITE.plugins.notify.vapid_admin_email
                )
            },
        )
        if user is None:
            subs = settings.SITE.models.notify.Subscription.objects.all()
        else:
            subs = settings.SITE.models.notify.Subscription.objects.filter(
                user=user)
        async for sub in subs.aiterator():
            sub_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256dh": sub.p256dh,
                    "auth": sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    await database_sync_to_async(sub.delete)()
                else:
                    raise e

    async def send_panel_update(self, event):
        from lino.api import rt, dd

        msg = json.loads(event["text"])
        ups = [rt.models.resolve(aID) for aID in msg["actorIDs"]]
        data = dict(
            [
                (a.actor_id, {"mk": None, "mt": None, "pk": msg["pk"]})
                for a in ups
                if not is_slave(a)
            ]
        )
        if msg["mk"] is not None:
            MasterModel = rt.models.resolve(msg["master_model"])
            ContentType = rt.models.contenttypes.ContentType
            mt = (
                await database_sync_to_async(ContentType.objects.get_for_model)(
                    MasterModel
                )
            ).pk
            data.update(
                **dict(
                    [
                        (a.actor_id, {"mk": msg["mk"],
                         "mt": mt, "pk": msg["pk"]})
                        for a in ups
                        if is_slave(a)
                        and match_master(ContentType, MasterModel, a.master)
                    ]
                )
            )
        await self.channel_layer.group_send(
            BROADCAST_CHANNEL,
            {
                "type": "send.notification",
                "text": json.dumps({"type": msg["type"], "data": data}),
            },
        )

    # async def dev_worker(self, event: dict):
    #     # dev.worker in linod
    #     # worker_sock = str(worker_sock_path)
    #
    #     def add_client(sock: socket.socket) -> None:
    #         self.clients.add(get_from_socket(sock))
    #         sock.close()
    #
    #     def remove_client(sock: socket.socket, close: bool = True) -> None:
    #         self.clients.discard(get_from_socket(sock))
    #         if close:
    #             sock.close()
    #
    #     def client_exists(sock: socket.socket) -> None:
    #         if get_from_socket(sock) in self.clients:
    #             send_through_socket(sock, b'true')
    #         else:
    #             send_through_socket(sock, b'false')
    #         handle_msg(sock)
    #
    #     def process_remove_get(sock: socket.socket) -> None:
    #         remove_client(sock, False)
    #         data = pickle.dumps({'clients': len(self.clients), 'pid': os.getpid()})
    #         send_through_socket(sock, data)
    #         sock.close()
    #
    #     SIGNALS = {
    #         b'add': add_client,
    #         b'exists': client_exists,
    #         b'remove': remove_client,
    #         b'remove_get': process_remove_get,
    #         b'close': lambda sock: sock.close()
    #     }
    #
    #     def handle_msg(client_sock: socket.socket) -> None:
    #         msg = get_from_socket(client_sock)
    #         if msg not in SIGNALS:
    #             send_through_socket(client_sock, b"Invalid signal!")
    #             client_sock.close()
    #         else:
    #             SIGNALS[msg](client_sock)
    #
    #     try:
    #         with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    #             worker_sock_path.unlink(True)
    #             sock.bind(str(worker_sock_path))
    #             sock.listen(5)
    #             while True:
    #                 client_sock, _ = sock.accept()
    #                 handle_msg(client_sock)
    #     finally:
    #         worker_sock_path.unlink(True)
