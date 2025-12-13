# -*- coding: UTF-8 -*-
# Copyright 2006-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See introduction in :doc:`/specs/memo`.

TODO:

- the auto-completer might insert the full text into the editor after the
  pattern. The user can then decide whether to leave it or not.

- The memo commands might also be defined as suggesters with a trigger of type
  "[ticket ". Note that in that case we need to add a new attribute "suffix",
  which would be empty for # and @ but "]" for memo commands.

"""
from etgen import etree
from django.conf import settings
# from lino import logger
import re
import traceback
from typing import Callable, Any
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


# COMMAND_REGEX = re.compile(r"\[(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")
#                                         ===...... .......=
COMMAND_REGEX = re.compile(r"(\\?\[)(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")
#                                            ===...... .......=

EVAL_REGEX = re.compile(r"\[=((?:[^[\]]|\[.*?\])*?)\]")


class Suggester:
    """

    Holds the configuration for the behaviour of a given "trigger".

    Every value of :attr:`Parser.suggesters` is an instance of this.

    """

    def __init__(
        self,
        trigger,
        data,
        fldname,
        formatter=str,
        value=lambda x, y: getattr(x, y),
        getter=None,
    ):
        """
        `trigger` is a short text, usually one character, like "@" or "#",
        which will trigger a list of autocomplete suggestions to pop up.

        `func` is a callable expected to yield a series of suggestions to be
        displayed in text editor.

        Every suggestion is expected to be a tuple `(abbr, text)`, where `abbr`
        is the abbreviation to come after the trigger (e.g. a username or a
        ticket number), and text is a full description of this suggestion to be
        displayed in the list.

        Usage examples: see :mod:`lino_xl.lib.tickets` and :mod:`lino.modlib.users`

        """
        self.trigger = trigger
        if len(trigger) != 1:
            raise Exception("Trigger text must be exactly 1 character.")
        self.data = data
        self.fldname = fldname
        self.formatter = formatter
        self.value = value

        if getter is None:

            def getter(abbr):
                return data.get(**{fldname: abbr})

        self.getter = getter

    def get_suggestions(self, query=""):
        flt = self.data.model.quick_search_filter(query)
        for obj in self.data.filter(flt)[:5]:
            # v = self.formatter(obj)
            yield {
                "value": self.value(obj, self.fldname),
                "title": self.formatter(obj),
                "link": self.get_href(obj),
            }

    def get_object(self, abbr):
        return self.getter(abbr)

    def get_href(self, obj, ar=None):
        da = obj.get_detail_action(ar)
        return (
            r"javascript:window.App.runAction({"
            + f"'actorId': '{self.formatter(da.actor)}', "
            + f"'action_full_name': '{da.action.full_name()}', "
            + "'rp': null, "
            + r"'status': {"
            + f"'record_id': {self.formatter(obj.pk)}"
            + r"}"
            + r"})"
        )


class Parser:
    """The memo parser."""

    safe_mode = False

    def __init__(self, **context):
        self.commands = dict()
        self.context = context
        self.suggesters = dict()

    def add_suggester(self, *args, **kwargs):
        """
        Add a :class:`Suggester` (see there for args and kwargs).

        """

        s = Suggester(*args, **kwargs)
        if s.trigger in self.suggesters:
            raise Exception("Duplicate suggester for {}".format(s.trigger))
        self.suggesters[s.trigger] = s

    def compile_suggester_regex(self):
        triggers = "".join(
            [
                r"\\" if key in r"[\^$.|?*+(){}" else "" + key
                for key in self.suggesters.keys()
            ]
        )
        return re.compile(r"([^\w])?([" + triggers + r"])(\w+)")

    def register_command(self, cmdname, func: Callable[[Any, str, str, dict], None]):
        """Register a memo command identified by the given text `cmd`.

        `func` is the command handler.  It must be a callable that will be
        called with two positional arguments `ar` and `params`.

        """
        # print("20170210 register_command {} {}".format(cmdname, func))
        existing_func = self.commands.get(cmdname, None)
        if existing_func is not None:
            if issubclass(func._for_model, existing_func._for_model):
                return
            if not issubclass(existing_func._for_model, func._for_model):
                raise Exception(
                    "Duplicate definition of memo command '{}'".format(cmdname)
                )
        self.commands[cmdname] = func

    def register_django_model(self, name, model, cmd=None, rnd=None):
        """
        Register the given string `name` as command for referring to
        database rows of the given Django database model `model`.

        Optional keyword arguments are

        - `cmd` the command handler used by :meth:`parse`
        """
        # print("20170210 register_django_model {} {}".format(name, model))
        # if rnd is None:
        #     def rnd(obj):
        #         return "[{} {}] ({})".format(name, obj.id, title(obj))
        if rnd is None:
            rnd = model.memo2html
        if cmd is None:

            def cmd(ar, s, cmdname, mentions, context):
                # args = s.split(None, 1)
                pk, text = split_name_rest(s)

                # ar = parser.context.get('ar', None)
                # kw = dict()
                # dd.logger.info("20161019 %s", ar.renderer)
                # if text:
                #     kw.update(title=text)
                pk = int(pk)
                obj = model.objects.get(pk=pk)

                if mentions is not None:
                    mentions.add(obj)
                # if usages.get(cmdname, None) is None:
                #     usages[cmdname] = [obj]
                # else:
                #     usages[cmdname].append(obj)

                # try:
                # except model.DoesNotExist:
                #     return "[{} {}]".format(name, s)
                # if not caption:
                #     caption = obj.get_memo_title()
                # txt = "#{0}".format(obj.id)
                # kw.update(title=title(obj))
                # return obj.memo2html(ar, text)
                return rnd(obj, ar, text)
                # e = ar.obj2html(obj, txt, **kw)
                # # return str(ar)
                # return etree.tostring(e)

        # if manage_usage is None:
        #     def manage_usage(ar, cmdusages=[]):
        #         pass

        cmd._for_model = model
        if cmd.__doc__ is None:
            cmd.__doc__ = rnd.__doc__ or """
