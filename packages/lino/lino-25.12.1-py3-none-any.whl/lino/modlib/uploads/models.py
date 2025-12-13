# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from os.path import join, exists
from pathlib import Path
from html import escape

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils.html import format_html, mark_safe
# from django.utils.translation import pgettext_lazy as pgettext

# from rstgen.sphinxconf.sigal_image import parse_image_spec
# from rstgen.sphinxconf.sigal_image import Standard, Thumb, Tiny, Wide, Solo, Duo, Trio
# SMALL_FORMATS = (Thumb, Tiny, Duo, Trio)

from lino.utils.html import E, join_elems
from lino.api import dd, rt, _
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored

from lino.mixins import Referrable
from lino.utils.soup import register_sanitizer, DATA_UPLOAD_ID
from lino.utils.mldbc.mixins import BabelNamed
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.publisher.mixins import Publishable

from .actions import CameraStream
from .choicelists import Shortcuts, UploadAreas, ImageFormats, ImageSizes, htmlimg
from .mixins import UploadBase, base64_to_image
from .utils import previewer, UploadMediaFile

from . import VOLUMES_ROOT
from .ui import *


class Volume(Referrable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, "Volume")
        app_label = "uploads"
        verbose_name = _("Library volume")
        verbose_name_plural = _("Library volumes")

    preferred_foreignkey_width = 5

    root_dir = dd.CharField(_("Root directory"), max_length=255)
    # base_url = dd.CharField(_("Base URL"), max_length=255, blank=True)
    description = dd.CharField(_("Description"), max_length=255, blank=True)

    def __str__(self):
        return self.ref or self.root_dir

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        pth = dd.plugins.uploads.volumes_root / self.ref
        if pth.exists():
            if pth.resolve().absolute() != Path(self.root_dir).resolve().absolute():
                raise ValidationError(
                    "Existing %s must resolve to %s", pth, self.root_dir)
        else:
            settings.SITE.makedirs_if_missing(pth.parent)
            pth.symlink_to(self.root_dir)

    def get_filenames(self):
        root_len = len(self.root_dir) + 1
        for root, dirs, files in os.walk(self.root_dir):
            relroot = root[root_len:]
            if relroot:
                relroot += "/"
            for fn in files:
                # print(relroot + "/" + fn)
                yield relroot + fn


class UploadType(BabelNamed):
    class Meta:
        abstract = dd.is_abstract_model(__name__, "UploadType")
        app_label = "uploads"
        verbose_name = _("Upload type")
        verbose_name_plural = _("Upload types")

    upload_area = UploadAreas.field(default="general")

    max_number = models.IntegerField(
        _("Max. number"),
        default=-1,
        # help_text=string_concat(
        #     _("No need to upload more uploads than N of this type."),
        #     "\n",
        #     _("-1 means no limit.")))
        help_text=format_lazy(
            "{}\n{}",
            _("No need to upload more uploads than N of this type."),
            _("-1 means no limit."),
        ),
    )
    wanted = models.BooleanField(
        _("Wanted"),
        default=False,
        help_text=_("Add a (+) button when there is no upload of this type."),
    )

    shortcut = Shortcuts.field(blank=True)


