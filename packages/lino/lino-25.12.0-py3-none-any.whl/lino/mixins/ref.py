# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines the :class:`Referrable` model mixin.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Length

from lino.utils.html import E
from lino.utils import nextref
from lino.core import model
from lino.core.vfields import displayfield


class Referrable(model.Model):
    """
    Mixin for things that have a unique reference, i.e. an identifying
    name used by humans to refer to an individual object.

    A reference, unlike a primary key, can easily be changed.

    Referrable objects are mergeable by default.

    .. attribute:: ref

        The reference. This must be either empty or unique.
    """

    class Meta(object):
        abstract = True

    allow_merge_action = True

    ref_max_length = 40
    """
    The preferred width of the :attr:`ref` field.

    TODO: rename this to preferred_ref_width.
    """

    ref = models.CharField(
        _("Reference"), max_length=200, blank=True, null=True, unique=True
    )

    @classmethod
    def on_analyze(cls, site):
        cls.set_widget_options("ref", width=cls.ref_max_length)
        super().on_analyze(site)

    def on_duplicate(self, ar, master):
        """
        Before saving a duplicated object for the first time, we must
        change the :attr:`ref` in order to avoid an IntegrityError.
        """
        if self.ref:
            self.ref += " (DUP)"
        super().on_duplicate(ar, master)

    def __str__(self):
        return self.ref or super().__str__()

    def get_next_row(self):
        """Return the next database row, or None if this is the last one.
        """
        ref = nextref(self.ref)
        if ref is None:
            return None
        return self.__class__.get_by_ref(ref, None)

    @staticmethod
    def ref_prefix(obj, ar=None):
        return obj.as_ref_prefix(ar)

    @classmethod
    def get_by_ref(cls, ref, default=models.NOT_PROVIDED, **more):
        """
        Return the object identified by the given reference.
        """
        try:
            return cls.objects.get(ref=ref, **more)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "There is no {} with reference {!r}".format(
                        cls._meta.verbose_name, ref))
            return default

        # try:
        #     return cls.objects.get(ref=ref, **more)
        # except cls.DoesNotExist:
        #     if default is models.NOT_PROVIDED:
        #         raise cls.DoesNotExist(
        #             "No %s with reference %r" % (str(cls._meta.verbose_name), ref))
        #     return default

    @classmethod
    def quick_search_filter(cls, search_text, prefix=""):
        """Overrides the default behaviour defined in
        :meth:`lino.core.model.Model.quick_search_filter`. For
        Referrable objects, when quick-searching for a text containing
        only digits, the user usually means the :attr:`ref` and *not*
        the primary key.

        """
        # if search_text.isdigit():
        if search_text.startswith("*"):
            return models.Q(**{prefix + "ref__icontains": search_text[1:]})
        return super().quick_search_filter(search_text, prefix)


class StructuredReferrable(Referrable):
    """

    A referrable whose `ref` field is used to define a hierarchical structure.

    Example::

        1       Foos
         10     Good foos
           1000 Nice foos
           1020 Obedient foos
         11     Bad foos
           1100 Nasty foo
           1110 Lazy foo
        2       Bars
           2000 Normal bars
           2090 Other bars

    The length of the reference determines the hierarchic level: the
    shorter it is, the higher the level.

    The hierarchic level becomes visible a virtual field :attr:`ref_description`
    in together with the designation.

    .. attribute:: ref_description

        Displays the structured together with the designation.

    The mixin differentiates between "headings" and "leaves": objects whose
    :attr:`ref` has :attr:`ref_max_length` characters are considered "leaves"
    while all other objects are "headings".

    Subclasses must provide a method :meth:`get_designation`.

    .. method:: get_designation

        Return the "designation" part (without the reference).


    """

    class Meta:
        abstract = True

    ref_max_length = 4

    def __str__(self):
        if self.ref:
            return "({}) {}".format(self.ref, self.get_designation())
        return self.get_designation()

    @classmethod
    def get_usable_items(cls):
        return cls.objects.annotate(ref_len=Length("ref")).filter(
            ref_len=cls.ref_max_length
        )

    @classmethod
    def get_heading_objects(cls):
        return cls.objects.annotate(ref_len=Length("ref")).exclude(
            ref_len=cls.ref_max_length
        )

    def is_heading(self):
        if self.ref is None:
            return True
        return len(self.ref) < self.__class__.ref_max_length

    @displayfield(_("Description"), max_length=50)
    def description(self, ar):
        if self.ref is None:
            s = self.get_designation()
        else:
            s = self.ref
            s = " " * (len(s) - 1) + s
            s += " " + self.get_designation()
        if self.is_heading():
            s = E.b(s)
        return s
