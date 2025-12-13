# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils.translation import gettext_lazy as _

# from lino.api import dd
from lino.core.choicelists import Choice, ChoiceList
from lino.core.workflows import Workflow
from lino.core.fields import displayfield


class PeriodType(Choice):
    ref_template = None

    def __init__(self, value, text, duration, ref_template):
        super().__init__(value, text, value)
        self.ref_template = ref_template
        self.duration = duration
        self.seqnos = tuple(range(1, int(12/duration)+1))


class PeriodTypes(ChoiceList):
    item_class = PeriodType
    verbose_name = _("Period type")
    verbose_name_plural = _("Period types")
    column_names = "value text duration ref_template"

    @displayfield(_("Duration"))
    def duration(cls, p, ar):
        return str(p.duration)

    @displayfield(_("Template for reference"))
    def ref_template(cls, p, ar):
        return p.ref_template


add = PeriodTypes.add_item
# value/names,  text, duration, ref_template
add("month",     _("Month"),     1, "{month:0>2}")
add("quarter",   _("Quarter"),   3, "Q{seqno}")
add("trimester", _("Trimester"), 4, "T{seqno}")
add("semester",  _("Semester"),  6, "S{seqno}")


class PeriodStates(Workflow):
    pass


add = PeriodStates.add_item
add('10', _("Open"), 'open')
add('20', _("Closed"), 'closed')
