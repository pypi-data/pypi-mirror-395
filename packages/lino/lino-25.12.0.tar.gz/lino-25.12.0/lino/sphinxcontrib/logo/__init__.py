# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Sets the `html_logo` and `html_favicon` for all Lino-related sites.

Using this extension currently means that you cannot set these config
settings yourself.

Also adds some css styling.


"""

from pathlib import Path
from sphinx.util.fileutil import copy_asset_file

static_path = (Path(__file__).parent / "static").absolute()
tpl_path = (Path(__file__).parent / "templates").absolute()
assert (tpl_path / "footer.html").exists()


def config_inited(app, config):
    """Define certain settings"""
    # print("20240224 config_inited")
    # raise Exception("20230616")
    config.html_static_path.append(str(static_path))

    # config.html_logo = str(static_path / 'logo_web3.png')
    # config.html_favicon = str(static_path / 'favicon.ico')

    # pth = Path("../docs/.templates").resolve()
    config.templates_path.insert(0, str(tpl_path))
    config.html_sidebars = {"**": []}
    config.html_favicon = str(static_path / "favicons/favicon.ico")

    # for logo_file in ['synodalsoft-logo.svg']:
    #     tpl_path /
    #     src_dir = Path('../docs/dl').resolve()
    #     static_dir = Path('../docs/.static').resolve()
    #     static_logo_file = static_dir / logo_file
    #     if not static_logo_file.exists():
    #         static_logo_file.symlink_to(src_dir / logo_file)


def copy_custom_files(app, env, docnames):
    if app.builder.format == "html":
        # In older Sphinx version the builder.outdir was a simple string
        staticdir = Path(app.builder.outdir) / "_static"
        staticdir.mkdir(exist_ok=True)
        (staticdir / "favicons").mkdir(exist_ok=True)
        for fn in ("synodal-logo.png", "favicons/favicon.ico"):
            # print("20240224 Copy", static_path / fn, "to", staticdir / fn)
            copy_asset_file(static_path / fn, staticdir / fn)


def setup(app):
    # app.add_css_file('linodocs.css')
    # app.add_stylesheet('centeredlogo.css')
    # app.connect('builder-inited', builder_inited)
    app.connect("config-inited", config_inited)
    # app.connect('build-finished', copy_custom_files)
    app.connect("env-before-read-docs", copy_custom_files)
