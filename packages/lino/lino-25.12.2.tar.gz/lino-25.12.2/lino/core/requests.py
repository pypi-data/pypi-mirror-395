# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
See introduction in :doc:`/dev/ar` and API reference in
:class:`lino.api.core.Request`.
"""

# from past.utils import old_div

import sys
import json
import logging
from io import StringIO
from lino import logger
from contextlib import contextmanager
from types import GeneratorType
from copy import deepcopy
from xml.sax.saxutils import escape
from etgen import html as xghtml

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from django.utils.translation import get_language, activate
from django.utils.html import format_html
from django.utils import translation
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.core import exceptions
from django.db import models
from django.db.models.query import QuerySet
from asgiref.sync import sync_to_async

from lino.utils.html import E, tostring, mark_safe
from lino.utils import AttrDict
from lino.utils import capture_output
from lino.utils import MissingRow
from lino.utils.html import html2text
from lino.core import constants
from lino.core import callbacks
from lino.core import actions
from lino.core.tables import AbstractTable
from lino.core.boundaction import BoundAction
from lino.core.signals import on_ui_created, pre_ui_save
from lino.core.diff import ChangeWatcher
from lino.core.utils import getrqdata
from lino.core.utils import obj2unicode
from lino.core.utils import obj2str
from lino.core.utils import format_request
from lino.core.utils import PhantomRow
from lino.core.atomizer import get_atomizer

# try:
#     from django.contrib.contenttypes.models import ContentType
# except RuntimeError:
#     pass

if settings.SITE.is_installed("contenttypes"):
    from django.contrib.contenttypes.models import ContentType
else:
    ContentType = None

from lino.core.vfields import FakeField, TableRow, RemoteField


CATCHED_AJAX_EXCEPTIONS = (Warning, exceptions.ValidationError)

PRINT_EMAIL = """send email
Sender: {sender}
To: {recipients}
Subject: {subject}

