# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import base64
import os
import shutil
import uuid
from pathlib import Path

# from rstgen.sphinxconf.sigal_image import parse_image_spec
# from rstgen.sphinxconf.sigal_image import Standard, Thumb, Tiny, Wide, Solo, Duo, Trio
# SMALL_FORMATS = (Thumb, Tiny, Duo, Trio)
#
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError, FieldError
from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html
from django.utils import timezone

from lino.core import constants
from lino.utils import DATE_TO_DIR_TPL
from lino.utils import needs_update
from lino.utils.html import E
from lino.api import dd, rt, _
from lino.modlib.uploads import UPLOADS_ROOT
from lino.modlib.comments.mixins import Commentable

# from lino.mixins.sequenced import Sequenced
# from lino.modlib.gfks.mixins import Controllable
from .choicelists import UploadAreas

upload_to_tpl = UPLOADS_ROOT + "/" + DATE_TO_DIR_TPL


def safe_filename(name):
    # Certain Python versions or systems don't manage non-ascii filenames, so we
    # replace any non-ascii char by "_". In Py3, encode() returns a bytes
    # object, but we want the name to remain a str.
    name = name.encode("ascii", "replace").decode("ascii")
    name = name.replace("?", "_")
    name = name.replace("/", "_")
    name = name.replace(" ", "_")
    return name


def make_uploaded_file(filename, src=None, upload_date=None):
    """
    Create a dummy file that looks as if a file had really been uploaded.

    """
    if src is None:
        src = Path(__file__).parent / "dummy_upload.pdf"
    if upload_date is None:
        upload_date = dd.demo_date()
    if not src.exists():
        raise Exception(f"Source {src} does not exist")
    filename = default_storage.generate_filename(safe_filename(filename))
    upload_to = Path(upload_date.strftime(upload_to_tpl))
    upload_filename = default_storage.generate_filename(
        str(upload_to / filename))
    dest = settings.SITE.media_root / upload_filename
    if needs_update(src, dest):
        print("cp {} {}".format(src, dest))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    return upload_filename


def base64_to_image(imgstring):
    type, file = imgstring.split(";base64,")
    imgdata = base64.b64decode(file)
    return make_captured_image(imgdata, dd.now(), ext=f".{type.split('/')[1]}")


def make_captured_image(imgdata, upload_date=None, filename=None, ext='.jpg'):
    if upload_date is None:
        upload_date = dd.today()
    if not filename:
        filename = str(uuid.uuid4()) + ext
    filename = default_storage.generate_filename(safe_filename(filename))
    upload_to = Path(upload_date.strftime(upload_to_tpl))
    upload_filename = default_storage.generate_filename(
        str(upload_to / filename))
    dest = Path(settings.MEDIA_ROOT) / upload_filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(imgdata)
    # with dest.open("wb") as f:
    #     f.write(imgdata)
    return upload_filename


def demo_upload(filename, src=None, upload_date=None, **kw):
    """
    Return an upload entry that looks as if a file had really been uploaded.

    """
    kw["file"] = make_uploaded_file(filename, src, upload_date)
    return rt.models.uploads.Upload(**kw)


# class FileUsable(Sequenced, Controllable):
#
#     class Meta:
#         abstract = True
#
#     file = None
#
#     @classmethod
#     def on_analyze(cls, site):
#         if cls.file is None:
#             raise FieldError("Set 'file' field to ForeignKey pointing to a file model.")
#         return super().on_analyze(site)


class UploadController(dd.Model):
    class Meta(object):
        abstract = True

    def get_upload_area(self):
        return UploadAreas.general

    def get_uploads_volume(self):
        return None

    if dd.is_installed("uploads"):
        show_uploads = dd.ShowSlaveTable(
            "uploads.UploadsByController", react_icon_name="pi-upload", button_text="❏"
        )  # 274f
        # button_text="⍐")  # 2350
        # button_text="🖿")  # u"\u1F5BF"


