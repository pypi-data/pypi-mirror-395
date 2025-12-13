# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Documentation: https://dev.lino-framework.org/plugins/accounting.html

from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP

ZERO = Decimal(0)
CENT = Decimal('.01')
HUNDRED = Decimal('100.00')
ONE = Decimal('1.00')
MAX_AMOUNT = Decimal("9999999.00")


def myround(d):
    return d.quantize(CENT, rounding=ROUND_HALF_UP)


class SumCollector:
    """A dictionary of sums to be collected using an arbitrary key.

    This is also included in the default context used by the Jinja
    renderer (:mod:`lino.modlib.jinja`) when rendering templates,
    which makes it a more complete solution for a problem asked also
    elsewhere, e.g. on `Stackoverflow
    <https://stackoverflow.com/questions/7537439/how-to-increment-a-variable-on-a-for-loop-in-jinja-template>`__.

    See examples in :doc:`/topics/utils`.

    """

    def __init__(self):
        self._sums = OrderedDict()

    def collect(self, k, value):
        """Add the given value to the sum at the given key k."""
        if value is None:
            return
        if k in self._sums:
            # print("20230614 a", k, "=", self._sums[k], "+", value)
            self._sums[k] += value
        else:
            # print("20230614 b", k, "=", value)
            self._sums[k] = value

    def myround(self):
        self._sums = {k: myround(v) for k, v in self._sums.items()}

    def __getattr__(self, k):
        return self._sums.get(k)

    def __getitem__(self, k):
        return self._sums.get(k)

    def total(self):
        return sum(self._sums.values())

    def items(self, *args, **kwargs):
        return self._sums.items(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self._sums.keys(*args, **kwargs)

    def values(self, *args, **kwargs):
        return self._sums.values(*args, **kwargs)

    def __len__(self):
        return self._sums.__len__()

    def __str__(self):
        return str(self._sums)

    def __repr__(self):
        return repr(self._sums)
