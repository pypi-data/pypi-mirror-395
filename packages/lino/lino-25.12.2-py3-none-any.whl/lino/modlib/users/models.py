# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import random
import string
from datetime import timedelta
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

from lino.api import dd, rt, _, gettext
from lino.core import userprefs
from lino.core.roles import Supervisor
from lino.core.roles import SiteAdmin
# from lino.core.fields import NullCharField
from lino.mixins import CreatedModified, Contactable
from lino.mixins import DateRange
from lino.modlib.about.choicelists import TimeZones, DateFormats
from lino.modlib.printing.mixins import Printable
# from lino.modlib.publisher.mixins import Publishable
from lino.modlib.about.models import About
from lino.utils.html import tostring, format_html, mark_safe

from .choicelists import UserTypes
from .mixins import UserAuthored  # , TimezoneHolder
from .actions import ChangePassword, SignOut, CheckedSubmitInsert
from .actions import SendWelcomeMail, SignIn, ConnectAccount
from .actions import CreateAccount, ResetPassword, VerifyUser, VerifyMe

from .ui import *


if multi_ledger := dd.is_installed("ledgers"):
    from lino_xl.lib.ledgers.actions import SubscribeToLedger


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # thanks to https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    # dd.logger.info("20240418 Gonna call random.SystemRandom()")
    return "".join(random.SystemRandom().choice(chars) for _ in range(size))


partner_model = dd.plugins.users.partner_model

SYNCHRONIZED_FIELDS = ("first_name", "last_name", "email", "language", "remarks")

# Setting this to True would be more consistent in some regards but causes about
# 25 doctests in welfare to fail, and it's not sure whether  the welfare end
# users would like it:

UPPERCASE_LAST_NAME_FOR_USERS = False


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("user_type", UserTypes.user)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("user_type", UserTypes.admin)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, Contactable, CreatedModified, Printable, DateRange):

    class Meta:
        app_label = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        abstract = dd.is_abstract_model(__name__, "User")
        ordering = ["last_name", "first_name", "username"]

    USERNAME_FIELD = "username"
    _anon_user = None
    objects = UserManager()

    preferred_foreignkey_width = 15
    hidden_columns = "password remarks"
    # authenticated = True
    quick_search_fields = "username user_type first_name last_name remarks"
    allow_merge_action = True

    username = models.CharField(
        _("Username"), max_length=30, unique=True, null=True, blank=True)
    user_type = UserTypes.field(blank=True)
    initials = models.CharField(_("Initials"), max_length=10, blank=True)
    if dd.plugins.users.with_nickname:
        nickname = models.CharField(_("Nickname"), max_length=50, blank=True)
    else:
        nickname = dd.DummyField("")
    first_name = models.CharField(_("First name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True)
    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)
    partner = dd.ForeignKey(
        partner_model, blank=True, null=True, related_name="users_by_partner"
    )

    verification_password = models.CharField(max_length=200, blank=True)
    verification_code = models.CharField(max_length=200, blank=True, default="!")
    verification_code_sent_on = models.DateTimeField(null=True, blank=True)

    if settings.USE_TZ:
        time_zone = TimeZones.field(default="default")
    else:
        time_zone = dd.DummyField()

    date_format = DateFormats.field(default="default")

    ledger = dd.ForeignKey("ledgers.Ledger", null=True, blank=True)

    if multi_ledger:
        ledger_subscribe__user = SubscribeToLedger(
            params_layout="""
        company role
        ledger
        """
        )

    submit_insert = CheckedSubmitInsert()

    verify_me = VerifyMe()
    send_welcome_email = SendWelcomeMail()
    change_password = ChangePassword()
    # sign_in = SignIn()
    sign_out = SignOut()

    if dd.get_plugin_setting("users", "third_party_authentication"):
        connect_account = ConnectAccount()

    # if settings.SITE.default_ui == "lino_react.react":
    #     my_settings = MySettings()

    def __str__(self):
        return self.nickname or self.get_full_name()

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "user_type"

    @property
    def is_active(self):
        # if not self.has_usable_password():
        if not self.user_type or not self.username:
            return False
        if self.start_date and self.start_date > dd.today():
            return False
        if self.end_date and self.end_date < dd.today():
            return False
        return True

    def must_verify(self):
        self.verification_code = id_generator(12)
        self.verification_code_sent_on = dd.now()

    def is_verified(self):
        return not self.verification_code

    def mark_verified(self):
        self.verification_code = ""

    def is_verification_code_expired(self):
        if self.verification_code_sent_on is None:
            return False
        return (
            self.verification_code_sent_on
            + timedelta(minutes=dd.plugins.users.verification_code_expires)
            < dd.now()
        )

    def get_as_user(self):
        """
        Overrides :meth:`lino_xl.lib.contacts.Partner.get_as_user`.
        """
        return self

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.initials or self.username or str(self.pk)
        if UPPERCASE_LAST_NAME_FOR_USERS and settings.SITE.uppercase_last_name:
            last_name = self.last_name.upper()
        else:
            last_name = self.last_name
        if settings.SITE.last_name_first:
            return f"{last_name}, {self.first_name}".strip()
        return f"{self.first_name} {last_name}".strip()

    @dd.displayfield(_("Status"))
    def status(self, ar):
        s = _("Active") if self.is_active else _("Inactive")
        s += ". " + (_("Verified") if self.is_verified() else _("Not verified"))
        if self.verification_password:
            s += ". " + _("Password reset")
        return s + "."

    # @dd.displayfield(_("Other authentication providers"))
    # def social_auth_links(self, ar=None):
    #     return settings.SITE.get_social_auth_links        ()
    #     # elems = []
    #     # for backend in get_social_auth_backends()
    #     # elems.append(E.a("foo"))
    #     # return E.p(elems)

    @dd.virtualfield(dd.ForeignKey("contacts.Person"))
    def person(self, ar):
        if self.partner:
            return self.partner.get_mti_child("person")

    # person = property(get_person)

    @dd.virtualfield(dd.ForeignKey("contacts.Company"))
    def company(self, ar):
        if self.partner:
            return self.partner.get_mti_child("company")

    def is_editable_by_all(self):
        return False

    def has_required_roles(self, *args):
        return self.user_type.has_required_roles(*args)

    def get_row_permission(self, ar, state, ba):
        # import pdb ; pdb.set_trace()
        if not ba.action.readonly:
            user = ar.get_user()
            if user != self:
                if not user.user_type.has_required_roles([SiteAdmin]):
                    if not self.is_editable_by_all():
                        return False
        return super().get_row_permission(ar, state, ba)
        # ~ return False

    def disabled_fields(self, ar):
        """
        Only System admins may change the `user_type` of users.
        See also :meth:`Users.get_row_permission`.
        """
        rv = super().disabled_fields(ar)
        user = ar.get_user()
        if self.is_verified():
            rv.add("verify_me")
        if not user.user_type.has_required_roles([SiteAdmin]):
            rv.add("user_type")
            rv.add("partner")
            rv.add("send_email")
            # merging two users is only for SiteAdmin, even when you are Expert
            rv.add("merge_row")
            if user != self:
                rv.add("change_password")
        return rv

    def full_clean(self, *args, **kw):
        if not self.password:
            self.set_unusable_password()
        # if not self.initials:
        #     if self.first_name and self.last_name:
        #         self.initials = self.first_name[0] + self.last_name[0]
        super().full_clean(*args, **kw)
        self.sync_partner()
        if not self.language:
            self.language = settings.SITE.get_default_language()

    def sync_partner(self, **kw):
        if partner_model is None:
            return
        if self.user_type and self.user_type.has_required_roles([SiteAdmin]):
            # if self.user_type and isinstance(self.user_type.role, SiteAdmin):
            # site admins are not automatically linked to a partner
            return
        p = self.partner
        # if not issubclass(rt.models.contacts.Person, partner_model):
        #     return
        if p is None:
            if self.is_verified():
                for k in SYNCHRONIZED_FIELDS:
                    v = getattr(self, k)
                    if v:
                        kw[k] = v
                    else:
                        return
                p = rt.models.contacts.Person(**kw)
                p.full_clean()
                p.save()
                self.partner = p
        else:
            p = p.get_mti_child("person")
            if p is not None:
                for k in SYNCHRONIZED_FIELDS:
                    if not getattr(self, k):
                        setattr(self, k, getattr(p, k))

    def on_create(self, ar):
        self.must_verify()
        self.start_date = dd.today()
        return super().on_create(ar)

    def email_changed(self, ar):
        self.must_verify()

    def get_received_mandates(self):
        # ~ return [ [u.id,_("as %s")%u] for u in self.__class__.objects.all()]
        return [[u.id, str(u)] for u in self.__class__.objects.all()]
        # ~ return self.__class__.objects.all()

    # @dd.htmlbox(_("Welcome"))
    # def welcome_email_body(self, ar):
    #     # return join_words(self.last_name.upper(),self.first_name)
    #     return self.get_welcome_email_body(ar)

    def get_welcome_email_body(self, ar):
        template = rt.get_template("users/welcome_email.eml")
        # sar = ar.spawn_request(permalink_uris=True)
        ar.permalink_uris = True
        context = self.get_printable_context(ar)
        # dict(obj=self, E=E, rt=rt)
        return template.render(**context)

    @classmethod
    def get_active_users(cls, required_roles=[], unwanted_roles=None, **kwargs):
        user_types = [
            t
            for t in UserTypes.get_list_items()
            if t.has_required_roles(required_roles)
        ]
        if unwanted_roles is not None:
            user_types = [
                t for t in user_types if not t.has_required_roles(unwanted_roles)
            ]
        qs = cls.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gt=dd.today()),
            Q(start_date__isnull=True) | Q(start_date__lt=dd.today()),
            user_type__in=user_types,
        )
        if kwargs:
            qs = qs.filter(**kwargs)
        return qs

    @classmethod
    def get_by_username(cls, username, default=models.NOT_PROVIDED):
        """
        `User.get_by_username(x)` is equivalent to
        `User.objects.get(username=x)` except that the text of the
        DoesNotExist exception is more useful.
        """
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with username %r" % (str(cls._meta.verbose_name), username)
                )
            return default

    def get_preferences(self):
        """
        Return the preferences of this user. The returned object is a
        :class:`lino.core.userprefs.UserPrefs` object.
        """
        return userprefs.reg.get(self)

    @classmethod
    def get_anonymous_user(cls):
        return settings.SITE.get_anonymous_user()

    @classmethod
    def filter_active_users(self, qs, today, prefix=""):
        qs = qs.filter(
            Q(**{prefix + "start_date__isnull": True})
            | Q(**{prefix + "start_date__lte": today})
        )
        qs = qs.filter(
            Q(**{prefix + "end_date__isnull": True})
            | Q(**{prefix + "end_date__gte": today})
        )
        return qs

    # @dd.action(label=_("Send e-mail"),
    #            show_in_toolbar=True, show_in_workflow=False,
    #            button_text="✉")  # u"\u2709"
    # def do_send_email(self, ar):
    #     self.send_welcome_email()

    def usertext(self):
        return "{0} {1}, {3} ({2})".format(
            self.last_name, self.first_name, self.username, self.user_type
        )

    def get_authorities(self):
        if self.has_required_roles([Supervisor]):
            users = settings.SITE.user_model.objects.exclude(user_type="").exclude(
                id=self.id
            )
        else:
            qs = (
                rt.models.users.Authority.objects.filter(authorized=self)
                .exclude(user__user_type="")
                .select_related("user")
            )
            qs = qs.order_by("user__last_name", "user__first_name", "user__username")
            users = [a.user for a in qs]
        return [(u.id, u.usertext()) for u in users]

    # @classmethod
    # def get_default_table(cls):
    #     return rt.models.users.MySettings

    def dt_astimezone(self, dt):
        """
        Convert datetime to user timezone if time_zone is not None otherwise to default timezone.
        Used in template notify/summary.eml
        """
        default_tz = rt.models.about.TimeZones.default
        aware_dt = dt.astimezone(default_tz.tzinfo)
        if self.time_zone:
            aware_dt = aware_dt.astimezone(self.time_zone.tzinfo)
        return aware_dt


