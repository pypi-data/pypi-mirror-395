# -*- coding: UTF-8 -*-
# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# See https://dev.lino-framework.org/src/lino/utils/soup.html

# Inspired by
# https://chase-seibert.github.io/blog/2011/01/28/sanitize-html-with-beautiful-soup.html
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
# https://www.geeksforgeeks.org/python-check-url-string/

# TODO: Explain why we don't use Django's Truncator instead of this.
# from django.utils.text import Truncator
# def truncate_comment(html_str, max_length=300):
#     return Truncator(html_str).chars(max_length, html=True)


import re
from html import escape
from urllib.parse import urlparse
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
from django.conf import settings

MORE_INDICATOR = "..."
MORE_MARKER = "=MORE="
DATA_UPLOAD_ID = "data-upload_id"
HEADER_REGEX = re.compile("h[0-9]{1}")

URL_REGEX = re.compile(
    r'([^"]|^)(https?:\/\/)((www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
)

# URL_REGEX = re.compile(r'([^"])(https?://\S+|www\.\S+)')


def urlrepl(match):
    url = match[2] + match[3]
    # raise Exception(repr(url))
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return match[1] + f'<a href="{url}" target="_blank">{match[3]}</a>'
    return match[0]


def url2a(s):
    return URL_REGEX.sub(urlrepl, s)


PARAGRAPH_TAGS = {
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "h7",
    "h8",
    "h9",
    "pre",
    "li",
    "div",
}

WHITESPACE_TAGS = PARAGRAPH_TAGS | {
    "[document]",
    "ul",
    "ol",
    "html",
    "head",
    "body",
    "base",
}

SHORT_PREVIEW_IMAGE_HEIGHT = "8em"
REMOVED_IMAGE_PLACEHOLDER = "⌧"


class Style:
    # TODO: Extend rstgen.sphinxconf.sigal_image.Format to incoroporate this.
    def __init__(self, s):
        self._map = {}
        if s:
            for i in s.split(";"):
                k, v = i.split(":", maxsplit=1)
                self._map[k.strip()] = v.strip()
        self.is_dirty = False

    def __contains__(self, *args):
        return self._map.__contains__(*args)

    def __setitem__(self, k, v):
        if k in self._map and self._map[k] == v:
            return
        self._map[k] = v
        self.is_dirty = True

    def __delitem__(self, k):
        if k in self._map:
            self.is_dirty = True
        return self._map.__delitem__(k)

    def adjust_size(self):
        # if self['float'] == "none":
        #     return
        if True:
            self["width"] = "auto"
        else:
            if "width" in self._map:
                del self["width"]
        self["height"] = SHORT_PREVIEW_IMAGE_HEIGHT

    def as_string(self):
        return ";".join(["{}:{}".format(*kv) for kv in self._map.items()])


# def truncate_soup(soup, max_length=None):
#     elems = []
#     found_image = False
#     remaining = max_length or settings.SITE.plugins.memo.short_preview_length
#     stop = False
#     for ch in soup:
#         if ch.name == "img":
#             if found_image:
#                 continue
#             style = Style(ch.get("style", None))
#             if not "float" in style:
#                 style["float"] = "right"
#             style.adjust_size()
#             if style.is_dirty:
#                 ch["style"] = style.as_string()
#             found_image = True
#             elems.append(ch)
#             continue
#
#         if ch.string is not None:
#             strlen = len(ch.string)
#             if strlen > remaining:
#                 stop = True
#                 end_text = ch.string[:remaining] + "..."
#                 ch.string.replace_with(end_text)
#             elems.append(ch)
#             remaining -= strlen
#     if isinstance(ch, Tag):
#         for c in ch.children:
#             if c.name in PARAGRAPH_TAGS:
#                 c.unwrap()
#
#         if stop:


class TextCollector:
    def __init__(self, max_length=None):
        self.text = ""
        self.sep = ""  # becomes " " after WHITESPACE_TAGS
        self.remaining = max_length or settings.SITE.plugins.memo.short_preview_length
        self.found_image = False

    def add_chunk(self, ch):
        # print(f"20250207 add_chunk {ch.__class__} {ch.name} {ch}")
        # if isinstance(ch, Tag):
        if ch.name in WHITESPACE_TAGS:
            # for c in ch.contents:
            # for c in ch:
            for c in ch.children:
                if not self.add_chunk(c):
                    return False
            # if ch.name in PARAGRAPH_TAGS:
            #     # self.sep = "\n\n"
            #     self.sep = "<br/>"
            # else:
            #     self.sep = " "
            self.sep = " "
            return True

        # assert ch.name != "IMG"
        we_want_more = True

        # print(f"20250207c add_chunk {ch.__class__} {ch}")

        # Ignore all images except the first one. And for the first one we
        # enforce our style.
        if ch.name == "img":
            if self.found_image:
                # self.text += self.sep
                self.text += REMOVED_IMAGE_PLACEHOLDER
                return True
            self.found_image = True
            style = Style(ch.get("style", None))
            if "float" not in style:
                style["float"] = "right"
            style.adjust_size()
            if style.is_dirty:
                ch["style"] = style.as_string()
            # print("20231023 a", ch)

        elif ch.string is not None:
            text = ch.string
            if self.sep == "" and self.text == "":
                text = text.lstrip()
            strlen = len(text)
            if strlen > self.remaining:
                we_want_more = False
                text = text[:self.remaining] + MORE_INDICATOR
                # raise Exception(f"20250208 {strlen} > {self.remaining} {end_text}")
            self.remaining -= strlen
            # print(f"20250606 {text} becomes {escape(text, quote=False)}")
            text = escape(text, quote=False)
            if isinstance(ch, NavigableString):
                # ch = NavigableString(end_text)
                ch = text
            else:
                ch.string.replace_with(text)

        # if isinstance(ch, NavigableString):
        #     self.text += self.sep + ch.string
        # else:
        #     self.text += self.sep + str(ch)
        self.text += self.sep + str(ch)
        self.remaining -= len(self.sep)
        # self.remaining -= 1  # any separator counts as 1 char
        self.sep = ""
        return we_want_more


