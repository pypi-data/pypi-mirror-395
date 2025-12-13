# Copyright 2010-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from os import symlink
from os.path import join
from lino import ad, _
from lino.modlib.memo.parser import split_name_rest

UPLOADS_ROOT = 'uploads'
VOLUMES_ROOT = 'volumes'


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Uploads")
    menu_group = "office"
    # needs_plugins = ['lino.modlib.checkdata']

    remove_orphaned_files = False
    """
    Whether `checkdata --fix` should automatically delete orphaned files in the
    uploads folder.

    """

    with_thumbnails = False
    """Whether to use PIL, the Python Imaging Library.
    """

    with_volumes = True
    """Whether to use library files (volumes).
    """
    # TODO: Also remove the Volume model and its actors when with_volumes is set
    # to False.

    # def get_uploads_root(self):
    #     # return join(self.site.django_settings["MEDIA_ROOT"], "uploads")
    #     return self.site.media_root / UPLOADS_ROOT

    # def get_volumes_root(self):
    #     return self.site.media_root / VOLUMES_ROOT

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("uploads.MyUploads")

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("uploads.Volumes")
        m.add_action("uploads.UploadTypes")

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("uploads.AllUploads")
        m.add_action("uploads.UploadAreas")

    def post_site_startup(self, site):

        self.uploads_root = site.media_root / UPLOADS_ROOT
        self.volumes_root = site.media_root / VOLUMES_ROOT

        if site.is_installed("memo"):

            def gallery(ar, text, cmdname, mentions, context):
                Upload = site.models.uploads.Upload
                photos = [Upload.objects.get(pk=int(pk))
                          for pk in text.split()]
                # ctx = dict(width="{}%".format(int(100/len(photos))))
                if mentions is not None:
                    mentions.update(photos)
                html = "".join([obj.memo2html(ar, obj.description)
                               for obj in photos])
                return '<p align="center">{}</p>'.format(html)

            site.plugins.memo.parser.register_command("gallery", gallery)

        super().post_site_startup(site)

        # site.makedirs_if_missing(self.get_uploads_root())
        # site.makedirs_if_missing(self.volumes_root)

    def get_requirements(self, site):
        if self.with_thumbnails:
            yield "Pillow"
            yield "PyMuPDF"
