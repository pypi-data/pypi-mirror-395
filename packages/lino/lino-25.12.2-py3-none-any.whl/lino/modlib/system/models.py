# -*- coding: UTF-8 -*-
# Copyright 2009-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.report import EmptyTable
from lino.core.signals import testcase_setup
from django.test.signals import setting_changed
from .mixins import Lockable
from .choicelists import (
    YesNo,
    Genders,
    PeriodEvents,
    DurationUnits,
    Recurrences,
    Weekdays,
    DisplayColors
)
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.printing.choicelists import BuildMethods
# from lino.core.actors import resolve_action
from lino.core.roles import SiteStaff
from lino.core.utils import is_devserver
from lino.core.utils import full_model_name
from lino.core import actions
from lino.api import dd, rt
from lino.utils.html import E
from django.conf import settings
from django.utils.encoding import force_str

from django.db import models
from django.db.utils import DatabaseError
from django.utils.translation import gettext_lazy as _

from django.apps import apps

get_models = apps.get_models


# import them here to have them on rt.models.system:


class BuildSiteCache(dd.Action):
    label = _("Rebuild site cache")
    url_action_name = "buildjs"

    def run_from_ui(self, ar):
        settings.SITE.build_site_cache(force=True)
        return ar.success(
            """\
Seems that it worked. Refresh your browser.
<br>
Note that other users might experience side effects because
of the unexpected .js update, but there are no known problems so far.
Please report any anomalies.""",
            alert=_("Success"),
            clear_site_cache=True,
        )


if False:

    class SiteConfigManager(models.Manager):
        def get(self, *args, **kwargs):
            return settings.SITE.site_config


class SiteConfig(dd.Model):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, "SiteConfig")
        verbose_name = _("Site configuration")

    config_id = 1
    """
    The primary key of the one and only :class:`SiteConfig
    <lino.modlib.system.SiteConfig>` instance of this
    :class:`Site`. Default value is 1.

    This is Lino's equivalent of Django's :setting:`SITE_ID` setting.
    Lino applications don't need ``django.contrib.sites`` (`The
    "sites" framework
    <https://docs.djangoproject.com/en/5.2/ref/contrib/sites/>`_)
    because an analog functionality is provided by
    :mod:`lino.modlib.system`.
    """

    if False:
        objects = SiteConfigManager()
        real_objects = models.Manager()

    default_build_method = BuildMethods.field(
        verbose_name=_("Default build method"), blank=True, null=True
    )

    simulate_today = models.DateField(
        _("Simulated date"), blank=True, null=True)

    _site_config = None

    @classmethod
    def clear_site_config(cls):
        cls._site_config = None

    @classmethod
    def get_site_config(cls):
        site = settings.SITE

        if not site._startup_done:
            site.logger.debug("site_config is None because startup not done")
            return None

        if cls._site_config is None:
            # ~ raise Exception(20130301)
            # ~ print '20130320 create _site_config'
            # ~ from lino.core.utils import resolve_model
            # from lino.core.utils import obj2str
            SiteConfig = cls
            try:
                cls._site_config = SiteConfig.objects.get(id=cls.config_id)
                # print("20180502 loaded SiteConfig {}",
                #       obj2str(self._site_config, True))
            except (SiteConfig.DoesNotExist, DatabaseError):
                # e.g. during migrate the SiteConfig maybe doesn't yet exist
                # except SiteConfig.DoesNotExist:
                # ~ except Exception,e:
                kw = dict(id=cls.config_id)
                # ~ kw.update(settings.SITE.site_config_defaults)
                kw.update(site.site_config_defaults)
                site_config = SiteConfig(**kw)
                site_config.full_clean()
                # site_config.save() 20220824 don't save it too quickly
                cls._site_config = site_config
                # print("20180502 Created SiteConfig {}".format(
                #     obj2str(self._site_config, True)))
                # 20120725
                # polls_tutorial menu selection `Config --> Site configuration`
                # said "SiteConfig 1 does not exist"
                # cannot save the instance here because the db table possibly doesn't yet exit.
                # ~ self._site_config.save()
            # cls._site_config.on_startup()
        return cls._site_config

    def __str__(self):
        return force_str(_("Site configuration"))

    def update(self, **kw):
        """
        Set some field of the SiteConfig object and store it to the
        database.
        """
        # print("20180502 update({})".format(kw))
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("SiteConfig has no attribute %r" % k)
            setattr(self, k, v)
        self.full_clean()
        self.save()

    # def update_from(self, other):
    #     cls = self.__class__
    #     kw = dict()
    #     for fld in cls._meta.concrete_fields:
    #         if fld.attname != "id":
    #             kw[fld.attname] = getattr(other, fld.attname)
    #     self.update(**kw)

    # def on_startup(self):
    #     # if not self.site_company:
    #     #     raise Exception("20230423")
    #     # if self.site_company:
    #     site = settings.SITE
    #     if (owner := site.get_plugin_setting('contacts', 'site_owner')) is not None:
    #         # print("20230423", self.site_company)
    #         site.copyright_name = str(owner)
    #         if owner.url:
    #             site.copyright_url = owner.url

    # def full_clean(self, *args, **kw):
    #     super().full_clean(*args, **kw)

    def save(self, *args, **kw):
        cls = self.__class__
        if cls._site_config is None:
            cls._site_config = self
        elif cls._site_config is not self:
            diffs = []
            for fld in cls._meta.concrete_fields:
                oldval = getattr(cls._site_config, fld.attname)
                newval = getattr(self, fld.attname)
                if oldval != newval:
                    diffs.append(
                        "{}: {} -> {}".format(fld.attname, oldval, newval))
            if len(diffs):
                print(
                    "20220824 Overriding SiteConfig instance (diffs={})".format(
                        diffs)
                )
            cls._site_config = self
            # cls._site_config.update_from(self)
            # return
        # print("20180502 save() {}".format(dd.obj2str(self, True)))
        super().save(*args, **kw)
        # settings.SITE.clear_site_config()

    @property
    def site_company(self):
        # Backwards compatibility after 20250617
        return settings.SITE.plugins.contacts.site_owner