{body}
"""


def noop(ar):
    return ar.success(gettext("Aborted"))


def mi2bp(master_instance, bp):
    if master_instance is not None:
        if isinstance(master_instance, (models.Model, TableRow)):
            bp[constants.URL_PARAM_MASTER_PK] = master_instance.pk
            if ContentType is not None and isinstance(
                master_instance, models.Model
            ):
                assert not master_instance._meta.abstract
                mt = ContentType.objects.get_for_model(
                    master_instance.__class__).pk
                bp[constants.URL_PARAM_MASTER_TYPE] = mt
            # else:
            #     logger.warning("20141205 %s %s",
            #                    self.master_instance,
            #                    ContentType)
        else:  # if self.master is None:
            # e.g. in accounting.MovementsByMatch the master is a `str`
            bp[constants.URL_PARAM_MASTER_PK] = master_instance
            # raise Exception("No master key for {} {!r}".format(
            #     self.master_instance.__class__, self.master_instance))


class PrintLogger(logging.Logger):
    format = "%(message)s"

    def __init__(self, level):
        super().__init__("~", level)
        h = logging.StreamHandler(stream=sys.stdout)
        h.setFormatter(logging.Formatter(self.format))
        self.addHandler(h)
        # print("20231012", logging.getLevelName(self.level), self.__class__)


class StringLogger(logging.Logger):
    # Instantiated by BaseRequest.capture_logger()

    # format = '%(levelname)s: %(message)s'
    # format = '%(levelname)s:%(name)s: %(message)s'
    format = "%(message)s"

    def __init__(self, parent, level):
        super().__init__(parent.name + "~", level)
        self.parent = parent
        self.streamer = StringIO()
        h = logging.StreamHandler(stream=self.streamer)
        h.setFormatter(logging.Formatter(self.format))
        self.addHandler(h)
        # print("20231012", logging.getLevelName(self.level), self.__class__)

    # def handle(self, record):
    #     # print("20231012 handle", record)
    #     assert self.parent is None
    #     super().handle(record)
    #     if True:  # logger.isEnabledFor(self.level):
    #         logger.handle(record)

    def getvalue(self):
        return self.streamer.getvalue()

    # def __str__(self):
    #     return self.streamer.getvalue()


class ValidActionResponses(object):
    """
    These are the allowed keyword arguments for :meth:`ar.set_response
    <BaseRequest.set_response>`, and the action responses supported by
    :js:func:`Lino.handle_action_result` (defined in
    :xfile:`linolib.js`).

    This class is never instantiated, but used as a placeholder for
    these names and their documentation.
    """

    message = None
    """
    A translatable message text to be shown to the user.
    """

    alert = None
    """
    Set this to some translatable text to specify that the message is rather
    important and should alert and should be presented in a dialog box to be
    confirmed by the user. The text is used as the title of the alert box.  If
    you specify `True`, then Lino uses a default text like "Alert" or "Warning"
    (depending on context).
    """
    alert_eval_js = None
    """
    Javascript code to be evaluated after the confirmation of the alert dialog.
    """

    success = None

    errors = None
    html = None

    rows = None
    """An iterable of database objects that will be serialized as a list.
    """

    no_data_text = None
    title = None
    """The dynamic title to give to the window or component that shows this response.
    TODO: is this still being used?
    """

    count = None
    """The number of rows in a list response."""

    navinfo = None
    data_record = None
    """
    Certain requests are expected to return detailed information about
    a single data record. That's done in :attr:`data_record` which
    must itself be a dict with the following keys:

    - id : the primary key of this record_deleted
    - title : the title of the detail window
    - data : a dict with one key for every data element
    - navinfo : an object with information for the navigator
    - disable_delete : either null (if that record may be deleted, or
      otherwise a message explaining why.

    """

    record_id = None
    """
    When an action returns a `record_id`, it asks the user interface to
    jump to the given record.
    """

    refresh = None
    refresh_delayed_value = None
    """
    A string referencing an actor_id corresponding to a DelayedValue equivalent element
    or boolean `True` meaning all the DelayedValue(s) should be refreshed.
    """
    refresh_all = None
    close_window = None
    record_deleted = None
    clear_site_cache = None

    xcallback = None
    """
    Used for dialogs asking simple yes/no/later style questions.
    Includes all the data the client needs in order to send the same action
    request again, but with some extra confirmation values.

    Is a dict which includes the following values:

    - actor_id : The id of the actor
    - an : The action name of the action which was run
    - sr : List of selected values
    """

    goto_url = None
    """
    Leave current page and go to the given URL.

    In react, this works within the URLContext object (within
    the hash router context but NOT in browser native location
    object) where url must match the
    route "/api/:packId/:actorId/:pk?/:fieldName?" or "/"
    """

    open_url = None
    """
    Open the given URL in a new browser window.
    """

    replace_url = None
    """
    Open the given URL in the current browser window overriding
    the current url.

    In react, unlike `goto_url` this overrides the browser native
    location object (sets href on it).
    """

    master_data = None

    open_webdav_url = None
    info_message = None
    warning_message = None
    "deprecated"

    eval_js = None
    active_tab = None

    detail_handler_name = None
    """
    The name of the detail handler to be used.  Application code should
    not need to use this.  It is automatically set by
    :meth:`ActorRequest.goto_instance`.
    """

    version_mismatch = False

    editing_mode = False


inheritable_attrs = frozenset(
    ["user", "subst_user", "renderer", "requesting_panel", "master_instance",
     "logger", "show_urls"])


def bool2text(x):
    if x:
        return _("Yes")
    return _("No")


class SearchQuerySet:
    pass


class SearchQuery:
    pass


if settings.SITE.is_installed("search"):
    if settings.SITE.use_elasticsearch:
        try:
            from elasticsearch_django.models import SearchQuery
        except ImportError:
            pass
    elif settings.SITE.use_solr:
        try:
            from haystack.query import SearchQuerySet
        except ImportError:
            pass

WARNINGS_LOGGED = dict()


def column_header(col):
    # ~ if col.label:
    # ~ return join_elems(col.label.split('\n'),sep=E.br)
    # ~ return [unicode(col.name)]
    label = col.get_label()
    if label is None:
        return col.name
    return str(label)


def sliced_data_iterator(qs, offset, limit):
    # qs is either a Django QuerySet or iterable
    # When limit is None or 0, offset cannot be -1
    if offset is not None:
        if isinstance(qs, QuerySet):
            num = qs.count()
        else:
            num = len(qs)
        if offset == -1:
            page_num = num // limit
            offset = limit * page_num
        qs = qs[offset:num]
    if limit is not None and limit != 0:
        qs = qs[:limit]
    return qs


class BaseRequest:
    # Base class of all :term:`action requests <action request>`.
    user = None
    subst_user = None
    renderer = None
    actor = None
    action_param_values = None
    param_values = None
    bound_action = None
    known_values = None
    no_data_text = _("No data to display")
    is_on_main_actor = True
    permalink_uris = False
    show_urls = True
    master = None
    master_instance = None
    request = None
    selected_rows = []
    obvious_fields = None
    order_by = None
    filter = None
    gridfilters = None,
    quick_search = None
    extra = None
    content_type = "application/json"
    requesting_panel = None
    xcallback_answers = {}
    row_meta = None
    logger = logger
    _alogger = None
    _status = None  # cache when get_status() is called multiple times

    def __init__(
        self,
        request=None,
        parent=None,
        is_on_main_actor=True,
        permalink_uris=None,
        known_values=None,
        obvious_fields=None,
        **kw
    ):
        self.response = dict()
        self.obvious_fields = set()
        if obvious_fields is not None:
            self.obvious_fields |= obvious_fields
        # if str(kw.get('actor', None)) == "cal.EntriesByController":
        # if kw.get('actor', None):

        self.known_values = dict()

        if request is not None:
            assert parent is None
            self.request = request
            self.rqdata = getrqdata(request)
            kw = self.parse_req(request, self.rqdata, **kw)
            if permalink_uris is None:
                permalink_uris = False  # todo: which default value?
        elif parent is not None:
            # if parent.actor is None:
            # 20190926 we want to have javascript extjs links in dasboard
            # 20200317 and in slave table summaries
            # self.request = parent.request
            self.xcallback_answers = parent.xcallback_answers
            self._confirm_answer = parent._confirm_answer
            for k in inheritable_attrs:
                if k in kw:
                    if kw[k] is None:
                        raise Exception("%s : %s is None" % (kw, k))
                else:
                    kw[k] = getattr(parent, k)
            # kv = kw.setdefault("known_values", {})
            if parent.actor is not None and parent.actor is self.actor:
                kw['param_values'] = parent.param_values
                if parent.known_values is not None:
                    self.known_values.update(parent.known_values)
            # kw.setdefault('user', parent.user)
            # kw.setdefault('subst_user', parent.subst_user)
            # kw.setdefault('renderer', parent.renderer)
            # kw.setdefault('requesting_panel', parent.requesting_panel)
            # if not parent.is_on_main_actor or parent.actor != kw.get('actor', None):
            if not parent.is_on_main_actor:
                is_on_main_actor = False
            elif parent.actor is not None and parent.actor is not self.actor:
                is_on_main_actor = False
            # is_on_main_actor = False
            if permalink_uris is None:
                permalink_uris = parent.permalink_uris
        # else:
        #     kw.setdefault("show_urls", False)

        self.is_on_main_actor = is_on_main_actor
        self.permalink_uris = permalink_uris

        if known_values is not None:
            self.known_values.update(known_values)

        self.setup(**kw)

        # print("20241101", self.__class__.__name__, self.show_urls)

        self.obvious_fields |= set(self.known_values.keys())

        if self.actor is not None:

            for k, v in self.actor.known_values.items():
                self.known_values.setdefault(k, v)

            self.obvious_fields |= self.actor.obvious_fields
            # self.obvious_fields.update(obvious_fields.split())
            # if parent.obvious_fields is not None:
            if parent is not None and parent.actor is self.actor and parent.obvious_fields:
                self.obvious_fields |= parent.obvious_fields
            self.obvious_fields.add(self.actor.master_key)

        if self.master is not None and settings.SITE.strict_master_check:
            if self.master_instance is None:
                raise exceptions.BadRequest(
                    "Request on slave table {} has no master instance ({})".format(
                        self.actor, locals()
                    )
                )
            if isinstance(self.master_instance, MissingRow):
                raise exceptions.BadRequest(self.master_instance)
                # raise Exception(
                #     "Invalid master type {} for slave request on {}".format(
                #         self.master_instance, self.actor))

    def setup(
        self,
        user=None,
        subst_user=None,
        current_project=None,
        display_mode=None,
        master=None,
        master_instance=None,
        master_key=None,
        master_type=None,
        limit=None,
        logger=None,
        requesting_panel=None,
        renderer=None,
        xcallback_answers=None,
        show_urls=None,
        quick_search=None,
        order_by=None,
        filter=None,
        gridfilters=None,
        extra=None,
        selected_rows=None,
    ):
        if logger is not None:
            self.logger = logger
        self.requesting_panel = requesting_panel
        self.quick_search = quick_search
        self.order_by = order_by
        self.filter = filter
        self.gridfilters = gridfilters
        self.extra = extra
        if user is None:
            self.user = settings.SITE.get_anonymous_user()
        else:
            self.user = user
        self.current_project = current_project
        self.display_mode = display_mode
        if renderer is None:
            renderer = settings.SITE.kernel.text_renderer
            # renderer = settings.SITE.kernel.default_renderer
        self.renderer = renderer
        if show_urls is not None:
            self.show_urls = show_urls
        self.subst_user = subst_user
        if xcallback_answers is not None:
            self.xcallback_answers = xcallback_answers

        if selected_rows is not None:
            self.selected_rows = selected_rows

        if self.actor is not None:
            if master is None:
                master = self.actor.master
            if master_type and ContentType is not None:
                try:
                    master = ContentType.objects.get(
                        pk=master_type).model_class()
                except ContentType.DoesNotExist:
                    raise exceptions.BadRequest(
                        f"Invalid master_type {master_type}") from None
            self.master = master

            if self.master is not None and self.master_instance is None:
                # master_instance might have been inherited from parent
                # print(f"20251025 b {self} {self.master} {master_key} {master_instance}")
                if master_instance is None:
                    master_instance = self.get_master_instance(
                        self.master, master_key, master_type
                    )
                self.master_instance = self.actor.cast_master_instance(
                    master_instance)

        self.row_meta = dict(meta=True)

    @property
    def alogger(self):
        if self._alogger is None:
            self._alogger = AttrDict(
                {
                    "info": sync_to_async(self.logger.info),
                    "debug": sync_to_async(self.logger.debug),
                    "warning": sync_to_async(self.logger.warning),
                    "warn": sync_to_async(self.logger.warn),
                    "error": sync_to_async(self.logger.error),
                    "exception": sync_to_async(self.logger.exception),
                }
            )
        return self._alogger

    @contextmanager
    def capture_logger(self, level=logging.INFO):
        old_logger = self.logger

        try:
            # We instantiate a temporary Logger object, which is not known by the
            # root logger.
            # self.logger = PrintLogger(level)
            self.logger = StringLogger(old_logger, level)
            # self.logger.parent =
            yield self.logger

        finally:
            self.logger.streamer.flush()
            # print(self.logger.getvalue())
            self.logger = old_logger

    @contextmanager
    def print_logger(self, level=logging.INFO):
        old_logger = self.logger
        try:
            # We instantiate a temporary Logger object, which is not known by the
            # root logger.
            self.logger = PrintLogger(level)
            yield None

        finally:
            self.logger = old_logger

    @contextmanager
    def override_attrs(self, **kwargs):
        old_values = {k: getattr(self, k) for k in kwargs.keys()}
        for k, v in kwargs.items():
            setattr(self, k, v)
        try:
            yield
        finally:
            for k, v in old_values.items():
                setattr(self, k, v)

    def get_row_classes(self, row):
        if self.actor is None or self.actor.get_row_classes is None:
            return
        classes = self.actor.get_row_classes(row, self)
        if isinstance(classes, GeneratorType):
            row_classes = " ".join([klass for klass in classes])
        else:
            row_classes = classes
        self.row_meta["styleClass"] = row_classes
        return row_classes

    def scrap_row_meta(self, row, row_items):
        self.get_row_classes(row)
        meta_exists = False
        for i, item in enumerate(row_items):
            if isinstance(item, dict) and item.get("meta", False):
                meta_exists, meta_index = True, i
                break
        meta = deepcopy(self.row_meta)
        if meta_exists:
            row_items[meta_index] = meta
        else:
            row_items.append(meta)
        self.row_meta = dict(meta=True)

    def parse_req(self, request, rqdata, **kw):
        """Parse the given incoming HttpRequest and set up this action
        request from it.

        The `mt` url param is parsed only when needed. Usually it is
        not needed because the `master_class` is constant and known
        per actor. But there are exceptions:

        - `master` is `ContentType`

        - `master` is some abstract model

        - `master` is not a subclass of Model, e.g.
          :class:`lino_xl.lib.polls.AnswersByResponse`, a
          virtual table that defines :meth:`get_row_by_pk
          <lino.core.actors.Actor.get_row_by_pk>`.

        """
        # logger.info("20120723 %s.parse_req() %s", self.actor, rqdata)
        # ~ rh = self.ah

        if "master_instance" not in kw:
            # e.g. GET http://127.0.0.1:8000/i/28/1 in noi2
            if (v := rqdata.get(constants.URL_PARAM_MASTER_TYPE, None)) is not None:
                kw.update(master_type=v)
            if (v := rqdata.get(constants.URL_PARAM_MASTER_PK, None)) is not None:
                kw.update(master_key=v)

        if settings.SITE.use_gridfilters:
            if (v := rqdata.get(constants.URL_PARAM_GRIDFILTER, None)) is not None:
                v = json.loads(v)
                kw["gridfilters"] = [constants.dict2kw(flt) for flt in v]

        # kw = ActionRequest.parse_req(self, request, rqdata, **kw)
        if settings.SITE.user_model:
            kw.update(user=request.user)
            kw.update(subst_user=request.subst_user)
        kw.update(requesting_panel=request.requesting_panel)
        kw.update(current_project=rqdata.get(
            constants.URL_PARAM_PROJECT, None))
        kw.update(display_mode=rqdata.get(
            constants.URL_PARAM_DISPLAY_MODE, None))

        # If the incoming request specifies an active tab, then the
        # response must forward this information. Otherwise Lino would
        # forget the current tab when a user saves a detail form for
        # the first time.  The `active_tab` is not (yet) used directly
        # by Python code, so we don't store it as attribute on `self`,
        # just in the response.
        tab = rqdata.get(constants.URL_PARAM_TAB, None)
        if tab is not None:
            tab = int(tab)
            # logger.info("20150130 b %s", tab)
            self.set_response(active_tab=tab)

        kw.update(
            xcallback_answers={
                id: rqdata[id]
                for id in [
                    callbackID
                    for callbackID in rqdata.keys()
                    if callbackID.startswith("xcallback__")
                ]
            }
        )

        # ~ if settings.SITE.user_model:
        # ~ username = rqdata.get(constants.URL_PARAM_SUBST_USER,None)
        # ~ if username:
        # ~ try:
        # ~ kw.update(subst_user=settings.SITE.user_model.objects.get(username=username))
        # ~ except settings.SITE.user_model.DoesNotExist, e:
        # ~ pass
        # logger.info("20140503 ActionRequest.parse_req() %s", kw)

        # if str(self.actor) == 'comments.CommentsByRFC':
        #     print("20230426", kw)

        quick_search = rqdata.get(constants.URL_PARAM_FILTER, None)
        if quick_search:
            kw.update(quick_search=quick_search)

        sort = rqdata.get(constants.URL_PARAM_SORT, None)
        if sort:
            sortfld = self.actor.get_data_elem(sort)
            if isinstance(sortfld, FakeField):
                sort = sortfld.sortable_by
                # sort might be None when user asked to sort a virtual
                # field without sortable_by.
            else:
                sort = [sort]
            # print("20231006 sort", sortfld, sort)
            if sort is not None:

                def si(k):
                    if k[0] == "-":
                        return k[1:]
                    else:
                        return "-" + k

                sort_dir = rqdata.get(constants.URL_PARAM_SORTDIR, "ASC")
                if sort_dir == "DESC":
                    sort = [si(k) for k in sort]
                    # sort = ['-' + k for k in sort]
                # print("20171123", sort)
                kw.update(order_by=sort)

        if self.actor is not None and issubclass(self.actor, AbstractTable):
            try:
                offset = rqdata.get(constants.URL_PARAM_START, None)
                if offset:
                    kw.update(offset=int(offset))
                limit = rqdata.get(constants.URL_PARAM_LIMIT,
                                   self.actor.preview_limit)
                if limit:
                    kw.update(limit=int(limit))
            except ValueError:
                # Example: invalid literal for int() with base 10:
                # 'fdpkvcnrfdybhur'
                raise SuspiciousOperation("Invalid value for limit or offset")

            kw = self.actor.parse_req(request, rqdata, **kw)
        # print("20171123 %s.parse_req() --> %s" % (self, kw))
        return kw

    def setup_from(self, other):
        """
        Copy certain values (renderer, user, subst_user & requesting_panel)
        from this request to the other.

        Deprecated. You should rather instantiate a request and
        specify parent instead. Or use :meth:`spawn_request` on
        parent.
        """
        if not self.must_execute():
            return
            # raise Exception("Request %r was already executed" % other)
        self.renderer = other.renderer
        # self.cellattrs = other.cellattrs
        # self.tableattrs = other.tableattrs
        self.user = other.user
        self.subst_user = other.subst_user
        self.xcallback_answers = other.xcallback_answers
        # self.master_instance = other.master_instance  # added 20150218
        self.requesting_panel = other.requesting_panel

    def spawn_request(self, **kw):
        """
        Create a new request of same class which inherits from this one.
        """
        kw.update(parent=self)
        return self.__class__(**kw)

    def spawn(self, spec=None, **kw):
        """
        Deprecated. Use the more explicit spawn_request() if possible.

        Create a new action request using default values from this one and
        the action specified by `spec`.

        The first argument, `spec` can be:

        - a string with the name of a model, actor or action
        - a :class:`BoundAction` instance
        - another action request (deprecated use)

        """
        from lino.core.resolve import resolve_action

        if isinstance(spec, ActionRequest):  # deprecated use
            # raise Exception("20160627 Deprecated")
            for k, v in kw.items():
                assert hasattr(spec, k)
                setattr(spec, k, v)
            spec.setup_from(self)
        elif isinstance(spec, BoundAction):
            kw.update(parent=self)
            spec = spec.create_request(**kw)
        else:
            kw.update(parent=self)
            ba = resolve_action(spec)
            spec = ba.create_request(**kw)
            # from lino.core.menus import create_item
            # mi = create_item(spec)
            # spec = mi.bound_action.create_request(**kw)
        return spec

    def get_printable_context(self, **kw):
        """
        Adds a series of names to the context used when rendering printable
        documents.
        """
        # from django.conf import settings
        from django.utils.translation import gettext
        from django.utils.translation import pgettext
        from lino.api import dd, rt
        from lino.utils import iif
        from lino.utils.restify import restify
        from django.db import models

        # needed e.g. for polls tutorial
        for n in ("Count", "Sum", "Max", "Min", "Avg", "F"):
            kw[n] = getattr(models, n)

        kw["_"] = gettext
        kw.update(
            ar=self,
            E=E,
            tostring=tostring,
            dd=dd,
            rt=rt,
            decfmt=dd.decfmt,
            fds=dd.fds,
            fdm=dd.fdm,
            fdl=dd.fdl,
            fdf=dd.fdf,
            fdmy=dd.fdmy,
            iif=iif,
            bool2text=bool2text,
            bool2js=lambda b: "true" if b else "false",
            unicode=str,  # backwards-compatibility. In new templates
            # you should prefer `str`.
            pgettext=pgettext,
            now=dd.now(),
            getattr=getattr,
            restify=restify,
            activate_language=activate,
            requested_language=get_language(),
        )

        def parse(s):
            # Jinja doesn't like a name 'self' in the context, which
            # might exist there in a backwards-compatible appypod
            # template:
            kw.pop("self", None)
            return dd.plugins.jinja.renderer.jinja_env.from_string(s).render(**kw)

        kw.update(parse=parse)
        return kw

    def set_selected_pks(self, *selected_pks):
        """
        Given a tuple of primary keys, set :attr:`selected_rows` to a list
        of corresponding database objects.

        TODO: Explain why the special primary keys -99998 and -99999 are
        filtered out.

        """
        # ~ print 20131003, selected_pks
        self.selected_rows = []

        # Until 20250212 we catched for ObjectDoesNotExist here in order to
        # reformulate the message. This made #5924 (Menu "My invoicing plan"
        # fails) difficult to diagnose.
        if True:
            for pk in selected_pks:
                if pk and pk != "-99998" and pk != "-99999":
                    self.selected_rows.append(self.get_row_by_pk(pk))
        else:
            try:
                for pk in selected_pks:
                    if pk and pk != "-99998" and pk != "-99999":
                        self.selected_rows.append(self.get_row_by_pk(pk))
            except ObjectDoesNotExist:
                # raise exceptions.BadRequest(
                raise ObjectDoesNotExist(
                    f"No row with primary key {repr(pk)} in {self.actor}") from None
        # self.selected_rows = filter(lambda x: x, self.selected_rows)
        # note: ticket #523 was because the GET contained an empty pk ("&sr=")

    def get_master_instance(self, master, mk, mt):
        # print(f"20251025 c {self} {master} {mk} {mt}")
        # if str(self.actor) == 'comments.CommentsByRFC':
        #     print("20230426 ", mt)

        if master is None:
            raise exceptions.BadRequest("Invalid master type {}".format(mt))
        return self.actor.get_master_instance(self, master, mk)

    def get_permission(self):
        """
        Whether this request has permission to run.  `obj` can be None if
        the action is a list action (whose `select_rows` is `False`).
        """
        # raise Exception(f"20251006 {self}, {self.permalink_uris}")
        if not self.bound_action.get_bound_action_permission(self, None, None):
            # print("20240402a no permission", self)
            return False
        if self.renderer.readonly and not self.bound_action.action.readonly:
            return False
        if self.permalink_uris:
            return False
        if not self.bound_action.action.select_rows:
            return True
        for obj in self.selected_rows:
            # obj = self.selected_rows[0]
            state = self.bound_action.actor.get_row_state(obj)
            if not self.bound_action.get_row_permission(self, obj, state):
                # raise Exception(f"20241001 {self.bound_action}")
                return False
        return True
        # obj = state = None
        # print("20240402b no permission", self)

    def set_response(self, **kw):
        """
        Set (some part of) the response to be sent when the action request
        finishes.  Allowed keywords are documented in
        :class:`ValidActionResponses`.

        This does not yet respond anything, it is stored until the action
        has finished. The response might be overwritten by subsequent
        calls to :meth:`set_response`.

        :js:func:`Lino.handle_action_result` will get these instructions
        as *keywords* and thus will not know the order in which they have
        been issued. This is a design decision.  We *want* that, when
        writing custom actions, the order of these instructions does not
        matter.
        """
        for k in kw.keys():
            if not hasattr(ValidActionResponses, k):
                raise Exception("Unknown key %r in action response." % k)
        self.response.update(kw)

    def error(self, e=None, message=None, **kw):
        """
        Shortcut to :meth:`set_response` used to set an error response.

        The first argument should be either an exception object or a
        text with a message.

        If a message is not explicitly given, Lino escapes any
        characters with a special meaning in HTML. For example::

            NotImplementedError: <dl> inside <text:p>

        will be converted to::

            NotImplementedError: &lt;dl&gt; inside &lt;text:p&gt;
        """
        kw.update(success=False)
        kw.update(alert=_("Error"))  # added 20140304
        if isinstance(e, Exception):
            if False:  # useful when debugging, but otherwise rather disturbing
                logger.exception(e)
            if hasattr(e, "message_dict"):
                kw.update(errors=e.message_dict)
        if message is None:
            try:
                message = str(e)
            except UnicodeDecodeError as e:
                message = repr(e)
            message = escape(message)
        kw.update(message=message)
        self.set_response(**kw)

    def success(self, message=None, alert=None, **kw):
        """
        Tell the client to consider the action as successful. This is the
        same as :meth:`set_response` with `success=True`.

        First argument should be a translatable message.

        If you want the message to be shown as an alert message, specify
        `alert=True`.

        """
        kw.update(success=True)
        if alert is not None:
            if alert is True:
                alert = _("Success")
            kw.update(alert=alert)
        if message is not None:
            if "message" in self.response and alert is None:
                # ignore alert-less messages when there is already a
                # message set. For example
                # finan.FinancialVoucherItem.parter_changed with more
                # than 1 suggestion.
                pass
            else:
                kw.update(message=message)
        self.set_response(**kw)

    # def append_message(self, level, msg, *args, **kw):
    #     if args:
    #         msg = msg % args
    #     if kw:
    #         msg = msg % kw
    #     # print("20221124", msg)
    #     k = level + '_message'
    #     old = self.response.get(k, None)
    #     if old is None:
    #         self.response[k] = msg
    #     else:
    #         self.response[k] = old + '\n' + msg
    #     # return self.success(*args,**kw)
    #
    # def debug(self, msg, *args, **kw):
    #     if settings.SITE.verbose_client_info_message:
    #         self.append_message('info', msg, *args, **kw)
    #
    # def info(self, msg, *args, **kw):
    #     # deprecated?
    #     self.append_message('info', msg, *args, **kw)
    #
    # def warning(self, msg, *args, **kw):
    #     # deprecated?
    #     self.append_message('warning', msg, *args, **kw)

    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)

    async def adebug(self, *args, **kwargs):
        return await self.alogger.debug(*args, **kwargs)

    async def ainfo(self, *args, **kwargs):
        return await self.alogger.info(*args, **kwargs)

    async def awarning(self, *args, **kwargs):
        return await self.alogger.warning(*args, **kwargs)

    def send_email(self, subject, sender, body, recipients):
        """Send an email message with the specified arguments (the same
        signature as `django.core.mail.EmailMessage`.

        `recipients` is an iterator over a list of strings with email
        addresses. Any address containing '@example.com' will be
        removed. Does nothing if the resulting list of recipients is
        empty.

        If `body` starts with "<", then it is considered to be HTML.

        """
        if "@example.com" in sender:
            # used by book/lino_book/projects/noi1e/tests/test_notify.py
            self.logger.debug("Ignoring email because sender is %s", sender)
            self.logger.debug(
                PRINT_EMAIL.format(
                    subject=subject,
                    sender=sender,
                    body=body,
                    recipients=", ".join(recipients),
                )
            )
            return

        self.logger.info("Send email '%s' from %s to %s",
                         subject, sender, recipients)

        recipients = [a for a in recipients if "@example.com" not in a]
        if not len(recipients):
            self.logger.info(
                "Ignoring email '%s' because there is no recipient", subject
            )
            # self.logger.info("Email body would have been %s", body)
            return

        kw = {}
        if body.startswith("<"):
            kw["html_message"] = body
            body = html2text(body)
        # self.logger.info("20161008b %r %r %r %r", subject, sender, recipients, body)
        try:
            send_mail(subject, body, sender, recipients, **kw)
        except Exception as e:
            self.logger.warning("send_mail() failed : %s", e)
        # msg = EmailMessage(subject=subject,
        #                    from_email=sender, body=body, to=recipients)

        # from django.core.mail import EmailMessage

        # msg = EmailMessage(subject=subject,
        #                    from_email=sender, body=body, to=recipients)
        # self.logger.info(
        #     "Send email '%s' from %s to %s", subject, sender, recipients)
        # msg.send()

    _confirm_answer = True

    def set_confirm_answer(self, ans):
        """
        Set an answer for following confirm in a non-interactive renderer.
        """
        self._confirm_answer = ans

    def confirm(self, ok_func, *msgs, uid=None):
        """
        Execute the specified callable `ok_func` after the user has
        confirmed the specified message.

        The confirmation message may be specified as a series of positional
        arguments, which will be concatenated to a single prompt.

        Pitfall: an action that uses :meth:`ar.confirm
        <lino.core.requests.BaseRequest.confirm>` will be called several times,
        once for each call to :meth:`confirm`. The full text of the confirmation
        message must remain the same each time because it serves as the
        identifier for connecting the two AJAX requests. If the action does
        changes to the database before its last call to :meth:`confirm`, it must
        take care to actually do them only when :attr:`xcallback_answers` is an
        empty `dict`.

        The callable will be called with a single positional argument, which
        will be the action request that confirmed the message. In a web context
        this will be another object than this one.

        In a non-interactive renderer (e.g. in a doctest or when using #
        :class:`lino.core.renderer.TestRenderer`) the `ok_func` function (or
        :func:`noop`) is called directly depending on the value of
        :attr:`_confirm_answer`, which potentially has been set by a previous
        call to :meth:`set_confirm_answer`.

        """
        cb = self.add_callback(*msgs, uid=uid)
        cb.add_choice("yes", ok_func, gettext("Yes"))
        cb.add_choice("no", noop, gettext("No"))
        self.set_callback(cb)

        if not self.renderer.is_interactive:
            if self._confirm_answer:
                return ok_func(self)
            else:
                return noop(self)

    def parse_memo(self, txt, **context):
        return settings.SITE.plugins.memo.parser.parse(txt, self, context)

    def show_detail(self, *args, **kwargs):
        return self.renderer.show_detail(self, *args, **kwargs)

    def get_detail_url(self, *args, **kwargs):
        return self.renderer.get_detail_url(self, *args, **kwargs)

    def get_permalink(self, *args, **kwargs):
        return self.renderer.get_permalink(self, *args, **kwargs)

    def set_callback(self, *args, **kw):
        return callbacks.set_callback(self, *args, **kw)

    def add_callback(self, *args, **kw):
        return callbacks.add_callback(self, *args, **kw)

    def goto_instance(self, *args, **kwargs):
        return self.renderer.goto_instance(self, *args, **kwargs)

    def ar2js(self, *args, **kwargs):
        return self.renderer.ar2js(self, *args, **kwargs)

    def check_visibility(self, *args, **kwargs):
        return self.renderer.check_visibility(self, *args, **kwargs)

    def goto_pk(self, pk, text, **kwargs):
        """Return a HTML link that navigates to the record with the specified primary key.

        When `pk`  is `None`, returns just the text.
        The `text` argument is mandatory.

        This is similar to :meth:`goto_instance`, but is more lightweight (does
        not do permission checks and no database lookup) and therefore works
        only in a detail view.

        """

        r = self.renderer
        if pk is None:
            return text
        if r.extjs_version:
            url = r.js2url("Lino.goto_record_id(%s)" % pk)
        else:
            url = self.get_detail_url(self.actor, pk)
        return r.href(url, text, **kwargs)

    def close_window(self, **kw):
        """Ask client to close the current window. This is the same as
        :meth:`BaseRequest.set_response` with `close_window=True`.

        """
        kw.update(close_window=True)
        self.set_response(**kw)

    def set_content_type(self, ct):
        # logger.info("20140430 set_content_type(%r)", ct)
        self.content_type = ct

    def get_data_value(self, obj, name):
        """
        Return the value of the virtual field `name` for this action
        request on the given object `obj`.
        """
        fld = obj.get_data_elem(name)
        return fld.value_from_object(obj, self)

    def is_obvious_field(self, name):
        """

        Whether the given field is an :term:`obvious field` in this action
        request.

        .. glossary::

            obvious field

              A field whose value is known from the context and hence should not
              be included when rendering a :term:`database row`.

        For example when you are viewing the partners living in a given city,
        then the city doesn't need to be displayed for each partner because that
        information is "obvious".

        This is used e.g. in customized
        :meth:`lino.core.model.Model.as_paragraph` methods.

        General rule: in a request on a slave table, the master instance is
        an obvious value.

        """
        return name in self.obvious_fields
        # if name in self.known_values:
        #     return True
        # # if self.param_values is not None and name in self.param_values:
        # #     return True
        # if self.actor is not None:
        #     if self.actor.master_key == name:
        #         return True
        #     if name in self.actor.obvious_fields:
        #         return True
        # return False

    def get_user(self):
        """
        Return the :class:`User <lino.modlib.users.models.User>` instance
        of the user who issued the request.  If the authenticated user
        is acting as somebody else, return that user's instance.
        """
        return self.subst_user or self.user

    def run(self, ia, *args, **kwargs):  # BaseRequest
        """
        Run the given :term:`instance action` `ia` in a child request of this
        request.

        Additional arguments are forwarded to the action.
        Returns the response of the child request.
        Does not modify response of parent request.

        Usage examples:
        :ref:`dev.custom_actions` defines a custom action and then runs it.
        :ref:`voga.specs.voga` and :ref:`voga.specs.trading`
        use :attr:`lino_xl.lib.exceprts.Excerpt.do_print` to generate a printable document.
        The :fixture:`demo2` fixture of :mod:`lino_xl.lib.excerpts` does the same (but for generating demo data).
        :ref:`dev.users` calls :attr:`lino.modlib.users.User.change_password` with arguments.
        """
        return ia.run_from_session(self, *args, **kwargs)

    def story2html(self, story, *args, **kwargs):
        """
        Convert a story into a stream of HTML elements.
        """
        # return self.renderer.show_story(self, story, *args, **kwargs)
        return settings.SITE.kernel.html_renderer.show_story(
            self, story, *args, **kwargs)

    def story2rst(self, story, *args, **kwargs):
        return self.renderer.show_story(self, story, *args, **kwargs)

    def shows(self, *args, **kwargs):
        return capture_output(self.show, *args, **kwargs)

    def show(
        self,
        spec=None,
        master_instance=None,
        column_names=None,
        header_level=None,
        language=None,
        nosummary=False,
        stripped=True,
        show_links=False,
        show_urls=False,
        max_width=None,
        header_links=False,
        display_mode=None,
        **kwargs,
    ):
        """
        Show the specified table or action using the current renderer.

        The first argument specifies the table or actor to show. It is
        forwarded to :meth:`spawn`.

        If the table is a slave table, then a `master_instance` must
        be specified as second argument.

        Optional keyword arguments are:

        :column_names: overrides default list of columns

        :show_links: show links and other html formatting.  Used
                     .e.g. in :ref:`avanti.specs.roles` where we want
                     to show whether cells are clickable or not.

        :show_urls: show the real URLs. URLs in doctests are usually replaced by
                    "…" to increase readability. If this is explicitly set to True, Lino
                    prints the full URLs.

        :nosummary: if it is a table with :attr:`display_mode
                    <lino.core.tables.AbstractTable.display_mode>`
                    set to ``((None, DISPLAY_MODE_SUMMARY), )``,
                    force rendering it as a table.

        :display_mode: override the table's default display_mode specified by
                       :attr:`default_display_modes <lino.core.tables.AbstractTable.default_display_modes>`.

                       Unlike `nosummary` this can be used to ask a summary for
                       a table that would not show as summary by default.
                       Instead of saying `nosummary=True` you can say
                       `display_mode=DISPLAY_MODE_GRID` or
                       `display_mode=DISPLAY_MODE_HTML` (The display
                       modes DISPLAY_MODE_GRID and DISPLAY_MODE_HTML have the
                       same result in a printed document or in a tested spec).

        :header_level: show also the table header (using specified level)

        :header_links: make column headers clickable so that user can
                       interactively change the sorting order.

        :language: overrides the default language used for headers and
                   translatable data

        Any other keyword arguments are forwarded to :meth:`spawn`.

        Note that this function either returns a string or prints to
        stdout and returns None, depending on the current renderer.

        Usage in a :doc:`tested document </dev/doctests>`:

        >>> from lino.api import rt
        >>> rt.login('robin').show('users.UsersOverview', limit=5)

        Usage in a Jinja template::

          {{ar.show('users.UsersOverview')}}
        """
        from lino.utils.report import Report
        from lino.utils.report import EmptyTable
        # from lino.core.actors import Actor

        if master_instance is not None:
            kwargs.update(master_instance=master_instance)

        if spec is None:
            ar = self
        elif isinstance(spec, BaseRequest):
            assert not kwargs
            ar = spec
        else:
            # assert isinstance(spec, type) and issubclass(spec, Actor)
            ar = self.spawn(spec, **kwargs)
            # return self.renderer.show_story(spec, **kwargs)

        ar.show_urls = show_urls

        def doit():
            # print 20160530, ar.renderer
            if issubclass(ar.actor, Report):
                story = ar.actor.get_story(None, ar)
                return ar.renderer.show_story(
                    self,
                    story,
                    header_level=header_level,
                    header_links=header_links,
                    stripped=stripped)
            elif issubclass(ar.actor, EmptyTable):
                # e.g. rt.show('system.Dashboard')  20210910
                return ar.renderer.show_detail(ar, None)
            elif isinstance(ar.bound_action.action, actions.ShowTable):
                return ar.renderer.show_table(
                    ar,
                    column_names=column_names,
                    header_level=header_level,
                    header_links=header_links,
                    nosummary=nosummary,
                    stripped=stripped,
                    max_width=max_width,
                    show_links=show_links,
                    display_mode=display_mode,
                )
            elif isinstance(ar.bound_action.action, actions.ShowDetail):
                if len(ar.selected_rows) > 0:
                    obj = ar.selected_rows[0]
                else:
                    obj = ar.actor.get_request_queryset().first()
                    # e.g. rt.show('system.SiteConfigs')  20220801
                return ar.renderer.show_detail(ar, obj)
            else:
                print("Cannot show", ar.bound_action.action)

        if language:
            with translation.override(language):
                return doit()
        return doit()

    def show_story(self, *args, **kwargs):
        """
        Shortcut to the renderer's :meth:`show_story
        <lino.core.renderer.HtmlRenderer.show_story>` method.
        """
        return self.renderer.show_story(self, *args, **kwargs)

    def get_home_url(self, *args, **kw):
        """Return URL to the "home page" as defined by the renderer, without
        switching language to default language.

        """
        # if translation.get_language() != settings.SITE.DEFAULT_LANGUAGE:
        #     kw[constants.URL_PARAM_USER_LANGUAGE] = translation.get_language()
        return self.renderer.get_home_url(self, *args, **kw)

    def get_request_url(self, *args, **kw):
        return self.renderer.get_request_url(self, *args, **kw)

    # def row_as_summary(self, obj, *args, **kwargs):
    #     return obj.as_summary_item(self, *args, **kwargs)

    def obj2url(self, *args, **kwargs):
        """Return a url that points to the given database object."""
        return self.renderer.obj2url(self, *args, **kwargs)

    def obj2html(self, obj, text=None, **kwargs):
        # Return a clickable HTML element that points to a detail view of the
        # given database object.
        if obj is None:
            return ""
        return self.renderer.obj2html(self, obj, text, **kwargs)

    def obj2htmls(self, *args, **kwargs):
        """
        Like :meth:`obj2html`, but return a safe html fragment instead of an
        ElementTree element.
        """
        return self.renderer.obj2htmls(self, *args, **kwargs)

    # def add_detail_link(self, obj, txt):
    #     """
    #     Adds a detail link when there is a detail view and when the text does
    #     not yet contain html.
    #
    #     This is rather for internal use to make the items in `DISPLAY_MODE_LIST`
    #     clickable when needed.
    #
    #     Compare the following use cases:
    #
    #     :class:`lino.modlib.users.UsersOverview`,
    #     :class:`lino_xl.lib.working.WorkedHours`,
    #     :class:`lino_xl.lib.contacts.RolesByCompany` and :class:`lino_xl.lib.contacts.RolesByPerson`
    #
    #     """
    #     raise Exception("20240505 is this still used?")
    #     # print("20230303", txt)
    #     if txt.startswith("<"):
    #         return txt
    #     url = self.obj2url(obj)
    #     if url is not None:
    #         url = html.escape(url)
    #         # par += ' <a href="{}">(Detail)</a>'.format(url)
    #         return '<a href="{}">{}</a>'.format(url, txt)
    #     # a funny way to debug:
    #     # return '<a href="{}">{}</a>'.format(str(sar.renderer), txt)
    #     return txt

    def html_text(self, *args, **kwargs):
        return self.renderer.html_text(*args, **kwargs)

    def href_button(self, *args, **kwargs):
        return self.renderer.href_button(*args, **kwargs)

    def href_to_request(self, *args, **kwargs):
        return self.renderer.href_to_request(self, *args, **kwargs)

    def menu_item_button(self, *args, **kwargs):
        """Forwards to :meth:`lino.core.renderer.`"""
        return self.renderer.menu_item_button(self, *args, **kwargs)

    def show_menu_path(self, spec, language=None):
        """
        Print the menu path of the given actor or action.

        This is the replacement for :func:`show_menu_path
        <lino.api.doctest.show_menu_path>`.  It has the advantage that
        it automatically sets the language of the user and that it
        works for any user type.
        """
        from lino.sphinxcontrib.actordoc import menuselection_text

        u = self.get_user()
        mi = u.user_type.find_menu_item(spec)
        if mi is None:
            raise Exception("Invalid spec {0}".format(spec))
        if language is None:
            language = u.language
        with translation.override(language):
            print(menuselection_text(mi))

    def open_in_own_window_button(self, *args, **kwargs):
        return self.renderer.open_in_own_window_button(self, *args, **kwargs)

    def window_action_button(self, *args, **kwargs):
        # settings.SITE.logger.info(
        #     "20160529 window_action_button %s %s", args, self.renderer)
        return self.renderer.window_action_button(self, *args, **kwargs)

    def action_link(self, spec, obj=None, text=None, title=None, pv={}):
        # Used in users/config/users/welcome_email.eml
        from lino.core.resolve import resolve_action

        rnd = self.renderer
        ba = resolve_action(spec)
        if self.permalink_uris:
            url = rnd.get_permalink(self, ba, obj, **pv)
        else:
            url = rnd.js2url(rnd.action_call(self, ba, {}))
        return tostring(rnd.href_button(url, str(text), title))

    def row_action_button(self, obj, ba, *args, **kwargs):
        return self.renderer.row_action_button(obj, self, ba, *args, **kwargs)
        # 20210715 dangerous change: replaced None by self in above line

    def row_action_button_ar(self, obj, *args, **kw):
        """Return an HTML element with a button for running this action
        request on the given database object. Does not spawn another
        request.

        """
        return self.renderer.row_action_button_ar(obj, self, *args, **kw)

    def plain_toolbar_buttons(self, **btnattrs):
        # btnattrs = {'class': "plain-toolbar"}
        cls = self.actor
        buttons = []
        if cls is not None:
            user_type = self.get_user().user_type
            for ba in cls.get_toolbar_actions(self.bound_action.action, user_type):
                if ba.action.show_in_plain and not ba.action.select_rows:
                    ir = ba.request_from(self)
                    # assert ir.user is self.user
                    if ir.get_permission():
                        # try:
                        #     btn = ir.ar2button(**btnattrs)
                        # except AttributeError:
                        #     raise Exception("20200513 {}".format(ir))
                        btn = ir.ar2button(**btnattrs)
                        # assert iselement(btn)
                        buttons.append(btn)
        # print("20181106", cls, self.bound_action, buttons)
        buttons.append(self.open_in_own_window_button())  # 20250713
        return buttons
        # if len(buttons) == 0:
        #     return None
        # return E.p(*buttons, **btnattrs)

    def ar2button(self, *args, **kwargs):
        """Return an HTML element with a button for running this action
        request. Does not spawn another request. Does not check
        permissions.

        """
        # raise Exception("20230331 {}".format(self.subst_user))
        return self.renderer.ar2button(self, *args, **kwargs)

    def as_button(self, *args, **kw):
        """Return a button which when activated executes (a copy of)
        this request.

        """
        return self.renderer.action_button(None, self, self.bound_action, *args, **kw)

    def instance_action_button(self, ia, *args, **kwargs):
        """Return an HTML element with a button that would run the given
        :class:`InstanceAction <lino.core.requests.InstanceAction>`
        ``ia`` on the client.

        Maybe deprecated. Use :meth:`row_action_button` instead.

        """
        # logger.info("20200417 %s", ia)
        return self.renderer.row_action_button(
            ia.instance, self, ia.bound_action, *args, **kwargs
        )

    def action_button(self, ba, obj, *args, **kwargs):
        """Returns the HTML of an action link that will run the specified
        action.

        ``kwargs`` may contain additional html attributes like `style`.

        """
        return self.renderer.action_button(obj, self, ba, *args, **kwargs)

    def get_detail_title(self, elem):
        return self.actor.get_detail_title(self, elem)

    def get_card_title(self, elem):
        return self.actor.get_card_title(self, elem)

    def get_main_card(self):
        return self.actor.get_main_card(self)

    def elem2rec1(ar, rh, elem, fields=None, **rec):
        rec.update(data=rh.store.row2dict(ar, elem, fields))
        return rec

    def elem2rec_insert(self, ah, elem):
        """
        Returns a dict of this record, designed for usage by an InsertWindow.
        """
        lh = ah.actor.insert_layout.get_layout_handle()
        fields = [df._lino_atomizer for df in lh._data_elems]
        if ah.store._disabled_fields_storefield is not None:
            fields.append(ah.store._disabled_fields_storefield)
        rec = self.elem2rec1(ah, elem, fields=fields)
        rec.update(title=self.get_action_title())
        rec.update(phantom=True)
        return rec

    def elem2rec_detailed(ar, elem, with_navinfo=True, **rec):
        """Adds additional information for this record, used only by detail
        views.

        The "navigation information" is a set of pointers to the next,
        previous, first and last record relative to this record in
        this report.  (This information can be relatively expensive
        for records that are towards the end of the queryset.  See
        `/blog/2010/0716`, `/blog/2010/0721`, `/blog/2010/1116`,
        `/blog/2010/1207`.)

        recno 0 means "the requested element exists but is not
        contained in the requested queryset".  This can happen after
        changing the quick filter (search_change) of a detail view.

        """
        # logger.debug("20190924 elem2rec_detailed %s", elem)
        rh = ar.ah
        rec = ar.elem2rec1(rh, elem, None, **rec)
        if ar.actor.hide_top_toolbar or ar.bound_action.action.hide_top_toolbar:
            # TODO: above test is suspicious. To be observed.
            rec.update(title=ar.get_detail_title(elem))
        else:
            rec.update(title=ar.get_breadcrumbs(elem))
            # rec.update(title=ar.get_title() + u" » " +
            #            ar.get_detail_title(elem))
        rec.update(id=elem.pk)
        # rec.update(id=ar.actor.get_pk_field().value_from_object(elem))
        if not ar.actor.hide_editing(ar.get_user().user_type):
            rec.update(disable_delete=rh.actor.disable_delete(elem, ar))
        if rh.actor.show_detail_navigator and with_navinfo:
            rec.update(navinfo=rh.actor.get_navinfo(ar, elem))
        if ar.actor.parameters:
            rec.update(
                param_values=ar.actor.params_layout.params_store.pv2dict(
                    ar, ar.param_values))

        return rec

    def get_breadcrumbs(self, elem=None):
        # print("20250910 get_breadcrumbs", self)
        crumbs = list(self.actor.get_breadcrumbs(self, elem))
        if elem is not None:
            crumbs.append(self.get_detail_title(elem))
        return mark_safe(" &raquo; ".join(map(str, crumbs)))
        # return mark_safe(" &raquo; ".join(crumbs))

    def form2obj_and_save(ar, data, elem, is_new):
        """
        Parses the data from HttpRequest to the model instance and saves
        it.

        This is deprecated, but still used by Restful (which is used
        only by Extensible).
        """
        if is_new:
            watcher = None
        else:
            watcher = ChangeWatcher(elem)
        ar.ah.store.form2obj(ar, data, elem, is_new)
        elem.full_clean()

        if is_new or watcher.is_dirty():
            pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
            elem.before_ui_save(ar, watcher)

            kw2save = {}
            if is_new:
                kw2save.update(force_insert=True)
            else:
                kw2save.update(force_update=True)

            elem.save(**kw2save)

            if is_new:
                on_ui_created.send(elem, request=ar.request)
                ar.success(_("%s has been created.") % obj2unicode(elem))
            else:
                watcher.send_update(ar)
                ar.success(_("%s has been updated.") % obj2unicode(elem))
        else:
            ar.success(_("%s : nothing to save.") % obj2unicode(elem))

        elem.after_ui_save(ar, watcher)

    def get_help_url(self, docname=None, text=None, **kw):
        """
        Generate a link to the help section of the documentation (whose
        base is defined by :attr:`lino.core.site.Site.help_url`)

        Usage example::

            help = ar.get_help_url("foo", target='_blank')
            msg = _("You have a problem with foo."
                    "Please consult %(help)s "
                    "or ask your system administrator.")
            msg %= dict(help=tostring(help))
            kw.update(message=msg, alert=True)
        """
        if text is None:
            text = str(_("the documentation"))
        url = settings.SITE.help_url
        if docname is not None:
            url = "%s/help/%s.html" % (url, docname)
        return E.a(text, href=url, **kw)


class ActionRequest(BaseRequest):
    """
    Holds information about an individual web request and provides
    methods like

    - :meth:`get_user <lino.core.requests.BaseRequest.get_user>`
    - :meth:`confirm <lino.core.requests.BaseRequest.confirm>`
    - :meth:`spawn <lino.core.requests.BaseRequest.spawn>`

    An `ActionRequest` is also a :class:`BaseRequest` and inherits its
    methods.

    An ActionRequest is instantiated from different shortcut methods:

    - :meth:`lino.core.actors.Actor.request`
    - :meth:`lino.core.actions.Action.request`

    """

    create_kw = None
    renderer = None
    offset = None
    limit = None
    master = None
    title = None
    limit = None
    offset = None

    _data_iterator = None
    _sliced_data_iterator = None
    _insert_sar = None
    _ah = None

    def __init__(
        self,
        actor=None,
        action=None,
        rqdata=None,
        **kw
    ):
        # print("20170116 ActionRequest.__init__()", actor, kw)
        self.actor = actor
        self.rqdata = rqdata
        self.bound_action = action or actor.default_action
        super().__init__(**kw)

    @property
    def ah(self):
        if self._ah is None and not self.actor.is_abstract():
            self._ah = self.actor.get_request_handle(self)
            # if self.ah.store is None:
            #     raise Exception("20240530 {} has no store!?".format(self.ah))
        return self._ah

    def parse_req(self, request, rqdata, **kw):
        if "selected_pks" not in kw and "selected_rows" not in kw:
            selected = rqdata.getlist(constants.URL_PARAM_SELECTED)
            kw.update(selected_pks=selected)
        return super().parse_req(request, rqdata, **kw)

    def setup(
        self,
        param_values=None,
        action_param_values={},
        offset=None,
        limit=None,
        title=None,
        exclude=None,
        selected_pks=None,
        **kw
    ):
        if exclude is not None:
            assert isinstance(exclude, models.Q)
        if title is not None:
            self.title = title
        if offset is not None:
            self.offset = offset
        if limit is not None:
            self.limit = limit

        super().setup(**kw)

        if self.bound_action is None:
            return  # 20200825 e.g. a request on an abstract table
        assert self.actor is not None
        request = self.request

        self.actor.setup_request(self)

        if self.actor.parameters is not None:
            pv = self.actor.param_defaults(self)
            for k in pv.keys():
                if k not in self.actor.parameters:
                    msg = f"{self.actor} param_defaults() returned keyword {k}"
                    msg += f" (must be one of {sorted(self.actor.parameters.keys())})"
                    raise Exception(msg)

            # New since 20120913.  E.g. newcomers.Newcomers is a
            # simple pcsw.Clients with
            # known_values=dict(client_state=newcomer) and since there
            # is a parameter `client_state`, we override that
            # parameter's default value.

            for k, v in self.known_values.items():
                if k in pv:
                    pv[k] = v

            # New since 20120914.  MyClientsByGroup has a `group` as
            # master, this must also appear as `group` parameter
            # value.  Lino now understands tables where the master_key
            # is also a parameter.

            if self.actor.master_key is not None:
                if self.actor.master_key in pv:
                    pv[self.actor.master_key] = self.master_instance
            if param_values is None:
                if self.actor.params_layout is None:
                    pass  # 20200825 e.g. users.Users
                    # raise Exception(
                    #     "{} has parameters ({}) but no params_layout. {}".format(
                    #     self.actor, self.actor.parameters, self.actor._setup_done))

                elif request is not None:
                    # call get_layout_handle to make sure that
                    # params_store has been created:
                    self.actor.params_layout.get_layout_handle()
                    ps = self.actor.params_layout.params_store
                    # print('20160329 requests.py', ps, self.actor.parameters)
                    if ps is not None:
                        pv.update(ps.parse_params(request))
                    else:
                        raise Exception(
                            "20160329 params_layout {0} has no params_store "
                            "in {1!r}".format(
                                self.actor.params_layout, self.actor)
                        )
            else:
                for k in param_values.keys():
                    if k not in pv:
                        msg = ("Invalid key '%s' in param_values of %s "
                               "request (possible keys are %s)"
                               % (k, self.actor, list(pv.keys())))
                        # print(msg)  # 20250309
                        raise Exception(msg)
                pv.update(param_values)
            # print("20160329 ok", pv)
            self.param_values = AttrDict(**pv)
            # self.actor.check_params(self.param_values)

        action = self.bound_action.action
        if action.parameters is not None:
            if len(self.selected_rows) == 1:
                apv = action.action_param_defaults(self, self.selected_rows[0])
            else:
                apv = action.action_param_defaults(self, None)
                # msg = "20170116 selected_rows is {} for {!r}".format(
                #     self.selected_rows, action)
                # raise Exception(msg)
            # print(f"20250523 {self.bound_action} {request}")
            if request is not None:
                apv.update(
                    action.params_layout.params_store.parse_params(request))
            self.action_param_values = AttrDict(**apv)
            # action.check_params(action_param_values)
            self.set_action_param_values(**action_param_values)
        self.bound_action.setup_action_request(self)

        # if str(self.actor) == 'outbox.MyOutbox':
        #     if self.master_instance is None:
        #         raise Exception("20230426 b {}".format(self.master))

        if issubclass(self.actor, AbstractTable):
            if self.actor.exclude is not None:
                if not isinstance(self.actor.exclude, models.Q):
                    raise Exception(
                        f"{self.actor}.exclude must be a Q object",
                        f" not {self.actor.exclude}")
            self.exclude = exclude or self.actor.exclude
            self.page_length = self.actor.page_length

            if isinstance(self.actor.master_field, RemoteField):
                # cannot insert rows in a slave table with a remote master
                # field
                self.create_kw = None
            elif isinstance(self.master_instance, MissingRow):
                self.create_kw = None  # 20230426
            else:
                self.create_kw = self.actor.get_filter_kw(self)

        # set_selected_pks() needs the master_instance and the param_values to
        # be set up. e.g. SuggestedMovements.set_selected_pks() needs to know
        # the voucher because the D/C of a DueMovement depends on the "target".
        # Or working.MySessionsByDay needs param_values

        if selected_pks is not None:
            # self.param_values = None
            # print(f"20241003 {selected_pks}")
            self.set_selected_pks(*selected_pks)

    def __str__(self):
        return f"{self.__class__.__name__} for {self.bound_action}"

    # def __str__(self):
    #     return "{0} {1}".format(self.__class__.__name__, self.bound_action)
    #
    # def __repr__(self):
    #     return "{0} {1}".format(self.__class__.__name__, self.bound_action)

    def gen_insert_button(
        self, target=None, button_attrs=dict(style="float: right;"), **values
    ):
        """
        Generate an insert button using a cached insertable object.

        This is functionally equivalent to saying::

            if self.insert_action is not None:
                ir = self.insert_action.request_from(ar)
                if ir.get_permission():
                    return ir.ar2button()

        The difference is that gen_insert_button is more efficient when you do
        this more than once during a single request.

        `target` is the actor into which we want to insert an object. When this is `None`, Lino uses :attr:`self.actor`.
        `button_attrs` if given, are forwarded to :meth:`ar2button`.
        `values` is a dict of extra default values to apply to the insertable object.

        The `values` must be atomized by the caller, which is especially
        important when you want to set a :term:`foreign key` field. So instead
        of saying::

            gen_insert_button(None, user=u)

        you must say::

            gen_insert_button(None, user=u.pk, userHidden=str(u))

        First usage example is in :mod:`lino_xl.lib.calview`.
        Second usage example is :class:`lino_prima.lib.prima.PupilsAndProjects`.

        """
        if target is None:
            target = self.actor
        if self._insert_sar is None:
            if target.insert_action is None:
                raise Exception(f"20241212 {target} has no insert_action")
            self._insert_sar = target.insert_action.request_from(self)
        else:
            assert self._insert_sar.actor is target
        if self._insert_sar.get_permission():
            st = self._insert_sar.get_status()
            st["data_record"]["data"].update(values)
            # obj = st['data_record']
            # for k, v in values.items():
            #     setattr(obj, k, v)
            # print(20241018, st['data_record'])
            return self._insert_sar.ar2button(**button_attrs)

    def run(self, *args, **kw):
        """
        Runs this action request.
        """
        return self.bound_action.action.run_from_code(self, *args, **kw)

    def execute(self):
        """This will actually call the :meth:`get_data_iterator` and run the
        database query.

        Automatically called when either :attr:`data_iterator`
        or :attr:`sliced_data_iterator` is accesed.

        """
        # print("20181121 execute", self.actor)
        try:
            self._data_iterator = self.get_data_iterator()
        except Warning as e:
            # ~ logger.info("20130809 Warning %s",e)
            self.no_data_text = str(e)
            self._data_iterator = []
        except Exception as e:
            if not settings.SITE.catch_layout_exceptions:
                raise
            # Report this exception. But since such errors may occur rather
            # often and since exception loggers usually send an email to the
            # local system admin, make sure to log each exception only once.
            e = str(e)
            self.no_data_text = e + " (set catch_layout_exceptions to see details)"
            self._data_iterator = []
            w = WARNINGS_LOGGED.get(e)
            if w is None:
                WARNINGS_LOGGED[e] = True
                # raise
                logger.warning(f"Error while executing {repr(self)}: {e}\n"
                               "(Subsequent warnings will be silenced.)")
                logger.exception(e)

        if self._data_iterator is None:
            raise Exception(f"No data iterator for {self}")

        if isinstance(self._data_iterator, GeneratorType):
            # print 20150718, self._data_iterator
            self._data_iterator = tuple(self._data_iterator)
        if isinstance(self._data_iterator, (SearchQuery, SearchQuerySet)):
            self._sliced_data_iterator = tuple(
                self.actor.get_rows_from_search_query(
                    self._data_iterator, self)
            )
        else:
            offset = self.offset

            if self.actor.start_at_bottom and offset is None and self.limit is not None:
                count = self.get_total_count()
                if not self.actor.no_phantom_row:
                    count += 1
                offset = (count // self.limit) * self.limit
                if (count % self.limit) == 0 and count != 0:
                    offset -= self.limit

            self._sliced_data_iterator = sliced_data_iterator(
                self._data_iterator, offset, self.limit
            )
        # logger.info("20171116 executed : %s", self._sliced_data_iterator)

    def must_execute(self):
        if issubclass(self.actor, AbstractTable):
            return self._data_iterator is None
        return True

    def get_data_iterator_property(self):
        if self._data_iterator is None:
            self.execute()
        return self._data_iterator

    def get_sliced_data_iterator_property(self):
        if self._sliced_data_iterator is None:
            self.execute()
        return self._sliced_data_iterator

    data_iterator = property(get_data_iterator_property)
    sliced_data_iterator = property(get_sliced_data_iterator_property)

    def get_data_iterator(self):
        assert issubclass(self.actor, AbstractTable)
        self.actor.check_params(self.param_values)
        if self.actor.get_data_rows is not None:
            lst = []
            for row in self.actor.get_data_rows(self):
                group = self.actor.group_from_row(row)
                group.process_row(lst, row)
            return lst
        # ~ logger.info("20120914 tables.get_data_iterator %s",self)
        # ~ logger.info("20120914 tables.get_data_iterator %s",self.actor)
        # print("20181121 get_data_iterator", self.actor)
        return self.actor.get_request_queryset(self)

    def get_total_count(self):
        """
        Return the number of rows.

        When actor is not a table, we assume that there is one row.  This is
        used e.g. when courses.StatusReport is shown in the the dashboard. A
        Report must return 1 because otherwise the dashboard believes it is
        empty.

        Calling `len()` on a QuerySet would execute the whole SELECT.
        See `/blog/2012/0124`
        """
        if self.actor is None or not issubclass(self.actor, AbstractTable):
            return 1
        di = self.data_iterator
        if isinstance(di, SearchQuery):
            return di.total_hits
        if isinstance(di, QuerySet):
            return di.count()
            # try:
            #     return di.count()
            # except Exception as e:
            #     raise e.__class__("{} : {}".format(self, e))
        # ~ if di is None:
        # ~ raise Exception("data_iterator is None: %s" % self)
        if True:
            return len(di)
        else:
            try:
                return len(di)
            except TypeError:
                raise TypeError("{0} has no length".format(di))

    def __iter__(self):
        return self.data_iterator.__iter__()

    def __getitem__(self, i):
        return self.data_iterator.__getitem__(i)

    def create_phantom_rows(self, **kw):
        # phantom row disturbs when there is an insert button in
        # the toolbar
        if self.actor.no_phantom_row:
            return
        # if self.actor.insert_layout is not None: #  and not self.actor.stay_in_grid \
        #     return
        if self.create_kw is None:
            # print("20250127 self.create_kw is None")
            return
        if not self.actor.get_create_permission(self):
            return
        # raise Exception("20250127 create_phantom_rows")
        if self.actor.model is not None:
            if self.actor.model.disable_create(self) is not None:
                return
        yield PhantomRow(self, **kw)

    def create_instance(self, **kw):
        """
        Create a database row using  the specified keyword arguments.
        """
        if self.create_kw:
            kw.update(self.create_kw)
        if self.known_values:
            # kw.update(self.known_values)
            for k, v in self.known_values.items():
                if "__" not in k:
                    kw[k] = v
        obj = self.actor.create_instance(self, **kw)
        return obj

    def create_instances_from_request(self, **kwargs):
        elems = []
        if self.actor.handle_uploaded_files is not None:
            files = self.request.FILES.getlist("file")
            for f in files:
                e = self.create_instance(**kwargs)
                self.actor.handle_uploaded_files(e, self.request, file=f)
                elems.append(e)
        else:
            elems.append(self.create_instance(**kwargs))

        if self.request is not None:
            for e in elems:
                self.ah.store.form2obj(
                    self, self.request.POST or self.rqdata, e, True)
        for e in elems:
            e.full_clean()
        return elems

    def create_instance_from_request(self, **kwargs):
        elem = self.create_instance(**kwargs)
        if self.actor.handle_uploaded_files is not None:
            self.actor.handle_uploaded_files(elem, self.request)

        if self.request is not None:
            self.ah.store.form2obj(
                self, self.request.POST or self.rqdata, elem, True)
        elem.full_clean()
        return elem

    def get_status(self, **kw):
        """Return a `dict` with the "status", i.e. a json representation of
        this request.

        """
        # print("20230331 712 get_status() {}".format(self.subst_user))
        if self._status is not None and not kw:
            return self._status
        if self.actor.parameters and self.actor.params_layout.params_store is not None:
            pv = self.actor.params_layout.params_store.pv2dict(
                self, self.param_values)
            # print(f"20250121c {self}\n{self.actor.params_layout.params_store.__class__}\n{self.actor.params_layout.params_store.param_fields}")
            # print(f"20250121c {self} {self.param_values.keys()}\n{self.actor.params_layout}\n{pv.keys()}")
            # print(f"20250121c {self}|{self.actor.params_layout.params_store}\n{}")
            kw.update(param_values=pv)

        kw = self.bound_action.action.get_status(self, **kw)
        bp = kw.setdefault("base_params", {})
        if self.current_project is not None:
            bp[constants.URL_PARAM_PROJECT] = self.current_project
        if self.display_mode is not None:
            bp[constants.URL_PARAM_DISPLAY_MODE] = self.display_mode
        if self.subst_user is not None:
            # raise Exception("20230331")
            bp[constants.URL_PARAM_SUBST_USER] = self.subst_user.id
        if self.quick_search:
            bp[constants.URL_PARAM_FILTER] = self.quick_search

        if self.order_by:
            sort = self.order_by[0]
            if sort.startswith("-"):
                sort = sort[1:]
                bp[constants.URL_PARAM_SORTDIR] = "DESC"
            bp[constants.URL_PARAM_SORT] = sort

        if self.known_values:
            for k, v in self.known_values.items():
                if self.actor.known_values.get(k, None) != v:
                    bp[k] = v
        mi2bp(self.master_instance, bp)
        self._status = kw
        return kw

    def clear_cached_status(self):
        """Remove any previously computed status information.

        The status information of a request is cached to avoid performance
        issues e.g. in calendar views where a many buttons can be rendered for a
        same request and where the status information can be relatively heavy.

        But sometimes you don't want this. In that case you call
        :meth:`clear_cached_status`.

        """
        self._status = None

    # def spawn(self, actor, **kw):
    #     """Same as :meth:`BaseRequest.spawn`, except that the first positional
    #     argument is an `actor`.

    #     """
    #     if actor is None:
    #         actor = self.actor
    #     return super(ActorRequest, self).spawn(actor, **kw)

    def row_as_summary(self, obj, text=None, **kwargs):
        return self.actor.row_as_summary(self, obj, text, **kwargs)

    # def row_as_page(self, row, **kwargs):
    #     return self.actor.row_as_page(self, row, **kwargs)

    def row_as_paragraph(self, row, **kwargs):
        return self.actor.row_as_paragraph(self, row, **kwargs)

    def get_sum_text(self, sums):
        return self.actor.get_sum_text(self, sums)

    def get_row_by_pk(self, pk):
        return self.actor.get_row_by_pk(self, pk)

    def get_action_title(self):
        return self.bound_action.action.get_action_title(self)

    def get_title(self):
        # print(20200125, self.title, self.master_instance)
        if self.title is not None:
            return self.title
        # if self.master_instance is not None:
        #     self.master_instance
        return self.actor.get_title(self)

    def get_title_base(self):
        return self.actor.get_title_base(self)

    def render_to_dict(self):
        return self.bound_action.action.render_to_dict(self)

    def absolute_uri(self, *args, **kw):
        ar = self.spawn(*args, **kw)
        location = ar.get_request_url()
        return self.request.build_absolute_uri(location)

    def build_webdav_uri(self, location):
        if self.request is None:
            return location
        url = self.request.build_absolute_uri(location)
        if settings.SITE.webdav_protocol:
            url = settings.SITE.webdav_protocol + "://" + url
            # url = urlsplit(url)
            # url.scheme = settings.SITE.webdav_protocol
            # url = url.unsplit()
        # print("20180410 {}", url)
        return url

    def pk2url(self, pk):
        return self.get_detail_url(self.actor, pk)

    def set_action_param_values(self, **action_param_values):
        apv = self.action_param_values
        for k in action_param_values.keys():
            if k not in apv:
                raise Exception(
                    "Invalid key '%s' in action_param_values "
                    "of %s request (possible keys are %s)"
                    % (k, self.actor, list(apv.keys()))
                )
        apv.update(action_param_values)

    def get_base_filename(self):
        return str(self.actor)
        # ~ s = self.get_title()
        # ~ return s.encode('us-ascii','replace')

    def to_rst(self, *args, **kw):
        """Returns a string representing this table request in
        reStructuredText markup.

        """
        stdout = sys.stdout
        sys.stdout = StringIO()
        self.table2rst(*args, **kw)
        rv = sys.stdout.getvalue()
        sys.stdout = stdout
        return rv

    def table2rst(self, *args, **kwargs):
        """
        Print a reStructuredText representation of this table request to
        stdout.
        """
        settings.SITE.kernel.text_renderer.show_table(self, *args, **kwargs)

    def table2xhtml(self, **kwargs):
        """
        Return an HTML representation of this table request.
        """
        t = xghtml.Table()
        self.dump2html(t, self.sliced_data_iterator, **kwargs)
        e = t.as_element()
        # print "20150822 table2xhtml", tostring(e)
        # if header_level is not None:
        #     return E.div(E.h2(str(self.actor.label)), e)
        return e

    def dump2html(
        self,
        tble,
        data_iterator,
        column_names=None,
        header_links=False,
        max_width=None,  # ignored
        show_links=None,  # ignored
        hide_sums=None,
    ):
        """
        Render this table into an existing :class:`etgen.html.Table`
        instance.  This central method is used by all Lino
        renderers.

        Arguments:

        `tble` An instance of :class:`etgen.html.Table`.

        `data_iterator` the iterable provider of table rows.  This can
        be a queryset or a list.

        `column_names` is an optional string with space-separated
        column names.  If this is None, the table's
        :attr:`column_names <lino.core.tables.Table.column_names>` is
        used.

        `header_links` says whether to render column headers clickable
        with a link that sorts the table.

        `hide_sums` : whether to hide sums. If this is not given, use
        the :attr:`hide_sums <lino.core.tables.Table.hide_sums>` of
        the :attr:`actor`.
        """
        ar = self
        tble.attrib.update(self.renderer.tableattrs)
        # print("20251012", self.renderer, self.renderer.tableattrs)
        tble.attrib.setdefault("name", self.bound_action.full_name())

        grid = ar.ah.grid_layout.main
        # from lino.core.widgets import GridWidget
        # if not isinstance(grid, GridWidget):
        #     raise Exception("20160529 %r is not a GridElement", grid)
        columns = grid.columns
        fields, headers, cellwidths = ar.get_field_info(column_names)
        columns = fields
        show_detail_links = self.renderer.show_detail_links
        if show_detail_links and self.ah.actor.detail_action is None:
            show_detail_links = False

        sums = [fld.zero for fld in columns]
        if not self.ah.actor.hide_headers:
            # if cellwidths and self.renderer.is_interactive:
            headers = list(grid.headers2html(
                    self, columns, headers, header_links,
                    **self.renderer.cellattrs))
            if cellwidths:
                totwidth = sum([int(w) for w in cellwidths])
                widths = [str(int(int(w) * 100 / totwidth))
                          + "%" for w in cellwidths]
                for i, td in enumerate(headers):
                    # td.set('width', six.text_type(cellwidths[i]))
                    td.set("width", widths[i])
            if show_detail_links:
                headers.insert(0, E.th("", **self.renderer.cellattrs))
            tble.head.append(xghtml.E.tr(*headers))
        # ~ print 20120623, ar.actor
        recno = 0
        for obj in data_iterator:
            cells = ar.row2html(recno, columns, obj, sums,
                                **self.renderer.cellattrs)
            if cells is not None:
                recno += 1
                if show_detail_links:
                    url = self.obj2url(obj)
                    if url is None:
                        dlcontent = ""
                    else:
                        dlcontent = E.td(E.a("↗", href=url))
                    cells.insert(0, dlcontent)
                tble.body.append(xghtml.E.tr(*cells, **self.renderer.cellattrs))

        if recno == 0:
            tble.clear()
            tble.body.append(str(ar.no_data_text))

        if hide_sums is None:
            hide_sums = ar.actor.hide_sums

        if not hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    has_sum = True
                    break
            if has_sum:
                cells = ar.sums2html(columns, sums, **self.renderer.cellattrs)
                tble.body.append(xghtml.E.tr(*cells))

    def get_field_info(ar, column_names=None):
        """
        Return a tuple `(fields, headers, widths)` which expresses which
        columns, headers and widths the user wants for this
        request. If `self` has web request info (:attr:`request` is
        not None), checks for GET parameters cn, cw and ch.  Also
        calls the tables's :meth:`override_column_headers
        <lino.core.actors.Actor.override_column_headers>` method.
        """
        from lino.modlib.users.utils import with_user_profile
        from lino.core.layouts import ColumnsLayout

        def getit():
            if ar.request is None:
                columns = None
            else:
                data = getrqdata(ar.request)
                columns = [str(x) for x in data.getlist(
                    constants.URL_PARAM_COLUMNS)]
            if columns:
                all_widths = data.getlist(constants.URL_PARAM_WIDTHS)
                hiddens = [
                    (x == "true") for x in data.getlist(constants.URL_PARAM_HIDDENS)
                ]
                fields = []
                widths = []
                ah = ar.actor.get_handle()
                for i, cn in enumerate(columns):
                    col = None
                    for e in ah.grid_layout.main.columns:
                        if e.name == cn:
                            col = e
                            break
                    if col is None:
                        raise Exception(
                            "No column named %r in %s"
                            % (cn, ar.ah.grid_layout.main.columns)
                        )
                    if not hiddens[i]:
                        fields.append(col)
                        widths.append(int(all_widths[i]))
            else:
                if column_names:
                    ll = ColumnsLayout(column_names, datasource=ar.actor)
                    lh = ll.get_layout_handle()
                    fields = lh.main.columns
                    fields = [e for e in fields if not e.hidden]
                else:
                    ah = ar.actor.get_request_handle(ar)

                    fields = ah.grid_layout.main.columns
                    # print(20160530, ah, columns, ah.grid_layout.main)

                # render them so that babelfields in hidden_languages
                # get hidden:
                for e in fields:
                    e.value = e.ext_options()
                    # try:
                    #     e.value = e.ext_options()
                    # except AttributeError as ex:
                    #     raise AttributeError("20160529 %s : %s" % (e, ex))
                #
                fields = [e for e in fields if not e.value.get(
                    "hidden", False)]
                fields = [e for e in fields if not e.hidden]

                widths = ["%d" % (e.width or e.preferred_width)
                          for e in fields]
                columns = [e.name for e in fields]

            headers = [column_header(col) for col in fields]

            # if str(ar.actor).endswith("DailySlave"):
            #     print("20181022", fields[0].field.verbose_name)

            oh = ar.actor.override_column_headers(ar)
            if oh:
                for i, colname in enumerate(columns):
                    header = oh.get(colname, None)
                    if header is not None:
                        headers[i] = header
                # ~ print 20120507, oh, headers

            return fields, headers, widths

        u = ar.get_user()
        if u is None:
            return getit()
        else:
            return with_user_profile(u.user_type, getit)

    def row2html(self, recno, columns, row, sums, **cellattrs):
        has_numeric_value = False
        cells = []
        for i, col in enumerate(columns):
            v = col.field._lino_atomizer.full_value_from_object(row, self)
            if v is None:
                td = E.td(**cellattrs)
            else:
                td = col.value2html(self, v, **cellattrs)
                # print("20240506 {} {}".format(col.__class__, tostring(td)))
                nv = col.value2num(v)
                if nv != 0:
                    sums[i] += nv
                    has_numeric_value = True
            col.apply_cell_format(td)
            self.actor.apply_cell_format(self, row, col, recno, td)
            cells.append(td)
        if self.actor.hide_zero_rows and not has_numeric_value:
            return None
        return cells

    def row2text(self, fields, row, sums):
        """
        Render the given `row` into an iteration of text cells, using the given
        list of `fields` and collecting sums into `sums`.
        """
        # print(20160530, fields)
        for i, fld in enumerate(fields):
            if fld.field is not None:
                sf = get_atomizer(row.__class__, fld.field, fld.field.name)
                # print(20160530, fld.field.name, sf)
                if False:
                    try:
                        getter = sf.full_value_from_object
                        v = getter(row, self)
                    except Exception as e:
                        raise Exception("20150218 %s: %s" % (sf, e))
                        # was used to find bug 20130422:
                        yield "%s:\n%s" % (fld.field, e)
                        continue
                else:
                    getter = sf.full_value_from_object
                    v = getter(row, self)

                if v is None:
                    # if not v:
                    yield ""
                else:
                    sums[i] += fld.value2num(v)
                    # # In case you want the field name in error message:
                    # try:
                    #     sums[i] += fld.value2num(v)
                    # except Exception as e:
                    #     raise e.__class__("%s %s" % (fld.field, e))
                    yield fld.format_value(self, v)

    def sums2html(self, columns, sums, **cellattrs):
        sums = {fld.name: sums[i] for i, fld in enumerate(columns)}
        return [
            fld.sum2html(self, sums, i, **cellattrs) for i, fld in enumerate(columns)
        ]

    def __repr__(self):
        kw = dict()
        if self.master_instance is not None:
            kw.update(master_instance=obj2str(self.master_instance))
        if self.filter is not None:
            kw.update(filter=repr(self.filter))
        if self.known_values:
            kw.update(known_values=self.known_values)
        if self.requesting_panel:
            kw.update(requesting_panel=self.requesting_panel)
        u = self.get_user()
        if u is not None:
            kw.update(user=u.username)
        if False:  # self.request:
            kw.update(request=format_request(self.request))
        return "<%s %s(%s)>" % (
            self.__class__.__name__,
            self.bound_action.full_name(),
            kw,
        )
