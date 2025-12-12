# -*- coding: UTF-8 -*-
# Copyright 2010-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from os.path import splitext
from django.conf import settings
from django.utils.text import format_lazy
from lino.api import dd, rt, _
from lino.utils import needs_update

try:
    from PIL import Image  # pip install Pillow
    import pymupdf    # pip install PyMuPDF
except ImportError:
    pass

with_thumbnails = dd.get_plugin_setting('uploads', 'with_thumbnails', False)


class UploadMediaFile:

    def __init__(self, url):
        self.url = url
        assert url is not None
        root, suffix = splitext(url)
        self.suffix = suffix.lower()

    def get_image_name(self):
        if self.suffix not in previewer.PREVIEW_SUFFIXES:
            return None
        if previewer.base_dir is None:
            if self.suffix == ".pdf":
                return None
            return self.url
        url = self.url
        if self.suffix == ".pdf":
            url += ".png"
        return previewer.base_dir + "/" + url

    def is_image(self):
        # whether this can be rendered in an <img> tag
        if self.get_image_name() is None:
            return False
        return self.suffix in previewer.PREVIEW_SUFFIXES

    def get_mimetype_description(self):
        if self.suffix == ".pdf":
            return _("PDF file")
        if self.get_image_name():
            return _("picture")
        return _("media file")

    def get_image_url(self):
        url = self.get_image_name()
        if url is not None:
            return settings.SITE.build_media_url(url)

    def get_download_url(self):
        return settings.SITE.build_media_url(self.url)


class Previewer:
    # The bare media previewer. It doesn't do any real work.
    base_dir = None
    max_width = None
    PREVIEW_SUFFIXES = {'.png', '.jpg', '.jpeg'}

    def check_preview(self, obj, fix=False):
        return []


class FilePreviewer(Previewer):
    # A media previewer that builds thumbnails in a separate directory tree
    PREVIEW_SUFFIXES = {'.png', '.jpg', '.jpeg', '.pdf'}

    def __init__(self, base_dir=None, max_width=None):
        self.base_dir = base_dir
        self.max_width = max_width
        super().__init__()

    def check_preview(self, obj, fix=False):
        mf = obj.get_media_file()
        if mf is None:
            return
        if (dst := mf.get_image_name()) is None:
            return
        if dst == mf.url:
            raise Exception("20241113 should never happen")
            return
        src = settings.SITE.media_root / mf.url
        dst = settings.SITE.media_root / dst

        if needs_update(src, dst):
            yield (True, format_lazy(_("Must build thumbnail for {}"), mf.url))
            if fix:
                dst.parent.mkdir(parents=True, exist_ok=True)
                # Make parent dir also for pdf previews. See #6181 (Issues after
                # uploading two PDFs to froinde)
                if src.suffix.lower() == ".pdf":
                    doc = pymupdf.open(src)
                    page = doc.load_page(0)
                    pixmap = page.get_pixmap(dpi=120)
                    pixmap.save(dst)
                    return
                with Image.open(src) as im:
                    im.thumbnail((self.max_width, self.max_width))
                    im.save(dst)


if with_thumbnails:
    previewer = FilePreviewer("thumbs", 720)
else:
    previewer = Previewer()