class Upload(UploadBase, UserAuthored, Controllable, Publishable):

    class Meta:
        app_label = "uploads"
        abstract = dd.is_abstract_model(__name__, "Upload")
        verbose_name = _("Upload file")
        verbose_name_plural = _("Upload files")

    memo_command = "upload"

    upload_area = UploadAreas.field(default="general")
    type = dd.ForeignKey("uploads.UploadType", blank=True, null=True)
    volume = dd.ForeignKey("uploads.Volume", blank=True, null=True)
    library_file = models.CharField(
        _("Library file"), max_length=255, blank=True)
    description = models.CharField(
        _("Description"), max_length=200, blank=True)
    source = dd.ForeignKey("sources.Source", blank=True, null=True)

    camera_stream = CameraStream()

    def __str__(self):
        if self.description:
            s = self.description
        elif self.file:
            s = filename_leaf(self.file.name)
        elif self.library_file:
            s = filename_leaf(self.library_file)
            # s = "{}:{}".format(self.volume.ref, self.library_file)
        else:
            s = str(self.id)
        if self.type:
            s = str(self.type) + " " + s
        return s

    def get_file_path(self):
        if self.file and self.file.name:
            return self.file.name
        elif self.library_file and self.volume_id and self.volume.ref:
            return VOLUMES_ROOT + "/" + self.volume.ref + "/" + self.library_file
        return None

    def get_media_file(self):
        url = self.get_file_path()
        if url is not None:
            return UploadMediaFile(url)

    def get_create_comment_text(self, ar):
        mf = self.get_media_file()
        if mf is None:
            return super().get_create_comment_text(ar)
        return _("Uploaded an {obj}.").format(obj=mf.get_mimetype_description())
        # or mf.get_image_url() is None:
        # return _("Uploaded {obj}. [{obj.memo_command} {obj.id}].").format(obj=self)

    def get_memo_command(self, ar=None):
        if dd.is_installed("memo"):
            return f"[{self.memo_command} {self.pk} {self}]"
            # cmd = f"[{self.memo_command} {self.pk}"
            # if self.description:
            #     cmd += " " + self.description + "]"
            # else:
            #     cmd += "]"
            # return cmd
        return None

    def get_real_file_size(self):
        if self.file:
            return self.file.size
        if self.volume_id and self.library_file:
            pth = dd.plugins.uploads.volumes_root / self.volume.ref / self.library_file
            return pth.stat().st_size
            # return os.path.getsize(pth)

    def disabled_fields(self, ar):
        df = super().disabled_fields(ar)
        if ar.renderer.front_end.app_label != "react":
            df.add("camera_stream")
        return df

    @dd.displayfield(_("Description"))
    def description_link(self, ar):
        s = str(self)
        if ar is None:
            return s
        return self.get_file_button(s)

    @dd.chooser(simple_values=True)
    def library_file_choices(self, volume):
        if volume is None:
            return []
        return list(volume.get_filenames())

    @dd.chooser()
    def type_choices(self, upload_area):
        UploadType = rt.models.uploads.UploadType
        if upload_area is None:
            return UploadType.objects.all()
        return UploadType.objects.filter(upload_area=upload_area)

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        if self.type is not None:
            self.upload_area = self.type.upload_area
        for i in self.check_previews(True):
            pass

    def check_previews(self, fix):
        p = rt.models.uploads.previewer
        for i in p.check_preview(self, fix):
            yield i

    def as_html(self, ar, mf, title='', **ctx):
        if ar is None:
            return format_html("<em>{}</em>", self)
        ctx.update(src=mf.get_download_url())
        if not mf.is_image():
            ctx.update(title=title)
            tpl = '(<a href="{src}" target="_blank">{title}</a>'
            tpl += '| <a href="{href}">Detail</a>)'
            return format_html(tpl, **ctx)

        ctx.update(src=mf.get_image_url())
        with ar.override_attrs(permalink_uris=True):
            ctx.update(href=ar.obj2url(self))
        if not title:
            title = self.description or str(self)
            if self.source:
                title += " ({}: {})".format(_("Source"), self.source)
        ctx.update(title=title)
        return htmlimg(**ctx)

    def as_tile(self, ar, prev, **kwargs):
        mf = self.get_media_file()
        if mf is None:
            return super().as_tile(ar, prev)
        return self.as_html(ar, mf, **kwargs)

    def get_gallery_item(self, ar):
        d = super().get_gallery_item(ar)
        d.update(title=str(self), id=self.pk)
        cmd = self.get_memo_command(ar)
        if cmd is not None:
            d.update(memo_cmd=cmd)
        return d

    @dd.htmlbox()
    def preview(self, ar):
        mf = self.get_media_file()
        if mf is None:
            txt = _("No preview available")
            return format_html(
                '<p style="text-align:center;padding:2em;">({})</p>', txt)
        # return self.as_html(mf, ImageFormats.default)
        return format_html(
            '<img src="{}" style="max-width:100%;max-height:20em">',
            mf.get_image_url())

    @dd.htmlbox(_("Thumbnail"))
    def thumbnail(self, ar):
        mf = self.get_media_file()
        if mf is None:
            return ""
        return self.as_html(ar, mf, image_size=ImageSizes.tiny)
        # return '<img src="{}" style="height: 15ch; max-width: 22.5ch">'.format(mf.get_image_url())

    def as_page(self, ar, **kwargs):
        yield format_html("<h1>{}</h1>", self)
        mf = self.get_media_file()
        if mf is not None:
            yield format_html('<img src="{}" style="width: 100%;">', mf.get_image_url())
        if self.description:
            yield escape(self.description)
        if self.source:
            yield _("Source") + ": "
            yield ar.obj2htmls(self.source)

    def as_paragraph(self, ar, **kwargs):
        rv = self.memo2html(ar, "")
        # rv = ar.obj2htmls(self)
        # mf = self.get_media_file()
        # if mf is not None:
        #     src = mf.get_image_url()
        #     if src is not None:
        #         url = mf.get_download_url()
        #         rv += f'<a href="{url}"><img src="{src}" style="width: 30%;"></a>'
        if self.source:
            rv += format_html(
                " ({}: {})", _("Source"), ar.obj2htmls(self.source))
        return mark_safe(rv)

    # def get_choices_text(self, ar, actor, field):
    #     if self.file:
    #         return str(obj) + "&nbsp;<span style=\"float: right;\">" + obj.thumbnail + "</span>"
    #     return str(obj)

    def as_memo_include(self, ar, text=None, **ctx):
        # fmt = parse_image_spec(text, **ctx)
        # TODO: When an image is inserted with format "wide", we should not use
        # the thumbnail but the original file. But for a PDF file we must always
        # use the img_src because the download_url is not an image.
        # fmt.context.update(src=mf.get_image_url())
        # if isinstance(fmt, SMALL_FORMATS):
        #     fmt.context.update(src=img_src)
        # else:
        #     print(f"20241116 {fmt} {fmt.context}")

        # if not fmt.context["caption"]:
        #     fmt.context["caption"] = self.description or str(self)

        mf = self.get_media_file()
        if mf is None:
            return format_html("<em>{}</em>", text or str(self))
        if text is None:
            text = ""
        chunks = list(map(str.strip, text.split("|", 1)))
        sizename = fmtname = title = ""
        if len(chunks) == 2:
            fmtname, title = chunks
        elif len(chunks) == 3:
            sizename, fmtname, title = chunks
        else:
            title = text
        if fmtname:
            fmt = ImageFormats.get_by_value(fmtname.strip(), None)
            if fmt is None:
                raise Exception(f"Invalid image format '{fmtname}'")
            ctx.update(image_format=fmt)
        if sizename:
            size = ImageSizes.get_by_value(sizename.strip(), None)
            if size is None:
                raise Exception(f"Invalid image size '{sizename}'")
            ctx.update(image_size=size)
        return self.as_html(ar, mf, title=title, **ctx)


