# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings

suffix = "_" + settings.SITE.site_dir.name

CHANNEL_NAME = "linod" + suffix
BROADCAST_CHANNEL = "broadcast" + suffix

get_channel_name = lambda name: str(name) + suffix
