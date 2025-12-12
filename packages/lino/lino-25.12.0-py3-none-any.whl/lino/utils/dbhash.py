# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Utilities around a "database hash".
See :doc:`/utils/dbhash`.
"""

import json
from django.conf import settings
from django.apps import apps

HASH_FILE = settings.SITE.site_dir / "dbhash.json"


def fmn(m):
    return f"{m._meta.app_label}.{m._meta.object_name}"


def compute_dbhash():
    """
    Return a dictionary with a hash value of the current database content.
    """
    rv = dict()
    for m in apps.get_models(include_auto_created=True):
        k = fmn(m)
        if k != "sessions.Session":
            # rv[k] = m.objects.count()
            rv[k] = list(m.objects.values_list('pk', flat=True))
    return rv


def mark_virgin(**kwargs):
    """
    Mark the database as virgin. This is called by :manage:`prep`.
    """
    dbhash = compute_dbhash()
    with HASH_FILE.open("w") as fp:
        json.dump(dbhash, fp)


def load_dbhash():
    """
    Load the dbhash that was saved in :xfile:`dbhash.json`
    """
    if not HASH_FILE.exists():
        raise Exception(
            f"No file {HASH_FILE} (did you run `django-admin prep`?)")
    with HASH_FILE.open("r") as fp:
        return json.load(fp)


def check_virgin(restore=True, verbose=True):
    """
    Verify whether the database is virgin. Print the differences if there
    are any.
    """
    new = compute_dbhash()
    old = load_dbhash()

    first_diff = True
    can_restore = True
    must_delete = {}
    for k, v in new.items():
        v = set(v)
        oldv = set(old.get(k, None))
        if oldv != v:
            if first_diff:
                if verbose:
                    print(f"Database {HASH_FILE.parent} isn't virgin:")
                first_diff = False
            diffs = []
            added = v - oldv
            if len(added):
                diffs.append(f"{len(added)} rows added")
                must_delete[apps.get_model(k)] = added
                # for pk in added:
                #     must_delete.append(m.objects.get(pk=pk))
            if (removed := len(oldv-v)):
                diffs.append(f"{removed} rows deleted")
                can_restore = False
            if verbose:
                print(f"- {k}: {', '.join(diffs)}")
    if can_restore and len(must_delete) == 0 or not restore:
        return
    if not can_restore:
        print("Cannot restore database because some rows have been deleted")
        return
    must_delete = list(must_delete.items())
    if verbose:
        print(f"Tidy up {len(must_delete)} rows from database: {must_delete}.")
    while len(must_delete):
        todo = []
        hope = False
        for m, added in must_delete:
            try:
                # It can happen that some rows refer to each other with a
                # protected fk,  so we call bulk delete() to avoid Lino deleting
                # the items of an invoice.
                m.objects.filter(pk__in=added).delete()
                # obj.delete()
                hope = True
            except Exception:
                todo.append((m, added))
        if not hope:
            raise Exception(f"Failed to delete {todo}")
        must_delete = todo
    if verbose:
        print("Database has been restored.")
