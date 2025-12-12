# Copyright 2014-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
See :doc:`/plugins/export_excel`.
"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Export to Excel xls format")

    def get_requirements(self, site):
        yield "openpyxl"
