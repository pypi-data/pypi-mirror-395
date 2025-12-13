# -*- coding: UTF-8 -*-
# Copyright 2013-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.models import ContentType
from django.db import models

from lino.api import dd, rt, gettext, _
from lino.modlib.users.mixins import My
from lino.utils.html import E, tostring
import lxml

# from lino.utils.soup import truncate_comment
from lino import mixins
from lino.core import constants
from lino.utils.html import qs2summary
from lino.core.gfks import gfk2lookup
from lino.core import constants
from .roles import CommentsReader, CommentsUser, CommentsStaff
from .choicelists import CommentEvents, Emotions


class CommentTypes(dd.Table):
    required_roles = dd.login_required(CommentsStaff)
    model = "comments.CommentType"
    column_names = "name *"
    order_by = ["name"]

    insert_layout = """
    name
    id
    """

    detail_layout = """
    id name
    comments.CommentsByType
    """


class CommentDetail(dd.DetailLayout):
    main = "general more"

    general = dd.Panel(
        """
    general1:30 general2:30
    """,
        label=_("General"),
    )

    general1 = """
    owner private
    reply_to pick_my_emotion
    body #body_full_preview
    """
    general2 = """
    RepliesByComment
    # reply
    """
    # I moved the reply field to the bottom, and later removed it altogether,
    # because i stopped using it after repeated cases where my editing got lost
    # because there was a traceback after hitting submit, leaving me unable to
    # even copy the text I just typed in order to re-create my comment after
    # reloading the page. And these tracebacks are difficult to reproduce.

    more = dd.Panel(
        """
    more1 more2
    """,
        label=_("More"),
    )

    more1 = """
    id user group
    owner_type owner_id
    comment_type
    ReactionsByComment
    """
    more2 = """
    created modified
    memo.MentionsByTarget
    memo.MentionsByOwner
    """


class Comments(dd.Table):
    required_roles = dd.login_required(CommentsUser)
    model = "comments.Comment"
    default_display_modes = {None: constants.DISPLAY_MODE_LIST}
    # The idea is maybe good, but story mode has no insert button:
    # default_display_modes = {
    #     70: constants.DISPLAY_MODE_LIST,
    #     None: constants.DISPLAY_MODE_STORY}
    extra_display_modes = {constants.DISPLAY_MODE_STORY}
    # display mode "html" is not needed for comments

    params_layout = "start_date end_date observed_event user reply_to"
    column_names = "id modified body_short_preview owner *"

    insert_layout = dd.InsertLayout(
        """
        reply_to owner owner_type owner_id
        # comment_type
        body
        private
        """,
        window_size=(60, dd.auto_height(15)),
        hidden_elements="reply_to owner owner_type owner_id",
    )

    detail_layout = "comments.CommentDetail"

    # card_layout = dd.Panel(
    #     """
    #     # reply_to owner owner_type owner_id
    #     # comment_type
    #     body_short_preview
    #     # private
    #     """,
    #     label=_("Cards"),
    # )

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "reply_to"

    @classmethod
    def comments_created(cls, user, sd, ed):
        pv = dict(user=user, start_date=sd, end_date=ed,
                  observed_event=CommentEvents.created)
        # pv = dict(start_date=sd, end_date=ed, observed_event=CommentEvents.created)
        return cls.create_request(user=user, param_values=pv)

    # @classmethod
    # def get_card_title(cls, ar, obj):
    #     """Overrides the default behaviour"""
    #     return cls.get_comment_header(obj, ar)
    #     # title = _("Created {created} by {user}").format(
    #     #     created=naturaltime(obj.created), user=str(obj.user))
    #     # if cls.get_view_permission(ar.get_user().user_type):
    #     #     title = tostring(ar.obj2html(obj, title))
    #     # return title

    # @classmethod
    # def get_comment_header(cls, comment, ar):
    #     if (comment.modified - comment.created).total_seconds() < 1:
    #         t = _("Created " + comment.created.strftime("%Y-%m-%d %H:%M"))
    #     else:
    #         t = _("Modified " + comment.modified.strftime("%Y-%m-%d %H:%M"))
    #     ch = ar.obj2htmls(comment, naturaltime(comment.created), title=t)
    #     ch += " " + _("by") + " "
    #     if comment.user is None:
    #         ch += _("system")
    #     else:
    #         ch += ar.obj2htmls(comment.user)
    #
    #     if cls.insert_action is not None:
    #         sar = cls.insert_action.request_from(ar)
    #         # print(20170217, sar)
    #         sar.known_values = dict(
    #             reply_to=comment, **gfk2lookup(comment.__class__.owner, comment.owner)
    #         )
    #         # if ar.get_user().is_authenticated:
    #         if sar.get_permission():
    #             btn = sar.ar2button(None, _(" Reply "), icon_name=None)
    #             # btn.set("style", "padding-left:10px")
    #             ch += " [" + tostring(btn) + "]"
    #
    #     # ch.append(' ')
    #     # ch.append(
    #     #     E.a(u"⁜", onclick="toggle_visibility('comment-{}');".format(
    #     #         comment.id), title=str(_("Hide")), href="#")
    #     # )
    #     return ch


