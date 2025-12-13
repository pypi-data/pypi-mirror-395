# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from dateutil.rrule import rrule

try:
    from num2words import num2words
except ImportError:
    # ignore silently to avoid test failures when it is not installed
    # print("num2words not installed, use `python manage.py install` to install")
    pass  # run `manage.py install` to install it

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.encoding import force_str
from django.utils.translation import gettext, ngettext

from lino import logger
from lino.api import dd, _, rt
from lino.core import constants
from lino.core.utils import resolve_fields_list, models_by_base
from lino.utils import ONE_DAY
from lino.mixins.periods import Started, Ended

from .actions import EditRow, AbortEdit
from .choicelists import Recurrences, Weekdays


def format_time(t):
    if t is None:
        return ""
    return t.strftime(settings.SITE.time_format_strftime)


class EditSafe(dd.Model):
    """
    Ensure data integrity by calling :meth:`before_ui_edit` and :meth:`on_ui_abort`.
    """

    class Meta:
        abstract = True

    edit_row = EditRow()
    abort_edit = AbortEdit()

    def editing_mode(self, ar):
        return False

    def before_ui_edit(self, ar, **kwargs):
        """
        Called from :class:`EditRow<lino.core.actions.EditRow>` when a user hits the edit button.
        """
        raise NotImplementedError

    def on_ui_abort(self, ar, **kwargs):
        """
        Called from :class:`AbortEdit<lino.core.actions.AbortEdit>` when a user hits the
        abort button to discard changes in an editing window.
        """
        raise NotImplementedError

    def save_existing_instance(self, ar):
        super().save_existing_instance(ar)
        ar.set_response(editing_mode=False)

    def disabled_fields(self, ar):
        """
        Take a set and add either "edit_row" or (x-or) "abort_edit" to the set and return it.

        PS> Must define the logic to alternate between the actions `EditRow` and `AbortEdit`.
        """
        raise NotImplementedError


class Lockable(EditSafe):
    lockable_fields = None

    locked_by = dd.ForeignKey(
        rt.settings.SITE.user_model,
        verbose_name=_("Locked by"),
        null=True,
        default=None,
        blank=True,
        on_delete=dd.SET_NULL,
    )

    class Meta(object):
        abstract = True

    @staticmethod
    def get_lockables():
        return models_by_base(Lockable)

    @staticmethod
    def get_lockable_rows(user):
        for m in Lockable.get_lockables():
            for row in m.objects.filter(locked_by=user):
                yield row

    @classmethod
    def on_analyze(cls, site):
        super().on_analyze(site)
        if cls.lockable_fields is None:
            cls.lockable_fields = cls._meta.get_fields()
        else:
            resolve_fields_list(cls, "lockable_fields")
        cls.lockable_fields = set([f.name for f in cls.lockable_fields])

    def before_ui_edit(self, ar, **kwargs):
        self.lock_row(ar)
        ar.success(refresh=True)

    def lock_row(self, ar):
        user = ar.get_user()
        if self.locked_by_id is not None:
            # msg = _("{} is being edited by another user. " "Please try again later.")
            # msg = _("{row} is being edited by {user}. Please try again later.")
            msg = _("{row} is being edited by {user}.")
            msg += " " + _("Please try again later.")
            raise Warning(msg.format(row=self, user=self.locked_by))
        for obj in self.get_lockable_rows(user):
            obj.unlock_row(ar)
        self.locked_by = user
        self.save()
        rt.settings.SITE.logger.debug(
            "%s locks %s.%s" % (user, self.__class__, self.pk)
        )
        self._disabled_fields = None  # clear cache

    def on_ui_abort(self, ar, **kwargs):
        self.unlock_row(ar)
        ar.success(refresh=True)

    def unlock_row(self, ar):
        user = ar.get_user()

        if self.locked_by == user:
            rt.settings.SITE.logger.debug(
                "%s releases lock on %s.%s", user, self.__class__, self.pk
            )
            self.locked_by = None
            self.save()
            self._disabled_fields = None  # clear cache

        elif self.locked_by is None:
            # silently ignore a request to unlock a row if it wasn't
            # locked.  This can happen e.g. when user click Save on a
            # row that wasn't locked.
            rt.settings.SITE.logger.debug(
                "%s cannot unlock %s.%s because it was not locked",
                self.user,
                self.__class__,
                self.pk,
            )
            return

        else:
            # locked by another user.
            # Should we inlcude a better message?
            rt.settings.SITE.logger.debug(
                "%s cannot unlock %s.%s because it was locked by %s",
                self.user,
                self.__class__,
                self.pk,
                self.locked_by,
            )
            return

    def has_row_lock(self, ar=None, user=""):
        user = user if user else ar.get_user()
        return self.locked_by == user

    #
    # def after_ui_save(self, ar, cw):
    #     self.unlock_row(ar)
    #     super(Lockable, self).after_ui_save(ar, cw)

    def save_existing_instance(self, ar):
        # this is called from both SubmitDetail and SaveGridCell
        if not self.has_row_lock(ar):
            self.lock_row(ar)
        super().save_existing_instance(ar)
        self.unlock_row(ar)

    def disabled_fields(self, ar):
        df = set()
        df.add("locked_by")
        if self.pk is None or self.has_row_lock(ar):
            df.add("edit_row")
        else:
            df.add("abort_edit")
            if ar.bound_action.action.window_type != constants.WINDOW_TYPE_TABLE:
                df |= self.lockable_fields
                df.add("submit_detail")

        # dd.logger.info("20181008 lockable_fields %s", self.lockable_fields)
        return df


