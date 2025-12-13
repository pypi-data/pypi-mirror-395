# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from collections import OrderedDict

from django.db import models
from django.conf import settings
from django.utils import translation
from django.template.defaultfilters import pluralize

from lino import logger
from lino.core import constants
from lino.core.gfks import gfk2lookup
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.linod.choicelists import background_task
from lino.core.roles import SiteStaff
from lino.api import dd, rt, _

from .choicelists import Checker, Checkers
from .roles import CheckdataUser

MAX_LENGTH = 250
MORE = " (...)"


class CheckerAction(dd.Action):
    fix_them = False
    required_roles = dd.login_required(CheckdataUser)

    def run_it(self, ar, fix, checkers, objects):
        if fix is None:
            fix = self.fix_them
        Message = rt.models.checkdata.Message
        gfk = Message.owner
        for obj in objects:
            if checkers is None:
                checkers = get_checkers_for(obj.__class__)
            qs = Message.objects.filter(**gfk2lookup(gfk, obj))
            qs.delete()
            for chk in checkers:
                chk.update_problems(ar, obj, False, fix)
        ar.set_response(refresh=True)


class UpdateMessage(CheckerAction):
    icon_name = "bell"
    ui5_icon_name = "sap-icon://bell"
    label = _("Check data")
    combo_group = "checkdata"
    sort_index = 90
    # custom_handler = True
    # select_rows = False
    default_format = None

    def run_from_ui(self, ar, fix=None):
        if fix is None:
            fix = self.fix_them
        Message = rt.models.checkdata.Message
        # print(20150327, ar.selected_rows)
        for obj in ar.selected_rows:
            assert isinstance(obj, Message)
            chk = obj.checker
            owner = obj.owner
            if owner is None:
                # A problem where owner is None means that the owner
                # has been deleted.
                obj.delete()
            else:
                self.run_it(ar, fix, [chk], [owner])
                # qs = Message.objects.filter(
                #     **gfk2lookup(Message.owner, owner, checker=chk))
                # qs.delete()
                # chk.update_problems(ar, owner, False, fix)
        ar.set_response(refresh_all=True)


class FixProblem(UpdateMessage):
    label = _("Fix data problems")
    fix_them = True
    sort_index = 91


class UpdateMessagesByController(CheckerAction):
    icon_name = "bell"
    ui5_icon_name = "sap-icon://bell"
    label = _("Check data")
    combo_group = "checkdata"

    # def __init__(self, model=None, **kwargs):
    #     self.model = model
    #     super().__init__(**kwargs)

    def run_from_ui(self, ar, fix=None):
        self.run_it(ar, fix, None, ar.selected_rows)
        # if fix is None:
        #     fix = self.fix_them
        # Message = rt.models.checkdata.Message
        # gfk = Message.owner
        # checkers = get_checkers_for(self.model)
        # for obj in ar.selected_rows:
        #     assert isinstance(obj, self.model)
        #     qs = Message.objects.filter(**gfk2lookup(gfk, obj))
        #     qs.delete()
        #     for chk in checkers:
        #         chk.update_problems(ar, obj, False, fix)
        # ar.set_response(refresh=True)


class FixMessagesByController(UpdateMessagesByController):
    label = _("Fix data problems")
    fix_them = True


class QuickFixMessagesByController(UpdateMessagesByController):
    # label = _("Fix data problems")
    fix_them = True
    combo_group = None
    # icon_name = "lightning"
    icon_name = None
    button_text = ' ⚡ '  # 26A1
    # button_text = "✓"  # u"\u2713"


class FixAllProblems(CheckerAction):
    select_rows = False
    show_in_plain = True
    # http_method = "POST"
    label = _("Fix all data problems")
    button_text = "✓"  # u"\u2713"
    fix_them = True

    def run_from_ui(self, ar, fix=None):
        mi = ar.master_instance
        # print(f"20250307 {mi}")
        self.run_it(ar, fix, get_checkers_for(mi.__class__), [mi])
        ar.set_response(refresh=True)


