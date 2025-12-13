# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.utils.soup import sanitized_soup
import re

TOC_MARKER = "=TOC="

COLLAPSIBLE_TOC = False


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s


def replace_toc(html):
    if TOC_MARKER not in html:
        return html
    if settings.SITE.sidebar_width:
        return html.replace(TOC_MARKER, "")
    soup = sanitized_soup(html)
    toc_tag = None
    level = None
    headers = []
    for tag in soup.children:
        if tag.name is None:
            # print(f"Oops: {repr(tag)}")
            continue
        tag_name = tag.name.lower()
        if tag.string and tag.string.strip() == TOC_MARKER:
            tag.clear()
            toc_tag = tag
            continue
        elif level is None and tag_name in {"h1", "h2", "h3"}:
            level = tag_name
        if tag_name == level:
            headers.append(tag)
            # todo add an anchor and a backlink
            # if tag.contents[-1].name == "a"
            # <a class="headerlink" href="#kuhu-minna" title="Link to this heading">¶</a>
        # else:
        #     print(20251102, tag)

    if toc_tag and len(headers) > 1:
        # print("20251102", headers)
        toc_tag['id'] = "contents"
        ul = soup.new_tag('ul')
        for i, htag in enumerate(headers):
            text = str(htag.string)
            slug = slugify(text)
            backref = "toc" + str(i+1)
            a = soup.new_tag('a', href="#"+slug, id=backref, string=text)
            li = soup.new_tag('li')
            li.append(a)
            ul.append(li)
            htag.append(soup.new_tag(
                'a', href="#"+backref, title="Jump back to the TOC", string="¶"))
            htag['id'] = slug
            # print(20251102, slug)

        if True:  # needs bootstrap
            # toggle = soup.new_tag('button', **{
            if COLLAPSIBLE_TOC:
                toggle = soup.new_tag('button', **{
                    'class': "btn btn-primary btn-sm",
                    'type': "button",
                    'role': "button",
                    'data-bs-toggle': "collapse",
                    'data-bs-target': "#tableOfContents",
                    # 'data-bs-toggle': "button",
                    'aria-expanded': "false",
                    'aria-controls': "tableOfContents",
                    'string': "show"
                })
                toc = soup.new_tag('div', **{
                     'class': "collapse",
                     'id': "tableOfContents"})
                toc.append(ul)
            else:
                toc = ul
            ctext = soup.new_tag('div', **{
                 'class': "card-text"})
            ctext.append(toc)
            cbody = soup.new_tag('div', **{
                 'class': "card-body",
                 'width': "30rem"})
            cbody.append("Table of contents: ")
            if COLLAPSIBLE_TOC:
                cbody.append(toggle)
            cbody.append(ctext)
            card = soup.new_tag('div', **{
                 'class': "card",
                 'width': "30rem"})
            card.append(cbody)
            toc_tag.append(card)
        else:
            toc_tag.append(ul)
        # print("20251102 b", headers)

    return str(soup)
