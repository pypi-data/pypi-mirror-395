# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import Q

from django.utils.translation import gettext_lazy as _

# from django.utils.translation import pgettext_lazy as pgettext
from django.utils.text import format_lazy
from django.conf import settings

from lino.api import dd, rt

from lino.core.exceptions import ChangedAPI
from lino.core import model
from lino.core import actions
from lino.core import dbtables
from lino.core.roles import SiteStaff, SiteAdmin
from lino.modlib.printing.mixins import Printable

from .roles import Helper, AuthorshipTaker


class Authored(Printable):

    class Meta:
        abstract = True

    # author_field_name = None

    manager_roles_required = dd.login_required(SiteStaff)

    def get_author(self):
        return self.user
        # return getattr(self, self.author_field_name)

    def set_author(self, user):
        raise NotImplementedError()

    def on_duplicate(self, ar, master):
        """The default behaviour after duplicating is to change the author to
        the user who requested the duplicate.

        """
        if ar and ar.user:
            self.set_author(ar.user)
        super().on_duplicate(ar, master)

    def get_row_permission(self, ar, state, ba):
        """Only "managers" can edit other users' work.

        See also :attr:`manager_roles_required`.

        """
        if not super().get_row_permission(ar, state, ba):
            return False
        if ar and ba.action.select_rows:
            user = ar.get_user()
            author = self.get_author()
            if (
                author != ar.user
                and (ar.subst_user is None or author != ar.subst_user)
                and not user.user_type.has_required_roles(self.manager_roles_required)
            ):
                return ba.action.readonly
        return True

    # @classmethod
    # def on_analyze(cls, site):
    #     if hasattr(cls, "manager_level_field"):
    #         raise ChangedAPI("{0} has a manager_level_field".format(cls))
    #     super().on_analyze(site)

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     """Adds the :attr:`user` filter parameter field."""
    #     fld = cls._meta.get_field('user')
    #     fields.setdefault(
    #         'user', models.ForeignKey(
    #             'users.User', verbose_name=fld.verbose_name,
    #             blank=True, null=True))
    #     return super(Authored, cls).setup_parameters(**fields)

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "user"  # cls.author_field_name)

    def get_print_language(self):
        u = self.get_author()
        if u is None or not u.language:
            return super().get_print_language()
        return u.language


class UserAuthored(Authored):

    class Meta:
        abstract = True

    workflow_owner_field = "user"
    # author_field_name = 'user'
    # print("20251127", repr(dd))
    user = dd.ForeignKey(
        "users.User",
        verbose_name=_("Author"),
        related_name="%(app_label)s_%(class)s_set_by_user",
        blank=True,
        null=True,
    )

    def set_author(self, user):
        self.user = user
        # setattr(self, self.author_field_name, user)

    def on_create(self, ar):
        """
        Adds the requesting user to the `user` field.

        When acting as another user, the default implementation
        inserts the *real* user, not subst_user.
        This is important for cal.Event.
        """
        # raise Exception("20230331 {}".format(ar.user))
        if ar and self.user_id is None:
            u = ar.user
            if u is not None:
                self.user = u
        super().on_create(ar)

    def get_time_zone(self):
        """Return the author's timezone. Used by
        :class:`lino_xl.lib.cal.mixins.Started`.

        """
        if self.user_id is None:
            # return settings.TIME_ZONE
            return rt.models.about.TimeZones.default
        return self.user.time_zone or rt.models.about.TimeZones.default
        # return self.user.timezone or settings.TIME_ZONE


class My(dbtables.Table):
    """Mixin for tables on :class:`Authored` that sets the requesting
    user as default value for the :attr:`author` filter parameter.

    If the table's model does *not* inherit from :class:`Authored`,
    then it must define a parameter field named 'user' and a model
    attribute `user`.  This feature is used by
    :class:`lino_xl.lib.reception.models.MyWaitingVisitors`.

    Used by
    :mod:`lino_xl.lib.excerpts` and
    :mod:`lino_xl.lib.reception`.

    """

    abstract = True
    # required_roles = dd.login_required()

    @classmethod
    def get_actor_label(self):
        if self._label is not None:
            return self._label
        if self.model is None:
            return self.__name__
        return format_lazy(_("My {}"), self.model._meta.verbose_name_plural)

    @classmethod
    def setup_request(cls, ar):
        super().setup_request(ar)
        ar.obvious_fields.add("user")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        # kw.update(user=ar.get_user())
        # k = self.author_field_name or self.model.author_field_name
        # kw[k] = ar.get_user()
        # kw[self.model.author_field_name] = ar.get_user()
        kw["user"] = ar.get_user()
        return kw


