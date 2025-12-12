# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Runs the :manage:`checksummaries` management command.

"""

from django.core.management import call_command
from lino.api import dd


def objects():
    if not dd.is_installed("linod"):
        call_command("checksummaries")
    return []
