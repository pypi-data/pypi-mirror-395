# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from lino.api import rt
from lino.modlib.uploads.mixins import make_uploaded_file


def objects():
    print("Create an orphan file foo.pdf in uploads folder")
    make_uploaded_file("foo.pdf")

    Upload = rt.models.uploads.Upload
    u = Upload.objects.exclude(file="").first()
    if u is not None:
        print("Remove {}".format(u.file.path))
        os.remove(u.file.path)

    return []