class StartPlan(dd.Action):
    show_in_toolbar = False
    # icon_name = 'basket'
    sort_index = 52
    select_rows = False
    http_method = "POST"
    update_after_start = False

    def get_button_label(self, actor):
        return self.label or actor.model._meta.verbose_name
        # return format_lazy(
        #     pgettext("singular", "My {}"), actor.model._meta.verbose_name)

    # def attach_to_actor(self, owner, name):
    #     self.label = format_lazy(
    #         _("Start new {}"), owner.model._meta.verbose_name)
    #     # self.label = owner.model._meta.verbose_name
    #     print("20180905 {} on {} {}".format(name, owner, self.label))
    #     return super(StartPlan, self).attach_to_actor(owner, name)

    def get_plan_options(self, ar):
        return {}

    def get_plan_model(self, ar):
        # return self.defining_actor.model
        return ar.actor.model

    def run_from_ui(self, ar, **kw):
        options = self.get_plan_options(ar)
        pm = self.get_plan_model(ar)
        plan = pm.create_user_plan(ar.get_user(), **options)
        # plan = self.defining_actor.model.create_user_plan(
        #     ar.get_user(), **options)
        if self.update_after_start:
            plan.run_update_plan(ar)
        ar.goto_instance(plan, refresh=True)


class UpdatePlan(dd.Action):
    label = _("Update plan")
    icon_name = "lightning"
    sort_index = 53

    # button_text = "F"

    def run_from_ui(self, ar, **kw):
        for plan in ar.selected_rows:
            plan.run_update_plan(ar)
        ar.success(refresh=True)


class UserPlan(UserAuthored):
    class Meta:
        abstract = True

    today = models.DateField(_("Today"), default=dd.today)
    # 20240621 today is no longer readonly because the user may want to continue
    # a plan they started yesterday

    update_plan = UpdatePlan()
    start_plan = StartPlan()

    @classmethod
    def create_user_plan(cls, user, **options):
        qs = cls.objects.filter(user=user)
        num = qs.count()
        if num == 1:
            plan = qs.first()
            changed = False
            for k, v in options.items():
                if getattr(plan, k) != v:
                    changed = True
                    setattr(plan, k, v)
            if "today" not in options:
                if plan.today != dd.today():
                    plan.today = dd.today()
                    changed = True
            if changed:
                plan.reset_plan()
        else:
            if num > 1:
                dd.logger.warning(
                    f"Got {num} {cls._meta.verbose_name_plural} for {user}")
                qs.delete()
            plan = cls(user=user, **options)
        plan.full_clean()
        plan.save()
        return plan

    def __str__(self):
        return _("{plan} by {user}").format(
            plan=self._meta.verbose_name, user=self.user)

    def run_update_plan(self, ar):
        raise NotImplementedError()

    def reset_plan(self):
        """Delete all cached data for this plan."""
        pass


class AssignToMe(dd.Action):
    """Set yourself as assigned user.

    This will ask for confirmation and then set
    :attr:`Assignable.assigned_to`.

    """

    label = _("Assign to me")
    show_in_workflow = True
    show_in_toolbar = False  # added 20180515 for noi. possible side
    # effects in welfare.

    # readonly = False
    required_roles = dd.login_required(Helper)

    # button_text = u"\u2698"  # FLOWER (⚘)
    # button_text = u"\u26d1"  # ⛑
    # button_text = u"\u261D"  # ☝
    button_text = "\u270B"  # ✋

    # help_text = _("You become assigned to this.")

    def get_action_permission(self, ar, obj, state):
        if obj.assigned_to_id:
            return False
        # user = ar.get_user()
        # if obj.assigned_to == user:
        #     return False
        # if user == obj.get_author():
        #     return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.assigned_to = ar.get_user()
            obj.save()
            ar.set_response(refresh=True)

        ar.confirm(ok, _("You become assigned to this."), _("Are you sure?"))


