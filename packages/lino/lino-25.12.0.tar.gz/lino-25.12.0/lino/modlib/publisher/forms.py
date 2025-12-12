# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django import forms
from lino.api import dd


class ParamsForm(forms.Form):
    """
    A form dynamically built from an actor's parameters.
    """

    def __init__(self, *args, **kwargs):
        actor = kwargs.pop("actor")
        super().__init__(*args, **kwargs)
        for name, field in actor.parameters.items():
            if isinstance(field, dd.DummyField):
                continue
            fld = field.formfield()
            fld.help_text = None
            fld.widget.attrs.update({"class": "form-control", "title": field.help_text})
            self.fields[name] = fld