dd.update_field(Upload, "user", verbose_name=_("Uploaded by"))
dd.update_field(Upload, "owner", verbose_name=_("Attached to"))


class UploadChecker(Checker):
    verbose_name = _("Check metadata of upload files")
    model = "uploads.Upload"

    def get_checkdata_problems(self, ar, obj, fix=False):
        if obj.file:
            if not exists(join(settings.MEDIA_ROOT, obj.file.name)):
                yield (
                    False,
                    format_lazy(_("Upload entry {} has no file"),
                                obj.file.name),
                )
                return

        file_size = obj.get_real_file_size()

        if obj.file_size != file_size:
            tpl = "Stored file size {} differs from real file size {}"
            yield (False, format_lazy(tpl, obj.file_size, file_size))

        for i in obj.check_previews(fix):
            yield i


UploadChecker.activate()


class UploadsFolderChecker(Checker):
    verbose_name = _("Find orphaned files in uploads folder")

    # It is no problem to have multiple upload entries pointing to a same file
    # on the file system

    def get_checkdata_problems(self, ar, obj, fix=False):
        assert obj is None  # this is an unbound checker
        Upload = rt.models.uploads.Upload
        pth = dd.plugins.uploads.uploads_root
        assert str(pth).startswith(settings.MEDIA_ROOT)
        start = len(settings.MEDIA_ROOT) + 1
        for filename in Path(pth).rglob("*"):
            # print(filename)
            if filename.is_dir():
                continue
            rel_filename = str(filename)[start:]
            qs = Upload.objects.filter(file=rel_filename)
            if not qs.exists():
                msg = format_lazy(
                    _("File {} has no upload entry."), rel_filename)
                # print(msg)
                yield (True, msg)
                if fix:
                    if dd.plugins.uploads.remove_orphaned_files:
                        filename.unlink()
                    else:
                        obj = Upload(
                            file=rel_filename, user=ar.get_user(),
                            description=f"Found on {dd.today()} by {self}")
                        obj.full_clean()
                        obj.save()
            # else:
            #     print("{} has {} entries.".format(filename, n))
            # elif n > 1:


UploadsFolderChecker.activate()


