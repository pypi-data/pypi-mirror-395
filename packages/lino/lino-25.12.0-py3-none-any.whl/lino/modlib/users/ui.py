# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Documentation: :doc:`/specs/users` and :doc:`/dev/users`

from lino.core.site import has_socialauth
from datetime import datetime
from textwrap import wrap
from importlib import import_module
from lino.utils.html import E, tostring

from django.contrib.humanize.templatetags.humanize import naturaltime
# from django.utils import timezone
from django.utils.html import mark_safe
from django.conf import settings
from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _
from lino.core import actions
from lino.core.roles import SiteAdmin, SiteUser, UserRole
from lino.core.utils import djangoname
from lino.core.auth import SESSION_KEY

from .choicelists import UserTypes
# from .actions import SendWelcomeMail
# from .actions import SendWelcomeMail, SignInWithSocialAuth


def mywrap(t, ls=80):
    t = "\n".join([ln.strip() for ln in t.splitlines() if ln.strip()])
    return "\n".join(wrap(t, ls))


def format_timestamp(dt):
    if dt is None:
        return ""
    return "{} {} ({})".format(
        dt.strftime(settings.SITE.date_format_strftime),
        dt.strftime(settings.SITE.time_format_strftime),
        naturaltime(dt),
    )


class UserDetail(dd.DetailLayout):
    box1 = """
    username user_type:20
    first_name last_name
    email status
    time_zone
    """
    box2 = """
    id language
    initials nickname
    person company
    created modified
    """

    main = """
    box1 box2 #MembershipsByUser:20 remarks
    AuthoritiesGiven:20 AuthoritiesTaken:20 SocialAuthsByUser:30
    """

    # main_m = """
    # username
    # user_type
    # partner
    # first_name last_name
    # initials
    # email language time_zone
    # id created modified
    # remarks
    # AuthoritiesGiven
    # """


class UserInsertLayout(dd.InsertLayout):
    window_size = (60, "auto")

    main = """
    username email
    first_name last_name
    partner
    language user_type
    """


class Users(dd.Table):
    # ~ debug_actions  = True
    model = "users.User"
    # ~ order_by = "last_name first_name".split()
    order_by = ["username"]
    active_fields = "partner"
    abstract = True
    required_roles = dd.login_required(SiteAdmin)

    parameters = dict(show_active=dd.YesNo.field(_("Active"), blank=True))

    params_layout = "user_type show_active start_date end_date"

    # simple_parameters = ["user_type"]

    # ~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = "username user_type first_name last_name *"
    detail_layout = "users.UserDetail"
    insert_layout = UserInsertLayout()
    # column_names_m = 'mobile_item *'

    @classmethod
    def render_list_item(cls, obj, ar):
        return "<p>{}</p>".format(obj.username)

    # ~ @classmethod
    # ~ def get_row_permission(cls,action,user,obj):
    # ~ """
    # ~ Only system managers may edit other users.
    # ~ See also :meth:`User.disabled_fields`.
    # ~ """
    # ~ if not super(Users,cls).get_row_permission(action,user,obj):
    # ~ return False
    # ~ if user.level >= UserLevel.manager: return True
    # ~ if action.readonly: return True
    # ~ if user is not None and user == obj: return True
    # ~ return False


class AllUsers(Users):
    # send_welcome_email = SendWelcomeMail()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        if (pv := ar.param_values) is None:
            return qs
        if pv.show_active == dd.YesNo.no:
            qs = qs.filter(Q(username__isnull=True) | Q(user_type=''))
        elif pv.show_active == dd.YesNo.yes:
            qs = qs.exclude(Q(username__isnull=True) | Q(user_type=''))
        return qs


