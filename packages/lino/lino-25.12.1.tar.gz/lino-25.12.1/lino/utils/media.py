# -*- coding: UTF-8 -*-
# Copyright 2013-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the :class:`MediaFile` class.
"""

from pathlib import Path
from django.conf import settings
# from lino.core.utils import is_devserver

# davlink = settings.SITE.plugins.get('davlink', None)
# has_davlink = davlink is not None and settings.SITE.use_java
has_davlink = False


class MediaFile(object):
    """
    Represents a file on the server below :setting:`MEDIA_ROOT` with
    two properties :attr:`path` and :attr:`url`.

    It takes into consideration the settings
    :attr:`webdav_root <lino.core.site.Site.webdav_root>`,
    :attr:`webdav_protocol <lino.core.site.Site.webdav_protocol>`
    and
    :attr:`webdav_url <lino.core.site.Site.webdav_url>`.

    .. attribute:: path

        A :class:`pathlib.Path` naming the file on the server's file system.

    .. attribute:: url

        The URL to use for getting this file from a web client.

    Used by :meth:`lino.modlib.jinja.XMLMaker.get_xml_file`,
    :attr:`lino.core.tables.AbstractTable.export_excel` and others.

    """

    def __init__(self, editable, *parts):
        self.editable = editable
        # self.parts = parts
        if editable and settings.SITE.webdav_protocol:
            path = Path(settings.SITE.webdav_root, *parts)
            # 20250302 Removed the file:// trick on a devserver because anyway
            # it doesn't work anymore. For editable media files we need a a
            # webdav server and a protocol handler.
            # if is_devserver():
            if False:
                url = "file://" + settings.SITE.webdav_root + "/".join(parts)
            else:
                url = settings.SITE.webdav_url + "/".join(parts)
                if settings.SITE.webdav_protocol:
                    url = settings.SITE.webdav_protocol + "://" + url
        else:
            path = Path(settings.MEDIA_ROOT, *parts)
            url = settings.SITE.build_media_url(*parts)
        self.url = url
        self.path = path


class TmpMediaFile(MediaFile):
    def __init__(self, ar, fmt):
        ip = ar.request.META.get("REMOTE_ADDR", "unknown_ip")
        super().__init__(
            False, "cache", "appy" + fmt, ip, str(ar.actor) + "." + fmt)