@dd.receiver(dd.pre_analyze)
def before_analyze(sender, **kwargs):
    # This is the successor for `quick_upload_buttons`.

    # remember that models might have been overridden.
    UploadType = sender.models.uploads.UploadType
    Shortcuts = sender.models.uploads.Shortcuts

    # raise Exception(f"20241112 {UploadType}")

    for i in Shortcuts.items():

        def f(obj, ar):
            if obj is None or ar is None:
                return E.div()
            try:
                utype = UploadType.objects.get(shortcut=i)
            except UploadType.DoesNotExist:
                return E.div()
            items = []
            target = sender.modules.resolve(i.target)
            sar = ar.spawn_request(
                actor=target, master_instance=obj, known_values=dict(
                    type=utype))
            # param_values=dict(pupload_type=et))
            n = sar.get_total_count()
            if n == 0:
                iar = target.insert_action.request_from(
                    sar, master_instance=obj)
                btn = iar.ar2button(
                    None,
                    "⊕",  # _("Upload"),
                    # icon_name="page_add",
                    title=_("Upload a file from your PC to the server."))
                items.append(btn)
            # elif n == 1:
            else:
                after_show = ar.get_status()
                obj = sar.data_iterator[0]
                if (mf := obj.get_media_file()) is not None:
                    items.append(
                        sar.renderer.href_button(
                            mf.get_download_url(),
                            "⎙",  # Unicode symbol Print Screen
                            target="_blank",
                            # icon_name="page_go",
                            # style="vertical-align:-30%;",
                            title=_(
                                "Open the uploaded file in a new browser window"),
                        )
                    )
                after_show.update(record_id=obj.pk)
                items.append(
                    sar.window_action_button(
                        sar.ah.actor.detail_action,
                        after_show,
                        "⎆",  # Unicode symbol Enter
                        # icon_name="application_form",
                        title=_("Edit the information about the uploaded file."),
                    )
                )
            # else:
            #     obj = sar.sliced_data_iterator[0]
            #     items.append(ar.obj2html(
            #         obj, pgettext("uploaded file", "Last")))

            btn = sar.renderer.action_button(
                obj,
                sar,
                sar.bound_action,
                settings.SITE.expand_panel_symbol,  # _("All {0} files").format(n),
                icon_name=None,
                title=_("Manage the list of uploaded files.")
            )
            items.append(btn)

            return E.div(*join_elems(items, ", "))

        vf = dd.VirtualField(dd.DisplayField(i.text), f)
        dd.inject_field(i.model_spec, i.name, vf)
        # logger.info("Installed upload shortcut field %s.%s",
        #             i.model_spec, i.name)


# raise Exception("20241112")


@dd.receiver(dd.post_startup)
def setup_memo_commands(sender=None, **kwargs):
    # Adds another memo command for Upload
    # See :doc:`/specs/memo`

    if not sender.is_installed('memo'):
        return

    def file2html(self, ar, text, **ctx):
        """
        Insert an image tag of the specified upload file.
        """
        return self.as_memo_include(ar, text, **ctx)

    mp = sender.plugins.memo.parser
    mp.register_django_model('file', rt.models.uploads.Upload, rnd=file2html)


def on_sanitize(soup, save=False, ar=None, mentions=None):
    # raise Exception(f"20250301")
    if save:
        for tag in soup.find_all('img'):
            if (src := tag.get('src')) and src.startswith("data:image"):
                file = base64_to_image(src)
                user = ar.get_user() if ar else dd.plugins.users.get_demo_user()
                obj = rt.models.uploads.Upload(file=file, user=user)
                tag["src"] = obj.get_media_file().get_image_url()
                if ar:
                    sar = obj.get_default_table().create_request(parent=ar)
                    obj.save_new_instance(sar)  # create comment or notify message
                else:
                    obj.save()
                rt.models.checkdata.fix_instance(ar, obj)  # create thumbnail
                # style = ''
                # if (s := tag.get("style")):
                #     # if not s.strip().endswith(";"):
                #     #     s += ";"
                #     style += s
                # if (w := tag.get("width")) is not None:
                #     style += f" width: {w}px;"
                # else:
                #     # 20ex comes from the default value of Format.height in rstgen.sphinxconf.sigal_image
                #     style += " height: 20ex;"
                # tag.replace_with(f'[file {upload.pk} style="{style}"]')
                tag[DATA_UPLOAD_ID] = obj.id
    if mentions is not None:
        for tag in soup.find_all('img'):
            if (upload_id := tag.get(DATA_UPLOAD_ID)):
                mentions.add(rt.models.uploads.Upload(id=upload_id))


register_sanitizer(on_sanitize)
