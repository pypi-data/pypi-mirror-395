# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils import isidentifier
from lino.api import dd, _, pgettext


class MessageType(dd.Choice):
    # required_roles = set({})

    def __init__(self, value, text, **kwargs):
        if not isidentifier(value):
            raise Exception("{} not a valid identifier".format(value))
        super().__init__(value, text, value, **kwargs)


class MessageTypes(dd.ChoiceList):
    verbose_name = _("Message Type")
    verbose_name_plural = _("Message Types")
    item_class = MessageType

    # @classmethod
    # def register_type(cls, name, *args, **kwargs):
    #     cls.add_item_lazy(name, *args, **kwargs)


add = MessageTypes.add_item
add("system", _("System event"))
add("change", pgettext("message type", "Change"))


class MailModes(dd.ChoiceList):
    verbose_name = _("Notification mode")
    verbose_name_plural = _("Notification modes")


add = MailModes.add_item
add("silent", _("Silent"), "silent")
add("never", _("No mails"), "never")
# add('immediately', _("Immediately"), 'immediately')  # obsolete
add("often", _("Mail often"), "often")
add("daily", _("Daily email digest"), "daily")
add("weekly", _("Weekly email digest"), "weekly")  # not yet implemented