POSITION_TEXTS = {
    "1": _("first"),
    "-1": _("last"),
    "2": _("second"),
    "-2": _("second last"),
    "3": _("third"),
    "-3": _("third last"),
    "4": _("fourth"),
    "-4": _("fourth last"),
}


class RecurrenceSet(Started, Ended):
    class Meta:
        abstract = True

    every_unit = Recurrences.field(blank=True)  # default='monthly'
    every = models.IntegerField(_("Repeat every"), default=1)
    positions = models.CharField(_("Positions"), blank=True, max_length=50)
    # positioning_type = PositioningTypes.field(blank=True, null=True)

    monday = models.BooleanField(Weekdays.monday.text, default=False)
    tuesday = models.BooleanField(Weekdays.tuesday.text, default=False)
    wednesday = models.BooleanField(Weekdays.wednesday.text, default=False)
    thursday = models.BooleanField(Weekdays.thursday.text, default=False)
    friday = models.BooleanField(Weekdays.friday.text, default=False)
    saturday = models.BooleanField(Weekdays.saturday.text, default=False)
    sunday = models.BooleanField(Weekdays.sunday.text, default=False)

    max_events = models.PositiveIntegerField(
        _("Number of events"), blank=True, null=True
    )

    def build_rrule(self) -> str:
        rule = f"FREQ={self.every_unit.name.upper()};INTERVAL={self.every}"
        if self.end_date:
            rule += f";UNTIL={self.get_datetime('end').isoformat()}"
        elif self.max_events:
            rule += f";COUNT={self.max_events}"
        # for r in self.recur_by_rules.all():
        #     rule += f";{r.recurby.name.name.upper()}={r.positions}"
        return rule

    @classmethod
    def on_analyze(cls, site):
        cls.WEEKDAY_FIELDS = dd.fields_list(
            cls, "monday tuesday wednesday thursday friday saturday sunday"
        )
        super().on_analyze(site)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        for f in cls.WEEKDAY_FIELDS:
            yield f
        yield "every"
        yield "every_unit"
        yield "max_events"
        # ~ yield 'event_type'
        yield "start_date"
        yield "end_date"
        yield "start_time"
        yield "end_time"

    def full_clean(self, *args, **kwargs):
        if self.every_unit == Recurrences.per_weekday:
            self.every_unit = Recurrences.weekly
        # elif self.every_unit == Recurrences.once:
        #     self.max_events = 1
        #     self.positions = ''
        #     self.every = 0
        super().full_clean(*args, **kwargs)
        # if self.positions:
        #     if self.every != 1:
        #         raise ValidationError(
        #             "Cannot specify positions together with repeat value!")

    def disabled_fields(self, ar):
        rv = super().disabled_fields(ar)
        if self.every_unit == Recurrences.once:
            rv.add("max_events")
            rv.add("every")
        # if self.every_unit != Recurrences.per_weekday:
        # rv |= self.WEEKDAY_FIELDS
        return rv

    @dd.displayfield(_("Description"))
    def what_text(self, ar):
        return str(self)

    @dd.displayfield(_("Times"))
    def times_text(self, ar):
        if self.start_time or self.end_time:
            return "%s-%s" % (format_time(self.start_time), format_time(self.end_time))
        return ""

    @dd.displayfield(_("When"))
    def weekdays_text(self, ar=None):
        if self.every_unit is None:
            return _("Not specified")
        elif self.every_unit == Recurrences.never:
            return _("Never")
        elif self.every_unit == Recurrences.once:
            if self.end_date and self.end_date != self.start_date:
                return gettext("{0}-{1}").format(
                    dd.fds(self.start_date), dd.fds(self.end_date)
                )
                # return _("From {0} until {1}").format(
                #     dd.fdf(self.start_date), dd.fdf(self.end_date))
            day_text = self.weekdays_text_(", ")
            if day_text:
                return gettext("Once starting on {0} (only {1})").format(
                    dd.fds(self.start_date), day_text
                )
            return gettext("On {0}").format(dd.fdf(self.start_date))
        elif self.every_unit == Recurrences.daily:
            day_text = gettext("day")
        elif self.every_unit == Recurrences.weekly:
            day_text = self.weekdays_text_(", ")
            if not day_text:
                return gettext("Every week")
        elif self.every_unit == Recurrences.monthly:
            if self.positions:
                # assert self.every == 1
                # day_text = " {} ".format(gettext("and")).join(positions) \
                #     + " " + self.weekdays_text_(gettext(' and '), gettext("day")) \
                #     + " " + gettext("of the month")
                day_text = (
                    self.positions_text_(" {} ".format(gettext("and")))
                    + " "
                    + self.weekdays_text_(" {} ".format(gettext("and")), gettext("day"))
                )
                return gettext("Every {day} of the month").format(day=day_text)
            else:
                s = ngettext("Every month", "Every {count} months", self.every)
                return s.format(count=self.every)

        elif self.every_unit == Recurrences.yearly:
            s = ngettext("Every year", "Every {count} years", self.every)
            return s.format(count=self.every)
        elif self.every_unit == Recurrences.easter:
            s = ngettext(
                "Every year (with Easter)",
                "Every {count} years (with Easter)",
                self.every,
            )
            return s.format(count=self.every)
        else:
            return "Invalid recurrency unit {}".format(self.every_unit)
        s = ngettext("Every {day}", "Every {ord_count} {day}", self.every)
        # num2words does not have support for every other language; and raises NotImplementedError.
        try:
            ord_count = num2words(
                self.every, to="ordinal", lang=translation.get_language()
            )
        except NotImplementedError:
            ord_count = num2words(self.every, to="ordinal")
        return s.format(ord_count=ord_count, day=day_text)
        # if self.every == 1:
        #     return gettext("Every {what}").format(what=every_text)
        # return gettext("Every {ordinal} {what}").format(
        #     ordinal=ordinal(self.every), what=every_text)
        # return gettext("Every %snd %s") % (self.every, every_text)

    def weekdays_text_(self, sep, any=""):
        if (
            self.monday
            and self.tuesday
            and self.wednesday
            and self.thursday
            and self.friday
            and not self.saturday
            and not self.sunday
        ):
            return gettext("working day")
        weekdays = []
        for wd in Weekdays.get_list_items():
            if getattr(self, wd.name):
                weekdays.append(str(wd.text))
        if len(weekdays) == 0:
            return any
        return sep.join(weekdays)

    def positions_text_(self, sep):
        positions = []
        for i in self.positions.split():
            positions.append(str(POSITION_TEXTS.get(i, "?!")))
        return sep.join(positions)

    def move_event_to(self, ev, newdate):
        """Move given event to a new date.  Also change `end_date` if
        necessary.

        """
        ev.start_date = newdate
        if self.end_date is None or self.end_date == self.start_date:
            ev.end_date = None
        else:
            duration = self.end_date - self.start_date
            ev.end_date = newdate + duration

    def get_next_alt_date(self, ar, date):
        """Currently always returns date + 1."""
        if date is None:
            return None
        return self.find_start_date(date + ONE_DAY)

    def get_next_suggested_date(self, date, logger=logger):
        """Find the next date after the given date, without worrying about
        conflicts.

        """
        if self.every_unit in (Recurrences.once, Recurrences.never, None):
            logger.debug("No next date when recurrency is %s.", self.every_unit)
            return None

        freq = self.every_unit.du_freq
        # Recurrences without du_freq silently ignore positions
        if freq is not None and self.positions:
            bysetpos = [int(i) for i in self.positions.split()]
            kw = dict(
                freq=freq,
                count=2,
                dtstart=date + ONE_DAY,
                interval=self.every,
                bysetpos=bysetpos,
            )
            weekdays = []
            if self.monday:
                weekdays.append(0)
            if self.tuesday:
                weekdays.append(1)
            if self.wednesday:
                weekdays.append(2)
            if self.thursday:
                weekdays.append(3)
            if self.friday:
                weekdays.append(4)
            if self.saturday:
                weekdays.append(5)
            if self.sunday:
                weekdays.append(6)
            if len(weekdays):
                kw.update(byweekday=weekdays)
            rr = rrule(**kw)
            # if len(rr) == 0:
            #     ar.debug("rrule(%s) returned an empty list.", kw)
            #     return None
            try:
                return rr[0].date()
            except IndexError:
                logger.debug("No date matches your recursion rule(%s).", kw)
                return None

        if self.every_unit == Recurrences.per_weekday:
            # per_weekday is deprecated to be replaced by daily.
            date = date + ONE_DAY
        else:
            date = self.every_unit.add_duration(date, self.every)
        return self.find_start_date(date)

    def find_start_date(self, date):
        """Find the first available date for the given date (possibly
        including that date), according to the weekdays
        of this recurrence set.

        """
        if date is not None and self.every_unit != Recurrences.never:
            for i in range(7):
                if self.is_available_on(date):
                    return date
                date += ONE_DAY
        return None

    def is_available_on(self, date):
        """Whether the given date `date` is allowed according to the weekdays
        of this recurrence set.

        """
        if (
            self.monday
            or self.tuesday
            or self.wednesday
            or self.thursday
            or self.friday
            or self.saturday
            or self.sunday
        ):
            wd = date.isoweekday()  # Monday:1, Tuesday:2 ... Sunday:7
            wd = Weekdays.get_by_value(str(wd))
            rv = getattr(self, wd.name)
            # ~ logger.info('20130529 is_available_on(%s) -> %s -> %s',date,wd,rv)
            return rv
        return True

    def compare_auto_event(self, obj, ae):
        original_state = dict(obj.__dict__)
        summary = force_str(ae.summary)
        if obj.summary != summary:
            obj.summary = summary
        if obj.user != ae.user:
            obj.user = ae.user
        if obj.start_date != ae.start_date:
            obj.start_date = ae.start_date
        if obj.end_date != ae.end_date:
            obj.end_date = ae.end_date
        if obj.start_time != ae.start_time:
            obj.start_time = ae.start_time
        if obj.end_time != ae.end_time:
            obj.end_time = ae.end_time
        if obj.event_type != ae.event_type:
            obj.event_type = ae.event_type
        if obj.room != ae.room:
            obj.room = ae.room
        if not obj.is_user_modified():
            self.before_auto_event_save(obj)
        if obj.__dict__ != original_state:
            obj.save()

    def before_auto_event_save(self, event):
        """
        Called for automatically generated events after their automatic
        fields have been set and before the event is saved.  This
        allows for additional application-specific automatic fields.

        E.g. the :attr:`room` field in :mod:`lino_xl.lib.rooms`.

        :class:`EventGenerator`
        by default manages the following **automatic event fields**:

        - :attr:`auto_type``
        - :attr:`user`
        - :attr:`summary`
        - :attr:`start_date`,

        NB: also :attr:`start_time` :attr:`end_date`, :attr:`end_time`?

        """
        if self.end_date and self.end_date != self.start_date:
            duration = self.end_date - self.start_date
            event.end_date = event.start_date + duration
            # if "Weekends" in str(event.owner):
            #     dd.logger.info("20180321 %s", self.end_date)
        else:
            event.end_date = None


dd.update_field(RecurrenceSet, "start_date", default=dd.today)

RecurrenceSet.set_widget_options("every", hide_sum=True)
