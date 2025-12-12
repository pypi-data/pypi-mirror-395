# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from html import escape
from lino.modlib.checkdata.choicelists import Checker
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.db.models import Q
from django.core import validators
from django.utils.html import mark_safe, format_html, SafeString
from django.utils.translation import ngettext
from django.conf import settings
# from lino.utils.html import E, tostring, fromstring

from lino.api import dd, rt, gettext, _

from lino.core.requests import BaseRequest
from lino.mixins import CreatedModified, BabelNamed
from lino.mixins.periods import DateRangeObservable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.mixins import PrivacyRelevant
from lino.modlib.notify.mixins import ChangeNotifier
from lino.modlib.search.mixins import ElasticSearchable
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.memo.mixins import Previewable, MemoReferrable
from lino.modlib.publisher.mixins import Publishable
from .choicelists import CommentEvents, Emotions
from .mixins import Commentable, MyEmotionField
from .roles import CommentsReader, CommentsStaff
# from .choicelists import PublishAllComments, PublishComment

from .ui import *


class CommentType(BabelNamed):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, "CommentType")
        verbose_name = _("Comment Type")
        verbose_name_plural = _("Comment Types")


class Comment(
    CreatedModified,
    UserAuthored,
    Controllable,
    ElasticSearchable,
    ChangeNotifier,
    Previewable,
    Publishable,
    DateRangeObservable,
    MemoReferrable,
    PrivacyRelevant
):
    class Meta:
        app_label = "comments"
        abstract = dd.is_abstract_model(__name__, "Comment")
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    # elastic search indexes
    ES_indexes = [
        (
            "comment",
            {
                "mappings": {
                    "properties": {
                        "body": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search",
                        },
                        "body_full_preview": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search",
                        },
                        "body_short_preview": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search",
                        },
                        "model": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search",
                        },
                        "modified": {"type": "date"},
                        "owner_id": {"type": "long"},
                        "owner_type": {"type": "long"},
                        "private": {"type": "boolean"},
                        "user": {"type": "long"},
                    }
                }
            },
        )
    ]

    # publisher_location = "c"
    memo_command = "comment"

    reply_to = dd.ForeignKey(
        "self",
        blank=True,
        null=True,
        verbose_name=_("Reply to"),
        related_name="replies_to_this",
    )
    # more_text = dd.RichTextField(_("More text"), blank=True)

    comment_type = dd.ForeignKey("comments.CommentType", blank=True, null=True)
    # reply_vote = models.BooleanField(_("Upvote"), null=True, blank=True)
    # reply_vote = models.SmallIntegerField(_("Vote"), default=0,
    #     validators=[validators.MinValueValidator(-1),
    #         validators.MaxValueValidator(1)])

    my_emotion = MyEmotionField()

    # reply = AddCommentField("comments.RepliesByComment")

    # def is_public(self):
    #     return not self.private

    def disabled_fields(self, ar):
        s = super().disabled_fields(ar)
        if ar.get_user().is_anonymous:
            s.add("my_emotion")
        return s

    def get_my_emotion(self, ar):
        if ar is None:
            return
        u = ar.get_user()
        if u.is_anonymous:
            return
        mr = rt.models.comments.Reaction.objects.filter(
            user=u, comment=self).first()
        if mr:
            return mr.emotion

    def as_paragraph(o, ar):
        if ar is None:
            return str(o)

        # tpl = "[{comment.pk}] "
        # tpl = """<a style="padding-left:1px;padding-right:1px;border-width:1px; border-style:solid; border-color:blue;">{comment.pk}</a> """
        # tpl = """<a class="bordertext">{comment.pk}</a> """
        # s = tpl.format(comment=o)
        s = mark_safe("")

        if o.num_reactions:
            e = o.get_my_emotion(ar)
            if e is not None:
                s += format_html(" {} ", e.button_text or e.text)
            # else:
            #     yield " foo "

        # Reaction = rt.models.comments.Reaction
        # qs = Reaction.objects.filter(comment=o)
        # c = qs.count()
        # if c:
        #     my_reaction = qs.filter(user=ar.get_user()).first()
        #     if my_reaction and my_reaction.emotion:

        #
        if o.modified is None or (o.modified - o.created).total_seconds() < 1:
            t = _("Created {}")
        else:
            t = _("Modified {}")

        t = t.format(o.created.strftime("%Y-%m-%d %H:%M"))

        # if o.emotion.button_text:
        #     yield o.emotion.button_text
        #     yield " "
        # if False:
        #     attrs = {"class": "bordertext"}
        # else:
        #     attrs = {}
        s += ar.obj2htmls(o, naturaltime(o.created), title=t)
        s += format_html(" {} ", _("by"))
        if o.user is None:
            by = gettext("system")
        else:
            by = o.user.username
        # yield E.b(by)
        s += format_html("<b>{}</b>", by)

        # Show `reply_to` and `owner` unless they are obvious.
        # When `reply_to` is obvious, then `owner` is "obviously obvious" even
        # though that might not be said explicitly.
        if not ar.is_obvious_field("reply_to"):
            if o.reply_to:
                s += format_html(" {} ", _("in reply to"))
                if o.reply_to.user is None:
                    s += gettext("system")
                else:
                    # yield E.b(o.reply_to.user.username)
                    s += format_html("<b>{}</b>", o.reply_to.user.username)
            if not ar.is_obvious_field("owner"):
                if o.owner:
                    s += format_html(" {} ", _("about"))
                    # s += ar.row_as_paragraph(o.owner)
                    s += ar.obj2htmls(o.owner)
                    # s += ar.obj2htmls(o.owner)
                    # if False:  # tickets show themselves their group in __str__()
                    #     group = o.owner.get_comment_group()
                    #     if group and group.ref:
                    #         s += "@" + group.ref

        if False and o.num_reactions:
            txt = ngettext("{} reaction", "{} reactions", o.num_reactions).format(
                o.num_reactions
            )
            s += " ({})".format(txt)

        # replies  = o.__class__.objects.filter(reply_to=o)
        if o.num_replies > 0:
            txt = ngettext("{} reply", "{} replies", o.num_replies).format(
                o.num_replies
            )
            s += format_html(" ({})", txt)

        if o.body_short_preview:
            s += mark_safe(" : " + o.body_short_preview)
            # try:
            #     # el = etree.fromstring(o.body_short_preview, parser=html_parser)
            #     for e in lxml.html.fragments_fromstring(o.body_short_preview): #, parser=cls.html_parser)
            #         yield e
            #     # el = etree.fromstring("<div>{}</div>".format(o.body_full_preview), parser=cls.html_parser)
            #     # print(20190926, tostring(el))
            # except Exception as e:
            #     yield "{} [{}]".format(o.body_short_preview, e)
        # assert isinstance(s, SafeString)  # temporary 20240506
        return s

    def as_story_item(self, ar, indent=0):
        def storypar(s):
            # return """<p class="bordertext">{}</p>""".format(s)
            if indent > 0:
                style = "padding-left:{}em;".format(indent)
                style += "border-left: medium dotted grey;"
                return format_html('<p style="{}">{}</p>', style, s)
            return format_html("<p>{}</p>", s)

        htmls = storypar(self.as_paragraph(ar))
        for child in RepliesByComment.create_request(master_instance=self, parent=ar):
            htmls += storypar(child.as_story_item(ar, indent=indent + 1))
        # if self.replies_to_this.count():
        #     # s += "<p>{}</p>".format("Replies:")
        #     for child in self.replies_to_this.all():
        #         htmls += child.as_story_item(ar, indent=indent + 2)
        # if indent > 0:
        #     style = "margin-left:{}em;".format(indent * 2)
        #     htmls = '<div style="{}">{}</div>'.format(style, htmls)
        # assert isinstance(htmls, SafeString)  # temporary 20240506
        return htmls

    def __str__(self):
        return "{} #{}".format(self._meta.verbose_name, self.pk)
        # return _('{user} {time}').format(
        #     user=self.user, obj=self.owner,
        #     time=naturaltime(self.modified))

    # def after_ui_create(self, ar):
    #     super(Comment, self).after_ui_create(ar)
    #     if self.owner_id:
    #         self.private = self.owner.is_comment_private(self, ar)

    def on_create(self, ar):
        super().on_create(ar)
        if self.owner_id:
            self.owner.on_create_comment(self, ar)

    def get_default_group(self):
        # implements PrivacyRelevant
        if self.owner:
            return self.owner.get_comment_group()
        return super().get_default_group()

    def after_ui_save(self, ar, cw):
        super().after_ui_save(ar, cw)
        if self.owner is not None:
            self.owner.on_commented(self, ar, cw)

    def full_clean(self):
        super().full_clean()
        if self.reply_to_id and not self.owner_id:
            # added only 2023-11-19, that's why we have CommentChecker
            self.owner = self.reply_to.owner
        # self.owner.setup_comment(self)

    def get_change_owner(self):
        return self.owner or self

    # def get_change_message_type(self, ar):
    #     if self.published is None:
    #         return None
    #     return super(Comment, self).get_change_message_type(ar)

    def get_change_observers(self, ar=None):
        if isinstance(self.owner, ChangeNotifier):
            obs = self.owner
        else:
            obs = super()
        for u in obs.get_change_observers(ar):
            yield u

    def get_change_subject(self, ar, cw):
        if cw is None:
            s = _("{user} commented on {obj}")
        else:
            s = _("{user} modified comment on {obj}")
        return s.format(user=ar.get_user(), obj=self.owner)

    def get_change_body(self, ar, cw):
        if cw is None:
            s = _("{user} commented on {obj}")
        else:
            s = _("{user} modified comment on {obj}")
        user = ar.get_user()
        # s = s.format(user=user, obj=self.owner.obj2memo())
        # return ar.obj2htmls(self.owner)
        s = s.format(user=user, obj=ar.obj2htmls(self.owner))
        # s += " (20240101 ar is {})".format(escape(str(ar)))
        s += ":<br>" + self.body
        # if False:
        #     s += '\n<p>\n' + self.more_text
        return s

    def get_notify_options(self):
        # Unlike all other change notifiers
        return dict(reply_to=self)

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(observed_event=CommentEvents.field(blank=True))
        super().setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        user = ar.get_user()
        if not user.user_type.has_required_roles([CommentsReader]):
            return qs.none()
        qs = qs.annotate(num_replies=models.Count("replies_to_this"))
        qs = qs.annotate(num_reactions=models.Count("reactions_to_this"))
        # qs = qs.annotate(my_emotion='reaction__emotion')
        if (pv := ar.param_values) is None:
            return qs
        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        return qs

    # @dd.htmlbox()
    # def card_summary(self, ar):
    #     if not ar:
    #         return ""
    #     # header = ar.actor.get_comment_header(self, ar) if ar else ""
    #     body = ar.parse_memo(self.body)
    #     # for e in lxml.html.fragments_fromstring(self.body_short_preview):  # , parser=cls.html_parser)
    #     #     html += tostring(e)
    #
    #     return "<div><p>{}</p></div>".format(
    #         # header,
    #         body)

    # def summary_row(o, ar):


