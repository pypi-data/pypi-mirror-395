# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from html import escape
from django.db import models
from django.conf import settings
from django.utils import translation
# from django.utils.translation import get_language
from django.core.exceptions import ValidationError
from lino.api import dd, rt, _
# from lino.utils import mti
from lino.utils.html import E, tostring, format_html, mark_safe
from lino.modlib.uploads.choicelists import ImageFormats, htmlimg
# from lino.utils.instantiator import get_or_create
# from lino.core.renderer import add_user_language
# from lino.utils.mldbc.fields import LanguageField
from lino.mixins import Hierarchical, Sequenced, Referrable
from lino.utils.mldbc.mixins import BabelDesignated
# from lino.modlib.summaries.mixins import Summarized
from lino.modlib.printing.mixins import PrintableType, TypedPrintable
from lino.modlib.comments.mixins import Commentable
from lino.modlib.linod.choicelists import schedule_daily
from lino.modlib.memo.mixins import TitledPreviewable
from lino.modlib.users.mixins import UserAuthored, PrivacyRelevant
from lino_xl.lib.topics.mixins import Taggable
from lino.modlib.bootstrap5 import PAGE_TITLE_TEMPLATE

if dd.plugins.publisher.with_translators:
    import translators as ts
    TRANSLATORS = ['deepl', 'google', 'bing', 'alibaba']


from .choicelists import PublishingStates, SpecialPages
from .mixins import Publishable, TranslatableContent, PublishableContent, Illustrated
from .ui import *

# child_node_depth = 1

TICKET_MODEL = dd.plugins.publisher.ticket_model


def translate(ar, text, from_language, to_language):
    if not dd.plugins.publisher.with_translators:
        return text

    func = ts.translate_html if text.startswith("<") else ts.translate_text
    for trl in TRANSLATORS:
        try:
            rv = func(text, translator=trl,
                      from_language=from_language,
                      to_language=to_language)
            ar.logger.debug("Got translation from %s", trl)
            return rv
        except Exception as e:
            ar.logger.info("Error while translating by %s: %s", trl, e)
    return text


class CreateTranslations(dd.Action):
    # button_text = "🐟"  #1f41f
    button_text = "𓆟"
    label = _("Create translations")

    def get_action_permission(self, ar, obj, state):
        # obj may be None when Lino asks whether this action
        # should be visible in the table toolbar
        if obj and obj.translated_from:
            return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        done = []
        for row in ar.selected_rows:
            page_items = row.items.all()
            Page = row.__class__
            for lng in settings.SITE.languages:
                if lng.django_code == row.language:
                    continue
                kwargs = dict(language=lng.django_code, translated_from=row)
                if row.parent is not None:
                    kwargs.update(
                        parent=row.parent.get_for_language(lng.django_code))
                qs = Page.objects.filter(**kwargs)
                if qs.count() == 0:
                    # ar.logger.info("Translate %s to %s", row, lng.django_code)
                    kwargs.update(title=translate(
                        ar, row.title, row.language, lng.django_code))
                    # kwargs.update(body=translate(
                    #     ar, row.body, row.language, lng.django_code))
                    new = Page(**kwargs)
                    new.full_clean()
                    new.save()
                    if TICKET_MODEL is not None:
                        for pi in page_items:
                            new_pi = pi.__class__(
                                seqno=pi.seqno, ticket=pi.ticket, page=new)
                            new_pi.full_clean()
                            new_pi.save()
                    done.append(_("Created {what} in {language}").format(
                        what=row, language=lng.django_code))

                elif qs.count() > 1:
                    done.append(_("Multiple pages for {}").format(kwargs))
        if len(done):
            ar.success(", ".join(done), refresh=True)


class PageType(BabelDesignated, PrintableType):
    templates_group = 'publisher/Page'

    class Meta:
        app_label = 'publisher'
        verbose_name = _("Page type")
        verbose_name_plural = _("Page types")


