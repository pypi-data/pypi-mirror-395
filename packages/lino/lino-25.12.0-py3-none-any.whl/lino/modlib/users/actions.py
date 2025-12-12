# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime

from lino.utils.html import E, tostring

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from lino.api import dd, rt, _
from lino.core.roles import SiteAdmin
from lino.core import auth, layouts
from lino.core.actions import SubmitInsert

MSG_TAKEN = _("The username {} is taken. Please choose another one")


def send_welcome_email(ar, obj, recipients):
    sender = settings.SERVER_EMAIL
    subject = _("Welcome on {site}").format(
        site=settings.SITE.title or settings.SITE.verbose_name
    )
    body = obj.get_welcome_email_body(ar)
    ar.send_email(subject, sender, body, recipients)


class CheckedSubmitInsert(SubmitInsert):
    """Like the standard :class:`lino.core.actions.SubmitInsert`, but
    checks certain things before accepting the new user.

    """

    def run_from_ui(self, ar, **kw):
        obj = ar.create_instance_from_request()
        if obj.username:
            if obj.__class__.objects.filter(username=obj.username).exists():
                ar.error(MSG_TAKEN.format(obj.username))
                return

        def ok(ar2):
            SubmitInsert.run_from_ui(self, ar, **kw)
            # self.save_new_instance(ar2, obj)
            ar2.success(
                _(
                    "Your request has been registered. "
                    "An email will shortly be sent to {0}"
                    "Please check your emails."
                ).format(obj.email)
            )
            # ar2.set_response(close_window=True)
            # logger.info("20140512 CheckedSubmitInsert")

        ok(ar)


class CreateAccount(dd.Action):
    label = _("Create Account")
    select_rows = False
    parameters = dict(
        first_name=dd.CharField(_("First name")),
        last_name=dd.CharField(_("Last name")),
        username=dd.CharField(_("Username"), blank=True),
        email=dd.CharField(_("Email")),
        password=dd.PasswordField(_("Password"), blank=True),
    )
    # if settings.SITE.plugins.users.third_party_authentication:
    #     parameters['social_auth_links'] = dd.Constant(
    #         get_social_auth_links_func(
    #             gettext("Create account with"), flex_row=False))
    # else:
    #     parameters['social_auth_links'] = dd.DummyField()

    params_layout = """
    first_name last_name
    email
    username
    password
    #social_auth_links
    """
    http_method = "POST"

    # show_in_toolbar = False

    def run_from_ui(self, ar, **kw):
        # validate_sessions_limit(ar.request)
        User = rt.models.users.User
        UserTypes = rt.models.users.UserTypes
        pv = ar.action_param_values
        if not pv["username"]:
            pv["username"] = pv["email"]
        if pv["username"]:
            if User.objects.filter(username=pv["username"]).exists():
                ar.error(MSG_TAKEN.format(pv.username))
                # ar.set_response(close_window=False)
                return

            validate_password(pv['password'])

        ut = UserTypes.get_by_name(dd.plugins.users.user_type_new)
        # pv.pop('social_auth_links')
        obj = User.objects.create_user(user_type=ut, **pv)
        obj.on_create(ar)
        obj.full_clean()
        obj.save()

        ar.selected_rows = [obj]
        recipients = ["{} <{}>".format(obj.get_full_name(), obj.email)]
        send_welcome_email(ar, obj, recipients)

        rt.models.about.About.sign_in.run_from_ui(ar)


