"""A shortcut import for usage in a Django shell or a :cmd:`pm run`
script.

Typical usage::

    >>> from lino.api.shell import *

This also defines every plugin name (by saying `globals().update(rt.models)`).
This has at least one side effect: if you have the :mod:`lino.modlib.help`
installed, you cannot use the built-in :func:`help` function.

"""
from lino import AFTER17

if AFTER17:
    import django

    django.setup()
from django.conf import settings
from lino.api import ad, dd, rt

rt.startup()
globals().update(rt.models)
