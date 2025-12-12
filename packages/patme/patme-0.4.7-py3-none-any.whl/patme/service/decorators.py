# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Created on 13.07.2016

@author: schu_a1
"""
import cProfile
import functools
import hashlib
import pickle

from patme.service.logger import log


def inheritDocStringFromFunction(fromFunction):
    """For the original implementation refer to https://groups.google.com/forum/#!msg/comp.lang.python/HkB1uhDcvdk/lWzWtPy09yYJ"""

    def docstringInheritingDecorator(toFunction):
        toFunction.__doc__ = fromFunction.__doc__
        return toFunction

    return docstringInheritingDecorator


def memoize(obj):
    """Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        # =======================================================================
        # calculate key
        # =======================================================================
        try:
            pickleString = pickle.dumps((args, kwargs), protocol=0)
            key = hashlib.sha256(pickleString).hexdigest()
        except AttributeError:  # if items can not be pickled
            try:
                key = args + tuple(kwargs.items())
                hash(key)  # try to hash key
            except TypeError:  # if args or kwargs can not be hashed
                log.debug("Args and kwargs can not be cached. Calculating function each time.")
                return obj(*args, **kwargs)
        # =======================================================================
        # call function or use cached samples and return them
        # =======================================================================
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        else:
            log.debug("use cached results for these args and kwargs: {}".format((args, kwargs)))
        return cache[key]

    return memoizer


def avoidDublicate(obj):
    """Returns None, if this input was already processed"""
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = repr(args) + str(kwargs)
        if key not in cache:
            cache[key] = True
            obj(*args, **kwargs)
        else:
            return

    return memoizer


def returnNoneOnFail(obj):
    @functools.wraps(obj)
    def returnFunc(*args, **kwargs):
        try:
            return obj(*args, **kwargs)
        except:
            return None

    return returnFunc
