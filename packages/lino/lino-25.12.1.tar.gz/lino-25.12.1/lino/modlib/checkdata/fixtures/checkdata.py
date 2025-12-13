# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Runs the :manage:`checkdata` management command with `--fix`
option.

"""

from django.core.management import call_command
from lino.api import dd


def objects():
    if not dd.is_installed("linod"):
        call_command("checkdata", fix=True)
    return []