def my_handler(sender, **kw):
    # print("20180502 {} my_handler calls clear_site_config()".format(
    #     settings.SITE))
    settings.SITE.clear_site_config()
    # ~ kw.update(sender=sender)
    # dd.database_connected.send(sender)
    # ~ dd.database_connected.send(sender,**kw)


setting_changed.connect(my_handler)
testcase_setup.connect(my_handler)
dd.connection_created.connect(my_handler)
models.signals.post_migrate.connect(my_handler)


class SiteConfigs(dd.Table):
    model = "system.SiteConfig"
    required_roles = dd.login_required(SiteStaff)
    hide_navigator = True
    allow_delete = False
    hide_top_toolbar = True

    detail_layout = dd.DetailLayout(
        """
    default_build_method
    simulate_today
    # lino.ModelsBySite
    """,
        window_size=(60, "auto"),
    )

    @classmethod
    def get_default_action(cls):
        return cls.detail_action

    do_build = BuildSiteCache()


class Dashboard(EmptyTable):
    # label = _("D")
    hide_navigator = True
    required_roles = set()
    allow_delete = False
    # detail_layout = """
    # welcome_messages
    # working.WorkedHours comments.RecentComments
    # tickets.MyTicketsToWork
    # notify.MyMessages
    # """

    @classmethod
    def get_default_action(cls):
        # raise Exception("20210530")
        # return None
        # return actions.ShowExtraDetail(None)
        # cls._bind_action("extra_"+name, a, False)
        ba = cls.get_action_by_name("extra_default")
        # assert ba is not None
        return ba

    @classmethod
    def get_detail_action(self, ar):
        u = ar.get_user()
        return cls.get_action_by_name("extra_default")

    @dd.htmlbox()
    def welcome_messages(cls, obj, ar=None):
        return settings.SITE.get_main_html(ar)
        # if ar.get_user().is_authenticated:
        #     return E.p(*settings.SITE.get_welcome_messages(ar))

    @classmethod
    def collect_extra_actions(cls):
        return settings.SITE.quicklinks.items
        # for ql in settings.SITE.quicklinks.items:
        #     yield ql.bound_action

        # for mi in settings.SITE.get_quicklinks(None).items:
        #     yield mi
        # for p in settings.SITE.sorted_plugins:
        #     for ql in p.get_quicklinks(None):
        #         yield ql
        #         # print(repr(ql))
        #         # ba = resolve_action(ql)
        #         # if ba is not None:
        #         #     yield ba


# if settings.SITE.user_model == 'users.User':
#     dd.inject_field(settings.SITE.user_model,
#                     'user_type', UserTypes.field())
#     dd.inject_field(settings.SITE.user_model, 'language', dd.LanguageField())

# @dd.receiver(dd.pre_analyze)
# def set_dashboard_actions(sender, **kw):
#     for p in settings.SITE.sorted_plugins:
#         for ql in p.get_quicklinks(None):
#             ba = resolve_action(ql)
#             Dashboard.define_action(ba.action.action_name=ba)

# for ql in settings.SITE.get_quicklinks()
# for m in get_checkable_models().keys():
#     if m is None:
#         continue
#     assert m is not Problem
#     m.define_action(check_data=UpdateMessagesByController(m))
#     m.define_action(fix_problems=FixMessagesByController(m))


class BleachChecker(Checker):
    verbose_name = _("Find unbleached html content")
    model = dd.Model

    def get_checkable_models(self):
        for m in super().get_checkable_models():
            if len(m._bleached_fields):
                yield m

    def get_checkdata_problems(self, ar, obj, fix=False):
        t = tuple(obj.fields_to_bleach(save=False))
        if len(t):
            fldnames = tuple([f.name for f, old, new in t])
            yield (True, _("Fields {} have unbleached content.").format(fldnames))
            if fix:
                # obj.before_ui_save(ar, None)
                obj.before_ui_save(None, None)
                obj.full_clean()
                obj.save()


BleachChecker.activate()
