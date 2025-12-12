# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This plugins installs two build methods for generating
:term:`printable documents <printable document>` using `weasyprint
<https://weasyprint.org/>`__.

See :doc:`/specs/weasyprint`.

"""

# trying to get rid of disturbing warnings in
# https://travis-ci.org/lino-framework/book/jobs/260560833
# import warnings
# warnings.filterwarnings(
#     "ignore", 'There are known rendering problems')
# warnings.filterwarnings(
#     "ignore", '@font-face support needs Pango >= 1.38')

try:
    import imagesize
except ImportError:
    imagesize = None

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("WeasyPrint")
    needs_plugins = ["lino.modlib.jinja"]

    header_height = 20
    footer_height = 20
    top_right_width = None
    page_background_image = None
    top_right_image = None
    bottom_left_image = None
    bottom_left_width = None
    header_image = None
    margin = 10
    margin_left = 17
    margin_right = 10
    space_before_recipient = 15
    with_bulma = False

    def get_needed_plugins(self):
        for p in super().get_needed_plugins():
            yield p
        if self.with_bulma:
            yield 'bulma'

    def get_requirements(self, site):
        yield "imagesize"
        if self.with_bulma:
            yield 'django-bulma'

    def pre_site_startup(self, site):
        fcf = site.confdirs.find_config_file
        for ext in ("jpg", "png"):
            if self.bottom_left_image is None:
                if fn := fcf("bottom-left." + ext, "weasyprint"):
                    self.bottom_left_image = fn
            if self.top_right_image is None:
                if fn := fcf("top-right." + ext, "weasyprint"):
                    self.top_right_image = fn
            if self.header_image is None:
                if fn := fcf("header." + ext, "weasyprint"):
                    # site.logger.info("Found header_image %s", fn)
                    self.header_image = fn
            if self.page_background_image is None:
                if fn := fcf("page-background." + ext, "weasyprint"):
                    # site.logger.info("Found page_background_image %s", fn)
                    self.page_background_image = fn
        if self.header_height:
            if self.top_right_image and not self.top_right_width:
                # if imagesize is None:
                #     site.logger.warning("imagesize is not installed")
                #     continue
                w, h = imagesize.get(self.top_right_image)
                self.top_right_width = self.header_height * w / h
        if self.footer_height:
            if self.bottom_left_image and not self.bottom_left_width:
                # if imagesize is None:
                #     site.logger.warning("imagesize is not installed")
                #     continue
                w, h = imagesize.get(self.bottom_left_image)
                self.bottom_left_width = self.footer_height * w / h
        super().pre_site_startup(site)
