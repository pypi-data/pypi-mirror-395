# -*- coding: UTF-8 -*-
# Copyright 2010-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
A collection of utilities that require Django settings to be
importable.
"""

import copy
import sys
import datetime
# import yaml
from importlib import import_module

from django.db import models
from django.apps import apps
from django.db.models import Q
# from django.utils.functional import lazy
from django.core.validators import validate_email, ValidationError, URLValidator
from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
from django.core import exceptions
from django.http import QueryDict
from django.utils.translation import gettext as _
from django.utils.html import format_html, mark_safe, SafeString
from django.utils.functional import Promise

from lino import logger
from lino.utils.html import E, assert_safe, tostring
from lino.utils import capture_output
from lino.utils.ranges import isrange
from lino.utils import IncompleteDate

# from .actors import AbstractTable
# from .vfields import DummyField, wildcard_data_elems
# from .vfields import fields_list


get_models = apps.get_models


validate_url = URLValidator()

DEVSERVER_COMMANDS = {
    "runserver", "testserver", "test", "demotest", "makescreenshots", "shell"}


def djangoname(o):
    return o.__module__.split(".")[-2] + "." + o.__name__


def set_default_verbose_name(f):
    """

    If the verbose_name of a ForeignKey was not set by user code, Lino sets it
    to the verbose_name of the model pointed to.  This rule holds also for
    virtual FK fields.

    For every FK field defined on a model (including virtual FK fields) this is
    called during kernel startup.  Django sets the `verbose_name` of every
    field to ``field.name.replace('_', ' ')``.

    For virtual FK fields defined on an actor or an action it is called a bit
    later. These fields don't have a name.

    """
    if f.verbose_name is None or (
            f.name is not None and f.verbose_name == f.name.replace("_", " ")):
        f.verbose_name = f.remote_field.model._meta.verbose_name


# def comma():
#     return ', '

def is_valid_url(s):
    """Returns `True` if the given string is a valid URL.  This calls
    Django's `URLValidator()`, but does not raise an exception.

    """
    try:
        validate_url(s)
        return True
    except ValidationError:
        return False


def is_valid_email(s):
    """Returns `True` if the given string is a valid email.  This calls
    Django's `validate_email()`, but does not raise an exception.

    """
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False


def is_devserver():
    """Returns `True` if this process is running as a development server.

    Thanks to Aryeh Leib Taurog in `How can I tell whether my Django
    application is running on development server or not?
    <https://stackoverflow.com/questions/1291755>`_

    My additions:

    - Added the `len(sys.argv) > 1` test because in a wsgi application
      the process is called without arguments.
    - Not only for `runserver` but also for `testserver` and `test`.
    - pytest removes the first item from sys.argv when running doctests

    """
    # ~ print 20130315, sys.argv[1]
    if settings.DEBUG:
        return True  # doctest under pytest
    if sys.argv[0].startswith("-"):
        return True  # doctest under pytest
    if len(sys.argv) <= 1:
        return False
    # if sys.argv[0] == 'daphne':
    #    return True
    # if sys.argv[0].endswith("doctest.py") or sys.argv[0].endswith("doctest_utf8.py"):
    if sys.argv[0].endswith("doctest.py") or sys.argv[0].endswith("pytest"):
        return True
    if sys.argv[1] in DEVSERVER_COMMANDS:
        return True
    # print(sys.argv)
    return False


def is_logserver():
    if sys.argv[0].startswith("-"):
        return False  # doctest under pytest
    if len(sys.argv) <= 1:
        return False
    if sys.argv[1] in ("lino_runworker", "linod"):
        return True
    return False


def obj2str(i, force_detailed=False):
    """Returns a human-readable ascii string representation of a model
    instance, even in some edge cases.

    """
    if not isinstance(i, models.Model):
        if isinstance(i, (int, IncompleteDate)):
            return str(i)  # AutoField is long on mysql, int on sqlite
        if isinstance(i, datetime.date):
            return i.isoformat()
        # if isinstance(i, str):
        #     return repr(i)[1:]
        return repr(i)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return "(Unsaved %s instance)" % (i.__class__.__name__)
        try:
            return "%s #%s (%s)" % (i.__class__.__name__, str(i.pk), repr(str(i)))
        except Exception as e:
            # ~ except TypeError,e:
            return "Unprintable %s(pk=%r,error=%r" % (i.__class__.__name__, i.pk, e)
            # ~ return unicode(e)
    # ~ names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    # ~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    pairs = []
    fields_list = i._meta.concrete_fields
    for fld in fields_list:
        # ~ if fld.name == 'language':
        # ~ print 20120905, model, fld
        if isinstance(fld, models.ForeignKey):
            v = getattr(i, fld.attname, None)  # 20130709 Django 1.6b1
            # ~ v = getattr(i,fld.name+"_id")
            # ~ if getattr(i,fld.name+"_id") is not None:
            # ~ v = getattr(i,fld.name)
        else:
            try:
                v = getattr(i, fld.name, None)  # 20130709 Django 1.6b1
            except Exception as e:
                v = str(e)
        if v:
            pairs.append("%s=%s" % (fld.name, obj2str(v)))
    s = ",".join(pairs)
    # ~ s = ','.join(["%s=%s" % (n, obj2str(getattr(i,n))) for n in names])
    # ~ print i, i._meta.get_all_field_names()
    # ~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__, s)
    # ~ return "%s(%s)" % (i.__class__,s)


def range_filter(value, f1, f2):
    """Assuming a database model with two fields of same data type named
    `f1` and `f2`, return a Q object to select those rows whose `f1`
    and `f2` encompass the given value `value`.

    """
    q1 = Q(**{f1 + "__isnull": True}) | Q(**{f1 + "__lte": value})
    q2 = Q(**{f2 + "__isnull": True}) | Q(**{f2 + "__gte": value})
    return Q(q1, q2)


def inrange_filter(fld, rng, **kw):
    """Assuming a database model with a field named `fld`, return a Q
    object to select the rows having value for `fld` within the given range `rng`.
    `rng` must be a tuple or list with two items.
    """

    # assert rng[0] <= rng[1]
    kw[fld + "__isnull"] = False
    if rng[0] is not None:
        kw[fld + "__gte"] = rng[0]
    if rng[1] is not None:
        kw[fld + "__lte"] = rng[1]
    return Q(**kw)


def overlap_range_filter(sv, ev, f1, f2, **kw):
    """

    Return a Q object to select all objects having fields `f1` and `f2` define a
    range that overlaps with the range specified by `sv` (start value) and `ev`
    (end value).

    For example, when I specify filter parameters `Date from` 2024-02-21 and
    `until` 2024-03-12 in a :class:`lino.modlib.periods.StoredPeriods` table, I
    want both February and March. Tested examples see
    :ref:`dg.plugins.periods.period_filter`.

    """
    # if not isrange(rng[0], rng[1]):
    #     raise ValueError(f"{rng} is not a valid range")
    if not ev:
        ev = sv
    return Q(**{f1+"__lte": ev, f2+"__gte": sv})


def babelkw(*args, **kw):
    return settings.SITE.babelkw(*args, **kw)


babel_values = babelkw  # old alias for backwards compatibility


def babelattr(*args, **kw):
    return settings.SITE.babelattr(*args, **kw)


class PseudoRequest(object):
    """A Django HTTP request which isn't really one.

    Typical usage example::

        from lino.core.diff import PseudoRequest, ChangeWatcher

        REQUEST = PseudoRequest("robin")

        for obj in qs:
            cw = ChangeWatcher(obj)
            # update `obj`
            obj.full_clean()
            obj.save()
            cw.send_update(REQUEST)

    """

    method = "GET"
    subst_user = None
    requesting_panel = None
    success = None

    def __init__(self, username):
        self.username = username
        self._user = None
        self.GET = QueryDict("")

    def get_user(self):
        if self._user is None:
            if settings.SITE.user_model is not None:
                # ~ print 20130222, self.username
                self._user = settings.SITE.user_model.objects.get(
                    username=self.username
                )
        return self._user

    user = property(get_user)


def error2str(self, e):
    """Convert the given Exception object into a string, but handling
    ValidationError specially.
    """
    if isinstance(e, list):
        return ", ".join([self.error2str(v) for v in e])
    if isinstance(e, exceptions.ValidationError):
        md = getattr(e, "message_dict", None)
        if md is not None:

            def fieldlabel(name):
                de = self.get_data_elem(name)
                return str(getattr(de, "verbose_name", name))

            return "\n".join(
                ["%s : %s" % (fieldlabel(k), self.error2str(v))
                 for k, v in md.items()]
            )
        return "\n".join(e.messages)
    return str(e)


def class_dict_items(cl, exclude=None):
    if exclude is None:
        exclude = set()
    for k, v in cl.__dict__.items():
        if k not in exclude:
            yield cl, k, v
            exclude.add(k)
    for b in cl.__bases__:
        for i in class_dict_items(b, exclude):
            yield i


def login(username=None, **kwargs):
    """Return a basic :term:`action request` with the specified user signed in.
    """
    from lino.core.requests import BaseRequest  # avoid circular import
    # settings.SITE.startup()
    User = settings.SITE.user_model
    if User and username:
        try:
            kwargs.update(user=User.objects.get(username=username))
        except User.DoesNotExist:
            raise User.DoesNotExist(f"'{username}' : no such user")

    kwargs.setdefault("show_urls", False)
    # import lino.core.urls  # hack: trigger ui instantiation
    return BaseRequest(**kwargs)


def show(*args, **kwargs):
    """Print the specified data table to stdout."""
    return login().show(*args, **kwargs)


def shows(*args, **kwargs):
    """Return the output of :func:`show`."""
    return capture_output(show, *args, **kwargs)


class Panel:
    """
    To be used when a panel cannot be expressed using a simple
    template string because it requires one or more options. These
    `options` parameters can be:

    - label
    - required_roles
    - window_size
    - label_align

    Unlike a :class:`BaseLayout` it cannot have any child panels
    and cannot become a tabbed panel.
    """

    def __init__(self, desc, label=None, **options):
        # assert not 'required' in options
        self.desc = desc
        if label is not None:
            options.update(label=label)
        self.options = options

    def replace(self, *args, **kw):
        """
        Calls the standard :meth:`string.replace`
        method on this Panel's template.
        """
        self.desc = self.desc.replace(*args, **kw)


def model_class_path(model):
    return model.__module__ + "." + model.__name__


def get_field(model, name):
    """Returns the field descriptor of the named field in the specified
    model.

    """
    # for vf in model._meta.virtual_fields:
    #     if vf.name == name:
    #         return vf
    return model._meta.get_field(name)

    # RemovedInDjango110Warning: 'get_field_by_name is an unofficial
    # API that has been deprecated. You may be able to replace it with
    # 'get_field()'
    # fld, remote_model, direct, m2m = model._meta.get_field_by_name(name)
    # return fld


class UnresolvedField:
    """
    Returned by :func:`resolve_field` if the specified field doesn't exist.
    This case happens when sphinx autodoc tries to import a module.
    See ticket :srcref:`docs/tickets/4`.
    """

    def __init__(self, name):
        self.name = name
        self.verbose_name = "Unresolved Field " + name


class UnresolvedModel:
    """The object returned by :func:`resolve_model` if the specified model
    is not installed.

    We don't want :func:`resolve_model` to raise an Exception because
    there are cases of :ref:`datamig` where it would disturb.  Asking
    for a non-installed model is not a sin, but trying to use it is.

    I didn't yet bother very much about finding a way to make the
    `model_spec` appear in error messages such as
    :message:`AttributeError: UnresolvedModel instance has no
    attribute '_meta'`.  Current workaround is to uncomment the
    ``print`` statement below in such situations...

    """

    def __init__(self, model_spec, app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        # ~ print(self)

    def __repr__(self):
        return self.__class__.__name__ + "(%r, %s)" % (self.model_spec, self.app_label)

    # ~ def __getattr__(self,name):
    # ~ raise AttributeError("%s has no attribute %r" % (self,name))


def resolve_app(app_label, strict=False):
    """Return the `modules` module of the given `app_label` if it is
    installed.  Otherwise return either the :term:`dummy module` for
    `app_label` if it exists, or `None`.

    If the optional second argument `strict` is `True`, raise
    ImportError if the app is not installed.

    This function is designed for use in models modules and available
    through the shortcut ``dd.resolve_app``.

    For example, instead of writing::

        from lino_xl.lib.trading import models as trading

    it is recommended to write::

        trading = dd.resolve_app('trading')

    because it makes your code usable (1) in applications that don't
    have the 'trading' module installed and (2) in applications who have
    another implementation of the `trading` module
    (e.g. :mod:`lino.modlib.auto.trading`)

    """
    # ~ app_label = app_label
    for app_name in settings.INSTALLED_APPS:
        if app_name == app_label or app_name.endswith("." + app_label):
            return import_module(".models", app_name)
    try:
        return import_module("lino.modlib.%s.dummy" % app_label)
    except ImportError:
        if strict:
            # ~ raise
            raise ImportError(
                "No app_label %r in %s" % (app_label, settings.INSTALLED_APPS)
            )


# def require_app_models(app_label):
#     return resolve_app(app_label, True)


# Note that restore.py uses from lino.core.utils import resolve_model

def resolve_model(model_spec, app_label=None, strict=False):
    """Return the class object of the specified model. `model_spec` is
    usually the global model name (i.e. a string like
    ``'contacts.Person'``).

    If `model_spec` does not refer to a known model, the function
    returns :class:`UnresolvedModel` (unless `strict=True` is
    specified).

    Using this method is better than simply importing the class
    object, because Lino applications can override the model
    implementation.

    This function **does not** trigger a loading of Django's model
    cache, so you should not use it at module-level of a
    :xfile:`models.py` module.

    In general we recommend to use ``from lino.api import rt`` and
    ``rt.models.contacts.Person`` over
    ``resolve_model('contacts.Person')``. Note however that this works
    only in a local scope, not at global module level.

    """
    # ~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec, str):
        if "." in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec

        if True:
            app = settings.SITE.models.get(app_label)
            model = getattr(app, model_name, None)
            # settings.SITE.logger.info("20181230 resolve %s --> %r, %r",
            #                           model_spec, app, model)
        else:
            # 20241112 Helped to explore #5797 (Could not resolve target
            # 'uploads.UploadType' of ForeignKey 'type' in <class
            # 'lino.modlib.uploads.models.Upload'>)
            from django.apps import apps

            try:
                model = apps.get_model(app_label, model_name)
            except LookupError:
                model = None
    else:
        model = model_spec
    # if not isinstance(model, type) or not issubclass(model, models.Model):
    if not isinstance(model, type):
        if strict:
            if False:
                from django.db.models import loading

                print((20130219, settings.INSTALLED_APPS))
                print([full_model_name(m) for m in get_models()])
                if len(loading.cache.postponed) > 0:
                    print(("POSTPONED:", loading.cache.postponed))

            if isinstance(strict, str):
                raise Exception(strict % model_spec)
            raise ImportError(
                "resolve_model(%r,app_label=%r) found %r "
                "(settings %s, INSTALLED_APPS=%s)"
                % (
                    model_spec,
                    app_label,
                    model,
                    settings.SETTINGS_MODULE,
                    settings.INSTALLED_APPS,
                )
            )
        return UnresolvedModel(model_spec, app_label)
    return model


def resolve_field(name, app_label=None):
    """Returns the field descriptor specified by the string `name` which
    should be either `model.field` or `app_label.model.field`.

    """
    l = name.split(".")
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        model = apps.get_model(app_label, l[0])
        if model is None:
            raise FieldDoesNotExist(
                "No model named '%s.%s'" % (app_label, l[0]))
        return model._meta.get_field(l[1])
        # fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        # assert remote_model is None or issubclass(model, remote_model), \
        #     "resolve_field(%r) : remote model is %r (expected None or base of %r)" % (
        #         name, remote_model, model)
        # return fld
    raise FieldDoesNotExist(name)
    # return UnresolvedField(name)


def full_model_name(model, sep="."):
    """Returns the "full name" of the given model, e.g. "contacts.Person" etc."""
    return model._meta.app_label + sep + model._meta.object_name


def obj2unicode(i):
    """Returns a user-friendly unicode representation of a model instance."""
    if not isinstance(i, models.Model):
        return str(i)
    return '%s "%s"' % (i._meta.verbose_name, str(i))


def sorted_models_list():
    # trigger django.db.models.loading.cache._populate()
    models_list = get_models()

    models_list.sort(key=lambda a: full_model_name(a))
    return models_list


def models_by_base(base, toplevel_only=False):
    """Yields a list of installed models that are subclass of the given
    base class.

    If `toplevel_only` is True, then do not include MTI children.
    See :ref:`tested.core_utils` for more explanations.

    The list is sorted alphabetically using :func:`full_model_name`.
    Before 2015-11-03 it was
    unpredictable and changed between Django versions.

    """
    found = []
    if base is None:
        return found
    for m in get_models(include_auto_created=True):
        if issubclass(m, base):
            add = True
            if toplevel_only:
                for i, old in enumerate(found):
                    if issubclass(m, old):
                        add = False
                    elif issubclass(old, m):
                        found[i] = m
                        add = False
            if add:
                found.append(m)

    found.sort(key=lambda m: full_model_name(m))
    return found


def getrqdata(request):
    """Return the request data.

    Unlike the now defunct `REQUEST
    <https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpRequest.REQUEST>`_
    attribute, this inspects the request's `method` in order to decide
    what to return.

    """
    if request.method in ("PUT", "DELETE"):
        return QueryDict(request.body)
        # note that `body` was named `raw_post_data` before Django 1.4
        # print 20130222, rqdata
    # rqdata = request.REQUEST
    if request.method == "HEAD":
        return request.GET
    return getattr(request, request.method)


def format_request(request):
    """Format a Django HttpRequest for logging it.

    This was written for the warning to be logged in
    :mod:`lino.utils.ajax` when an error occurs while processing an
    AJAX request.

    """
    s = "{0} {1}".format(request.method, request.path)
    qs = request.META.get("QUERY_STRING")
    if qs:
        s += "?" + qs
    # Exception: You cannot access body after reading from request's
    # data stream
    if request.body:
        data = QueryDict(request.body)
        # data = yaml.dump(dict(data))
        data = str(data)
        if len(data) > 200:
            data = data[:200] + "..."
        s += " (data: {0})".format(data)

    return s


def use_as_wildcard(de):
    if de.name.endswith("_ptr"):
        return False
    return True


def traverse_ddh_fklist(model, ignore_mti_parents=True):
    """
    Return an iterator over each foreign key (in other models) that points to
    this model.  Used e.g. to predict the related objects that are going to be
    deleted in cascade when a database object is being deleted.

    When an application uses MTI (e.g. with a Participant model being a
    specialization of Person, which itself a specialization of
    Partner) and we merge two Participants, then we must of course
    also merge their invoices and bank statement items (linked via a
    FK to Partner) and their contact roles (linked via a FK to
    Person).

    See also :ticket:`3891` (Lino says there are 2 related adresses when there
    is only one).

    """
    # if settings.SITE.is_hidden_plugin(model._meta.app_label):
    #     return
    found = set()
    for base in model.mro():
        ddh = getattr(base, "_lino_ddh", None)
        if ddh is not None:
            for k in ddh.fklist:
                # k is a tuple (m, fk)
                (m, fk) = k
                if ignore_mti_parents and isinstance(fk, models.OneToOneField):
                    pass
                    # logger.info("20160621 ignore OneToOneField %s", fk)
                elif k in found:
                    pass
                else:
                    # logger.info("20160621 yield %s (%s)",
                    #             fk, fk.__class__)
                    found.add(k)
                    yield k


def navinfo(qs, elem, limit=None):
    """Return a dict with navigation information for the given model
    instance `elem` within the given queryset.

    The returned dictionary contains the following keys:

    :recno:   row number (index +1) of elem in qs
    :first:   pk of the first element in qs (None if qs is empty)
    :prev:    pk of the previous element in qs (None if qs is empty)
    :next:    pk of the next element in qs (None if qs is empty)
    :last:    pk of the last element in qs (None if qs is empty)
    :message: text "Row x of y" or "No navigation"
    :id_list: list of the primary keys

    Used by :meth:`lino.core.actors.Actor.get_navinfo`.

    """
    first = None
    prev = None
    next = None
    prev_page = None
    next_page = None
    last = None
    recno = 0
    message = None
    page_num = None
    offset = None

    # ~ LEN = ar.get_total_count()
    if isinstance(qs, (list, tuple)):
        num = len(qs)
        id_list = [obj.pk for obj in qs]
        # ~ logger.info('20130714')
    else:
        num = qs.count()
        # this algorithm is clearly quicker on queries with a few thousand rows
        id_list = list(qs.values_list("pk", flat=True))
    if num > 0:
        # Uncommented the following assert because it failed in certain circumstances
        # (see `/blog/2011/1220`)
        # assert len(id_list) == ar.total_count, \
        # "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
        # print 20111220, id_list
        try:
            i = id_list.index(elem.pk)
        except ValueError:
            pass
        else:
            recno = i + 1
            first = id_list[0]
            last = id_list[-1]
            if limit:
                page_num = i // limit
                offset = limit * page_num
            if i > 0:
                prev = id_list[i - 1]
                if limit:
                    prev_page = id_list[max(0, offset - limit + 1)]
            if i < len(id_list) - 1:
                next = id_list[i + 1]
                if limit:
                    next_page = id_list[min(num - 1, offset + limit + 2)]
            message = _("Row %(rowid)d of %(rowcount)d") % dict(
                rowid=recno, rowcount=num
            )
    if message is None:
        message = _("No navigation")
    return dict(
        first=first,
        prev=prev,
        next=next,
        last=last,
        recno=recno,
        message=message,
        prev_page=prev_page,
        next_page=next_page,
        offset=offset,
    )


def resolve_fields_list(model, k, collection_type=tuple, default=None):
    value = getattr(model, k)
    if value is None:
        setattr(model, k, default)
        return
    elif value == default:
        return
    elif isinstance(value, collection_type):
        return
    if isinstance(value, str):
        value = value.split()
    if isinstance(value, (list, tuple)):
        lst = []
        for n in value:
            f = model.get_data_elem(n)
            if f is None:
                msg = f"Invalid field {n} in {k} of {model}"
                raise Exception(msg)
            lst.append(f)
        setattr(model, k, collection_type(lst))
        # fields.fields_list(model, model.quick_search_fields))
    else:
        raise ChangedAPI(
            f"{model}.{k} must be None or a string "
            f"of space-separated field names (not {value})")


class VirtualRow:
    def __init__(self, **kw):
        self.update(**kw)

    def update(self, **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)

    def get_row_permission(self, ar, state, ba):
        if ba.action.readonly:
            return True
        return False


class PhantomRow(VirtualRow):
    def __init__(self, request, **kw):
        self._ar = request
        VirtualRow.__init__(self, **kw)

    def __str__(self):
        return str(self._ar.get_action_title())


def DelayedValue(ar, fieldname, obj):
    # return dict(delayed_value_url=settings.SITE.buildurl("values",
    #     str(ar.actor).replace(".","/"), str(obj.pk), fieldname, mk=ar.master_instance.pk))
    return dict(
        delayed_value_url="values/{}/{}/{}".format(
            str(ar.actor).replace(".", "/"), obj.pk, fieldname
        )
    )


# class DelayedValue:
#     """
#
#     Creates an url for the related value and passes it to the frontend for the
#     value to be fetched later by the frontend.
#
#     """
#
#     def __init__(self, actor, fieldname, obj):
#         if fieldname is None:
#             raise Exception("20210617 {}".format(field))
#         # a = ar.actor
#         self.url = "values/{}/{}/{}".format(
#             str(actor).replace(".","/"), obj.pk, fieldname)
#         # print(self, self.url)
#         # self.field = field
#         # self.obj = obj
#
#     def get_url(self):
#         return self.url
#
#     def __repr__(self):
#         return "DelayedValue({})".format(self.url)


