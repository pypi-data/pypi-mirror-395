# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import subprocess

from lxml import etree
from lxml import isoschematron


# def validate_xml(doc, xsdfile):
def validate_xml(xmlfile, xsdfile):
    """

    Validate the given :attr:`xmlfile` using the given :attr:`xsdfile`.
    Validate the given XML document `doc` using the given :attr:`xsdfile`.
    The document must be an ElementTree root element.

    When :attr:`xsdfile` ends with :file:`.xsd`, the generated :attr:`xmlfile`
    file is validated using :class:`lxml.etree.XMLSchema`. When it ends with
    :file:`.sch`, the generated :attr:`xmlfile` file is validated using
    :class:`lxml.isoschematron.Schematron`.


    """
    doc = etree.parse(xmlfile)
    if xsdfile.suffix == ".xsd":
        # xsd = etree.XMLSchema(etree.parse(xsdfile))
        xsd = etree.XMLSchema(file=xsdfile)
        xsd.assertValid(doc)
    elif xsdfile.suffix == ".sch":
        if False:
            jarfile = "/home/luc/Downloads/saxon/saxon-he-12.5.jar"
            # cmd = ["/usr/bin/java", "-jar", jarfile, "-xsl:", xsdfile, "-s:", xmlfile]
            cmd = ["/usr/bin/java", "-jar", jarfile, f"-xsd:{xsdfile}", f"-s:{xmlfile}"]
            cp = subprocess.run(cmd)

        if False:
            # # sch = etree.parse(xsdfile)
            # # schematron = isoschematron.Schematron(sch, store_report=True)
            schematron = isoschematron.Schematron(file=xsdfile, store_report=True)
            schematron.assertValid(doc)
            # schematron.validation_report
