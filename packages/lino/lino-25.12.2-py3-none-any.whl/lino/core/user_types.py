# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines a set of user types "Anonymous", "User" and
"Administrator".

This can be used directly as :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for simple applications.
"""

from django.utils.translation import gettext_lazy as _
from lino.core.roles import UserRole, SiteAdmin, SiteUser
from lino.modlib.users.choicelists import UserTypes

add = UserTypes.add_item
add("000", _("Anonymous"), UserRole, name="anonymous", readonly=True)
add("100", _("User"), SiteUser, name="user")
add("900", _("Administrator"), SiteAdmin, name="admin")
