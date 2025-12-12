# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Measurement of the duration for executing functions and methods and within methods.

Usage for **functions and methods**::

    from patme.service.duration import Duration

    duration = Duration()
    @duration.timeit
    def testfunc():
        a='do something'

Usage **within functions/methods**::

    from patme.service.duration import measureDuration

    def testfunc():
        with measureDuration():
            a='do something'

The **logLevel** of all Duration instances may be changed with ``setDurationLogLevel``:

>>> from patme.service.logger import log
>>> from patme.service.duration import setDurationLogLevel
>>> setDurationLogLevel(log.logLevel + 1)


"""

import logging
import time
from contextlib import contextmanager

from patme.service.logger import log


class Duration:
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """

    def timeit(self, method):
        global _durationLogLevel

        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            log.log(
                _durationLogLevel,
                f"Duration for execution of method or class {method.__name__!r}: {te - ts:4.4f} sec",
            )
            return result

        return timed


_durationLogLevel = log.logLevel + 1
logging.addLevelName(_durationLogLevel, "TIME")


def setDurationLogLevel(logLevel):
    """Sets the log level to the logging module and the Duration class"""
    global _durationLogLevel
    logging.addLevelName(logLevel, "TIME")
    _durationLogLevel = logLevel


def getDurationLogLevel():
    """Returns the duration log level"""
    return _durationLogLevel


@contextmanager
def measureDuration():
    """doc"""
    start = time.time()
    yield
    end = time.time()
    print("Duration: %2.5f" % (end - start))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
