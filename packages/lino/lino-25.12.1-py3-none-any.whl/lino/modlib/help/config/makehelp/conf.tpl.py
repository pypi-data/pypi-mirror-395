# -*- coding: utf-8 -*-
# fmt: off

from pathlib import Path

docs_path = Path('../docs').resolve()

templates_path = []  # will be populated by lino.sphinxcontrib.configure()
intersphinx_mapping = {}

{% if makehelp.language.index == 0 -%}

html_context = dict(public_url="{{settings.SITE.server_url}}/media/cache/help")

from rstgen.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure ; configure(globals())

project = "{{settings.SITE.title}}"
html_title = "{{settings.SITE.title}}"

{% if settings.SITE.plugins.contacts.site_owner %}
import datetime
copyright = "{} {{settings.SITE.plugins.contacts.site_owner}}".format(
    datetime.date.today())
{% endif %}

extensions += ['lino.sphinxcontrib.logo']

{% else -%}{# elif makehelp.language.index == 0 -#}

fn = docs_path / 'conf.py'
with open(fn, "rb") as fd:
    exec(compile(fd.read(), fn, 'exec'))

{%- endif %}

language = '{{makehelp.language.django_code}}'

pth = docs_path / ".templates"
assert pth.exists()
templates_path.insert(0, str(pth.resolve()))

# print("20230314 intersphinx_mapping is", intersphinx_mapping)
