# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.utils.translation import get_language

# from django.utils.translation import get_language
# from django.utils.html import format_html

from lino.api import dd, rt, _
from lino.utils.html import E
from lino.utils.soup import MORE_MARKER
from lino.core import constants
# from lino.core.renderer import add_user_language
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from .choicelists import SpecialPages, PublishingStates
TICKET_MODEL = dd.plugins.publisher.ticket_model


class PageTypes(dd.Table):

    model = 'publisher.PageType'
    required_roles = dd.login_required(OfficeStaff)
    # ~ label = _("Page types")
    column_names = 'designation build_method template *'
    order_by = ["designation"]

    insert_layout = """
    designation
    build_method
    """

    detail_layout = """
    id designation
    build_method template
    publisher.PagesByType
    """


VARTABS = ""

if dd.is_installed("topics"):
    VARTABS += " topics.TagsByOwner"
if dd.is_installed("comments"):
    VARTABS += " comments.CommentsByRFC"

if TICKET_MODEL is not None:
    VARTABS += " publisher.ItemsByPage"


class PageDetail(dd.DetailLayout):
    # main = "general first_panel more"
    main = f"general first_panel {VARTABS} more"

    general = dd.Panel(
        """
        content_panel:60 right_panel:20
        """,
        label=_("General"),
        required_roles=dd.login_required(OfficeUser))

    content_panel = """
    title language:10
    subtitle
    body
    """

    # right_panel = """
    # parent seqno
    # child_node_depth
    # page_type
    # filler
    # """

    right_panel = """
    parent seqno
    publisher.PagesByParent
    """

    first_panel = dd.Panel(
        """
        treeview_panel:20 preview:60
        """, label=_("Preview"))

    # more = dd.Panel(
    #     VARTABS,
    #     label=_("Discussion"),
    #     required_roles=dd.login_required(OfficeUser),
    # )

    more = dd.Panel("""more1 more2""", label=_("More"))
    more1 = """
    root_page page_name id
    translated_from
    publisher.TranslationsByPage
    """
    more2 = """
    special_page page_type
    publishing_state album
    build_method build_time
    """


class Pages(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = "publisher.Page"
    column_names = "title root_page id *"
    detail_layout = "publisher.PageDetail"
    insert_layout = """
    title
    parent
    """
    default_display_modes = {None: constants.DISPLAY_MODE_LIST}
    # unique_keys = ['pk', 'page_name']

    @classmethod
    def get_row_by_pk(self, ar, pk):
        M = self.model
        try:
            return M.objects.get(pk=pk)
        except (ValueError, M.DoesNotExist):
            pass
        try:
            return M.objects.get(page_name=pk, language=get_language())
        except M.DoesNotExist:
            return None

    @classmethod
    def get_breadcrumbs(cls, ar, elem=None):
        if elem is not None:
            return elem.get_parent_links(ar)
        return []


class RootPages(Pages):
    filter = models.Q(parent=None)
    label = _("Root pages")
    # ~ column_names = "title user *"
    order_by = ["language", "id"]
    column_names = "id language title *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(language=get_language())
        return kw


class PagesByParent(Pages):
    master_key = "parent"
    label = _("Children")
    # ~ column_names = "title user *"
    order_by = ["seqno"]
    column_names = "seqno title *"
    # default_display_modes = {None: constants.DISPLAY_MODE_LIST}


class PagesByType(Pages):
    master_key = "page_type"


class PublicPages(Pages):
    required_roles = set([])
    label = _("Public pages")
    # filter = models.Q(publishing_state=PublishingStates.published)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(language=get_language())
        return kw


# PublisherViews.add_item_lazy("p", Pages)
# PublisherViews.add_item_lazy("n", Nodes)

# PageTypes.add_item(Pages, 'pages')


class TranslationsByPage(Pages):
    master_key = "translated_from"
    label = _("Translations")
    column_names = "title language id *"
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    @classmethod
    def row_as_summary(cls, ar, obj, text=None, **kwargs):
        # return format_html("({}) {}", obj.language, obj.as_summary_row(ar, **kwargs))
        return E.span("({}) ".format(obj.language), obj.as_summary_item(ar, text, **kwargs))


if TICKET_MODEL:

    class PageItems(dd.Table):
        model = 'publisher.PageItem'
        required_roles = dd.login_required(OfficeStaff)
        detail_layout = dd.DetailLayout("""
        ticket
        page seqno
        """, window_size=('auto', 40))

        insert_layout = """
        page
        ticket
        """

    class ItemsByPage(PageItems):
        master_key = "page"
        required_roles = set()  # also for anonymous
        default_display_modes = {None: constants.DISPLAY_MODE_TILES}
        column_names = "seqno ticket *"
        insert_layout = """
        ticket
        """

    class ItemsByTicket(PageItems):
        master_key = "ticket"
        default_display_modes = {
            None: constants.DISPLAY_MODE_SUMMARY,
            70: constants.DISPLAY_MODE_GRID}
        column_names = "seqno page *"
        insert_layout = """
        page
        """


SpecialPages.add_item(
    "roots",  # filler=filler,
    body=_("List of root pages on this site.") +
    MORE_MARKER + " [show publisher.RootPages]",
    title=_("Root pages"),
    parent='home')
