# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
This logger extends the python logging with several features.

- it utilizes a simple method to create log file handlers - for debug and for regular log messages.
- it cuts the log width by introducing linebreaks automatically
- it can switch the log level using the with-statement easily (switchLevelTemp)
- it counts the log entries

As example, please refer to ``test.test_service.test_logger``

"""

import logging
import os
import re
import sys
import time
import traceback
from contextlib import contextmanager

from _io import StringIO

from patme.service.exceptions import ImproperParameterError, InternalError


def resetLoggerToNewRunDir(runDir, logLevel=logging.INFO):
    """resets the logger to the given run dir"""
    if not os.path.exists(runDir) or not os.path.isdir(runDir):
        raise ImproperParameterError(f"The given path does not exist: {runDir}")

    log.log(logLevel, f"Change logging to this directory: {runDir}")
    # create dummy logger having handlers with correct paths. these handlers are moved to the old logger
    log.setLogPath(runDir)

    # err log file
    from patme.service import exceptionhook

    if sys.excepthook is exceptionhook.excepthook:
        exceptionhook.errorLogFilename = os.path.join(runDir, os.path.basename(exceptionhook.errorLogFilename))


class MyLogger(logging.Logger):
    """ """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.FATAL
    CRITICAL = logging.CRITICAL
    NOTSET = logging.NOTSET
    TABSTR = "    "

    def __init__(
        self,
        name,
        baseDirectory=None,
        logFileName=None,
        debugLogFileName=None,
        logLevel=logging.INFO,
        enableParallelHandling=False,
    ):
        """doc"""
        logging.Logger.__init__(self, name, level=MyLogger.DEBUG)
        """Logger is initialized with DEBUG as log level. This is required for the
        debug.log handler. The real log level used is set in each handler.
        See self._setLogLevel for details."""
        self.startTime = time.time()
        self.debugCount = 0
        self.infoCount = 0
        self.warningCount = 0
        self.errorCount = 0
        self.maxLineLength = 120
        self._intendationDepth = 0
        self.logFileName = logFileName
        self.debugLogFileName = debugLogFileName

        self.debugHandler = None
        """This is the debug log handler. It is stored as extra variable to identify it
        and prevent it from changing the loglevel of the handler. The debug log handler
        should always have DEBUG as level"""

        procID = None
        for keyToTest in ["SLURM_PROCID", "PMI_RANK"]:
            if keyToTest in os.environ.keys():
                enableParallelHandling = True
                procID = os.environ[keyToTest]
                break

        if enableParallelHandling:

            formatStr = "%(levelname)s  "
            if procID is not None:
                formatStr += f"RK{procID}"
            else:
                formatStr += "P%(process)s"

            formatStr += "  %(asctime)s: %(message)s"
            self.parallelMode = True

        else:

            self.parallelMode = False
            formatStr = "%(levelname)s\t%(asctime)s: %(message)s"

        self.formatter = logging.Formatter(formatStr, None)

        # stream handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        handler.setLevel(logLevel)
        self.addHandler(handler)

        if logFileName or debugLogFileName:
            self.addFileHandlers(baseDirectory, logFileName, debugLogFileName)

    def increaseIntendationLevel(self):
        """doc"""
        self._intendationDepth += 1

    def decreaseIntendationLevel(self):
        """doc"""
        self._intendationDepth -= 1
        self._intendationDepth = max(self._intendationDepth, 0)

    def addFileHandlers(self, baseDirectory, logFileName, debugLogFileName):
        """Adds a file handler that is identical to the stream handler and one
        file handler with debug log level"""
        self.logFileName = logFileName
        self.debugLogFileName = debugLogFileName

        if baseDirectory is None:
            # initialize handlers as stream until they are set to a directory in setLogPath()

            # run log handler
            handler = logging.StreamHandler(StringIO())
            handler.setFormatter(self.formatter)
            handler.setLevel(self.logLevel)
            self.addHandler(handler)
            # debug log handler
            self.debugHandler = logging.StreamHandler(StringIO())
            self.addHandler(self.debugHandler)

        else:

            logFileNameFull = os.path.join(baseDirectory, logFileName)
            debugLogFileNameFull = os.path.join(baseDirectory, debugLogFileName)

            for ffile in [logFileNameFull, debugLogFileNameFull]:
                try:
                    # remove log files in case they are greater than approx 10MB
                    if os.path.getsize(ffile) > 1e7:
                        os.remove(ffile)
                except:
                    pass

            # run log handler
            handler = logging.FileHandler(logFileNameFull, "a")
            handler.setFormatter(self.formatter)
            handler.setLevel(self.logLevel)
            self.addHandler(handler)

            # debug log handler
            self.debugHandler = logging.FileHandler(debugLogFileNameFull, "a")
            self.addHandler(self.debugHandler)

        self.debugHandler.setFormatter(self.formatter)
        self.debugHandler.setLevel(log.DEBUG)

    def debug(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.debugCount += 1
        returnMessageList = self.parallelMode
        longMesageDelim = kwargs.pop("longMesageDelim", None)
        retMsg = self.formatLongMessages(msg, returnMessageList, longMesageDelim=longMesageDelim)
        if not returnMessageList:
            retMsg = [retMsg]

        pref = self.TABSTR * self.intendationDepth
        for msg in retMsg:
            logging.Logger.debug(self, f"{pref}{msg}", *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.infoCount += 1
        returnMessageList = self.parallelMode
        longMesageDelim = kwargs.pop("longMesageDelim", None)
        retMsg = self.formatLongMessages(msg, returnMessageList, longMesageDelim=longMesageDelim)
        if not returnMessageList:
            retMsg = [retMsg]

        pref = self.TABSTR * self.intendationDepth
        for msg in retMsg:
            logging.Logger.info(self, f"{pref}{msg}", *args, **kwargs)

    def infoHeadline(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.infoCount += 1
        pref = self.TABSTR * self.intendationDepth
        logging.Logger.info(
            self, f"{pref}================================================================================"
        )
        logging.Logger.info(self, f"{pref}  {msg}", *args, **kwargs)
        logging.Logger.info(
            self, f"{pref}================================================================================"
        )

    def warn(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.warningCount += 1
        returnMessageList = self.parallelMode
        retMsg = self.formatLongMessages(msg, returnMessageList)
        if not returnMessageList:
            retMsg = [retMsg]

        pref = self.TABSTR * self.intendationDepth
        for msg in retMsg:
            logging.Logger.warning(self, f"{pref}{msg}", *args, **kwargs)

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        sio = StringIO()
        tb = ei[2]
        # See issues #9427, #1553375. Commented out for now.
        # if getattr(self, 'fullstack', False):
        #    traceback.print_stack(tb.tb_frame.f_back, file=sio)
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]

        return s

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self.error(msg, *args, exc_info=exc_info, **kwargs)

    def error(self, msg, *args, **kwargs):
        """see description of logging.Logger.<methodname>"""
        self.errorCount += 1
        exc_info = kwargs.pop("exc_info", False)
        logging.Logger.error(self, msg, *args, **kwargs)

        if exc_info:
            exceptionLines = self.formatException(sys.exc_info()).split("\n")
            for msg in exceptionLines:
                logging.Logger.error(self, msg, *args, **kwargs)

    def end(self):
        """doc"""
        duration = time.time() - self.startTime
        log.info(f"Program run finished. Runtime of program: {duration:4.4f} sec")
        msg = [
            f"{self.errorCount} errors",
            f"{self.warningCount} warnings",
            f"{self.infoCount + 1} info messages",
            f"{self.debugCount} debug messages",
        ]

        self.info("; ".join(msg))

        logging.shutdown()

    def _getLogLevel(self):
        """doc"""
        for handler in self.handlers:
            if handler is self.debugHandler:
                continue
            return handler.level
        raise InternalError("There is no log handler besides the debug handler. Please check your log handlers")

    def _setLogLevel(self, logLevel):
        """doc"""
        logging._checkLevel(logLevel)
        for handler in self.handlers:
            if handler is self.debugHandler:
                # the loglevel of the debug handler will not be changed
                continue
            handler.level = logLevel

    def setLogPath(self, logPath=None):
        """This method reinitializes the file based log handlers according to the new path given.

        :param logPath: New Path of the handlers. If it is not given, the current directory is used.
        """
        if not logPath:
            logPath = os.getcwd()

        oldHandlers = self.handlers

        dummyLogger = MyLogger(
            "logger",
            baseDirectory=logPath,
            logFileName=self.logFileName,
            debugLogFileName=self.debugLogFileName,
            logLevel=self.logLevel,
        )
        self.handlers = dummyLogger.handlers
        self.debugHandler = dummyLogger.debugHandler

        for oldhandler, newHandler in zip(oldHandlers, self.handlers):

            if isinstance(oldhandler.stream, StringIO):
                newHandler.stream.write(oldhandler.stream.getvalue())

            oldhandler.close()

    @contextmanager
    def switchLevelTemp(self, temporaryLogLevel):
        """doc"""
        # changing loglevel for less output temporarily
        # can be used by "with log.switchLevelTemp(newLevel):"
        oldLogLevel = self.logLevel
        self.logLevel = temporaryLogLevel
        yield
        self.logLevel = oldLogLevel

    def formatLongMessages(self, msg, returnAsMessagesList=False, longMesageDelim=None):
        """doc"""
        msg_str = str(msg)
        if "\n" in msg_str:
            # message is already formatted
            return msg_str

        pattern = longMesageDelim
        if longMesageDelim is None:
            pattern = r"(,|\.?\s+)"

        subStrings = []
        while len(msg_str) > self.maxLineLength:
            indexes = [m.start() for m in re.finditer(pattern, msg_str) if m.start() <= self.maxLineLength]
            if indexes:
                nearestIx = max(indexes) + 1
            else:
                indexes = [m.start() for m in re.finditer(pattern, msg_str) if m.start() > self.maxLineLength]
                if indexes:
                    nearestIx = indexes[0] + 1
                else:
                    nearestIx = None

            subStrings.append(msg_str[:nearestIx])
            if nearestIx is None:
                msg_str = ""
            else:
                msg_str = msg_str[nearestIx:]

        if msg_str != "":
            subStrings.append(msg_str)

        if returnAsMessagesList:
            return subStrings
        else:
            return "\n\t\t\t\t ".join(subStrings)

    def _getIntendationDepth(self):
        """doc"""
        return self._intendationDepth

    def getFileHandlerFilenames(self):
        """Returns a list of the filenames of the file handlers"""
        return [handler.baseFilename for handler in self.handlers if hasattr(handler, "baseFilename")]

    intendationDepth = property(fget=_getIntendationDepth)
    logLevel = property(fget=_getLogLevel, fset=_setLogLevel)


log = MyLogger("logger")