Insert a reference to the specified {}.

The first argument is mandatory and specifies the primary key.
All remaining arguments are used as the text of the link.
""".format(model._meta.verbose_name)

        self.register_command(name, cmd)
        # if manage_usage is not None:
        #     self.register_usage_manager(name, manage_usage)
        # self.register_renderer(model, rnd)

    def eval_match_func(self, context):
        def func(matchobj):
            expr = matchobj.group(1)
            try:
                return self.format_value(eval(expr, context))
            except Exception as e:
                # raise
                # don't log an exception because that might cause lots of
                # emails to the admins.
                # logger.warning(e)
                return self.handle_error(matchobj, e)

        return func

    def format_value(self, v):
        if etree.iselement(v):
            return str(etree.tostring(v))
        return str(v)

    def get_referred_objects(self, text):
        """
        Yield all database objects referred in the given `text` using a
        suggester.
        """
        regex = self.compile_suggester_regex()
        all_matches = re.findall(regex, text)
        for match in all_matches:
            suggester = self.suggesters[match[1]]
            try:
                yield suggester.get_object(match[2])
            except Exception:
                pass  #

    def suggester_match_func(self, ar):
        def func(matchobj):
            whitespace = matchobj.group(1)
            whitespace = "" if whitespace is None else whitespace
            trigger = matchobj.group(2)
            abbr = matchobj.group(3)
            suggester = self.suggesters[
                trigger
            ]  # can't key error as regex is created from the keys
            try:
                obj = suggester.get_object(abbr)
                return whitespace + ar.obj2htmls(obj, trigger + abbr, title=str(obj))
            except Exception as e:
                # likely a mismatch or bad pk, return full match
                # return self.handle_error(matchobj, e)
                return matchobj.group(0)

        return func

    def cmd_match_func(self, ar, mentions, context):
        def func(matchobj):
            if matchobj.group(1).startswith("\\"):
                return matchobj.group(0)[1:]
            cmd = matchobj.group(2)
            cmdh = self.commands.get(cmd, None)
            if cmdh is None:
                return matchobj.group(0)

            params = matchobj.group(3)
            params = params.replace("\\\n", " ")
            params = params.replace("\xa0", " ")
            params = params.replace("\u200b", " ")
            params = params.replace("&nbsp;", " ")
            params = str(params.strip())
            try:
                return self.format_value(cmdh(ar, params, cmd, mentions, context))
            except Exception as e:
                # raise
                # logger.warning(e)
                # don't log an exception because that might cause lots of
                # emails to the admins.
                return self.handle_error(matchobj, e)

        return func

    def handle_error(self, mo, e):
        # ~ return mo.group(0)
        msg = "[ERROR %s in %r at position %d-%d]" % (
            e,
            mo.group(0),
            mo.start(),
            mo.end(),
        )
        # raise Exception(msg) from e
        # logger.debug(msg)
        # print(msg, ":")
        traceback.print_exc()
        return msg

    def parse_suggestions(self, src):
        soup = BeautifulSoup(src, "html.parser")
        while True:
            mention = soup.find("span", attrs={"class": "mention"})
            if mention is None:
                break
            attrs = mention.attrs
            link = attrs["data-link"]
            title = attrs["data-title"]
            value = mention.text
            sanitized_mention = BeautifulSoup(
                f'<a href="{link}" title="{title}">{value}</a>', "html.parser"
            )
            soup.find("span", attrs={"class": "mention"}).replaceWith(sanitized_mention)
        return str(soup)

    def simplify_suggestions(self, src):
        soup = BeautifulSoup(src, "html.parser")
        while True:
            mention = soup.find("span", attrs={"class": "mention"})
            if mention is None:
                break
            soup.find("span", attrs={"class": "mention"}).replaceWith(
                BeautifulSoup(mention.text, "html.parser")
            )
        return str(soup)

    def parse(self, src, ar=None, context=None, mentions=None):
        """
        Parse the given string `src`, replacing memo commands by their
        result.

        `ar` is the action request asking to parse. User permissions and
        front-end renderer of this request apply.

        `context` is a dict of variables to make available when parsing
        expressions in safe mode.

        If `mentions` is specified, it should be a :class:`set` to collect
        mentioned database objects.

        """
        if ar is None:
            ar = settings.SITE.plugins.memo.ar

        ctx = dict()
        ctx.update(self.context)
        if context is not None:
            ctx.update(context)

        if self.suggesters:
            src = self.simplify_suggestions(src)
            regex = self.compile_suggester_regex()
            mf = self.suggester_match_func(ar)
            src = regex.sub(mf, src)

        src = COMMAND_REGEX.sub(self.cmd_match_func(ar, mentions, ctx), src)

        if not self.safe_mode:
            # run-time context overrides the global parser context
            ctx.update(ar=ar, settings=settings)
            src = EVAL_REGEX.sub(self.eval_match_func(ctx), src)
        return src


# def split_name_rest(s: str) -> tuple[str, str]:  fails in Python 3.7
def split_name_rest(s: str):
    s = s.split(None, 1)
    return (s[0], s[1]) if len(s) == 2 else (s[0], None)