settings.AUTH_USER_MODEL = "users.User"


class Authority(UserAuthored):

    class Meta:
        app_label = "users"
        verbose_name = _("Authority")
        verbose_name_plural = _("Authorities")

    authorized = dd.ForeignKey(settings.SITE.user_model)

    @dd.chooser()
    def authorized_choices(cls, user):
        qs = settings.SITE.user_model.objects.exclude(user_type=None)
        # ~ user_type=UserTypes.blank_item) 20120829
        if user is not None:
            qs = qs.exclude(id=user.id)
            # ~ .exclude(level__gte=UserLevels.admin)
        return qs


dd.update_field(Authority, "user", null=False)

# @dd.receiver(dd.pre_startup)
# def inject_partner_field(sender=None, **kwargs):
#
#     User = sender.models.users.User
#
#     if dd.is_installed('contacts'):
#         Partner = sender.models.contacts.Partner
#         if not issubclass(User, Partner):
#             dd.inject_field(User, 'partner', dd.ForeignKey(
#                 'contacts.Partner', blank=True, null=True,
#                 related_name='users_by_partner',
#                 on_delete=models.PROTECT))
#             # a related_name is needed so that Avanti can have a Client
#             # who inherits from both Partner and UserAuthored
#             return
#     dd.inject_field(User, 'partner', dd.DummyField())


class Permission(dd.Model):

    class Meta:
        app_label = "users"
        abstract = True


About.sign_in = SignIn()
About.reset_password = ResetPassword()
About.verify_user = VerifyUser()

if dd.plugins.users.allow_online_registration:
    About.create_account = CreateAccount()


if dd.is_installed("memo"):

    @dd.receiver(dd.post_startup)
    def setup_memo_commands(sender=None, **kwargs):
        # See :doc:`/specs/memo`

        # if not sender.is_installed("memo"):
        #     return

        mp = sender.plugins.memo.parser
        mp.add_suggester(
            "@",
            sender.models.users.User.objects.filter(
                username__isnull=False).order_by("username"),
            "username")


if dd.plugins.users.allow_online_registration:

    def welcome_messages(ar):
        me = ar.get_user()
        if not me.is_verified():
            # sar = rt.models.users.Me.create_request(parent=ar)
            sar = ar
            if me.email:
                # verify_me =
                msg = format_html(
                    _("Your email address ({email}) is not verified, "
                      "please check your mailbox and {verify} or {resend}."),
                    email=me.email,
                    verify=tostring(sar.instance_action_button(
                        me.verify_me, _("verify now"))),
                    resend=tostring(sar.instance_action_button(
                        me.send_welcome_email, _("re-send our welcome email"))))
            else:
                msg = format_html(
                    _("You have no email address, please {edit}."),
                    edit=tostring(sar.obj2html(me, _("edit your user settings"))))
            yield mark_safe(msg)

    dd.add_welcome_handler(welcome_messages)