dd.update_field(Comment, "user", editable=False)
Comment.update_controller_field(verbose_name=_("Topic"))
Comment.add_picker("my_emotion")


class Reaction(CreatedModified, UserAuthored, DateRangeObservable):
    class Meta(object):
        app_label = "comments"
        abstract = dd.is_abstract_model(__name__, "Reaction")
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")

    allow_cascaded_delete = "user comment"

    comment = dd.ForeignKey(
        "comments.Comment", related_name="reactions_to_this")
    emotion = Emotions.field(default="ok")

    def as_summary_item(self, ar, text=None, **kwargs):
        return text or self.emotion.button_text


# @dd.receiver(dd.post_startup)
# def setup_memo_commands(sender=None, **kwargs):
#     # See :doc:`/specs/memo`
#
#     if not sender.is_installed('memo'):
#         return
#
#     Comment = sender.models.comments.Comment
#     mp = sender.plugins.memo.parser
#
#     mp.register_django_model('comment', Comment)


class CommentChecker(Checker):
    # temporary checker to fix #4084 (Comment.owner is empty when replying to a comment)
    verbose_name = _("Check for missing owner in reply to comment")
    model = Comment
    msg_missing = _("Missing owner in reply to comment.")

    def get_checkdata_problems(self, ar, obj, fix=False):
        if obj.reply_to_id and not obj.owner_id and obj.reply_to.owner_id:
            yield (True, self.msg_missing)
            if fix:
                obj.full_clean()
                obj.save()


CommentChecker.activate()
