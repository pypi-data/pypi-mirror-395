# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Some actions are described by a single action instance used by most actors:

from lino.core.actions import (ShowInsert, ShowTable, SubmitDetail,
                               DeleteSelected, SaveGridCell, ValidateForm)

SHOW_INSERT = ShowInsert()
SHOW_TABLE = ShowTable()
SUBMIT_DETAIL = SubmitDetail()
DELETE_ACTION = DeleteSelected()
UPDATE_ACTION = SaveGridCell()
VALIDATE_FORM = ValidateForm()
