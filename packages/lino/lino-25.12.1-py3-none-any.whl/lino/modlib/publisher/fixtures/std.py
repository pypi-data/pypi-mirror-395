# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt
from lino.modlib.publisher.models import create_special_pages


def objects():
    yield None
    # ar = rt.login("robin")
    ar = rt.login()
    create_special_pages(ar, publishing_state="published")


# from django.conf import settings
# from django.utils import translation
#
# from lino.modlib.publisher.choicelists import SpecialPages
#
# from lino.api import dd, rt
#
#
# def objects():
# Page = rt.models.publisher.Page
# if dd.plugins.publisher.with_trees:
#     Tree = rt.models.publisher.Tree
#     main = Tree(ref='main')
#     yield main
# tree = dict(publisher_tree=main)
# else:
#     tree = dict()

# for sp in SpecialPages.get_list_items():
#     translated_from = None
#     for lng in settings.SITE.languages:
#         with translation.override(lng.django_code):
#             # tree = lng2tree[lng.django_code]
#             kwargs = dict(special_page=sp, **tree)
#             kwargs.update(language=lng.django_code)
#             qs = Page.objects.filter(**kwargs)
#             if qs.count() == 0:
#                 kwargs.update(publishing_state="published")
#                 if lng.suffix:
#                     kwargs.update(translated_from=translated_from)
#                 obj = Page(**kwargs)
#                 sp.on_page_created(obj)
#                 obj.full_clean()
#                 obj.save()
#             elif qs.count() > 1:
#             if not lng.suffix:
#                 translated_from = obj