class Page(
    Hierarchical, Sequenced, TitledPreviewable, Commentable, TypedPrintable,
    TranslatableContent, PublishableContent, Illustrated, Taggable
):
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        abstract = dd.is_abstract_model(__name__, "Page")
        unique_together = ["page_name", "language"]
        # unique_together = ["publisher_tree", "language"]

    memo_command = "page"
    allow_cascaded_delete = ['parent']

    page_name = models.CharField(_("Page name"), max_length=200, blank=True, null=True)

    # child_node_depth = models.IntegerField(default=1)
    page_type = dd.ForeignKey("publisher.PageType", blank=True, null=True)
    special_page = SpecialPages.field(blank=True)
    # if dd.get_plugin_setting('publisher', 'with_trees', False):
    # if dd.plugins.publisher.with_trees:
    #     # publisher_tree = dd.ForeignKey("publisher.Tree", null=True, blank=True)
    #     publisher_tree = dd.ForeignKey("publisher.Tree")
    # else:
    #     publisher_tree = dd.DummyField()

    previous_page = dd.ForeignKey(
        "self", null=True, blank=True, editable=False,
        verbose_name=_("Previous page"), related_name='+',
        on_delete=models.SET_NULL)
    root_page = dd.ForeignKey(
        "self", null=True, blank=True,
        verbose_name=_("Root page"), related_name='+')

    def __str__(self):
        return self.title or super().__str__()

    def get_printable_type(self):
        return self.page_type

    @classmethod
    def get_simple_parameters(cls):
        lst = list(super().get_simple_parameters())
        lst.append('root_page')
        lst.append('parent')
        lst.append('language')
        lst.append('album')
        lst.append('publishing_state')
        return lst

    # @classmethod
    # def param_defaults(self, ar, **kw):
    #     kw = super().param_defaults(ar, **kw)
    #     kw.update(language=get_language())
    #     return kw

    # def on_create(self, ar):
    #     self.page_type = self.get_page_type()
    #     super().on_create(ar)

    # def get_for_language(self, lng):
    #     # lng is a LanguageInfo object settings.SITE.get_language_info()
    #     if lng.prefix:
    #         qs = self.__class__.objects.filter(
    #             translated_from=self, language=lng.code)
    #         return qs.first()
    #     return self

    def before_ui_save(self, ar, cw):
        # print(f"20250726 before_ui_save() {self}")
        if not self.language:
            if self.parent:
                self.language = self.parent.language
            elif ar:
                if ar.request:
                    self.language = ar.request.LANGUAGE_CODE
                else:
                    self.language = ar.get_user().language
            else:
                self.language = settings.SITE.get_default_language()
        super().before_ui_save(ar, cw)
        if (src := self.translated_from):
            if not self.title:
                self.title = translate(ar, src.title, src.language, self.language)
            if not self.body:
                self.body = translate(ar, src.body, src.language, self.language)

    def full_clean(self):
        if self.root_page is None:
            if self.parent is not None:
                self.root_page = self.parent.root_page
        elif self.root_page == self:
            self.root_page = None
        super().full_clean()
        if (src := self.translated_from):
            if src.language == self.language:
                raise ValidationError(
                    _("Cannot translate from a page of same language"))

    def get_root_page(self):
        return self.root_page or self

    def get_node_info(self, ar):
        return ""

    def get_publisher_pk(self):
        return self.page_name or str(self.pk)

    # def is_public(self):
    #     if self.root_page and not self.root_page.is_public():
    #         return False
    #     # if dd.plugins.publisher.with_trees:
    #     #     return not self.publisher_tree.private
    #     return super().is_public()

    # def mti_child(self):
    #     #     if self.page_type:
    #     #         return mti.get_child(self, self.page_type.nodes_table.model) or self
    #     return self

    def walk(self):
        yield self
        for c in self.children.all():
            for i in c.walk():
                yield i

    create_translations = CreateTranslations()

    # def get_print_templates(self, bm, action):
    #     return [bm.get_default_template(self)]

    # def as_summary_row(self, ar, **kwargs):
    #     return ar.obj2htmls(self, **kwargs)

    # def as_story_item(self, ar, **kwargs):
    #     return "".join(self.as_page(ar, **kwargs))

    def toc_html(self, ar, max_depth=1):
        def li(obj):
            # return "<li>{}</li>".format(obj.memo2html(ar, str(obj)))
            return "<li>{}</li>".format(tostring(ar.obj2html(obj)))

        html = "".join([li(obj) for obj in self.children.all()])
        return '<ul class="publisher-toc">{}</ul>'.format(html)

    def get_page_title(self):
        # tpl = f'<p class="display-4" style="{style}">{{}}</p>'
        # return format_html(tpl, self.title)
        return format_html(PAGE_TITLE_TEMPLATE, self.title)

    def as_page(self, ar, display_mode="detail", hlevel=1, home=None):
        if home is None:
            home = self
        yield self.get_title_div(ar)

        # if not self.is_public():
        #     return

        if True:  # display_mode in ("detail",):
            info = self.get_node_info(ar)
            if info:
                yield """<p class="small">{}</p>""".format(info)
                # https://getbootstrap.com/docs/3.4/css/#small-text

        if False:  # display_mode == "story":
            yield self.get_body_parsed(ar, short=True)

        # if display_mode in ("detail", "story"):
        if True:  # display_mode == "detail":
            # if hlevel == 1 and not dd.plugins.memo.use_markup and self.parent_id:
            #     yield self.toc_html(ar)

            if hlevel == 1 and self.main_image:
                yield f"""
                <div class="row">
                    <div class="center-block">
                        <a href="#" class="thumbnail">
                            <img src="{self.main_image.get_media_file().get_image_url()}">
                        </a>
                    </div>
                </div>
                """

            # yield self.body_full_preview
            yield self.get_body_parsed(ar, short=False)

            # if self.filler:
            #     if hlevel == 1:
            #         yield self.filler.get_dynamic_story(ar, self)
            #     else:
            #         yield self.filler.get_dynamic_paragraph(ar, self)

            # if dd.plugins.memo.use_markup:
            #     return

            if TICKET_MODEL:
                A = rt.models.publisher.ItemsByPage
                sar = A.create_request(master_instance=self, parent=ar)
                for obj in sar:
                    # for chunk in obj.as_page(sar):
                    #     yield chunk
                    # yield tostring(obj.as_summary_item(sar))
                    yield "<p>"
                    yield tostring(obj.as_paragraph(sar))
                    yield "</p>"
                # qs = rt.models.publisher.PageItem.objects.filter(page=self)
                # if qs.count() > 0:
                #     yield "<ol>"
                #     for obj in qs.order_by('seqno'):
                #         yield "<li>"
                #         yield tostring(obj.ticket.as_summary_item(ar))
                #         yield "</li>"
                #     yield "</ol>"

            if self.root_page is None:
                return

            A = rt.models.publisher.PagesByParent
            children = A.create_request(master_instance=self, parent=ar)

            # if not self.children.exists():
            if not children.get_total_count():
                return

            # yield "<p><b>{}</b></p>".format(_("Children:"))

            # if hlevel > child_node_depth:
            #     yield " (...)"
            #     return
            # if hlevel == child_node_depth:
            #     display_mode = "list"
            #     yield "<ul>"
            yield "<ul>"
            # children = self.children.order_by("seqno")
            for obj in children:
                yield "<li>"
                yield obj.as_paragraph(ar)
                yield "</li>"
            yield "</ul>"
        # else:
        #     yield " — "
        #     yield self.body_short_preview
        #     for obj in self.children.order_by('seqno'):
        #         for i in obj.as_page(ar, "list", hlevel+1):
        #             yield i

    # @classmethod
    # def lookup_page(cls, ref):
    #     try:
    #         return cls.objects.get(ref=ref, language=get_language())
    #     except cls.DoesNotExist:
    #         pass

    # if dd.plugins.publisher.with_trees:
    #
    #     def full_clean(self):
    #         if self.publisher_tree is None and self.parent is not None:
    #             self.publisher_tree = self.parent.publisher_tree
    #         super().full_clean()

    def update_page(self, prev, root):
        save = False
        if self.previous_page != prev:
            self.previous_page = prev
            save = True
        if self == root:
            root = None
        if self.root_page != root:
            self.root_page = root
            save = True
        # if dd.plugins.publisher.with_trees:
        #     if self.publisher_tree != tree:
        #         self.publisher_tree = tree
        #         save = True
        if save:
            self.save()

    def get_prev_page(self, ar):
        return self.previous_page

    def get_next_page(self, ar):
        return self.__class__.objects.filter(previous_page=self).first()

    @classmethod
    def get_dashboard_objects(cls, user):
        # print("20210114 get_dashboard_objects()", get_language())
        # qs = cls.objects.filter(parent__isnull=True, language=get_language())
        qs = cls.objects.filter(parent__isnull=True)
        for obj in qs.order_by("seqno"):
            yield obj

    def get_parent_links(self, ar):
        for p in list(self.get_parental_line())[:-1]:
            yield ar.obj2htmls(p)

    # def get_page_type(self):
    #     return PageTypes.pages

    # def is_public(self):
    #     return True


