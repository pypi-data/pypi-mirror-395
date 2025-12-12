# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger

import os
import shutil
import datetime
from lxml import etree

from django.conf import settings
from django.utils.timezone import make_aware

from lino.core.actions import Action
from lino.api import rt, _
from lino.core.keyboard import Hotkey
from lino.core.roles import SiteStaff
from lino.utils.html import E
from lino.utils.media import TmpMediaFile
from lino.utils.pdf import merge_pdfs
from lino.utils.xml import validate_xml

from .choicelists import BuildMethods


class BasePrintAction(Action):
    sort_index = 50
    url_action_name = "print"
    label = _("Print")
    build_method = None
    hotkey = Hotkey("p", code="KeyP", ctrl=True)

    def __init__(self, build_method=None, label=None, **kwargs):
        super().__init__(label, **kwargs)
        if build_method is not None:
            self.build_method = build_method

    def validate_result_file(self, bm, filename):
        """Validate the generated file."""
        pass

    def attach_to_actor(self, actor, name):
        from lino.core.utils import resolve_app
        if not resolve_app("system"):
            return False
        # if actor.__name__ == 'ExcerptsByProject':
        #     logger.info("20140401 attach_to_actor() %r", self)
        return super().attach_to_actor(actor, name)

    def get_print_templates(self, bm, elem):
        # print("20190506 BasePrintAction.get_print_templates", elem)
        return elem.get_print_templates(bm, self)

    def get_printable_context(self, bm, elem, ar):
        """A hook for defining action-specific context variables.
        The default
        implementation calls
        :meth:`lino.core.model.Model.get_printable_context`.

        """
        return elem.get_printable_context(ar)

    def before_build(self, bm, elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        # elem.before_printable_build(bm)
        if not elem.must_build_printable(bm):
            return
        # raise Exception("20170519 before_build didn't warn")
        filename = bm.get_target_file(self, elem).path
        filename.unlink(missing_ok=True)
        filename.parent.mkdir(exist_ok=True, parents=True)
        # if filename.exists():
        #     logger.debug("%s %s -> overwrite existing %s.", bm, elem, filename)
        #     os.remove(filename)
        # else:
        #     # logger.info("20121221 makedirs_if_missing %s",os.path.dirname(filename))
        #     rt.makedirs_if_missing(os.path.dirname(filename))
        logger.debug("%s : %s -> %s", bm, elem, filename)
        return filename

    def notify_done(self, ar, bm, leaf, url, **kw):
        # help_url = ar.get_help_url("print", target='_blank')
        # if bm.use_webdav:
        #     url = ar.build_webdav_uri(url)
        msg = _(
            "Your printable document ({}) "
            "should now open in a new browser window. "
            # "If it doesn't, please consult %(help)s "
            "If it doesn't, please "
            "ask your system administrator."
        )
        msg = msg.format(etree.tostring(
            E.a(leaf, href=url), encoding="unicode"))
        # msg %= dict(doc=leaf, help=etree.tostring(
        #     help_url, encoding="unicode"))
        kw.update(message=msg, alert=True)
        kw.update(open_url=url)
        ar.success(**kw)
        return

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]
        bm = self.build_method or elem.get_build_method()
        if isinstance(bm, str):
            bm = BuildMethods.get_by_value(bm)
        bm.build(ar, self, elem)
        mf = bm.get_target_file(self, elem)
        # leaf = mf.parts[-1]
        leaf = mf.path.name
        self.notify_done(ar, bm, leaf, mf.url, **kw)


class DirectPrintAction(BasePrintAction):
    url_action_name = None
    icon_name = "printer"
    # button_text = "🖶"  # 1F5B6
    tplname = None

    def __init__(self, label=None, tplname=None, build_method=None, **kw):
        super().__init__(build_method, label, **kw)
        if tplname is not None:
            self.tplname = tplname

    def get_print_templates(self, bm, obj):
        # assert bm is self.build_method
        if self.tplname:
            return [self.tplname + bm.template_ext]
        return obj.get_print_templates(bm, self)


class WriteXmlAction(DirectPrintAction):
    """Generate an XML file from this database object."""

    # combo_group = "writexml"
    label = _("XML")

    build_method = "xml"
    icon_name = None
    # show_in_toolbar = False
    xsd_file = None

    def validate_result_file(self, bm, xmlfile):
        if self.xsd_file:
            logger.info("Validate %s against %s ...", xmlfile, self.xsd_file)
            # doc = etree.parse(xmlfile)
            if True:
                validate_xml(xmlfile, self.xsd_file)
            else:
                try:
                    validate_xml(xmlfile, self.xsd_file)
                except Exception as e:
                    msg = _("XML file {} is invalid: {}").format(xmlfile, e)
                    # print(msg)
                    raise Warning(msg)


