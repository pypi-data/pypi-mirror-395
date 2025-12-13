# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt
from lino.modlib.system.choicelists import Recurrences
from lino.modlib.uploads.choicelists import Shortcuts


def objects():
    UploadType = rt.models.uploads.UploadType

    kw = dict(max_number=1, wanted=True)

    for us in Shortcuts.get_list_items():
        kw.update(dd.str2kw('name', us.text))
        yield UploadType(shortcut=us, **kw)
