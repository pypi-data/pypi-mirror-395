# -*- coding: UTF-8 -*-
# Copyright 2010-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.modlib.office.roles import OfficeStaff
from lino.utils.html import format_html, escape, mark_safe


class UploadAreas(dd.ChoiceList):
    required_roles = dd.login_required(OfficeStaff)
    verbose_name = _("Upload area")
    verbose_name_plural = _("Upload areas")


add = UploadAreas.add_item
add("90", _("Uploads"), "general")


class Shortcut(dd.Choice):
    """Represents a shortcut field."""

    model_spec = None
    target = "uploads.UploadsByController"

    def __init__(self, model_spec, name, verbose_name, target=None):
        if target is not None:
            self.target = target
        self.model_spec = model_spec
        value = model_spec + "." + name
        super().__init__(value, verbose_name, name)

    def get_uploads(self, **kw):
        """Return a queryset with the uploads of this shortcut."""
        return rt.models.uploads.Upload.objects.filter(type__shortcut=self, **kw)


class Shortcuts(dd.ChoiceList):
    verbose_name = _("Upload shortcut")
    verbose_name_plural = _("Upload shortcuts")
    item_class = Shortcut
    max_length = 50  # fields get created before the values are known


def add_shortcut(*args, **kw):
    return Shortcuts.add_item(*args, **kw)


class ImageSize(dd.Choice):  # TODO: move this to published
    size = ''

    def __init__(self, value, text, **kwargs):
        super().__init__(value, text, value, **kwargs)


class ImageSizes(dd.ChoiceList):
    required_roles = dd.login_required(OfficeStaff)
    verbose_name = _("Image size")
    verbose_name_plural = _("Image sizes")
    item_class = ImageSize


add = ImageSizes.add_item
add('tiny', _("Tiny"), size="2em")
add('small', _("Small"), size="5em")
add('default', _("Default"), size="10em")
add('big', _("Big"), size="15em")
add('huge', _("Huge"), size="30em")
add('solo', _("Solo"), size="100%")
add('duo', _("Duo"), size="48%")
add('trio', _("Trio"), size="30%")
add('quartet', _("Quartet"), size="24%")


class ImageFormat(dd.Choice):  # TODO: move this to published
    style = ''
    class_names = ''

    def __init__(self, value, text, **kwargs):
        super().__init__(value, text, value, **kwargs)


class ImageFormats(dd.ChoiceList):
    required_roles = dd.login_required(OfficeStaff)
    verbose_name = _("Image format")
    verbose_name_plural = _("Image formats")
    item_class = ImageFormat


add = ImageFormats.add_item
# add('tiny', _("Tiny"), style="max-height:2em;height:auto;width:auto;padding:2pt;")
# add('3em', _("Small"), style="max-height:3em;height:auto;width:auto;padding:2pt;")
add('inline', _("Normal"),
    style="height:{size};width:auto;padding:1pt;")
add('cool', _("Cool"),
    style="max-height:{size};max-width:{size};width:auto;height:auto;padding:1pt;")
# add('10em', _("Big"), style="max-height:10em;height:auto;width:auto;padding:2pt;")
stylebase = "max-height:{size};max-width:40%;height:auto;padding:2pt;"
add('right', _("Right-aligned"), style=stylebase + "float:right;")
add('left', _("Left-aligned"), style=stylebase + "float:left;")
add('wide', _("Wide"), style="max-width:100%;height:auto;width:auto;max-height:15em;padding:2pt;")
add('full', _("Full"), style="width:100%;height:auto;padding-bottom:1em;")
# add('fluid', _("Fluid"), class_names=".img-fluid")
# add('thumbnail', _("Thumbnail"), class_names=".img-fluid .img-thumbnail")
add('carousel', _("Carousel"), style="max-height:{size};object-fit:contain")
add('square', _("Square"),
    style="width:{size};aspect-ratio:1/1;object-fit:cover;padding:1pt;")


def htmlimg(
            image_format=None, image_size=None,
            title='', class_names='', **ctx
        ):
    properties = ""
    if title:
        properties += f' title="{escape(title)}"'
    if image_format is None:
        image_format = ImageFormats.inline
    if image_size is None:
        image_size = ImageSizes.default
    if image_format.style:
        style = image_format.style.format(size=image_size.size)
        properties += f' style="{style}"'
    if not class_names:
        class_names = image_format.class_names
    if class_names:
        properties += f' class="{class_names}"'
    ctx.update(properties=mark_safe(properties))
    rv = format_html('<img src="{src}" {properties}/>', **ctx)
    if 'href' in ctx:
        rv = format_html('<a href="{href}" target="_blank">{}</a>', rv, **ctx)
    return rv