class VerifyUser(dd.Action):
    """Enter your verification code."""

    label = _("Verify")
    # http_method = 'POST'
    select_rows = False
    # default_format = 'json'
    # required_roles = set([])
    # required_roles = dd.login_required(SiteAdmin)
    # show_in_toolbar = False
    # show_in_workflow = True
    parameters = dict(
        email=models.EmailField(_("e-mail address")),
        verification_code=models.CharField(_("Verification code"), max_length=50),
    )
    params_layout = """
    email
    # instruct
    verification_code
    """

    def doit(self, ar, user, **kwargs):
        pv = ar.action_param_values
        if user.is_verification_code_expired():
            msg = _("Sorry, your verification code has expired.")
            return ar.error(msg)
        if user.verification_code != pv.verification_code:
            msg = _("Sorry, wrong verification code.")
            return ar.error(msg)
        UserTypes = rt.models.users.UserTypes
        ut = UserTypes.get_by_name(dd.plugins.users.user_type_verified)
        user.user_type = ut
        user.verification_code = ""
        msg = _("Your email address {} is now verified.").format(user.email)
        if user.verification_password:
            user.set_password(user.verification_password)
            user.verification_password = ""
            msg += " " + _("Your new password has been activated.")
        if ar.get_user() != user:
            msg += " " + _("Please sign in.")
        user.full_clean()
        user.save()
        ar.success(msg)

    def html_response(self, ar, user):
        result = ar.response.copy()
        if user is not None:
            href = result.get("goto_url")
            result.update(
                instance=f'<a href="/#{href}">Preferences ({user.get_full_name()})</a>'
            )
        page_content = ""
        for key, value in result.items():
            page_content += f"<tr><td>{key.capitalize()}</td><td>{value}</td></tr>"

        return HttpResponse(
            dd.plugins.jinja.renderer.jinja_env.get_template(
                "users/verification_response.html"
            ).render(
                **{
                    "site": settings.SITE,
                    "page_title": "User verification status:",
                    "page_content": page_content,
                }
            ),
            content_type="text/html",
        )

    def run_from_ui(self, ar, **kwargs):
        # assert len(ar.selected_rows) == 1
        # user = ar.selected_rows[0]
        pv = ar.action_param_values
        flt = dict(verification_code=pv.verification_code)
        # flt = dict()
        flt.update(email=pv.email)
        User = rt.models.users.User
        qs = User.objects.filter(**flt)
        user = None
        try:
            user = qs.get()

            self.doit(ar, user, **kwargs)
            ar.set_response(
                goto_url=ar.get_permalink(rt.models.users.Me.detail_action, user)
            )

        except User.DoesNotExist:
            msg = _("Invalid email address or verification code.")
            ar.error(msg)

        if ar.requesting_panel is None and ar.renderer.front_end.app_label == "react":
            return self.html_response(ar, user)


class VerifyMe(VerifyUser):
    select_rows = True
    required_roles = dd.login_required()
    params_layout = """
    # email
    # instruct
    verification_code
    """

    # def get_action_permission(self, ar, obj, state):
    #     if obj.is_verified():
    #         # print("20210712 False (is verified)")
    #         return False
    #     # print("20210712 True")
    #     return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kwargs):
        assert len(ar.selected_rows) == 1
        user = ar.selected_rows[0]
        self.doit(ar, user, **kwargs)


# if settings.SITE.default_ui == "lino_react.react":
#
#     class MySettings(dd.Action):
#         label = _("My settings")
#         select_rows = False
#         show_in_toolbar = False
#         # http_method = "POST"
#         default_format = None
#
#         def run_from_ui(self, ar, **kw):
#             # assert len(ar.selected_rows) == 1
#             # user = ar.selected_rows[0]
#             # raise PermissionError("20210811")
#             user = ar.get_user()
#             ar.goto_instance(user)


class SendWelcomeMail(dd.Action):
    label = _("Send welcome mail")
    if True:  # #1336
        show_in_toolbar = True
        show_in_workflow = False
    else:
        show_in_toolbar = False
        show_in_workflow = True
    button_text = "\u2709"  # ✉
    select_rows = True
    # required_roles = dd.login_required()

    # required_roles = dd.login_required(SiteAdmin)

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if user != obj and not user.user_type.has_required_roles([SiteAdmin]):
            # print(f"20250712 {user} != {obj}")
            return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        assert len(ar.selected_rows) == 1
        obj = ar.selected_rows[0]

        if not obj.is_verified():
            obj.must_verify()
            obj.full_clean()
            obj.save()

        if not obj.email:
            ar.error(_("Cannot verify without email address"), alert=True)
            return

        recipients = ["{} <{}>".format(obj.get_full_name(), obj.email)]

        def ok(ar):
            send_welcome_email(ar, obj, recipients)

            msg = _("Welcome mail has been sent to {}.").format(", ".join(recipients))
            ar.success(msg, alert=True)

        msg = _("Send welcome mail to {} ?").format(", ".join(recipients))
        return ar.confirm(ok, msg)


