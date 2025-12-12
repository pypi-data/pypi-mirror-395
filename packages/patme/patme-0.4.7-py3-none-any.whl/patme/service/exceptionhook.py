# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
In order to have better readable error messages for users, the standard exception output is modified.

This exception hook prints the exceptions message in a nice format without traceback. The console output and
traceback are written to a file. The exception hook is set in place using the redirectExceptions function.

Usage::

    from patme.service.exceptionhook import redirectExceptions
    redirectExceptions(progName='MyProg', ver='0.1.0')
    raise Exception('foobar')

Output::

    ################################################################################
    Error: Program "MyProg" stopped due to an exception
    2020-05-04, 18:20:49
    Version: 0.1.0
    Error log file at: C:\\eclipse_projects\\patme\\src\\patme\\service\\err.log
    Error message:
    --------------------------------------------------------------------------------
"""

import io
import os
import sys
import time
import traceback

from patme.service.logger import log

errorLogFilename = None
programName = None
version = None


def redirectExceptions(errorLogFile="err.log", toDir=None, progName=None, ver=None):
    """introduces the a nicer exception hook into this python process

    :param errorLogFile: File containing the exception message including the traceback
    :param toDir: Directory of the error log file.
    :param progName: name of the program
    :param ver: version of the program"""
    if toDir is not None:
        errorLogFile = os.path.join(toDir, os.path.basename(errorLogFile))

    global errorLogFilename, programName, version
    errorLogFilename = errorLogFile
    programName = progName
    version = ver

    # set system exception hook
    sys.excepthook = excepthook


def excepthook(excType, excValue, tracebackobj):
    """
    function to catch exceptions. It writes a log to errorLogFilename.

    :param excType: exception type
    :param excValue: exception value
    :param tracebackobj: traceback object
    """
    separator = "-" * 80
    separatorTop = "#" * 80

    versionInfo = "" if version is None else "Version: " + version + "\n"
    name = "" if programName is None else ' "' + programName + '"'
    logFileNotice = f"Error log file at: {os.path.abspath(errorLogFilename)}"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    notice = f"Error: Program{name} stopped due to an exception"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = "Traceback:\n" + tbinfofile.read()
    errmsg = f"{str(excType)}: \n{str(excValue)}"
    sections = [
        separatorTop,
        notice,
        timeString,
        versionInfo + logFileNotice,
        "Error message:",
        separator,
        errmsg,
        separator,
        tbinfo,
    ]
    msg = "\n".join(sections) + "\n" * 4
    if errorLogFilename:
        try:
            with open(os.path.normpath(errorLogFilename), "a") as f:
                f.write(msg)
        except OSError:
            pass
    log.end()
    sys.stdout.flush()
    sys.stderr.write("\n".join(sections[:8]) + "\n\n")
    sys.stderr.flush()