class CachedPrintAction(BasePrintAction):
    # select_rows = False
    http_method = "POST"
    icon_name = "printer"
    # button_text = "🖶"  # 1F5B6

    def before_build(self, bm, elem):
        if elem.build_time:
            return
        return BasePrintAction.before_build(self, bm, elem)

    def run_from_ui(self, ar, **kw):
        if len(ar.selected_rows) == 1:
            obj = ar.selected_rows[0]
            bm = obj.get_build_method()
            mf = bm.get_target_file(self, obj)
            # leaf = mf.parts[-1]
            leaf = mf.path.name
            if obj.build_time is None:
                obj.build_target(ar)
                ar.debug("%s has been built.", leaf)
            else:
                ar.debug("Reused %s from cache.", leaf)

            # url = mf.get_url(ar.request)
            self.notify_done(ar, bm, leaf, mf.url, **kw)
            ar.set_response(refresh=True)
            return

        def ok(ar2):
            # qs = [ar.actor.get_row_by_pk(pk) for pk in ar.selected_pks]
            mf = self.print_multiple(ar, ar.selected_rows)
            ar2.success(open_url=mf.url)
            # ar2.success(open_url=mf.get_url(ar.request))
            # kw.update(refresh_all=True)
            # return kw

        msg = _("This will print %d rows.") % len(ar.selected_rows)
        ar.confirm(ok, msg, _("Are you sure?"))

    def print_multiple(self, ar, qs):
        pdfs = []
        for obj in qs:
            # assert isinstance(obj,CachedPrintable)
            if obj.printed_by_id is None:
                obj.build_target(ar)
            # pdf = obj.get_target_file().name
            # assert pdf is not None
            # pdfs.append(pdf)
            mf = obj.get_target_file()
            pdfs.append(mf.path)

        mf = TmpMediaFile(ar, "pdf")
        # rt.makedirs_if_missing(os.path.dirname(mf.name))
        rt.makedirs_if_missing(mf.path.parent)
        merge_pdfs(pdfs, mf.path)
        return mf


class EditTemplate(BasePrintAction):
    sort_index = 51
    url_action_name = "edit_tpl"
    label = _("Edit Print Template")
    required_roles = set([SiteStaff])

    def attach_to_actor(self, actor, name):
        # if not settings.SITE.is_installed('davlink'):
        if not settings.SITE.webdav_protocol:
            return False
        return super().attach_to_actor(actor, name)

    def run_from_ui(self, ar, **kw):
        lcd = settings.SITE.confdirs.LOCAL_CONFIG_DIR
        if lcd is None:
            # ar.debug("No local config directory in %s " %
            #         settings.SITE.confdirs)
            raise Warning(
                "No local config directory. " "Contact your system administrator."
            )

        elem = ar.selected_rows[0]
        bm = elem.get_build_method()
        leaf = bm.get_template_leaf(self, elem)

        filename = bm.get_template_file(ar, self, elem)
        local_file = None
        groups = elem.get_template_groups()
        assert len(groups) > 0
        for grp in reversed(groups):
            # subtle: if there are more than 1 groups
            parts = [grp, leaf]
            local_file = os.path.join(lcd.name, *parts)
            if filename == local_file:
                break

        parts = ["webdav", "config"] + parts
        url = settings.SITE.build_media_url(*parts)
        # url = ar.build_webdav_uri(url)

        if not settings.SITE.webdav_protocol:
            msg = "cp %s %s" % (filename, local_file)
            ar.debug(msg)
            raise Warning(
                "WebDAV is not enabled. " "Contact your system administrator."
            )

        def doit(ar):
            ar.debug("Going to open url: %s " % url)
            if settings.SITE.webdav_protocol:
                ar.success(open_url=url)
            else:
                ar.success(open_webdav_url=url)
            # logger.info('20140313 EditTemplate %r', kw)

        if filename == local_file:
            doit(ar)
        else:
            # raise Exception("20191019 {} is not {}".format(filename, local_file))
            ar.debug("Gonna copy %s to %s", filename, local_file)

            def ok(ar2):
                logger.info("%s made local template copy %s",
                            ar.user, local_file)
                rt.makedirs_if_missing(os.path.dirname(local_file))
                shutil.copyfile(filename, local_file)
                # shutil.copy() can cause PermissionError if dst exists and is
                # owned by another user
                doit(ar2)

            msg = _(
                "Before you can edit this template we must create a "
                "local copy on the server. "
                "This will exclude the template from future updates."
            )
            ar.confirm(ok, msg, _("Are you sure?"))


class ClearCache(Action):
    sort_index = 51
    url_action_name = "clear"
    label = _("Clear cache")
    icon_name = "printer_delete"

    def get_action_permission(self, ar, obj, state):
        # obj may be None when Lino asks whether this action
        # should be visible in the table toolbar
        if obj is not None and not obj.build_time:
            return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        elem = ar.selected_rows[0]

        def doit(ar):
            elem.clear_cache()
            ar.success(_("%s printable cache has been cleared.") %
                       elem, refresh=True)

        t = elem.get_cache_mtime()
        if t is not None:
            # set microseconds to those of the stored field because
            # Django DateTimeField can have microseconds precision or
            # not depending on the database backend.

            t = datetime.datetime(
                t.year,
                t.month,
                t.day,
                t.hour,
                t.minute,
                t.second,
                elem.build_time.microsecond,
            )
            if settings.USE_TZ:
                t = make_aware(t)
            if t != elem.build_time:
                # logger.info("20140313 %r != %r", t, elem.build_time)
                return ar.confirm(
                    doit,
                    _("This will discard all changes in the generated file."),
                    _("Are you sure?"),
                )
        return doit(ar)