class ChangePassword(dd.Action):
    # button_text = u"\u205C"  # DOTTED CROSS (⁜)
    # button_text = u"\u2042"  # ASTERISM (⁂)
    button_text = "\u2731"  # 'HEAVY ASTERISK' (✱)
    # icon_name = "disk"
    label = _("Change password")

    parameters = dict(
        current=dd.PasswordField(_("Current password"), blank=True),
        new1=dd.PasswordField(_("New password"), blank=True),
        new2=dd.PasswordField(_("New password again"), blank=True),
    )
    params_layout = """
    current
    new1
    new2
    """

    def run_from_ui(self, ar, **kw):
        user = ar.get_user()
        pv = ar.action_param_values
        if pv.new1 != pv.new2:
            ar.error("New passwords didn't match!")
            return
        done_for = []
        validate_password(pv.new1, user=user)
        for obj in ar.selected_rows:
            if (
                user.user_type.has_required_roles([SiteAdmin])
                or not obj.has_usable_password()
                or obj.check_password(pv.current)
            ):
                obj.set_password(pv.new1)
                obj.full_clean()
                obj.save()
                done_for.append(obj)
            else:
                ar.debug("Incorrect current password for %s." % obj)

        # if ar.request is not None:
        #     auth.login(ar.request, obj)
        if len(done_for) and user.id in [user.id for user in done_for]:
            for u in done_for:
                if user.id == u.id:
                    user = u
                    break
            user = auth.authenticate(
                ar.request, username=user.username, password=pv.new1
            )
            auth.login(ar.request, user)
            # ar.set_response(goto_url=ar.renderer.front_end.build_plain_url())
        done_for = [str(obj) for obj in done_for]
        msg = _("New password has been set for {}.").format(", ".join(done_for))
        ar.success(msg, alert=True)


class ResetPassword(dd.Action):
    # button_text = u"\u205C"  # DOTTED CROSS (⁜)
    # button_text = u"\u2042"  # ASTERISM (⁂)
    # button_text = "\u2731"  # 'HEAVY ASTERISK' (✱)
    # icon_name = "disk"
    label = _("Reset password")
    select_rows = False
    http_method = "POST"

    parameters = dict(
        email=models.EmailField(_("e-mail address")),
        username=dd.CharField(_("Username (optional)"), blank=True),
        new1=dd.PasswordField(_("New password"), blank=True),
        new2=dd.PasswordField(_("New password again"), blank=True),
    )

    params_layout = """
    email
    username
    new1
    new2
    """

    def run_from_ui(self, ar, **kw):
        user = ar.get_user()
        pv = ar.action_param_values
        if pv.new1 != pv.new2:
            ar.error("New passwords didn't match!")
            return
        candidates = []
        flt = dict(email=pv.email)
        if pv.username:
            flt.update(username=pv.username)
        for obj in rt.models.users.User.objects.filter(**flt):
            if not obj.is_active:
                continue
            candidates.append(obj)

        if len(candidates) == 0:
            ar.error(_("No active users having {}").format(flt))
            return

        if len(candidates) > 1:
            ar.error(_("More than one active users having {}").format(flt))
            return

        obj = candidates[0]
        recipients = ["{} <{}>".format(obj.get_full_name(), obj.email)]

        def ok(ar):
            obj.verification_password = pv.new1
            obj.must_verify()
            obj.full_clean()
            obj.save()
            send_welcome_email(ar, obj, recipients)
            msg = _("Verification link has been sent to {}.").format(
                ", ".join(recipients)
            )
            ar.success(msg, alert=True)

        msg = _("Send verification link to {} ?").format(", ".join(recipients))
        return ar.confirm(ok, msg)


class SignOut(dd.Action):
    label = _("Sign out")
    select_rows = False
    default_format = "ajax"
    show_in_toolbar = False

    def run_from_ui(self, ar, **kw):
        # print(20170921, ar.request)
        user = ar.get_user()
        auth.logout(ar.request)
        ar.success(
            _("User {} logged out.").format(user),
            goto_url=ar.renderer.front_end.build_plain_url(),
        )


# from lino.core.fields import DisplayField, DummyField

# class SocialAuthField(DisplayField):

