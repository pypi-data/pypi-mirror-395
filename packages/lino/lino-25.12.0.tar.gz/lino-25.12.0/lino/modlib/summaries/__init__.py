# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Docs: https://dev.lino-framework.org/specs/summaries.html

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Summaries")
    start_year = None
    end_year = None
    duration_max_length = 6

    def pre_site_startup(self, site):
        if self.end_year is None:
            self.end_year = site.today().year
        if self.start_year is None:
            self.start_year = self.end_year - 2