class Message(Controllable, UserAuthored):
    class Meta:
        app_label = "checkdata"
        verbose_name = _("Data problem message")
        verbose_name_plural = _("Data problem messages")
        ordering = ["owner_type", "owner_id", "checker"]

    controller_is_optional = False
    allow_merge_action = False
    allow_cascaded_delete = "owner"

    # problem_type = ProblemTypes.field()
    checker = Checkers.field(verbose_name=_("Checker"))
    # severity = Severities.field()
    # feedback = Feedbacks.field(blank=True)
    message = models.CharField(_("Message text"), max_length=MAX_LENGTH)
    # fixable = models.BooleanField(_("Fixable"), default=False)

    update_problem = UpdateMessage()
    fix_problem = FixProblem()

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     fields.update(checker=Checkers.field(
    #         blank=True, help_text=_("Only problems by this checker.")))
    #     return fields

    def __str__(self):
        return self.message

    def full_clean(self):
        if len(self.message) > MAX_LENGTH:
            self.message = self.message[:MAX_LENGTH - len(MORE)] + MORE
        super().full_clean()

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Message, cls).get_simple_parameters():
            yield p
        yield "checker"


dd.update_field(Message, "user", verbose_name=_("Responsible"))
Message.set_widget_options("checker", width=10)
Message.set_widget_options("user", width=10)
Message.set_widget_options("message", width=50)
Message.update_controller_field(verbose_name=_("Database object"))


class Messages(dd.Table):
    required_roles = dd.login_required(CheckdataUser)
    model = "checkdata.Message"
    column_names = "user owner message #fixable checker *"
    auto_fit_column_widths = True
    editable = False
    cell_edit = False
    # parameters = dict(
    #     # user=models.ForeignKey(
    #     #     'users.User', blank=True, null=True,
    #     #     verbose_name=_("Responsible"),
    #     #     help_text=_("""Only problems for this responsible.""")),
    #     )
    params_layout = "user checker"

    # simple_parameters = ('user', 'checker')
    detail_layout = dd.DetailLayout(
        """
    checker
    owner
    message
    user id
    """,
        window_size=(70, "auto"),
    )


class AllMessages(Messages):
    """Show all data problem messages.

    This table can be opened by site managers using
    :menuselection:`Explorer --> System --> Data problem messages`.

    """

    required_roles = dd.login_required(SiteStaff)


class MessagesByOwner(Messages):
    """Show data problem messages related to this database object."""

    master_key = "owner"
    column_names = "message checker user #fixable *"
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    fix_all_problems = FixAllProblems()


# This was the first use case of a slave table with something else than a model
# instance as its master
class MessagesByChecker(Messages):
    """Show the data problem messages by checker."""

    master_key = "checker"
    column_names = "user owner message #fixable *"

    @classmethod
    def get_master_instance(cls, ar, model, pk):
        if not pk:
            return None
        return Checkers.get_by_value(pk)

    @classmethod
    def get_filter_kw(self, ar, **kw):
        kw.update(checker=ar.master_instance)
        return kw


class MyMessages(Messages):
    label = _("Data problem messages assigned to me")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyMessages, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        if not sar.get_permission():
            return
        count = sar.get_total_count()
        if count > 0:
            msg = _("There are {0} data problem messages assigned to you.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)


@dd.receiver(dd.pre_analyze)
def set_checkdata_actions(sender, **kw):
    for m in get_checkable_models().keys():
        if m is None:
            continue
        assert m is not Message
        # if hasattr(m, 'check_data'):
        if (label := getattr(m, 'quickfix_checkdata_label', None)):
            # print(f"20250324 Customized quickfix_checkdata_label {label} for {m}")
            m.define_action(quick_fix=QuickFixMessagesByController(label=label))
        else:
            # print(f"20250324 Default checkdata buttons for {m}")
            m.define_action(check_data=UpdateMessagesByController())
            m.define_action(fix_problems=FixMessagesByController())
        m.define_action(
            show_problems=dd.ShowSlaveTable(
                MessagesByOwner,
                label=_("Show data problems"),
                icon_name="bell",
                combo_group="checkdata",
            )
        )


def get_checkers_for(model):
    checkers = []
    for m, lst in get_checkable_models().items():
        if m is not None and issubclass(model, m):
            checkers += lst
    return checkers


def check_instance(ar, obj, **kwargs):
    for chk in get_checkers_for(obj.__class__):
        for fixable, msg in chk.check_instance(ar, obj, **kwargs):
            if fixable:
                msg = f"(\u2605) {msg}"
            print(msg)


def fix_instance(ar, obj, **kwargs):
    kwargs['fix'] = True
    for chk in get_checkers_for(obj.__class__):
        for fixable, msg in chk.check_instance(ar, obj, **kwargs):
            pass


def get_checkable_models(*args, only_auto=False):
    checkable_models = OrderedDict()
    for chk in Checkers.get_list_items():
        if only_auto and chk.no_auto:
            continue
        if len(args):
            skip = True
            for arg in args:
                if arg in chk.value:
                    skip = False
            if skip:
                continue
        for m in chk.get_checkable_models():
            lst = checkable_models.setdefault(m, [])
            lst.append(chk)
    return checkable_models


def check_data(ar, args=[], fix=True, prune=False):
    """Called by :manage:`checkdata`. See there."""
    # verbosity 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
    Message = rt.models.checkdata.Message
    # raise Exception("20231230")
    mc = get_checkable_models(*args, only_auto=True)
    if len(mc) == 0 and len(args) > 0:
        raise Exception("No checker matches {0}".format(args))
    if prune:
        qs = Message.objects.all()
        msg = "Prune {} existing messages...".format(qs.count())
        ar.logger.info(msg)
        qs.delete()

    final_sums = [0, 0, 0]
    with translation.override("en"):
        for m, checkers in mc.items():
            if m is None:
                qs = Message.objects.filter(
                    **gfk2lookup(Message.owner, None, checker__in=checkers)
                )
                qs.delete()
                qs = [None]
                name = "unbound data"
                msg = "Run {0} checkers on {1}...".format(len(checkers), name)
            else:
                assert not m._meta.abstract
                if settings.SITE.is_hidden_plugin(m._meta.app_label):
                    continue
                ct = rt.models.contenttypes.ContentType.objects.get_for_model(
                    m)
                qs = Message.objects.filter(
                    owner_type=ct, checker__in=checkers)
                qs.delete()
                name = str(m._meta.verbose_name_plural)
                qs = m.objects.all()
                msg = "Run {0} data checkers on {1} {2}...".format(
                    len(checkers), qs.count(), name
                )
            # 20230531 : Process freezed here:
            # Started manage.py checkdata -f (using lino_local.prod.settings) --> PID 3886758
            # Found 26 and fixed 0 problems in Clients.
            # We had no idea whether the connection was broken or it was still running.
            # To avoid this, we would have had to say "export LINO_LOGLEVEL=DEBUG".
            # 20230807 Now we use verbosity to decide whether to show it or not
            # and the daily background task sets verbosity to 0.
            # 20231012 verbosity would become a way to change the loglevel
            ar.logger.info(msg)
            # else:
            #     dd.logger.debug(msg)
            sums = [0, 0, name]
            for obj in qs:
                for chk in checkers:
                    todo, done = chk.update_problems(ar, obj, False, fix)
                    sums[0] += len(todo)
                    sums[1] += len(done)
            if sums[0] or sums[1]:
                # msg = "Fixed {1} problems and created {0} messages in {2}."
                msg = "Found {0} and fixed {1} problems in {2}."
                ar.logger.info(msg.format(*sums))
            else:
                ar.logger.debug("No data problems found in {0}.".format(name))
            final_sums[0] += 1
            final_sums[1] += sums[0]
            final_sums[2] += sums[1]
    # msg = "Done %d %s, fixed %d problems and created %d messages."
    msg = "%d %s have been run. Found %d and fixed %d problems."
    done, found, fixed = final_sums
    what = pluralize(done, "check,checks")
    ar.logger.info(msg, done, what, found, fixed)


@background_task(every_unit="daily", every=1, run_after='generate_calendar_entries')
def checkdata(ar):
    """Run all data checkers."""
    check_data(ar, fix=dd.plugins.checkdata.fix_in_background)
    # rt.login().run(settings.SITE.site_config.run_checkdata)