#     def value_from_object(self, obj, ar=None):
#         elems = []
#         elems.append(E.a("foo"))
#         return E.p(elems)

# def social_auth_field():
#     if settings.SITE.social_auth_backends:
#         return SocialAuthField()
#     return DummyField()


def count_active_sessions(request):
    qs = rt.models.sessions.Session.objects.filter(expire_date__gt=dd.now())
    if request.session.session_key:
        qs = qs.exclude(session_key=request.session.session_key)
    return qs.count()


def validate_sessions_limit(request):
    if (asl := dd.plugins.users.active_sessions_limit) == -1:
        return
    if count_active_sessions(request) >= asl:
        m = _("There are more than {} active user sessions.")
        m += " " + _("Please try again later.")
        raise Warning(m.format(asl))


def get_social_auth_links_func(content_header, flex_row, ar=None):
    def text_fn(*args):
        elems = [
            E.div(
                E.hr(style="width: -moz-available; margin-right: 1ch;"),
                E.span(content_header, style="white-space: nowrap;"),
                E.hr(style="width: -moz-available; margin-left: 1ch;"),
                style="display: flex;",
            )
        ]
        elems.append(E.br())
        links = []
        linked = set()
        if ar is not None:
            user = ar.get_user()
            if not user.is_anonymous:
                for sauth in user.social_auth.all():
                    linked.add(sauth.provider)
        style = (
            "padding:1ch;margin:2px;border:2px solid gray;border-radius:6px;"
        )
        for name, href in settings.SITE.get_social_auth_links(chunks=True):
            if name in linked:
                continue
            anchor = E.a(E.span(" " + name, CLASS="pi pi-" + name), href=href)
            if flex_row:
                el = E.div(anchor, style=style)
            else:
                el = E.span(anchor, style=style)
            links.append(el)
        anchor = E.a(E.span(gettext("Smart ID")), href="/auth/smart_id")
        if flex_row:
            links.append(E.div(anchor, style=style))
        else:
            links.append(E.span(anchor, style=style))
        elems.append(E.div(*links, style="text-align: center;"))
        return tostring(E.div(*elems))

    return text_fn


class SignIn(dd.Action):
    label = _("Sign in")
    select_rows = False
    parameters = dict(
        username=dd.CharField(_("Username")),
        password=dd.PasswordField(_("Password"), blank=True),
        social_auth_links=dd.Constant(
            get_social_auth_links_func(gettext("Or sign in with"), flex_row=True)
        ),
    )
    if not dd.get_plugin_setting("users", "third_party_authentication"):
        parameters["social_auth_links"] = dd.DummyField()

    params_layout = dd.Panel(
        """
        login_panel:50 social_auth_links:50
        """,  # label_align=layouts.LABEL_ALIGN_LEFT, window_size=(50, 9),
        login_panel="""
        username
        password
        """,
    )

    http_method = "POST"

    # show_in_toolbar = False

    def run_from_ui(self, ar, **kw):
        # ipdict = dd.plugins.ipdict
        # print("20210212 SignIn.run_from_ui()", ipdict.ip_records)
        validate_sessions_limit(ar.request)
        pv = ar.action_param_values
        # ar.subst_user = ar.request.subst_user = None
        user = auth.authenticate(ar.request, username=pv.username, password=pv.password)
        if user is None:
            ar.error(_("Failed to sign in as {}.".format(pv.username)))
        else:
            # user.is_authenticated:
            auth.login(ar.request, user)
            # gurl = ar.renderer.front_end.build_plain_url()
            ar.success(
                _("Now signed in as {}").format(user), close_window=True,
            )
            ar.set_response(goto_url="/")


class ConnectAccount(dd.Action):
    label = _("Connect account")

    def run_from_ui(self, ar, **kw):
        cb = ar.add_callback(
            get_social_auth_links_func(
                gettext("Connect account"), flex_row=False, ar=ar
            )()
        )
        cb.add_choice("cancel", lambda x: None, gettext("Cancel"))
        cb.set_title(gettext("Connect account"))
        ar.set_callback(cb)


class SignInWithSocialAuth(SignIn):
    params_layout = dd.Panel(
        """
    social_auth_links
    """
    )
