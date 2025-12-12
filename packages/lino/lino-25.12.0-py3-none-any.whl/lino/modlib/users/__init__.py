# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Docs: https://dev.lino-framework.org/plugins/users.html


from lino.api import ad, _
from lino import logger


class Plugin(ad.Plugin):
    verbose_name = _("Users")
    needs_plugins = ["lino.modlib.system"]
    active_sessions_limit = -1

    third_party_authentication = False
    allow_online_registration = False
    verification_code_expires = 5
    user_type_new = "user"
    user_type_verified = "user"
    my_setting_text = _("My settings")
    with_nickname = False
    # partner_model = 'contacts.Person'
    partner_model = "contacts.Partner"
    demo_password = "1234"
    demo_username = None
    private_default = True
    """
    Whether comments (and other PrivacyRelevant things) are private by default.

    The default value for the :attr:`lino.modlib.users.PrivacyRelevant.private`
    field.

    """

    def on_init(self):
        super().on_init()
        self.site.set_user_model("users.User")
        from lino.core.site import has_socialauth

        if has_socialauth and self.third_party_authentication:
            self.needs_plugins.append("social_django")

    def pre_site_startup(self, site):
        super().pre_site_startup(site)
        # if isinstance(self.partner_model, str):
        #     if not site.is_installed_model_spec(self.partner_model):
        #         self.partner_model = None
        #         return
        self.partner_model = site.models.resolve(self.partner_model)

    def post_site_startup(self, site):
        super().post_site_startup(site)
        if self.demo_username is None:
            if (kw := self.get_root_user_fields(site.DEFAULT_LANGUAGE)):
                self.demo_username = kw['username']

    _demo_user = None  # the cached User object

    def get_demo_user(self):
        if self.demo_username is None:
            return None
        if self._demo_user is None:
            User = self.site.models.users.User
            try:
                self._demo_user = User.objects.get(username=self.demo_username)
            except User.DoesNotExist:
                msg = "Invalid username '{0}' in `demo_username` "
                msg = msg.format(self.demo_username)
                raise Exception(msg)
        return self._demo_user

    def get_requirements(self, site):
        yield "social-auth-app-django"

    def get_used_libs(self, site):
        if self.third_party_authentication:
            try:
                import social_django

                version = social_django.__version__
            except ImportError:
                version = site.not_found_msg
            name = "social-django"

            yield (name, version, "https://github.com/python-social-auth")

    def setup_config_menu(self, site, user_type, m, ar=None):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action("users.AllUsers")

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action("users.Authorities")
        m.add_action("users.UserTypes")
        m.add_action("users.UserRoles")
        if self.third_party_authentication:
            m.add_action("users.SocialAuths")

    def setup_site_menu(self, site, user_type, m, ar=None):
        m.add_action("users.Sessions")

    def get_quicklinks(self):
        yield "users.Me"

    def get_root_user_fields(self, lang, **kw):
        # ~ kw.update(user_type='900') # UserTypes.admin)
        # ~ print 20130219, UserTypes.items()
        kw.update(user_type=self.site.models.users.UserTypes.admin)
        kw.update(email=self.site.demo_email)  # 'root@example.com'
        lang = lang.django_code
        kw.update(language=lang)
        lang = lang[:2]
        if lang == "en":
            kw.update(first_name="Robin", last_name="Rood")
        elif lang == "de":
            kw.update(first_name="Rolf", last_name="Rompen")
        elif lang == "fr":
            kw.update(first_name="Romain", last_name="Raffault")
        elif lang == "et":
            kw.update(first_name="Rando", last_name="Roosi")
        elif lang == "pt":
            kw.update(first_name="Ronaldo", last_name="Rosa")
        elif lang == "es":
            kw.update(first_name="Rodrigo", last_name="Rosalez")
        elif lang == "nl":
            kw.update(first_name="Rik", last_name="Rozenbos")
        elif lang == "bn":
            kw.update(first_name="Roby", last_name="Raza")
        else:
            logger.warning("No demo user for language %r.", lang)
            return None
        kw.update(username=kw.get("first_name").lower())
        return kw
