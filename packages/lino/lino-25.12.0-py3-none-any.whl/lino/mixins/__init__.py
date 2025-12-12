# -*- coding: UTF-8 -*-
# Copyright 2010-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
This package contains model mixins, some of which are heavily used
by applications and the :ref:`xl`. But none of them is mandatory.

.. autosummary::
   :toctree:


    dupable
    clonable
    sequenced
    human
    periods
    polymorphic
    ref
    registrable

"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# from django.utils.html import format_html
# from django.utils.text import format_lazy
# from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

# Note that reordering the imports here can cause the field ordering to change
# in models like lino_voga.lib.courses.TeacherType, which inherits from
# `(Referrable, BabelNamed, Printable)`. This can cause doctests like
# docs/specs/voga/courses.rst to fail because the `ref` field then came after
# the name field. The TeacherTypes table has no explicit `column_names`, so it
# uses the "natural" field ordering, which is, as this observation shows, quite
# unpredictable.

from lino.core import actions
from lino.core import fields
from lino.core import model
# from lino.core.workflows import ChangeStateAction
# from lino.core.exceptions import ChangedAPI
from lino.utils.mldbc.fields import LanguageField
from lino.utils.html import E
from lino.utils.mldbc.mixins import BabelNamed, BabelDesignated
from lino.utils.mldbc.fields import BabelCharField, BabelTextField

from .human import Human
from .polymorphic import Polymorphic
from .periods import ObservedDateRange, Yearly, Monthly, Today
from .periods import DateRange
from .sequenced import Sequenced, Hierarchical
from .clonable import Clonable, CloneRow
from .registrable import Registrable, RegistrableState
from .ref import Referrable, StructuredReferrable


class Contactable(model.Model):
    """
    Mixin for models that represent somebody who can be contacted by
    email.
    """

    class Meta:
        abstract = True

    email = models.EmailField(_("e-mail address"), blank=True)
    language = LanguageField(default=models.NOT_PROVIDED, blank=True)

    def get_as_user(self):
        """Return the user object representing this contactable."""
        raise NotImplementedError()


class Phonable(model.Model):
    """
    Mixin for models that represent somebody who can be contacted by
    phone.
    """

    class Meta:
        abstract = True

    url = models.URLField(_("URL"), blank=True)
    phone = models.CharField(_("Phone"), max_length=200, blank=True)
    gsm = models.CharField(_("Mobile"), max_length=200, blank=True)
    fax = models.CharField(_("Fax"), max_length=200, blank=True)


class Modified(model.Model):
    """
    Adds a a timestamp field that holds the last modification time of
    every individual database object.

    .. attribute:: modified

        The time when this database object was last modified.
    """

    auto_touch = True
    """
    Whether to touch objects automatically when saving them.

    If you set this to `False`, :attr:`modified` is updated only when
    you explicitly call :meth:`touch`.
    """

    class Meta:
        abstract = True

    modified = models.DateTimeField(_("Modified"), editable=False, null=True)

    def save(self, *args, **kwargs):
        if self.auto_touch and not settings.SITE.loading_from_dump:
            self.touch()
        super().save(*args, **kwargs)

    def touch(self):
        self.modified = settings.SITE.now()


class Created(model.Model):
    """
    Adds a timestamp field that holds the creation time of every
    individual :term:`database row`.

    .. attribute:: created

        The time when this :term:`database row` was created.

        Does not use Django's `auto_now` and `auto_now_add` features
        because their deserialization would be problematic.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(_("Created"), editable=False)

    @fields.displayfield(_("Created"))
    def created_natural(self, ar):
        return naturaltime(self.created)

    def save(self, *args, **kwargs):
        if self.created is None:  # and not settings.SITE.loading_from_dump:
            self.created = settings.SITE.now()
        super().save(*args, **kwargs)


class CreatedModified(Created, Modified):
    """
    Adds two timestamp fields `created` and `modified`.

    """

    class Meta:
        abstract = True


class ProjectRelated(model.Model):
    """
    Mixin for models that are related to a "project",
    i.e. to an object of the type given by your `lino.core.site.Site.project_model`.

    This adds a field named :attr:`project` and related methods.


    .. attribute:: project

        Pointer to the project to which this object is related.

        If the application's :attr:`project_model
        <lino.core.site.Site.project_model>` is empty, the
        :attr:`project` field will be a :class:`DummyField
        <lino.core.fields.DummyField>`.
    """

    class Meta:
        abstract = True

    project = fields.ForeignKey(
        settings.SITE.project_model,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_set_by_project",
    )

    def get_related_project(self):
        # if settings.SITE.project_model:
        # When project_model is None, project is a dummy field which always returns None
        return self.project

    # def on_create(self, ar):
    #     super().on_create(ar)
    #     print(20200327, ar.actor.master_key, ar.master_instance)
    #     if ar.actor.master_key and ar.actor.master_key == "project":
    #         self.project = ar.master_instance

    def as_summary_item(self, ar, text=None, **kwargs):
        e = super().as_summary_item(ar, text, **kwargs)
        # s = [ar.obj2html(self)]
        if text is None and ar and settings.SITE.project_model:
            if self.project and not ar.is_obvious_field("project"):
                e = E.span(e, " (", self.project.as_summary_item(ar), ")")
                # s += " ({)}".format(ar.obj2htmls(self.project))
                # s = format_html("{} ({})", s, self.project.as_summary_row(ar, **kwargs))
        return e

    def update_owned_instance(self, controllable):
        """
        When a :class:`project-related <ProjectRelated>` object controls
        another project-related object, then the controlled
        automatically inherits the `project` of its controller.
        """
        if isinstance(controllable, ProjectRelated):
            controllable.project = self.project
        super().update_owned_instance(controllable)

    def get_mailable_recipients(self):
        if isinstance(self.project, settings.SITE.models.contacts.Partner):
            if self.project.email:
                yield ("to", self.project)
        for r in super().get_mailable_recipients():
            yield r

    def get_postable_recipients(self):
        if isinstance(self.project, settings.SITE.models.contacts.Partner):
            yield self.project
        for p in super().get_postable_recipients():
            yield p

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        # if settings.SITE.project_model:
        yield "project"

    # @classmethod
    # def setup_parameters(cls, params):
    #     super(ProjectRelated, cls).setup_parameters(params)
    #     if settings.SITE.project_model:
    #         params['project'].help_text = format_lazy(
    #             _("Show only entries having this {project}."),
    #             project=settings.SITE.project_model._meta.verbose_name)


class Story(model.Model):
    class Meta:
        abstract = True

    def get_story(self, ar):
        return []

    @fields.virtualfield(fields.HtmlBox())
    def body(self, ar):
        if ar is None:
            return ""
        # ar.master_instance = self
        html = ar.renderer.show_story(ar, self.get_story(ar), header_level=1)
        return ar.html_text(html)
        # return ar.html_text(ar.story2html(
        #     self.get_story(ar), header_level=1))

    def as_appy_pod_xml(self, apr):
        chunks = tuple(apr.story2odt(self.get_story(apr.ar), master_instance=self))
        return str("").join(chunks)  # must be utf8 encoded


class DragAndDrop(actions.Action):
    select_rows = True
    show_in_toolbar = False

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.on_dropped(ar, **kw)


class Draggable(model.Model):
    class Meta:
        abstract = True

    drag_drop = DragAndDrop()

    def on_dropped(self, ar, **kwargs):
        pass
