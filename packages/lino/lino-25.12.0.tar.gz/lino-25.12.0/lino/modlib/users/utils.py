# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import threading
from django.conf import settings
from lino.utils import camelize

user_profile_rlock = threading.RLock()
_for_user_profile = None


def with_user_profile(profile, func, *args, **kwargs):
    global _for_user_profile

    with user_profile_rlock:
        old = _for_user_profile
        _for_user_profile = profile
        rv = func(*args, **kwargs)
        _for_user_profile = old
        return rv


def set_user_profile(profile):
    # Used in doctests to set a default profile
    global _for_user_profile
    _for_user_profile = profile


def get_user_profile():
    return _for_user_profile


class UserTypeContext(object):
    # A context manager which activates a current user type.

    def __init__(self, user_type):
        self.user_type = user_type

    def __enter__(self):
        global _for_user_profile
        self.old = _for_user_profile
        _for_user_profile = self.user_type

    def __exit__(self, exc_type, exc_value, traceback):
        global _for_user_profile
        _for_user_profile = self.old


# def set_user_profile(up):
#     global _for_user_profile
#     _for_user_profile = up

# set_for_user_profile = set_user_profile


def create_user(username, user_type=None, with_person=False, **kw):
    # with_person was used in noi1e demo
    first_name = camelize(username.upper())
    if user_type:
        # if with_person:
        #     p = rt.models.contacts.Person(first_name=first_name)
        #     p.full_clean()
        #     p.save()
        #     kw.update(partner=p)
        kw.update(username=username, user_type=user_type)
        kw.update(first_name=first_name)
        # kw.update(partner=person)
        return settings.SITE.models.users.User(**kw)
    else:
        # return dd.plugins.skills.supplier_model(first_name=first_name)
        return settings.SITE.models.contacts.Person(first_name=first_name)
