# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""
documentation
"""

import numpy as np

from patme.service.exceptions import ImproperParameterError


class Translation(np.ndarray):
    """
    This class describes a point in 3D space which is represented by a vector of length 3.

     With this class points in 3D space can be created and operations may be performed.
     For that purpose the class inherits from np.ndarray which is a class for storing
     matrix values and performing operations on them. For further details on np.ndarray
     please refer to the numpy/scipy documentation.

     Usage::

       >>> from patme.geometry.translate import Translation
       >>> t = Translation([1,2,0])
       >>> t
       Translation([1, 2, 0])
       >>> # getting only one coordinate
       >>> t.x
       1
       >>> # setting only one coordinate value
       >>> t.x = 5
       >>> t
       Translation([5, 2, 0])
       >>> #adding translations
       >>> t2 = t + t
       >>> t2
       Translation([10,  4,  0])
       >>> # getting the distance between two translations
       >>> t.distance(t2)
       5.385164807134504
       >>> # checking coordinate equality
       >>> t3=Translation([5,2,0])
       >>> t==t;t==t2;t==t3
       True
       False
       True

    """

    __hash__ = object.__hash__
    """hash reimplementation due to definition of __eq__. See __hash__ doc for more details.
    https://docs.python.org/3.4/reference/datamodel.html#object.__hash__"""

    def __new__(cls, input_array=None, id=None):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        if input_array is None:
            input_array = np.zeros(3)
        if not hasattr(input_array, "shape"):
            input_array = np.asarray(input_array)
        if not input_array.shape == (3,):
            raise ImproperParameterError(
                "The given translation must be a vector with 3 elements. Got this instead: %s" % input_array
            )

        obj = input_array.view(cls)
        # cope with numerical inaccuracy
        setZero = abs(obj) < 1e-15
        if np.any(setZero):
            obj[setZero] = 0.0
        # Finally, we must return the newly created object:
        return obj

    def distance(self, toPoint):
        """doc"""
        return np.linalg.norm(self - toPoint)

    def __eq__(self, other):
        """doc"""
        try:
            return np.allclose(self, other)
        except TypeError:
            return False

    def _getX(self):
        """doc"""
        return self[0]

    def _setX(self, x):
        """doc"""
        self[0] = x

    def _getY(self):
        """doc"""
        return self[1]

    def _setY(self, y):
        """doc"""
        self[1] = y

    def _getZ(self):
        """doc"""
        return self[2]

    def _setZ(self, z):
        """doc"""
        self[2] = z

    x = property(fget=_getX, fset=_setX)
    y = property(fget=_getY, fset=_setY)
    z = property(fget=_getZ, fset=_setZ)


def getNearestPointOrPointsIndex(fromPointOrPoints, toPoints):
    """calculates the index of the toPoint that is closest to fromPointOrPoints

    :param fromPointOrPoints: point or 2d array with points (fromPointNum, (x,y,z))
    :param toPoints: 2d array with points (toPointNum, (x,y,z))
    :return: index of nearest point or list of indices of nearest points (len = fromPointNum)
    """
    points = np.array(fromPointOrPoints)
    if len(points.shape) == 1:
        return np.argmin(np.linalg.norm(points - toPoints, axis=1))

    # create 3d arrays
    loadPointsExtended = np.array([toPoints])
    pointsExtended = np.array([[point] for point in points])
    distances = np.linalg.norm(pointsExtended - loadPointsExtended, axis=2)
    return np.argmin(distances, axis=1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
