# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _


def objects():
    User = rt.models.users.User
    UserTypes = rt.models.users.UserTypes

    def user(username, **kwargs):
        kwargs.update(user_type=UserTypes.user, username=username)
        if not dd.plugins.users.with_nickname:
            kwargs.pop('nickname', None)
        return User(**kwargs)

    yield user("andy", first_name="Andreas", last_name="Anderson", nickname="Andy", email="andy@example.com")
    yield user("bert", first_name="Albert", last_name="Bernstein", nickname="Bert", email="bert@example.com")
    yield user("chloe", first_name="Chloe", last_name="Cleoment", email="chloe@example.com")
