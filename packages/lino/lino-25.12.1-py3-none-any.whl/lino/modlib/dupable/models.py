# -*- coding: UTF-8 -*-
# Copyright 2014-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the :class:`Dupable` model mixin and related functionality
to assist users in finding unwanted duplicate database records.

Don't mix up this module with :mod:`lino.mixins.clonable`.  Models
are "clonable" if users may *want* to duplicate some instance
thereof, while "dupable" implies that the duplicates are *unwanted*.
To dupe *somebody* means "to make a dupe of; deceive; delude; trick."
(`reference.com <https://dictionary.reference.com/browse/dupe>`_), and
to dupe *something* means to duplicate it (eventually in order to
cheat somebody e.g. by making a cheap copy of a valuable object).

This requires the `metafone
<https://pypi.python.org/pypi/Metafone/0.5>`__ package (a successor of
`fuzzy <https://pypi.python.org/pypi/Fuzzy>`__ which isn't yet ported
to Python 3).  Applications that use this mixin must themselves add
`metafone` to their :term:`install_requires`.

The current implementation uses a helper table with "phonetic words"
and the `Double Metaphone
<https://en.wikipedia.org/wiki/Metaphone#Double_Metaphone>`_
algorithm.  Read also Doug Hellmann about `Using Fuzzy Matching to
Search by Sound with Python
<https://www.informit.com/articles/article.aspx?p=1848528>`_
(2012-03-22).

"""

from django.db import models

from lino.api import dd, _
from lino.modlib.gfks.mixins import Controllable
from lino.utils import join_elems
from lino.utils.html import E, tostring

from .mixins import Dupable
from lino.core import constants


class PhoneticWord(Controllable):
    """Base class for the table of phonetic words of a given dupable
    model. For every (non-abstract) dupable model there must be a
    subclass of `PhoneticWordBase`.
    The subclass must define a field
    :attr:`owner` which points to the `Dupable`, and the `Dupable`'s
    :attr:`dupable_word_model` must point to its subclass
    of `PhoneticWordBase`.

    """

    class Meta:
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    allow_cascaded_delete = ["owner"]
    # quick_search_fields = ['owner__' + dupable_words_field]

    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

    @classmethod
    def on_analyze(cls, site):
        pass
        # import metaphone as fuzzy
        # cls._fuzzy_DMetaphone = fuzzy.doublemetaphone()
        # import fuzzy
        # cls._fuzzy_DMetaphone = fuzzy.DMetaphone()

    @classmethod
    def reduce_word(cls, s):
        # from metaphone.word import Word
        import metaphone as fuzzy
        # import fuzzy

        # fuzzy.DMetaphone does not work with unicode strings, see
        # https://bitbucket.org/yougov/fuzzy/issue/2/fuzzy-support-for-unicode-strings-with
        # dm = fuzzy.doublemetaphone(s.encode('utf8'))
        dm = fuzzy.doublemetaphone(s)
        dms = dm[0] or dm[1]
        if dms is None:
            return ""
        if isinstance(dms, bytes):
            dms = dms.decode("utf8")
        return dms

    # @classmethod
    # def get_simple_parameters(cls):
    #     for p in super(PhoneticWord, cls).get_simple_parameters():
    #         yield p
    #     yield "owner_id"
    #     yield "owner_type"


class PhoneticWords(dd.Table):
    model = "dupable.PhoneticWord"
    required_roles = dd.login_required(dd.SiteAdmin)


class WordsByOwner(PhoneticWords):
    "Show the phonetic words for this database record."

    required_roles = dd.login_required()
    master_key = "owner"
    column_names = "word"
    label = " ♋ "  # 264B


class SimilarObjects(dd.VirtualTable):
    """Shows the other objects that are similar to this one."""

    label = _("Similar objects")
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    master = Dupable

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return

        for o in mi.find_similar_instances(4):
            yield o

    @dd.displayfield(_("Similar record"))
    def similar_record(self, obj, ar):
        return ar.obj2html(obj)

    @classmethod
    def table_as_summary(self, ar):
        chunks = []
        for other in ar:
            chunks.append(ar.obj2html(other))
        if len(chunks):
            chunks.append(E.br())
        obj = ar.master_instance
        s = getattr(obj, obj.dupable_words_field)
        words = " ".join(obj.get_dupable_words(s))
        chunks.append("({0})".format(words))
        return tostring(join_elems(chunks))