if dd.plugins.memo.use_markup:
    dd.update_field(Page, "body", format="plain")


if TICKET_MODEL:

    class PageItem(Sequenced, Publishable):

        class Meta:
            abstract = dd.is_abstract_model(__name__, 'PageItem')
            verbose_name = _("Page item")
            verbose_name_plural = _("Page items")
            ordering = ['page', 'seqno']

        allow_cascaded_delete = ['page']

        page = dd.ForeignKey('publisher.Page', related_name="items")
        ticket = dd.ForeignKey(TICKET_MODEL)

        def get_str_words(self, ar):
            yield str(self.seqno)+")"
            if not ar.is_obvious_field("ticket"):
                yield str(self.ticket)
            if not ar.is_obvious_field("page"):
                yield _("in {page}").format(page=self.page)

        def unused_as_summary_item(self, ar, text=None, **kwargs):
            # raise Exception("20240613")
            if ar is None:
                obj = super()
            elif ar.is_obvious_field('ticket'):
                obj = self.page
            elif ar.is_obvious_field('page'):
                obj = self.ticket
            else:
                obj = super()
            return obj.as_summary_item(ar, text, **kwargs)

        def get_siblings(self):
            return self.__class__.objects.filter(page=self.page)

        def get_page_title(self):
            # num = f'<span class="l-text-prioritaire">{self.seqno}</span>'
            # num = f'<span class="border border-dark rounded-3">{self.seqno}</span>'
            num = f'<span class="badge text-bg-primary">{self.seqno}</span>'
            title = mark_safe(num + " " + str(self.ticket))
            return format_html(PAGE_TITLE_TEMPLATE, title)

        def as_page(self, ar, **kwargs):
            kwargs.update(title=self.get_page_title())
            return self.ticket.as_page(ar, **kwargs)

        def as_page_item(self, ar):
            return self.ticket.as_page_item(self, ar)