def dbfield2params_field(db_field):
    """originally just for setting up actor parameters from get_simple_parameters()
    but also used in calview."""

    fld = copy.copy(db_field)
    fld.blank = True
    fld.null = True
    fld.default = None
    fld.editable = True
    return fld


def db2param(spec):
    """
    Return a copy of the specified :term:`database field` for usage as an
    :term:`actor parameter` field.

    A usage example is :class:`lino_xl.lib.tickets.SpawnTicket` action. This
    action has two parameter fields, one for the type of link to create, the
    other for the summary of the ticket to create. We might copy the definitions
    of these to fields from their respective models and say::

        parameters = dict(
            link_type=LinkTypes.field(default='requires'),
            ticket_summary=models.CharField(
                pgettext("Ticket", "Summary"), max_length=200,
                blank=False,
                help_text=_("Short summary of the problem."))
            )

    But it is easier and more maintainable to say::

        parameters = dict(
            link_type=db2param('tickets.Link.type'),
            ticket_summary=db2param('tickets.Ticket.summary'))

    Unfortunately that doesn't yet work because actions get instantiated when
    models aren't yet fully loaded :-/

    TODO: One idea to get it working is to say that parameter fields can be
    specified as names of fields, and Lino would resolve them at startup::

        parameters = dict(
            link_type='tickets.Link.type',
            ticket_summary='tickets.Ticket.summary')


    """
    return dbfield2params_field(resolve_field(spec))
