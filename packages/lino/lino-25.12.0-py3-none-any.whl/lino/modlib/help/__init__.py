# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Lino's help framework.  See :doc:`/plugins/help`.

"""

from lino.api import ad


class Plugin(ad.Plugin):
    menu_group = "system"

    needs_plugins = ["lino.modlib.system"]

    make_help_pages = False

    # interproject_specs = None
    # """
    #
    # Space-separated list of Python packages with extra intersphinx urls to be
    # used when generating local help pages using :manage:`makehelp`.
    #
    # """

    include_useless = False
    """Whether to include "useless" sections to the local help tree.
    """

    use_contacts = False
    """Whether to include site contacts.
    """

    def before_actors_discover(self):
        from lino.core.utils import get_models
        from lino.modlib.help.utils import HelpTextsLoader

        self.htl = HelpTextsLoader(self.site)
        # Install help texts to all database fields:
        # models_list = get_models(include_auto_created=True)
        models_list = get_models()
        for model in models_list:
            self.htl.install_help_text(model)  # needed only for makehelp
            for f in model._meta.get_fields(include_parents=False):
                # for f in model._meta.get_fields():
                self.htl.install_help_text(f, model, f.name)
            # for f in model._meta.private_fields:
            #     site.install_help_text(f, model, f.name)
            # if model.__name__ == "Client":
            #     print(' '.join([f.name for f in model._meta.private_fields]))

    def on_ui_init(self, kernel):
        from lino.core import actors

        for a in actors.actors_list:
            self.htl.install_help_text(a)
            if a.parameters is not None:
                for name, fld in a.parameters.items():
                    self.htl.install_help_text(fld, a, name)

            for ba in a.get_actions():
                # site.install_help_text(
                #     ba.action.__class__, ba.action.action_name)
                # site.install_help_text(ba.action, a, ba.action.action_name)
                # site.install_help_text(ba.action, ba.action.__class__)
                if a.model is not None:
                    self.htl.install_help_text(
                        ba, a.model, ba.action.action_name
                    )
                self.htl.install_help_text(ba, a, ba.action.action_name)
                self.htl.install_help_text(ba.__class__)
                # htl.install_help_text(
                #     ba.action, ba.action.__class__,
                #     attrname=ba.action.action_name)

                if ba.action.parameters is not None:
                    for name, fld in ba.action.parameters.items():
                        self.htl.install_help_text(fld, ba.action.__class__, name)

        self.htl = None  # free the resources

    def get_requirements(self, site):
        # temporary solution until the dependency gets fixed
        if self.make_help_pages:
            yield "atelier"

    def get_site_info(self, ar=None):
        if not self.use_contacts:
            return ""
        from lino.utils.html import E, tostring

        items = []
        for obj in self.site.models.help.SiteContact.objects.all():
            p = obj.company or obj.contact_person
            if p is not None:
                txt = tostring(E.b(str(obj.site_contact_type.text))) + ": "
                txt += "".join([tostring(e)
                               for e in p.get_name_elems(ar, sep=lambda: " ")])
                txt += ", "
                txt += ", ".join([tostring(e) for e in p.address_location_lines()])
                # txt += "".join(p.as_paragraph(ar))
                txt += ". "
                remark = self.site.babelattr(obj, "remark")
                if remark:
                    txt += remark + "."
                items.append("<li>{}</li>".format(txt))
        if len(items):
            return "<ul>{}</ul>".format("".join(items))
        # sc = self.site.site_config.site_company
        # if sc is not None:
        #     for chunk in sc.as_copyright_owner(ar):
        #         yield chunk

    def setup_config_menu(self, site, user_type, m, ar=None):
        if not self.use_contacts:
            return
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("help.SiteContacts")