# remove these tags including their content.
blacklist = frozenset(["script", "style", "head"])

# unwrap these tags (remove the wrapper and leave the content)
unwrap = frozenset(["html", "body"])

useless_main_tags = frozenset(["p", "div", "span"])

ALLOWED_TAGS = frozenset([
    "a",
    "b",
    "i",
    "em",
    "ul",
    "ol",
    "strong",
    "br",
    "span",
    "def",
    "img",
    "table",
    "th",
    "tr",
    "td",
    "thead",
    "tfoot",
    "tbody",
    "colgroup",
    "col",
]) | PARAGRAPH_TAGS

GENERALLY_ALLOWED_ATTRS = {"title", "style", "class", "id"}


# Map of allowed attributes by tag. Originally copied from bleach.sanitizer.
ALLOWED_ATTRIBUTES = {
    "a": {"href", "target"} | GENERALLY_ALLOWED_ATTRS,
    "img": {"src", "alt", "width", "height", DATA_UPLOAD_ID} | GENERALLY_ALLOWED_ATTRS,
}

ALLOWED_ATTRIBUTES["span"] = GENERALLY_ALLOWED_ATTRS | {
    # "data-index",
    # "data-denotation-char",
    # "data-link",
    # "data-title",
    # "data-value",
    "contenteditable",
}

ALLOWED_ATTRIBUTES["p"] = GENERALLY_ALLOWED_ATTRS | {"align"}
ALLOWED_ATTRIBUTES["col"] = GENERALLY_ALLOWED_ATTRS | {"width"}
ALLOWED_ATTRIBUTES["td"] = GENERALLY_ALLOWED_ATTRS | {"rowspan", "colspan"}

# def safe_css(attr, css):
#     if attr == "style":
#         return re.sub("(width|height):[^;]+;", "", css)
#     return css

PARSER = 'lxml'

SANITIZERS = []


def register_sanitizer(func):
    SANITIZERS.append(func)


def beautiful_soup(htmlstr):
    if not htmlstr.startswith("<"):
        htmlstr = f"<p>{htmlstr}</p>"
    htmlstr = url2a(htmlstr)
    return BeautifulSoup(htmlstr, features=PARSER)


def sanitized_soup(htmlstr, save=False, ar=None, mentions=None):
    soup = beautiful_soup(htmlstr)
    for tag in soup.find_all():
        # print(tag)
        tag_name = tag.name.lower()
        if tag_name in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()
        elif tag_name in unwrap:
            tag.unwrap()
        elif tag_name in ALLOWED_TAGS:
            # tag is allowed. Make sure all the attributes are allowed.
            allowed = ALLOWED_ATTRIBUTES.get(tag_name, GENERALLY_ALLOWED_ATTRS)
            tag.attrs = {
                k: v for k, v in tag.attrs.items()
                if k.startswith('data-') or k in allowed}
        else:
            # print(tag.name)
            # tag.decompose()
            # tag.extract()
            # not a whitelisted tag. I'd like to remove it from the tree
            # and replace it with its children. But that's hard. It's much
            # easier to just replace it with an empty span tag.
            tag.name = "span"
            tag.attrs = dict()

    # remove all comments because they might contain scripts
    comments = soup.find_all(text=lambda t: isinstance(t, (Comment, Doctype)))
    for comment in comments:
        comment.extract()

    for func in SANITIZERS:
        func(soup, save=save, ar=ar, mentions=mentions)

    # remove the wrapper tag if it is useless
    # if len(soup.contents) == 1:
    #     main_tag = soup.contents[0]
    #     if main_tag.name in useless_main_tags and not main_tag.attrs:
    #         main_tag.unwrap()

    return soup


def sanitize(htmlstr, **kwargs):
    # if len(chunks := htmlstr.split(MORE_MARKER, 1)) == 2:
    #     htmlstr = " ".join(chunks)
    htmlstr = htmlstr.strip()
    if htmlstr == "":
        return htmlstr
    soup = sanitized_soup(htmlstr, **kwargs)
    # insert_toc(soup)
    return str(soup).strip()


def truncate_comment(htmlstr, max_length=300, **kwargs):
    # new implementation since 20230713
    if len(chunks := htmlstr.split(MORE_MARKER, 1)) == 2:
        htmlstr = chunks[0]
    htmlstr = htmlstr.strip()  # remove leading or trailing newlines
    if htmlstr == '':
        return htmlstr
    soup = sanitized_soup(htmlstr, **kwargs)
    tc = TextCollector(max_length)
    tc.add_chunk(soup)
    return tc.text.strip()
