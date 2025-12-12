# Copyright 2015-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Provides a menu hook for several other plugins.

See :doc:`/plugins/office`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Office")
