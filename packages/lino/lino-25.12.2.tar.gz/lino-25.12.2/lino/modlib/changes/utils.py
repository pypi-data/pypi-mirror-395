# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines the :func:`watch_changes` function and :class:`WatcherSpec` class.

"""
from lino.core.fields import RemoteField, fields_list


class WatcherSpec:
    def __init__(self, ignored_fields, get_master, master_key):
        self.master_key = master_key
        self.ignored_fields = ignored_fields
        self.get_master = get_master


# def watch_all_changes(ignore=[]):
#     """Call this to activate change watching on *all* models. The default
#     behaviour is to watch only models that have been explicitly
#     declared using :func:`watch_changes`.
#
#     This is a fallback method and settings passed to specific model
#     using `watch_changes` call takes precedence.
#
#     :param ignore: specify list of model names to ignore
#
#     """
#     watch_all_changes.allow = True
#     watch_all_changes.ignore.extend(ignore)
#
#
# watch_all_changes.allow = False
# watch_all_changes.ignore = []
#


def return_self(obj):
    return obj


def watch_changes(model, ignore=[], master_key=None, **options):
    if isinstance(ignore, str):
        ignore = fields_list(model, ignore)
    if isinstance(master_key, str):
        fld = model.get_data_elem(master_key)
        if fld is None:
            raise Exception("No field %r in %s" % (master_key, model))
        master_key = fld
    if isinstance(master_key, RemoteField):
        get_master = master_key.func
    elif master_key is None:
        get_master = return_self
    else:

        def get_master(obj):
            return getattr(obj, master_key.name)

    ignore = set(ignore)
    cs = model.__dict__.get("change_watcher_spec", None)
    if cs is not None:
        raise Exception("20240330 Duplicate watch_changes() for model {}".format(model))
        ignore |= cs.ignored_fields
    for f in model._meta.fields:
        # if (not f.editable) or isinstance(f, fields.VirtualField):
        if not f.editable:
            ignore.add(f.name)
    model.change_watcher_spec = WatcherSpec(ignore, get_master, master_key)


# def get_change_watcher_spec(obj):
#     cs = obj.change_watcher_spec
#
#     if cs is None:
#         if not watch_all_changes.allow \
#            or obj.__class__.__name__ in watch_all_changes.ignore:
#             return None
#
#         cs = WatcherSpec([], return_self)
#         obj.change_watcher_spec = cs
#
#     return cs


def get_master(obj):
    if (cs := obj.change_watcher_spec) is not None:
        return cs.get_master(obj)
