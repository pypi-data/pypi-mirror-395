# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/dev/quantities`."""

import datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from lino.utils.sums import myround

DEC2HOUR = Decimal(1) / Decimal(60)


class Quantity(Decimal):
    # def __new__(cls, *args, **kwargs):
    #     raise Exception("You cannot instantiate the Quantity base class.")

    def __new__(cls, value=None, context=None):
        if value is NotImplemented:
            return value
        # if isinstance(value, str):
        #     value = Decimal(value)
        self = Decimal.__new__(cls, value, context)
        # try:
        #     self = Decimal.__new__(cls, value, context)
        # except InvalidOperation as e:
        #     raise Exception(f"Failed to parse {repr(value)}: {e}")
        self._text = str(value)
        return self

    def __str__(self):
        return self._text

    def as_decimal(self, places=None):
        rv = Decimal(self)
        if places is not None:
            q = Decimal(10) ** -places
            rv = rv.quantize(q, rounding=ROUND_HALF_UP)
        return rv

    def limit_length(self, max_length, excl=Exception):
        rv = self
        while len(rv) > max_length:
            if (pos := rv._text.find(".")) == -1:
                raise excl(f"Cannot reduce length of {self} to {max_length}")
            places = len(rv) - pos - 2  # one decimal place less than before
            q = Decimal(10) ** -places
            rv = self.__class__(self.quantize(q, rounding=ROUND_HALF_UP))
        return rv

    def __format__(self, format_spec):
        if format_spec:
            return format(self._text, format_spec)
        return self._text

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self)

    def __add__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__add__(self, other, **kwargs))

    __radd__ = __add__

    def __sub__(self, other, **kwargs):
        # print("20230616 __sub__(", self, other, ")")
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__sub__(self, other, **kwargs))

    # __rsub__ = __sub__

    def __rsub__(self, *args, **kw):
        return self.__class__(Decimal.__rsub__(self, *args, **kw))

    def __mul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__mul__(self, other, **kwargs))

    __rmul__ = __mul__

    # def __rmul__(self, other, **kwargs):
    #     other = convert_from(other, **kwargs)
    #     return self.__class__(Decimal.__rmul__(self, other, **kwargs))
    #     # return Decimal.__rmul__(self, other, **kwargs)
    #     # see Luc's blog 20190410

    def __truediv__(self, *args, **kw):
        return self.__class__(Decimal.__truediv__(self, *args, **kw))

    __rtruediv__ = __truediv__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __neg__(self, **kwargs):
        return self.__class__(Decimal.__neg__(self, **kwargs))

    def __eq__(self, other):
        if other in (None, "", [], (), {}):
            return NotImplemented
        return Decimal(self).__eq__(Decimal(other))
        # try:
        #     return Decimal(self).__eq__(Decimal(other))
        # except Exception:
        #     raise Exception("20231014 {} {}".format(repr(self), repr(other)))

    def deconstruct(self):
        return (self.__module__ + "." + self.__class__.__name__, (self._text,), {})


class Percentage(Quantity):
    def __new__(cls, value="0%", context=None):
        # print("20230617 Percentage.__new__()")
        if value is NotImplemented:
            return value
        if isinstance(value, str):
            text = value
            if text[-1] != "%":
                text += "%"
            cv = Decimal(text[:-1]) / Decimal(100)
        else:
            cv = value
            text = str(value * 100) + "%"
        self = Decimal.__new__(cls, cv, context)
        self._text = text
        return self

    # def __str__(self):
    #     return "{}%".format(self * 100)
    #     # return str(self._value)

    def __rmul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        # return self.__class__(Decimal.__rmul__(self, other, **kwargs))
        return Decimal.__rmul__(self, other, **kwargs)
        # see Luc's blog 20190410


class Duration(Quantity):
    def __new__(cls, value="0:00", context=None):
        if isinstance(value, datetime.timedelta):
            hours = 0
            if value.days != 0:
                hours += value.days * 24
                value = datetime.timedelta(seconds=value.seconds)
            a = str(value).split(":")[:2]
            hours += int(a[0])
            minutes = int(a[1])
            cv = Decimal(hours) + Decimal(minutes) * DEC2HOUR
            text = "%d:%02d" % (hours, minutes)
        else:
            text = str(value).strip()
            if ":" in text:
                minus = False
                if text.startswith("-"):
                    minus = True
                    text = text[1:]
                try:
                    h, m = text.split(":")
                except ValueError:
                    raise ValueError("Cannot convert %r to Duration" % value)
                cv = Decimal(h) + Decimal(m) * DEC2HOUR
                if minus:
                    cv = -cv
                    text = "-" + text
            else:
                # print("20231230", repr(value))
                cv = Decimal(value)
                minus = False
                if cv < 0:
                    minus = True
                    cv = -cv
                hours = int(cv)
                minutes = ((cv - hours) / DEC2HOUR).to_integral()
                # minutes = old_div((hours - int(self)), DEC2HOUR)
                text = "%d:%02d" % (hours, minutes)
                if minus:
                    text = "-" + text
                    cv = -cv
        self = Decimal.__new__(cls, cv, context)
        self._text = text
        return self

    # def __str__(self):
    #     i = int(self)
    #     minutes = (self - i) / DEC2HOUR
    #     return '%d:%02d' % (i, minutes)

    def __radd__(self, other, **kwargs):
        # add a Duration to a datetime.datetime
        if isinstance(other, datetime.datetime):
            return other + self.as_timedelta()
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__radd__(self, other, **kwargs))

    def __rsub__(self, other, **kwargs):
        # subtract a Duration from a datetime.datetime
        if isinstance(other, datetime.datetime):
            return other - self.as_timedelta()
        # return self.__rsub__(other, **kwargs)
        # other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__rsub__(self, other, **kwargs))

    def as_timedelta(self):
        h, m = self._text.split(":")
        return datetime.timedelta(seconds=int(h) * 60 * 60 + int(m) * 60)

    def __mul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__mul__(self, other, **kwargs))

    __rmul__ = __mul__

    # def limit_length(self, max_length):
    #     raise Exception("Cannot limit the length of a duration")


def convert_from(value, context=None):
    if isinstance(value, str):
        return parse(value)
    if isinstance(value, datetime.timedelta):
        return Duration(value)
    return value


def parse(s):
    if s.endswith("%"):
        return Percentage(s)
        # self = Decimal.__new__(
        #     Percentage, old_div(Decimal(s[:-1]), 100), context)
        # return self
    if ":" in s:
        return Duration(s)
    # if not isinstance(s, six.string_types):
    #     raise Exception("Expected a string, got %r" % s)
    # if ':' in s:
    #     return Duration(s)
    # if '/' in s:
    #     return Fraction(s)
    # if s.endswith('%'):
    #     return Percentage(s)
    return parse_decimal(s)


def parse_decimal(s):
    if not s:
        return None
    if "." in s and "," in s:
        raise ValueError("Invalid decimal value %r" % s)
    s = s.replace(",", ".")
    return Quantity(s)


ZERO_DURATION = Duration("0:00")