class GalleryViewable(dd.Model):
    class Meta:
        abstract = True

    def get_gallery_item(self, ar):
        return {}


class UploadBase(Commentable, GalleryViewable):

    class Meta:
        abstract = True

    extra_display_modes = {constants.DISPLAY_MODE_GALLERY}

    file = models.FileField(_("File"), blank=True, upload_to=upload_to_tpl)
    mimetype = models.CharField(
        _("MIME type"), blank=True, max_length=255, editable=False)
    file_size = models.IntegerField(_("File size"), editable=False, null=True)

    def handle_uploaded_files(self, request, file=None):
        # ~ from django.core.files.base import ContentFile
        if not file and "file" not in request.FILES:
            dd.logger.debug("No 'file' has been submitted.")
            return
        uf = file or request.FILES["file"]  # an UploadedFile instance

        self.save_newly_uploaded_file(uf)

    def save_newly_uploaded_file(self, uf):
        # ~ cf = ContentFile(request.FILES['file'].read())
        # ~ print f
        # ~ raise NotImplementedError
        # ~ dir,name = os.path.split(f.name)
        # ~ if name != f.name:
        # ~ print "Aha: %r contains a path! (%s)" % (f.name,__file__)
        self.size = uf.size
        self.mimetype = uf.content_type

        # ~ dd.logger.info('20121004 handle_uploaded_files() %r',uf.name)
        name = safe_filename(uf.name)

        # Django magics:
        self.file = name  # assign a string
        ff = self.file  # get back a django.core.files.File instance !
        # ~ print 'uf=',repr(uf),'ff=',repr(ff)

        # ~ if not ispure(uf.name):
        # ~ raise Exception('uf.name is a %s!' % type(uf.name))

        ff.save(name, uf, save=False)

        # The expression `self.file`
        # now yields a FieldFile instance that has been created from `uf`.
        # see Django FileDescriptor.__get__()

        dd.logger.info("Wrote uploaded file %s", ff.path)

    def get_gallery_item(self, ar):
        if (mf := self.get_media_file()) is not None:
            url = mf.get_image_url()
        else:
            url = "20250703"
        return dict(image_src=url)

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        self.file_size = self.get_real_file_size()

    def get_real_file_size(self):
        return None

    def get_file_button(self, text=None):
        if text is None:
            text = str(self)
        mf = self.get_media_file()
        if mf is None:
            return text
        return E.a(text, href=mf.get_download_url(), target="_blank")

    # def memo2html(self, ar, text, **ctx):
    #     mf = self.get_media_file()
    #     if mf is None:
    #         return format_html("<em>{}</em>", text or str(self))
    #     ctx.update(src=mf.get_download_url())
    #     ctx.update(href=ar.renderer.obj2url(ar, self))
    #     small_url = mf.get_image_url()
    #     if small_url is None or small_url == mf.url:  # non-previewable mimetype
    #         if not text:
    #             text = str(self)
    #         ctx.update(text=text)
    #         tpl = '(<a href="{src}" target="_blank">{text}</a>'
    #         tpl += '| <a href="{href}">detail</a>)'
    #         return format_html(tpl, **ctx)
    #
    #     fmt = parse_image_spec(text, **ctx)
    #     if isinstance(fmt, SMALL_FORMATS):
    #         fmt.context.update(src=small_url)
    #
    #     if not fmt.context["caption"]:
    #         fmt.context["caption"] = self.description or str(self)
    #
    #     rv = format_html(
    #         '<a href="{href}" target="_blank"><img src="{src}"'
    #         + ' style="{style}" title="{caption}"/></a>', **fmt.context)
    #     # if ar.renderer.front_end.media_name == 'react':
    #     #     return ('<figure class="lino-memo-image"><img src="{src}" ' +
    #     #         'style="{style}" title="{caption}"/><figcaption' +
    #     #         ' style="text-align: center;">{caption}</figcaption>' +
    #     #         '</figure>').format(**kwargs)
    #
    #     # print("20230325", rv)
    #     return rv
