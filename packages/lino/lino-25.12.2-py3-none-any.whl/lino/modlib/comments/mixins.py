# -*- coding: UTF-8 -*-
# Copyright 2015-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _
from lino.modlib.memo.mixins import MemoReferrable

from .choicelists import Emotions
from .roles import PrivateCommentsReader


class MyEmotionField(dd.VirtualField):
    """
    An editable virtual field to get and set my emotion about that comment.

    My emotion is stored in the Emotion table.

    """

    editable = True
    empty_values = set([None])

    def __init__(self, *args, **kwargs):
        kwargs.update(blank=True)
        dd.VirtualField.__init__(self, Emotions.field(*args, **kwargs), None)
        self.choicelist = self.return_type.choicelist

    def set_value_in_object(self, ar, obj, value):
        if ar is None:
            raise Exception("20201215")
            # dd.logger.info("20201215 oops")
            # return
        mr, created = rt.models.comments.Reaction.objects.get_or_create(
            user=ar.get_user(), comment=obj
        )
        mr.emotion = value
        mr.full_clean()
        mr.save()

    def value_from_object(self, obj, ar=None):
        return obj.get_my_emotion(ar)

# Removed because it requires much hacking and doesn't improve user experience
# dramatically:
# class AddCommentField(dd.VirtualField):
#     """
#     An editable virtual field to add a comment about that database object.
#
#     """
#
#     editable = True
#     # simple_elem = True
#
#     def __init__(self, slave_table):
#         t = models.TextField(_("Add comment"), blank=True)
#         super().__init__(t, None)
#         self.slave_table = slave_table
#
#     def set_value_in_object(self, ar, obj, value):
#         actor = rt.models.resolve(self.slave_table)
#         # 20240913: The following line fixes a variant of #5715
#         # (ObjectDoesNotExist: Invalid primary key 114 for
#         # storage.FillersByPartner). When programmatically creating an action
#         # request, we must not pass the incoming http request because that would
#         # ask Lino to re-parse the URL parameters, including (in this case) sr
#         # (the ids of selected rows).
#         sar = actor.request(master_instance=obj, parent=ar)
#         # sar = actor.request(
#         #     master_instance=obj, request=ar.request, renderer=ar.renderer
#         # )
#         obj = sar.create_instance(body=value)
#         obj.full_clean()
#         obj.save_new_instance(sar)
#
#         # The refresh_delayed_value response below is theoretically NOT needed
#         # because CommentsByRFC.live_panel_update does the update for delayed
#         # value already. But live_panel_update doesn't work when linod is not
#         # running or linod.use_channels is `False`.
#         ar.set_response(refresh_delayed_value=str(actor))
#
#         # if anybody complains that the refresh doesn't work in ExtJS, we would
#         # need to reactivate the following line:
#         # ar.set_response(refresh=True)
#
#     def value_from_object(self, obj, ar=None):
#         return None


class Commentable(MemoReferrable):

    class Meta:
        abstract = True

    # add_comment = AddCommentField("comments.CommentsByRFC")

    def on_commented(self, comment, ar, cw):
        pass

    def get_rfc_description(self, ar):
        return ""

    if dd.is_installed("comments"):

        def save_new_instance(self, ar):
            super().save_new_instance(ar)
            if rt.settings.SITE.loading_from_dump:
                return

            if (txt := self.get_create_comment_text(ar)) is not None:
                comment = rt.models.comments.Comment(body=txt, owner=self)
                comment.on_create(ar)
                comment.full_clean()
                comment.save_new_instance(ar)
                # print("20220916 save_new_instance() created", comment, txt)

    def get_create_comment_text(self, ar):
        return _("Created new {model} {obj}.").format(
            model=self.__class__._meta.verbose_name, obj=self)

    def get_comment_group(self):
        return None  # dd.plugins.groups.get_default_group()

    def on_create_comment(self, comment, ar):
        pass