class MyComments(My, Comments):
    required_roles = dd.login_required(CommentsUser)
    auto_fit_column_widths = True
    order_by = ["-modified"]
    column_names = "id modified body_short_preview owner workflow_buttons *"


class AllComments(Comments):
    required_roles = dd.login_required(CommentsStaff)
    order_by = ["-created"]


class CommentsByX(Comments):
    required_roles = dd.login_required(CommentsReader)
    order_by = ["-created"]


class RecentComments(CommentsByX):
    # required_roles = dd.login_required(CommentsReader)
    # required_roles = set([CommentsReader])
    # order_by = ["-modified"]
    label = _("Recent comments")
    allow_create = False
    column_names = "body_short_preview modified user owner *"
    stay_in_grid = True
    live_panel_update = True
    preview_limit = 10
    # default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}


class CommentsByType(CommentsByX):
    master_key = "comment_type"
    column_names = "body created user *"


# TODO: rename CommentsByRFC to CommentsByOwner
class CommentsByRFC(CommentsByX):
    master_key = "owner"
    details_of_master_template = _("%(details)s about %(master)s")
    column_names = "body created user *"
    stay_in_grid = True
    live_panel_update = True
    # display_mode = (
    #     (70, constants.DISPLAY_MODE_SUMMARY),
    #     (None, constants.DISPLAY_MODE_STORY),
    # )
    simple_slavegrid_header = True
    insert_layout = dd.InsertLayout(
        """
    reply_to
    # comment_type
    body
    private
    """,
        window_size=(60, dd.auto_height(13)),
        hidden_elements="reply_to",
    )

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        if ar.display_mode == constants.DISPLAY_MODE_STORY:
            kw["reply_to"] = constants.CHOICES_BLANK_FILTER_VALUE
        return kw

    # @classmethod
    # def get_main_card(self, ar):
    #     ticket_obj = ar.master_instance
    #     if ticket_obj is None:
    #         return None
    #     sar = self.request(parent=ar, master_instance=ticket_obj)
    #     html = ticket_obj.get_rfc_description(ar)
    #     sar = self.insert_action.request_from(sar)
    #     if sar.get_permission():
    #         btn = sar.ar2button(None, _("Write comment"), icon_name=None)
    #         html += "<p>" + tostring(btn) + "</p>"
    #
    #     if html:
    #         return dict(
    #             card_title="Description",
    #             main_card_body=html,  # main_card_body is special keyword
    #             id="[main_card]",  # needed for map key in react...
    #         )
    #     else:
    #         return None


class CommentsByMentioned(CommentsByX):
    # show all comments that mention the master instance
    master = dd.Model
    label = _("Mentioned in")
    # label = _("Comments mentioning this")
    # insert_layout = None
    # detail_layout = None
    editable = False

    @classmethod
    def get_filter_kw(cls, ar, **kw):
        mi = ar.master_instance
        if mi is None:
            return None
        Mention = rt.models.memo.Mention
        assert not cls.model._meta.abstract
        ct = ContentType.objects.get_for_model(cls.model)
        mkw = gfk2lookup(Mention.target, mi, owner_type=ct)
        mentions = Mention.objects.filter(
            **mkw).values_list("owner_id", flat=True)
        # mentions = [o.comment_id for o in Mention.objects.filter(**mkw)]
        # print(mkw, mentions)
        # return super(CommentsByMentioned, cls).get_filter_kw(ar, **kw)
        kw.update(id__in=mentions)
        return kw


class RepliesByComment(CommentsByX):
    master_key = "reply_to"
    details_of_master_template = _("Replies to %(master)s")
    stay_in_grid = True
    # display_mode = ((None, constants.DISPLAY_MODE_STORY), )
    # title = _("Replies")
    live_panel_update = True
    label = _("Replies")
    simple_slavegrid_header = True
    paginator_template = "PrevPageLink NextPageLink"
    hide_if_empty = True


def comments_by_owner(obj):
    return CommentsByRFC.create_request(master_instance=obj)


class Reactions(dd.Table):
    required_roles = dd.login_required(CommentsStaff)
    editable = False
    model = "comments.Reaction"
    column_names = "comment user emotion created *"


class ReactionsByComment(Reactions):
    master_key = "comment"
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
