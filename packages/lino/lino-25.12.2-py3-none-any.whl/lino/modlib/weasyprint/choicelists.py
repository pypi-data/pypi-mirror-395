# -*- coding: UTF-8 -*-
# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods
from lino.api import dd

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

BULMA_CSS = None

if dd.plugins.weasyprint.with_bulma:

    # Bulma causes weayprint to issue many warnings, more than 2000 during one
    # tested doc. So we deactivate them:
    from weasyprint.logger import LOGGER, logging
    LOGGER.setLevel(logging.ERROR)

    try:
        from pathlib import Path
        import bulma
        from weasyprint import CSS
        BULMA_CSS = Path(bulma.__file__).parent / "static/bulma/css/style.min.css"
        assert BULMA_CSS.exists()
    except ImportError:
        pass
# else:
#
#     from weasyprint.logger import LOGGER, logging
#     LOGGER.setLevel(logging.DEBUG)
#     LOGGER.addHandler(logging.StreamHandler())  # show messages on console


class WeasyBuildMethod(JinjaBuildMethod):
    template_ext = ".weasy.html"
    templates_name = "weasy"
    default_template = "default.weasy.html"


class WeasyHtmlBuildMethod(WeasyBuildMethod):
    target_ext = ".html"
    name = "weasy2html"


class WeasyPdfBuildMethod(WeasyBuildMethod):
    target_ext = ".pdf"
    name = "weasy2pdf"

    def html2file(self, html, filename, context):
        pdf = HTML(string=html)  # , base_url=settings.SITE.site_dir)
        if BULMA_CSS and context.get('use_bulma_css', False):
            pdf.write_pdf(
                filename, stylesheets=[CSS(filename=BULMA_CSS)])
        else:
            pdf.write_pdf(filename)


add = BuildMethods.add_item_instance
add(WeasyHtmlBuildMethod())
add(WeasyPdfBuildMethod())
