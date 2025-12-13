# Copyright 2015-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.modlib.uploads.roles import UploadsReader


class OfficeUser(UploadsReader):
    pass


class OfficeOperator(UploadsReader):
    pass


class OfficeStaff(OfficeUser, OfficeOperator):
    pass
