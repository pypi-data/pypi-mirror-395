# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Stored periods")
    period_name = _("Accounting period")
    period_name_plural = _("Accounting periods")
    year_name = _("Fiscal year")
    year_name_plural = _("Fiscal years")
    start_year = 2012
    start_month = 1
    period_type = "month"
    fix_y2k = False
    short_ref = False

    def pre_site_startup(self, site):
        if isinstance(self.period_type, str):
            self.period_type = site.models.periods.PeriodTypes.get_by_name(
                self.period_type)
        super().pre_site_startup(site)

    def before_analyze(self):
        if self.fix_y2k and self.start_month != 1:
            raise Exception("When fix_y2k is set, start_month must be 1")
        super().before_analyze()

    def setup_config_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action("periods.StoredYears")
        m.add_action("periods.StoredPeriods")
