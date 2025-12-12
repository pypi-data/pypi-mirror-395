# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""
documentation
"""
import numpy as np

from patme.service.exceptions import GeometryError, ImproperParameterError


class Scaling(np.ndarray):
    """
    This class describes a scaling in 3D space which is represented by a 3x3 matrix.

    With this class scalings in 3D space can be created and operations may be performed.
    For that purpose the class inherits from np.ndarray which is a class for storing
    matrix values and performing operations on them. For further details on np.ndarray
    please refer to the numpy/scipy documentation.

    Scalings are represented by a 3x3 diagonal scaling matrix.

    Usage::

        >>> import numpy as np
        >>> from patme.geometry.scale import Scaling
        >>> # creating identity Scaling
        >>> s=Scaling()
        >>> s
        Scaling([[1., 0., 0.],
                 [0., 1., 0.],
                 [0., 0., 1.]])
        >>> # creating empty scaling objects for demonstration below
        >>> sx=s.copy()
        >>> sxy=s.copy()
        >>> # creating scaling by defining scaling factors!
        >>> # scaling by 2.0 by x-coordinate
        >>> sx.factors = (2.0,1.0,1.0)
        >>> sx
        Scaling([[2., 0., 0.],
                 [0., 1., 0.],
                 [0., 0., 1.]])
        >>> # scaling by 2.0 by x-, y-coordinate and z-coordinate
        >>> sxyz=s.copy()
        >>> sxyz.factors = (2.0,2.0,2.0)
        >>> sxyz
        Scaling([[2., 0., 0.],
                 [0., 2., 0.],
                 [0., 0., 2.]])

        >>> # multiplying scalings
        >>> sx * sxyz
        Scaling([[4., 0., 0.],
                 [0., 2., 0.],
                 [0., 0., 2.]])

        >>> # scaling points
        >>> from patme.geometry.translate import Translation
        >>> t = Translation([1,2,0])
        >>> # scaling in x
        >>> sx * t
        Translation([2., 2., 0.])
        >>> # scaling in all directions
        >>> sxyz * t
        Translation([2., 4., 0.])
    """

    __hash__ = object.__hash__
    """hash reimplementation due to definition of __eq__. See __hash__ doc for more details.
    https://docs.python.org/3.4/reference/datamodel.html#object.__hash__"""

    def __new__(cls, input_array=None):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        if input_array is None:
            input_array = np.identity(3, dtype=np.float64)
        if not hasattr(input_array, "shape"):
            input_array = np.asarray(input_array)
        if not input_array.shape == (3, 3):
            raise ImproperParameterError(
                "The given scaling must be a 3x3 matrix like object. Got this instead: " + str(input_array)
            )
        obj = input_array.view(cls)
        # add the new attribute to the created instance
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        """ID of the Point within the FEM"""

    def isIdentity(self):
        """doc"""
        return np.allclose(self, np.identity(3, dtype=np.float64))

    def getInverse(self):
        """:return: returns a copy of the inverted array"""
        return np.linalg.inv(self)

    def __invert__(self):
        """doc"""
        self[:3, :3] = self.getInverse()

    def __mul__(self, other):
        """doc"""
        try:
            ret = np.dot(self, other)
            if ret.shape == (3,):
                cls = other.__class__
                if cls is np.ndarray:
                    cls = np.array
                return cls(ret)
            return ret
        except ValueError:  # possibly multiplication with coordinatesystem
            return np.dot(self, other[:3, :3])

    def __imul__(self, other):
        """doc"""
        if other.shape == (3,):
            raise GeometryError("Operator *= cannot be used with (rotation, translation) operands!")
        self = self * other

    def __eq__(self, other):
        """doc"""
        try:
            return np.allclose(self, other)
        except TypeError:
            return False

    def _getScaling(self):
        """doc"""
        return tuple(np.diag(self[:3, :3]))

    def _setScaling(self, factors):
        """doc"""
        self.setfield(np.diag(factors[:3]), np.float64)
        return self

    factors = property(fget=_getScaling, fset=_setScaling)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