class TakeAuthorship(dd.Action):
    """
    You declare to become the fully responsible user for this database
    object.

    Accordingly, this action is available only when you are not
    already fully responsible. You are fully responsible when (1)
    :attr:`Assignable.user` is set to *you* **and** (2)
    :attr:`Event.assigned_to` is *not empty*.

    Basically anybody can take any event, even if it is not assigned
    to them.

    New since 20160814 : I think that the Take action has never been
    really used. The original use case is when a user creates an
    apointment for their colleague: that colleague goes to assigned_to
    and is invited to "take" the appointment which has been agreed for
    him.
    """

    label = _("Take")
    show_in_workflow = True
    show_in_toolbar = False

    # This action modifies the object, but we don't tell Lino about it
    # because we want that even non-manager users can run it on
    # objects authored by others.
    # readonly = False

    required_roles = dd.login_required(AuthorshipTaker)

    button_text = "\u2691"  # flag (⚑)

    # def get_action_permission(self, ar, obj, state):
    #     # new since 20160814
    #     if obj.get_author() == ar.get_user():
    #         return False
    #     # if obj.assigned_to != ar.get_user():
    #     #     return False
    #     # if obj.get_author() == ar.get_user():
    #     #     if obj.assigned_to is None:
    #     #         return False
    #     # elif obj.assigned_to != ar.get_user():
    #     #     return False
    #     return super(TakeAuthorship,
    #                  self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        # obj is an Assignable

        def ok(ar):
            obj.set_author(ar.get_user())
            # obj.user = ar.get_user()
            obj.assigned_to = None
            # ~ kw = super(TakeAuthorship,self).run(obj,ar,**kw)
            obj.save()
            ar.set_response(refresh=True)

        ar.confirm(
            ok, _("You take responsibility for {}.").format(obj), _("Are you sure?")
        )


class Assignable(Authored):
    """.. attribute:: assigned_to

    This field is usually empty.  Setting it to another user means
    "I am not fully responsible for this item".

    This field is cleared when somebody calls
    :class:`TakeAuthorship` on the object.

    """

    class Meta:
        abstract = True

    assigned_to = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Assigned to"),
        related_name="%(app_label)s_%(class)s_set_assigned",
        blank=True,
        null=True,
    )

    take = TakeAuthorship()
    assign_to_me = AssignToMe()

    disable_author_assign = True
    """
    Set this to False if you want that the author of an object can
    also assign themselves.

    In Lino Noi you can be author of a ticket and then assign it to
    yourself, but e.g. in group calendar management we don't want this
    behaviour.
    """

    def disabled_fields(self, ar):
        s = super().disabled_fields(ar)
        user = ar.get_user()
        if self.assigned_to == user:
            s.add("assign_to_me")

        if self.disable_author_assign and user == self.get_author():
            s.add("assign_to_me")
            s.add("take")
        return s

    def on_create(self, ar):
        # 20130722 e.g. CreateClientEvent sets assigned_to it explicitly
        if self.assigned_to is None:
            self.assigned_to = ar.subst_user
        super().on_create(ar)

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "assigned_to"

    if dd.is_installed('notify'):

        # Send notification of assignment
        def assigned_to_changed(self, ar):

            if (self.assigned_to is None):
                return
            if ar.user == self.assigned_to and not ar.user.notify_myself:
                return

            ctx = dict(user=ar.user, what=self.obj2memo())

            def msg():
                subject = _("{user} assigned you to {what}").format(**ctx)
                return (subject, tostring(E.span(subject)))

            mt = rt.models.notify.MessageTypes.change

            rt.models.notify.Message.emit_notification(
                ar, self, mt, msg,
                [(self.assigned_to, self.assigned_to.mail_mode)])


# class Groupwise(dd.Model):
class PrivacyRelevant(dd.Model):

    class Meta:
        abstract = True

    private = models.BooleanField(
        _("Confidential"), default=dd.plugins.users.private_default)
    group = dd.ForeignKey("groups.Group", blank=True, null=True)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        # Show only rows that belong to a group of which I am a member or which
        # is public.
        qs = super().get_request_queryset(ar, **filter)
        user = ar.get_user()
        if user.is_anonymous:
            # if dd.is_installed('groups'):
            #     qs = qs.filter(group__private=False)
            return qs.filter(private=False)
        if user.user_type.has_required_roles([SiteAdmin]):
            return qs
        flt = Q(private=False)
        if issubclass(cls, UserAuthored):
            flt |= Q(user=user)
        if dd.is_installed('groups'):
            # flt |= Q(group__private=False)
            flt |= Q(group__members__user=user)
        qs = qs.filter(flt).distinct()
        return qs

    if dd.is_installed("groups"):

        def on_create(self, ar):
            # if not ar.is_obvious_field('group'):
            #     self.group = ar.get_user().current_group
            super().on_create(ar)
            if not self.group_id:
                self.group = ar.get_user().current_group
            if self.group:
                self.private = self.group.private

        def get_default_group(self):
            return None  # dd.plugins.groups.get_default_group()

        def full_clean(self):
            if not self.group_id:
                self.group = self.get_default_group()
            if self.group and self.group.private:
                self.private = True
            super().full_clean()
