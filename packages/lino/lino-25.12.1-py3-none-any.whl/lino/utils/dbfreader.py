# Copyright 2003-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""

Defines the :class:`DBFFile` class, used by  :doc:`lino_xl.lib.tim2lino` to read
DBF and DBT files when both settings :attr:`use_dbfread
<lino_xl.lib.tim2lino.Plugin.use_dbfread>` and :attr:`use_dbf_py
<lino_xl.lib.tim2lino.Plugin.use_dbf_py>` are `False` (which is default).

Based on original work by Lars Garshol
https://www.garshol.priv.no/download/software/python/dbfreader.py

Modified by Luc Saffre to add support for Clipper dialect. And to work under
Python 3. And to support char fields longer than 255 characters.

Sources of information:

- `What's the format of a Clipper .dbf file?
  <https://www.the-oasis.net/clipper-12.html#ss12.4>`__ (broken link)

`Xbase & dBASE File Format Description by Erik Bachmann
<https://www.clicketyclick.dk/databases/xbase/format/>`__

"""

import datetime
from dateutil import parser as dateparser

import sys
# import string

codepages = {
    "\x01": "cp437",
    "\x02": "cp850",
}

# --- Useful functions


def unpack_long(number):
    return number[0] + 256 * (number[1] + 256 * (number[2] + 256 * number[3]))


def unpack_long_rev(number):
    return number[3] + 256 * (number[2] + 256 * (number[1] + 256 * number[0]))


def unpack_int(number):
    return number[0] + 256 * number[1]


def unpack_int_rev(number):
    return number[1] + 256 * number[0]


def hex_analyze(number):
    for ch in number:
        print("%s\t%s\t%d" % (hex(ch), ch, ch))


# --- A class for the entire file


class DBFFile(object):
    "Represents a single DBF file."

    HAS_MEMO_FILE = 128  # "\x80"

    versionmap = {
        0x03: "dBASE III",
        0x83: "dBASE III+ with memo",
        0x8B: "dBASE IV with memo",
        0xF5: "FoxPro with memo",
    }

    def __init__(self, filename, codepage=None):
        self.filename = filename
        infile = open(self.filename, "rb")

        # Read header:
        header = infile.read(32)
        self.version = header[0]
        year = header[1] + 2000
        month = header[2]
        day = header[3]
        self.lastUpdate = datetime.date(year, month, day)
        # print(f"20250123 Loading {filename} (last updated {self.lastUpdate})")

        # Number of records in data file:
        self.rec_num = unpack_long(header[4:8])
        # length of header structure. Stored as binary (little endian), unsigned:
        self.first_rec = unpack_int(header[8:10])
        self.rec_len = unpack_int(header[10:12])
        self.codepage = codepage  # s[header[29]]

        # Read field defs:
        self.fields = {}
        self.field_list = []
        while 1:
            ch = infile.read(1)
            # if ch == 0x0D:
            # if ch == b'\r':
            if ch == b'\x0D':
                break
            field = DBFField(ch + infile.read(31), self)
            self.fields[field.name] = field
            self.field_list.append(field)
            # if len(self.field_list) > 20:
            #     sys.exit(1)
        # print(f"20250423 {self.field_list}")
        # n = 0
        # for fld in self.field_list:
        #     print(f"20250423 {fld.name} {fld.field_type} {
        #           fld.field_len} {fld.field_places}")
        #     n += fld.get_len()
        # print(f"20250423 {n}")

        infile.close()
        if self.has_memo():
            if self.version == 0x83:
                self.blockfile = DBTFile(self)
            else:
                self.blockfile = FPTFile(self)

    def has_memo(self):
        if self.version & self.HAS_MEMO_FILE:
            return True
        return False

    def has_blocksize(self):
        # FoxPro : return True
        return False

    def get_version(self):
        return DBFFile.versionmap[self.version]

    def __len__(self):
        return self.get_record_count()

    def get_record_count(self):
        return self.rec_num

    def get_record_len(self):
        return self.rec_len

    def get_fields(self):
        # return self.fields.values()
        return self.field_list

    def get_field(self, name):
        return self.fields[name]

    # --- Record-reading methods

    def open(self, deleted=False):
        self.recno = 0
        self.deleted = deleted
        self.infile = open(self.filename, "rb")
        # self.infile.read(32+len(self.fields)*32+1)
        self.infile.seek(self.first_rec)
        # self.field_list=sort_by_key(self.get_fields(),DBFField.get_pos)

    def get_next_record(self):
        values = {}
        ch = self.infile.read(1)
        if len(ch) == 0:
            raise Exception("Unexpected end of file")
        self.recno += 1
        # if ch == 0x1A or len(ch) == 0:
        if ch == b'\x1A':
            return None
        if ch == b"*":
            deleted = True
            # Skip the record
            # return self.get_next_record()
        else:
            deleted = False

        for field in self.field_list:
            data = self.infile.read(field.get_len())
            values[field.get_name()] = field.interpret(data)
        if deleted and not self.deleted:
            return self.get_next_record()
        # print(f"20250423 found {values}")
        return DBFRecord(self, values, deleted)

    def close(self):
        self.infile.close()
        del self.infile
        del self.deleted

    def __iter__(self):
        return self

    def __next__(self):
        rec = self.get_next_record()
        if rec is None:
            raise StopIteration
        return rec

    def fetchall(self):
        self.open()
        l = [rec for rec in self]
        self.close()
        return l


class NOTGIVEN(object):
    pass


class DBFRecord(object):
    def __init__(self, dbf, values, deleted):
        self._recno = dbf.recno
        self._values = values
        self._deleted = deleted
        self._dbf = dbf

    def deleted(self):
        return self._deleted

    def recno(self):
        return self._recno

    def __getitem__(self, name):
        return self._values[name.upper()]

    def __getattr__(self, name, default=NOTGIVEN):
        name = name.upper()
        try:
            return self._values[name]
        except KeyError:
            if default is NOTGIVEN:
                raise AttributeError(
                    "No field named %r in %s" % (name, list(self._values.keys()))
                )
            return default

    def get(self, *args, **kw):
        return self._values.get(*args, **kw)

    def __repr__(self):
        return self._dbf.filename + "#" + str(self._recno)


# --- A class for a single field


class DBFField(object):
    "Represents a field in a DBF file."

    typemap = {
        "C": "Character",
        "N": "Numeric",
        "L": "Logical",
        "M": "Memo field",
        "G": "Object",
        "D": "Date",
        "F": "Float",
        "P": "Picture",
    }

    def __init__(self, buf, dbf):
        pos = buf.find(0)
        if pos == -1 or pos > 11:
            pos = 11
        self.name = buf[:pos].decode()
        # print(f"20250123 field {self.name}")
        self.field_type = chr(buf[11])
        # self.field_pos = unpack_long(buf[12:16])
        # self.field_pos_raw = buf[12:16]
        self.field_len = buf[16]
        if self.field_type == "C":
            self.field_places = 0
            self.field_len += 256 * buf[17]
            # https://www.clicketyclick.dk/databases/xbase/format/data_types.html
            # Character fields can be up to 32 KB long (in Clipper and FoxPro)
            # using decimal count (field_places) as high byte in field length.
            # It's possible to use up to 64KB long fields by reading length as
            # unsigned.
        else:
            self.field_places = buf[17]
        self.dbf = dbf

    def __repr__(self):
        return (f"DBFField({self.name}, {self.field_type}, "
                f"{self.field_len}, {self.field_places})")

    # if self.field_type=="M" or self.field_type=="P" or \
    # self.field_type=="G" :
    # self.blockfile=blockfile

    def get_name(self):
        return self.name

    # def get_pos(self):
    #     return self.field_pos

    def get_type(self):
        return self.field_type

    def get_type_name(self):
        return DBFField.typemap[self.field_type]

    def get_len(self):
        return self.field_len

    def interpret(self, data):
        # raise Exception("20250123 good")
        # print(f"20250123 interpret {repr(self.field_type)}")
        if self.field_type == "C":
            if self.dbf.codepage is not None:
                data = data.decode(self.dbf.codepage)
            data = data.strip()
            # ~ if len(data) == 0: return None
            if len(data) == 0:
                return ""
            return data
        elif self.field_type == "L":
            return data == "Y" or data == "y" or data == "T" or data == "t"
        elif self.field_type == "M":
            try:
                # num = string.atoi(data)
                num = int(data)
            except ValueError:
                if len(data.strip()) == 0:
                    # ~ return None
                    return ""
                raise Exception("bad memo block number %s" % repr(data))
                # print("20250422 bad memo block number %s" % repr(data))
                # return ""
            return self.dbf.blockfile.get_block(num)

        elif self.field_type == "N":
            try:
                # return string.atoi(data)
                return int(data)
            except ValueError:
                return 0
        elif self.field_type == "D":
            data = data.strip()
            if not data:
                return None
            try:
                return dateparser.parse(data)
            except ValueError as e:
                raise ValueError("Invalid date value %r (%s) in field %s" %
                                 (data, e, self.name))
                # print("20250422 Invalid date value %r (%s) in field %s" %
                #       (data, e, self.name))
            # ~ return data # string "YYYYMMDD", use the time module or mxDateTime
        else:
            raise NotImplementedError("Unknown data type " + self.field_type)


# --- A class that represents a block file


class FPTFile(object):
    "Represents an FPT block file"

    def __init__(self, dbf):
        self.dbf = dbf
        self.filename = dbf.filename[:-4] + ".FPT"
        infile = open(self.filename, "rb")
        infile.read(6)
        self.blocksize = unpack_int_rev(infile.read(2))
        infile.close()

    def get_block(self, number):
        infile = open(self.filename, "rb")
        infile.seek(512 + self.blocksize * (number - 8))  # ?

        code = infile.read(4)
        if code != "\000\000\000\001":
            return "Block %d has invalid code %s" % (number, repr(code))

        length = infile.read(4)
        length = unpack_long_rev(length)
        data = infile.read(length)
        infile.close()

        data = data.strip()
        if len(data) == 0:
            return None
        return data


class DBTFile(object):
    "Represents a DBT block file"

    def __init__(self, dbf):
        self.dbf = dbf
        self.filename = dbf.filename[:-4] + ".DBT"
        self.blocksize = 512
        # print(f"20250123 Opening DBTFile {self.filename}")

    def get_block(self, number):
        infile = open(self.filename, "rb")
        infile.seek(512 + self.blocksize * (number - 1))
        data = b""
        while True:
            buf = infile.read(self.blocksize)
            if len(buf) != self.blocksize:
                raise Exception(f"20250123 {number}:{len(buf)}")
                data += buf
                break
            data += buf
            pos = data.find(0x1A)
            # pos = data.find("\x1A\x1A")
            if pos != -1:
                data = data[:pos]
                break

        infile.close()
        if self.dbf.codepage is not None:
            data = data.decode(self.dbf.codepage)
        # clipper adds "soft CR's" to memo texts. we convert them to
        # simple spaces:
        data = data.replace("\xec\n", "")

        # convert CR/LF to simple LF:
        data = data.replace("\r\n", "\n")

        data = data.strip()
        if len(data) == 0:
            return None
        return data


# --- A class that stores the contents of a DBF file as a hash of the
#     primary key


# class DBFHash(object):
#     def __init__(self, file, key):
#         self.file = DBFFile(file)
#         self.hash = {}
#         self.key = key
#
#         self.file.open()
#         while 1:
#             rec = self.file.get_next_record()
#             if rec is None:
#                 break
#             self.hash[rec[self.key]] = rec
#
#     def __getitem__(self, key):
#         return self.hash[key]


# --- Utility functions


def display_info(f):
    print(f.get_version())
    print(f.get_record_count())
    print(f.get_record_len())

    for field in f.get_fields():
        print(
            "%s: %s (%d)" % (field.get_name(), field.get_type_name(), field.get_len())
        )


def make_html(f, out=sys.stdout, skiptypes="MOP"):
    out.write("<TABLE>\n")

    # Writing field names
    out.write("<TR>")
    for field in f.get_fields():
        out.write("<TH>" + field.get_name())

    f.open()
    while 1:
        rec = f.get_next_record()
        if rec is None:
            break

        out.write("<TR>")
        for field in f.get_fields():
            if not field.get_type() in skiptypes:
                out.write("<TD>" + str(rec[field.get_name()]))
            else:
                out.write("<TD>*skipped*")

    f.close()
    out.write("</TABLE>\n")


if __name__ == "__main__":
    make_html(DBFFile(sys.argv[1]))
