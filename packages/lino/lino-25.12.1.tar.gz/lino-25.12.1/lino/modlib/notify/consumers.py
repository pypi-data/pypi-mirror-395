# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from lino import logger
from lino.modlib.linod.utils import BROADCAST_CHANNEL, get_channel_name


class ClientConsumer(AsyncWebsocketConsumer):
    groups = []
    user = None

    async def connect(self):
        await self.accept()
        if not self.channel_name:
            # 20230216 on Jane we had TypeError: int() argument must be a
            # string, a bytes-like object or a number, not 'NoneType'
            return
        self.user = self.scope.get("user")
        await self.channel_layer.group_add(BROADCAST_CHANNEL, self.channel_name)
        if not self.user.is_anonymous:
            await self.channel_layer.group_add(
                get_channel_name(self.user.id), self.channel_name
            )

    async def send_notification(self, text):
        # 'send.notification' in notify.send_notification
        await self.send(text_data=text["text"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(BROADCAST_CHANNEL, self.channel_name)
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(
                get_channel_name(self.user.id), self.channel_name
            )
