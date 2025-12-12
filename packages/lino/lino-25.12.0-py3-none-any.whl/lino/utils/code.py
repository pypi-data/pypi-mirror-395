# -*- coding: UTF-8 -*-
# Copyright 2012-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# docs: https://dev.lino-framework.org/topics/utils.html
"""
Defines some utilities to inspect Python code.
See :doc:`/topics/utils`.

"""
from lino import logger

import os
import sys
import time
import fnmatch
from importlib import import_module
from pathlib import Path
import rstgen


def codefiles_imported(pattern="*"):
    # ~ exp = re.compile(pattern, flags)

    for name, mod in sys.modules.copy().items():
        # ~ if name == 'lino.extjs' and pattern == '*':
        # ~ logger.info("20130801 %r -> %r", name,mod.__file__)
        if fnmatch.fnmatch(name, pattern):
            # ~ if exp.match(name):
            filename = getattr(mod, "__file__", None)
            if filename is not None:
                if filename.endswith(".pyc") or filename.endswith(".pyo"):
                    filename = filename[:-1]
                if filename.endswith("$py.class"):
                    filename = filename[:-9] + ".py"
                # File might be in an egg, so there's no source available
                if os.path.exists(filename):
                    yield name, filename


def codetime(*args, **kw):
    code_mtime = None
    pivot = None
    for name, filename in codefiles_imported(*args, **kw):
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if code_mtime is None or code_mtime < mtime:
            # print 20130204, filename, time.ctime(mtime)
            code_mtime = mtime
            pivot = filename
    # print('20130204 codetime:', args, time.ctime(code_mtime), pivot)
    return code_mtime


# def codefiles(pattern='*'):
def codefiles(module_name):
    # ~ exp = re.compile(pattern, flags)
    mod = import_module(module_name)
    filename = getattr(mod, "__file__", None)
    if filename is None:
        return

    main = Path(filename)
    suffix = main.suffix

    def recurse(root):
        for p in root.iterdir():
            if p.suffix == suffix:
                yield p
            elif p.is_dir():
                for i in recurse(p):
                    yield i

    for p in recurse(main.parent):
        yield p

    # if filename.endswith(".pyc") or filename.endswith(".pyo"):
    #     filename = filename[:-1]
    # if filename.endswith("$py.class"):
    #     filename = filename[:-9] + ".py"
    # File might be in an egg, so there's no source available
    # if os.path.exists(filename):

    # for name, mod in sys.modules.copy().items():
    #     #~ if name == 'lino.extjs' and pattern == '*':
    #         # ~ logger.info("20130801 %r -> %r", name,mod.__file__)
    #     if fnmatch.fnmatch(name, pattern):
    #     #~ if exp.match(name):
    #         filename = getattr(mod, "__file__", None)
    #         if filename is not None:
    #             if filename.endswith(".pyc") or filename.endswith(".pyo"):
    #                 filename = filename[:-1]
    #             if filename.endswith("$py.class"):
    #                 filename = filename[:-9] + ".py"
    #             # File might be in an egg, so there's no source available
    #             if os.path.exists(filename):
    #                 yield name, filename


def codetime_via_source_files(*args):  # not used
    code_mtime = None
    pivot = None
    for module_name in args:
        for filename in codefiles(module_name):
            stat = os.stat(filename)
            mtime = stat.st_mtime
            if code_mtime is None or code_mtime < mtime:
                # print 20130204, filename, time.ctime(mtime)
                code_mtime = mtime
                pivot = filename
    # print('20130204 codetime:', args, time.ctime(code_mtime), pivot)
    return code_mtime


def is_start_of_docstring(line):
    for delim in '"""', "'''":
        if (
            line.startswith(delim)
            or line.startswith("u" + delim)
            or line.startswith("r" + delim)
            or line.startswith("ru" + delim)
        ):
            return delim


class SourceFile(object):
    # Counts the number of code lines in a given Python source file.

    def __init__(self, filename):
        # print("20220917", filename)
        self.filename = filename
        self.analyze()

    # def __init__(self, modulename, filename):
    #     self.modulename = modulename
    #     self.filename = filename
    #     self.analyze()

    def analyze(self):
        self.count_code, self.count_total, self.count_blank, self.count_doc = 0, 0, 0, 0
        self.count_comment = 0
        # ~ count_code, count_total, count_blank, count_doc = 0, 0, 0, 0
        skip_until = None
        for line in open(self.filename).readlines():
            self.count_total += 1
            line = line.strip()
            if not line:
                self.count_blank += 1
            else:
                if line.startswith("#"):
                    self.count_comment += 1
                    continue
                if skip_until is None:
                    skip_until = is_start_of_docstring(line)
                    if skip_until is not None:
                        self.count_doc += 1
                        # ~ skip_until = '"""'
                        continue
                    # ~ if line.startswith('"""') or line.startswith('u"""'):
                    # ~ count_doc += 1
                    # ~ skip_until = '"""'
                    # ~ continue
                    # ~ if line.startswith("'''") or line.startswith("u'''"):
                    # ~ count_doc += 1
                    # ~ skip_until = "'''"
                    # ~ continue
                    self.count_code += 1
                else:
                    self.count_doc += 1
                    # ~ if line.startswith(skip_until):
                    if skip_until in line:
                        skip_until = None

        # ~ self.count_code, count_total, count_blank, count_doc


def analyze_rst(*packages):
    fields = "count_code count_doc count_comment count_total".split()
    headers = [
        "name",
        "code lines",
        "doc lines",
        "comment lines",
        "total lines",
        "files",
    ]
    rows = []

    def fmt(n):
        if n < 1000:
            return "{}".format(n)
        elif n < 2000:
            return "{}k".format(round(n / 1000.0, 1))
        return "{:.0f}k".format(round(n / 1000, 0))

    count_files = len(fields)
    SUMS_LEN = count_files + 1
    total_sums = [0] * SUMS_LEN
    for package in packages:
        sums = [0] * SUMS_LEN
        for filename in codefiles(package):
            sums[count_files] += 1
            sf = SourceFile(filename)
            for i, k in enumerate(fields):
                sums[i] += getattr(sf, k)
        rows.append([package] + [fmt(n) for n in sums])
        for i, k in enumerate(fields):
            total_sums[i] += sums[i]
        total_sums[count_files] += sums[count_files]
    rows.append(["total"] + [fmt(n) for n in total_sums])
    return rstgen.table(headers, rows)
