# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""

This module contains a generic writer to create arbitrary-based output. All Writers shall
contain the same public methods.
"""
import os
import traceback
from io import StringIO

from patme.service.logger import log


class GenericWriter:
    """Abstract geometry writer class"""

    commentChar = ""

    def __init__(self, filename="", **kwargs):
        """doc"""
        self.filename = filename
        self.lineBuffer = StringIO()

    def __enter__(self):
        """doc"""
        fObj = getattr(self, "f", None)
        logFunction = log.debug
        if not fObj:
            try:
                self.lineBuffer = StringIO()
                mode, descr = ("w", "") if getattr(self, "overwriteFile", True) else ("a", "re")
                logFunction(f"{descr}opening file {self.filename}")
                self.f = open(self.filename, mode)
            except:
                self.close()
                raise
        elif fObj.closed:
            try:
                logFunction(f"reopening file {self.filename}")
                self.lineBuffer = StringIO()
                self.f = open(self.filename, "a")
            except:
                self.close()
                raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """doc"""
        if exc_type:
            traceback.print_exception(exc_type, exc_val, exc_tb)
        else:
            self.end()

    def preamble(self, *args, **kwargs):
        """Doing writer-dependend initialization work"""
        raise NotImplementedError("This is an abstract method.")

    def end(self):
        """Writer-dependent finalizing of the writer."""
        raise NotImplementedError("This is an abstract method.")

    def includeOtherFile(self, otherFile):
        """Writer-dependent including of other files into current writer instance."""
        raise NotImplementedError("This is an abstract method.")

    def close(self):
        """doc"""
        try:
            # write line buffer content to file
            self.f.write(self.lineBuffer.getvalue())
        except:
            log.debug(f'Filedescriptor of writer "{self}" is not open! Could not write line')

        if hasattr(self, "f") and not self.f.closed:
            log.debug(f"closing file {self.filename}")
            self.f.close()

        self.lineBuffer.close()  # reset buffer

    def save(self):
        """Saving the writer output to a writer dependent path."""
        self._save()

    def functionPreamble(self, functionName="", sketchNumber=""):
        """Writes preamble of a function: like Subroutine ... or function ..."""

    def commentHeadline(self, comment="", printTime=False):
        """Big comment"""

    def comment(self, comment=""):
        self.writeRow(self.commentChar + comment)

    def printTime(self, outString):
        """This method makes the output language print the"""

    def writeRows(self, rows):
        """doc"""
        self.writeRow("\n".join(rows))

    def writeRow(self, outString=""):
        """doc"""
        self.lineBuffer.write(outString + "\n")

    def orientationPoint(self, point):
        """is intended for ansys to write the orientation point of beams

        Other geometry writer do not need this point, thus this method omits everything
        """

    def _getRunDir(self):
        """doc"""
        if self.filename:
            pathName = os.path.dirname(os.path.abspath(self.filename))
            if pathName != "":
                return pathName
        return "."

    runDir = property(fget=_getRunDir)