class UsersOverview(Users):
    required_roles = set([])
    column_names = "username user_type language"
    exclude = models.Q(user_type="")
    # abstract = not settings.SITE.is_demo_site
    detail_layout = None

    @classmethod
    def get_request_queryset(self, ar, **filter):
        for obj in super().get_request_queryset(ar, **filter):
            if obj.is_active:
                yield obj

    @classmethod
    def row_as_paragraph(cls, ar, self):
        pv = dict(username=self.username)
        if settings.SITE.is_demo_site:
            pv.update(password=dd.plugins.users.demo_password)
        btn = rt.models.about.About.get_action_by_name("sign_in")
        # print btn.get_row_permission(ar, None, None)
        btn = btn.create_request(
            action_param_values=pv, renderer=settings.SITE.kernel.default_renderer
        )
        btn = btn.ar2button(label=self.username)
        items = [tostring(btn), " : ", str(self), ", ", str(self.user_type)]
        if self.language:
            items += [
                ", ",
                "<strong>{}</strong>".format(
                    settings.SITE.LANGUAGE_DICT.get(self.language)
                ),
            ]
        return mark_safe("".join(items))

        # if settings.SITE.is_demo_site:
        #     p = "'{0}', '{1}'".format(self.username, '1234')
        # else:
        #     p = "'{0}'".format(self.username)
        # url = "javascript:Lino.show_login_window(null, {0})".format(p)
        # return E.li(E.a(self.username, href=url), ' : ',
        #             str(self), ', ',
        #             str(self.user_type), ', ',
        #             E.strong(settings.SITE.LANGUAGE_DICT.get(self.language)))


class Me(Users):
    label = _("My settings")
    help_text = _("Edit your user preferences.")
    required_roles = dd.login_required()
    default_record_id = "myself"

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        if obj == ar.get_user():
            return True
        # return super().get_row_permission(obj, ar, state, ba)
        return False

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        return ar.get_user()


# class MySettings(Users):
#     # use_as_default_table = False
#     # hide_top_toolbar = True
#     hide_navigator = True
#     required_roles = dd.login_required()
#     allow_create = False
#     allow_delete = False
#     default_list_action_name = 'detail'
#
#     @classmethod
#     def get_default_action(cls):
#         return cls.detail_action


class Authorities(dd.Table):
    required_roles = dd.login_required(SiteAdmin)
    model = "users.Authority"


class AuthoritiesGiven(Authorities):
    required_roles = dd.login_required()
    master_key = "user"
    label = _("Authorities given")
    column_names = "authorized"
    auto_fit_column_widths = True
    details_of_master_template = _("%(details)s by %(master)s")


class AuthoritiesTaken(Authorities):
    required_roles = dd.login_required()
    master_key = "authorized"
    label = _("Authorities taken")
    column_names = "user"
    auto_fit_column_widths = True
    details_of_master_template = _("%(details)s by %(master)s")


if has_socialauth and dd.get_plugin_setting("users", "third_party_authentication"):
    import social_django

    class SocialAuths(dd.Table):
        label = _("Third-party authorizations")
        required_roles = dd.login_required(SiteAdmin)
        model = "social_django.UserSocialAuth"

    class SocialAuthsByUser(SocialAuths):
        required_roles = dd.login_required(SiteUser)
        master_key = "user"

else:

    class SocialAuthsByUser(dd.Dummy):
        pass


class UserRoles(dd.VirtualTable):
    label = _("User roles")
    required_roles = dd.login_required(SiteAdmin)

    @classmethod
    def get_data_rows(self, ar):
        user_roles = set()
        utm = settings.SITE.user_types_module
        if utm:
            m = import_module(utm)
            for k in dir(m):
                v = getattr(m, k)
                if not v is UserRole:
                    if isinstance(v, type) and issubclass(v, UserRole):
                        user_roles.add(v)
        # for ut in UserTypes.get_list_items():
        #     user_roles.remove(ut.role.__class__)
        return sorted(user_roles, key=djangoname)

    @dd.displayfield(_("Name"))
    def name(self, obj, ar):
        return djangoname(obj)

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        return mywrap(obj.__doc__ or "", 40)

    @classmethod
    def setup_columns(cls):
        def w(ut):
            def func(fld, obj, ar):
                if isinstance(ut.role, obj):
                    return "☑"
                return ""

            return func

        names = []
        for ut in UserTypes.get_list_items():
            name = "ut" + ut.value
            # vf = dd.VirtualField(
            #     models.BooleanField(str(ut.value)), w(ut))
            vf = dd.VirtualField(dd.DisplayField(str(ut.value)), w(ut))
            cls.add_virtual_field(name, vf)
            names.append(name + ":3")
        # cls.column_names = "name:20 description:40 " + ' '.join(names)
        cls.column_names = "name:20 " + " ".join(names)


