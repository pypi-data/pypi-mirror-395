# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Created on 16.06.2021

@author: schu_a1
"""

from itertools import chain, tee
from operator import attrgetter

from patme.service.exceptions import InternalError


class GenericEntityList(list):
    """classdocs"""

    def __init__(self, *args, **kwargs):
        """doc"""
        if len(args) > 0 and isinstance(args[0], str):
            raise InternalError(
                "Incorrect initialization of structureElementList. "
                + 'Probably "defaultSortAttribute" needs to be added as key'
            )

        attr = kwargs.pop("defaultSortAttribute", None)
        list.__init__(self, *args, **kwargs)
        if attr is not None:
            self.defaultSortAttribute = attr

    def sort(self, key=None, reverse=False, attribute=None):
        """doc"""
        if key == None:
            if attribute == None:
                attribute = self.defaultSortAttribute

            if isinstance(attribute, str) or not hasattr(attribute, "__iter__"):
                # make attribute an iterable item if needed
                attribute = [attribute]

            key = attrgetter(*attribute)

        list.sort(self, key=key, reverse=reverse)

    def update(self, newEntries):
        """doc"""
        self += [elem for elem in newEntries if elem not in self]
        return self

    def copy(self):
        """doc"""
        return self.__class__(self[:], defaultSortAttribute=self.defaultSortAttribute)

    def applyFuncOnElements(self, func=None):
        """Method applies function on list and return flatten list"""
        return self.__class__(chain.from_iterable(map(func, self)), defaultSortAttribute=self.defaultSortAttribute)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def invertDict(mydict):
    """This method inverts a dictionary and returns it. To apply the inversion without
    loss of data the mapping should be bijective."""
    return dict([[v, k] for k, v in mydict.items()])