def create_special_pages(ar, **defaults):
    ar.logger.info("Create special pages...")
    for sp in SpecialPages.get_list_items():
        sp.create_pages(ar, **defaults)


@ schedule_daily()
def update_publisher_pages(ar):
    # BaseRequest(parent=ar).run(settings.SITE.site_config.check_all_summaries)
    # rt.login().run(settings.SITE.site_config.check_all_summaries)
    Page = rt.models.publisher.Page
    # for pv in PublisherViews.get_list_items():
    # for m in rt.models_by_base(Published, toplevel_only=True):
    create_special_pages(ar)
    count = 0
    ar.logger.info("Update publisher pages...")
    for root in Page.objects.filter(parent__isnull=True):
        prev = None
        for obj in root.walk():
            # obj.update_page(prev, root.publisher_tree)
            obj.update_page(prev, root)
            prev = obj
            count += 1
    ar.logger.info("%d pages have been updated.", count)


def make_demo_pages(pages_desc, root_ref, group=None):
    from lorem import get_paragraph
    # if dd.plugins.publisher.with_trees:
    #     # user = rt.models.users.User(username=root_ref, user_type=UserTypes.)
    #     # yield user
    #     user = dd.plugins.users.get_demo_user()
    #     get_or_create(rt.models.groups.Membership, group=group, user=user)
    #     tree = dict(publisher_tree=get_or_create(
    #         rt.models.publisher.Tree, ref=root_ref, group=group, user=user))
    # else:
    #     tree = dict()
    # Translation = rt.models.pages.Translation
    # for lc in settings.SITE.LANGUAGE_CHOICES:
    #     language = lc[0]
    #     kwargs = dict(language=language, ref='index')
    #     with translation.override(language):

    parent_nodes = []
    for lng in settings.SITE.languages:
        counter = {None: 0}
        # count = 0
        # home_page = Page.objects.get(
        #     special_page=SpecialPages.home, language=lng.django_code)

        with translation.override(lng.django_code):

            def make_pages(pages, parent=None, root_ref=None):
                root_page = None
                for page in pages:
                    if len(page) != 3:
                        raise Exception(f"Oops {page}")
                    title, body, children = page
                    kwargs = dict(title=title, language=lng.django_code)
                    if body is None:
                        kwargs.update(body=get_paragraph())
                    else:
                        kwargs.update(body=body)
                    if parent is not None:
                        kwargs.update(parent=parent)
                    if root_page is not None:
                        kwargs.update(root_page=root_page)
                    if lng.suffix:
                        kwargs.update(
                            translated_from=parent_nodes[counter[None]])
                    if dd.is_installed("publisher"):
                        kwargs.update(publishing_state='published')
                    obj = Page(**kwargs)
                    yield obj
                    if root_ref is not None:
                        root_page = obj
                    if not lng.suffix:
                        parent_nodes.append(obj)
                    counter[None] += 1
                    # print("20230324", title, kwargs)
                    yield make_pages(children, obj)

            # yield make_pages(pages_desc, parent=home_page)
            yield make_pages(pages_desc, None, root_ref)
