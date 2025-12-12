# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
This defines the :class:`Hotkey` class and some keystrokes.

The system is not yet heavily used.

React uses the attributes `ctrl`, `shift`, `alt` and `code`.

For the `code`, see:
https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code


"""


class Hotkey(object):
    "Represents a combination of keystrokes."

    key = None
    keycode = None
    code = None
    shift = False
    ctrl = False
    alt = False

    def __init__(self, key=None, **kw):
        if key:
            self.key = key.upper()
            self.keycode = ord(self.key)
        for k, v in kw.items():
            setattr(self, k, v)

        self.__dict__.update(
            keycode=self.keycode,
            code=self.code,
            shift=self.shift,
            key=self.key,
            ctrl=self.ctrl,
            alt=self.alt,
        )

# ExtJS src/core/EventManager-more.js
RETURN = Hotkey(keycode=13, code="Enter")
ESCAPE = Hotkey(keycode=27, code="Escape")
PAGE_UP = Hotkey(keycode=33, code="PageUp")
PAGE_DOWN = Hotkey(keycode=34, code="PageDown")
INSERT = Hotkey(keycode=44, code="Insert")
DELETE = Hotkey(keycode=46, code="Delete")