class KillSession(actions.Action):
    label = _("Kill")
    custom_handler = True
    readonly = False
    show_in_toolbar = False
    show_in_workflow = True

    def get_action_permission(self, ar, obj, state):
        if not super(KillSession, self).get_action_permission(ar, obj, state):
            return False
        # print("20210117", ar.request.session.session_key, obj.session_key)
        if ar.request.session.session_key == obj.session_key:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # print("20210117", ar.request.session.session_key, obj.session_key)
        assert ar.request.session.session_key != obj.session_key
        msg = _("Session {} has been deleted.").format(obj)
        obj.delete()
        kw = dict()
        kw.update(refresh_all=True)
        kw.update(message=msg)
        ar.success(**kw)


class Sessions(dd.Table):
    model = "sessions.Session"
    label = _("User sessions")
    required_roles = dd.login_required(dd.SiteAdmin)
    # column_names = "last_request:30 ip_address:12 login_failures:5 blacklisted_since:12 username:20 last_login:30"
    column_names = "last_activity:30 last_ip_addr:12 username:12 session_key:20 expire_date workflow_buttons"
    window_size = (90, 12)
    kill_session = KillSession()

    @classmethod
    def get_data_rows(cls, ar):
        # qs = cls.model.objects.filter(expire_date__gt=timezone.now())
        qs = cls.model.objects.all()
        lst = []
        for ses in qs:
            row = cls.session_to_row(ses)
            if row is not None:
                # ses.session_key, ses.expire_date, data)
                lst.append(row)
        # print("20231004", ar.order_by)
        # if type(ar.order_by) == list:
        #     order_by
        if ar.order_by is None:
            order_by = ['-last_activity']
        else:
            order_by = ar.order_by  # or '-last_activity'
        for fldname in order_by:
            if fldname.startswith("-"):
                reverse = True
                fldname = fldname[1:]
            else:
                reverse = False
            sk = cls.get_data_elem(fldname)
            # print("20231004", order_by, sk)
            if sk is None:
                dd.logger.debug(
                    "users.Sessions got invalid order_by spec %s", fldname)
                continue
            lst.sort(key=sk.value_from_object)
            # if order_by == 'last_activity':
            #     lst.sort(key=lambda ses:ses.last_activity)
            # elif order_by == 'username':
            #     lst.sort(key=lambda ses:ses.username)
            if reverse:
                lst.reverse()
        return lst

    @classmethod
    def session_to_row(cls, ses):
        data = ses.get_decoded()
        ses.data = data
        la = data.get("last_activity", None)
        if la is None:
            la = settings.SITE.startup_time
        else:
            la = datetime.strptime(la, "%Y-%m-%dT%H:%M:%S.%f")
        ses.last_activity = la
        # user = users.User.objects.get(pk=data[SESSION_KEY])
        user_id = data.get(SESSION_KEY, None)
        if user_id is None:
            ses.user = None
        else:
            u = rt.models.users.User.objects.get(pk=user_id)
            ses.user = u
        return ses

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        ses = cls.model.objects.get(pk=pk)
        return cls.session_to_row(ses)

    @dd.displayfield(_("session key"), sortable_by=["session_key"])
    def session_key(self, obj, ar):
        # ses = obj[2]
        return obj.session_key

    # @dd.displayfield(_("Blacklisted since"))
    # def blacklisted_since(self, obj, ar):
    #     return format_timestamp(obj.blacklisted_since)

    # @dd.displayfield(_("Login failures"))
    # def login_failures(self, obj, ar):
    #     return obj.login_failures

    @dd.displayfield(_("Username"), sortable_by=["username"])
    def username(self, obj, ar):
        # u = obj[1]
        if obj.user is None:
            return "(none)"
        return obj.user.username

    @dd.displayfield(_("Last activity"), sortable_by=["last_activity"])
    def last_activity(self, obj, ar):
        return format_timestamp(obj.last_activity)

    @dd.displayfield(_("IP address"), sortable_by=["last_ip_addr"])
    def last_ip_addr(self, obj, ar):
        return obj.data.get("last_ip_addr") or "?.?.?.?"

    # @dd.displayfield(_("Device type"))
    # def device_type(self, obj, ar):
    #     return obj[3].get('device_type', '')

    @dd.displayfield(_("Expires"), sortable_by=["expire_date"])
    def expire_date(self, obj, ar):
        return format_timestamp(obj.expire_date)

    # @dd.displayfield(_("Last login"))
    # def last_login(self, obj, ar):
    #     return format_timestamp(obj.last_login)


# from lino.modlib.publisher.choicelists import PublisherViews
# PublisherViews.add_item_lazy("u", Users)
