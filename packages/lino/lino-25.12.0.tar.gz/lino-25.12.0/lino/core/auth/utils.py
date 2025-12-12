# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Utilities for authentication. Adapted from `django.contrib.auth`.

"""

from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string


class AnonymousUser:
    """An instance of this will be assigned to the
    :attr:`user` attribute of anonymous incoming requests, similar to
    Django's approach.

    The memo parser uses another instance of this.

    See also :attr:`lino.core.site.Site.anonymous_user_type`.

    """

    # authenticated = False

    is_authenticated = False
    """This is always `False`.
    See also :attr:`lino.modlib.users.User.is_authenticated`.
    """

    is_active = False

    email = None
    modified = None
    partner = None
    language = None
    readonly = True
    pk = None
    id = None
    time_zone = None
    notify_myself = False
    is_anonymous = True

    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def get_preferences(self):
        """Return the preferences of this user. The returned object is a
        :class:`lino.core.userprefs.UserPrefs` object.

        """
        from lino.core import userprefs

        return userprefs.reg.get(self)

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def get_choices_text(self, ar, actor, field):
        return str(self)


def activate_social_auth_testing(
    globals_dict, google=True, github=True, wikimedia=True, facebook=True,
    smart_id=False
):
    """
    Used for testing a development server.
    See for example the :xfile:`settings.py` of :mod:`lino_book.projects.noi1e`.

    """
    Site = globals_dict["Site"]

    Site.social_auth_backends = []

    if github:
        Site.social_auth_backends.append(
            "social_core.backends.github.GithubOAuth2",
        )
        globals_dict.update(
            # https://github.com/organizations/lino-framework/settings/applications/632218
            SOCIAL_AUTH_GITHUB_KEY="355f66b1557f0cbf4d1d",
            SOCIAL_AUTH_GITHUB_SECRET="4dbeea1701bf03316c1759bdb422d9f88969b782",
        )

        # 'social_core.backends.google.GoogleOAuth2',
        # 'social_core.backends.google.GoogleOAuth',
        # 'social_core.backends.facebook.FacebookOAuth2',
    if smart_id:
        Site.social_auth_backends.append("lino.utils.smart_id.SmartID")
        # https://oauth.ee/docs
        globals_dict.update(
            SOCIAL_AUTH_SMART_ID_KEY="xxx",
            SOCIAL_AUTH_SMART_ID_SECRET="yyy",
        )
    if wikimedia:
        Site.social_auth_backends.append("social_core.backends.mediawiki.MediaWiki")
        globals_dict.update(
            SOCIAL_AUTH_MEDIAWIKI_KEY="7dbd2e1529e45108f798349811c7a2b7",
            SOCIAL_AUTH_MEDIAWIKI_SECRET="8041055fcd16333fa242b346e0ae52133fd2ee14",
            SOCIAL_AUTH_MEDIAWIKI_URL="https://meta.wikimedia.org/w/index.php",
            SOCIAL_AUTH_MEDIAWIKI_CALLBACK="oob",
        )
    if google:
        Site.social_auth_backends.append("social_core.backends.google.GooglePlusAuth")
        globals_dict.update(
            SOCIAL_AUTH_GOOGLE_PLUS_KEY="451271712409-9qtm9bvjndaeep2olk3useu61j6qu2kp.apps.googleusercontent.com",
            SOCIAL_AUTH_GOOGLE_PLUS_SECRET="NHyaqV2HY8lV5ULG6k51OMwo",
            SOCIAL_AUTH_GOOGLE_PLUS_SCOPE=[
                "profile",
                "https://www.googleapis.com/auth/plus.login",
                "https://www.googleapis.com/auth/contacts.readonly",  # To have just READ permission
                "https://www.googleapis.com/auth/contacts ",  # To have WRITE/READ permissions
            ],
        )

    if facebook:
        globals_dict.update(
            SOCIAL_AUTH_FACEBOOK_KEY="1837593149865295",
            SOCIAL_AUTH_FACEBOOK_SECRET="1973f9e9d9420c4c6502aa40cb8cb7db",
            SOCIAL_AUTH_FACEBOOK_SCOPE=["email", "public_profile", "user_friends"],
        )

    if not Site.social_auth_backends:
        Site.social_auth_backends = None
