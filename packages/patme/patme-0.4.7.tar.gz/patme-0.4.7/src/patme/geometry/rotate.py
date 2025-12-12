# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""
documentation
"""
import numpy as np

from patme import epsilon
from patme.geometry.transformations import euler_from_matrix, euler_matrix
from patme.geometry.translate import Translation
from patme.service.exceptions import GeometryError, ImproperParameterError
from patme.service.logger import log


class Rotation(np.ndarray):
    """
    This class describes a rotation in 3D space which is represented by a 3x3 matrix.

    With this class rotations in 3D space can be created and operations may be performed.
    For that purpose the class inherits from np.ndarray which is a class for storing
    matrix values and performing operations on them. For further details on np.ndarray
    please refer to the numpy/scipy documentation.

    Rotations are represented by a 3x3 symmetirc rotation matrix.

    Usage::

        >>> import numpy as np
        >>> from patme.geometry.rotate import Rotation
        >>> # creating identity rotation
        >>> r=Rotation()
        >>> r
        Rotation([[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
        >>> # creating empty rotation objects for demonstration below
        >>> rx=r.copy()
        >>> ry=r.copy()
        >>> rxy=r.copy()
        >>> # creating rotation by defining angles in radians!
        >>> # by default the rotation is performed in a static reference frame in the
        >>> # order x,y,z. Those 24 rotationstypes may be used: 'sxyz', 'sxyx', 'sxzy',
        >>> # 'sxzx', 'syzx', 'syzy', 'syxz', 'syxy', 'szxy', 'szxz', 'szyx', 'szyz',
        >>> # 'rzyx', 'rxyx', 'ryzx', 'rxzx', 'rxzy', 'ryzy', 'rzxy', 'ryxy', 'ryxz',
        >>> # 'rzxz', 'rxyz'(default), 'rzyz'.
        >>> # The first item represents a static or rotating reference frame respectively.
        >>> # Static reference frame means that also the rotation around the second and thrid
        >>> # angle is performed in reference to the initial rotation. Rotating reference frame
        >>> # means that rotation around the second angle is done in respect to the reference
        >>> # frame that is created by the rotation around the first angle; respectively
        >>> # for the third angle.
        >>> # Additionally a rotation 'sxyz' is equal to 'rzyx' and so on.
        >>> #
        >>> # rotating by 90 degrees by x-coordinate
        >>> rx.angles = [np.pi/2,0,0]  # or
        >>> rx.angles = [np.pi/2,0,0,'rxyz']
        >>> rx.round()
        Rotation([[ 1.,  0., -0.],
                  [-0.,  0., -1.],
                  [ 0.,  1.,  0.]])
        >>> # rotating by 90 degrees around x and subsequently by 90 degrees around y
        >>> # with a rotating reference frame
        >>> rxy.angles = [np.pi/2,np.pi/2,0,'rxyz']
        >>> rxy
        Rotation([[ 6.12323400e-17,  0.00000000e+00,  1.00000000e+00],
                  [ 1.00000000e+00,  6.12323400e-17, -6.12323400e-17],
                  [-6.12323400e-17,  1.00000000e+00,  3.74939946e-33]])

        >>> # multiplying rotations
        >>> ry.angles = [0,np.pi/2,0,'rxyz']
        >>> ry
        Rotation([[ 6.123234e-17,  0.000000e+00,  1.000000e+00],
                  [-0.000000e+00,  1.000000e+00,  0.000000e+00],
                  [-1.000000e+00, -0.000000e+00,  6.123234e-17]])
        >>> rx * ry
        Rotation([[ 6.12323400e-17,  0.00000000e+00,  1.00000000e+00],
                  [ 1.00000000e+00,  6.12323400e-17, -6.12323400e-17],
                  [-6.12323400e-17,  1.00000000e+00,  3.74939946e-33]])

        >>> # rotating points
        >>> from patme.geometry.translate import Translation
        >>> t = Translation([1,2,0])
        >>> # rotating around x
        >>> rx * t
        Translation([1., 0., 2.])
        >>> # rotating around x and then y with rotating reference frame
        >>> rxy * t
        Translation([0., 1., 2.])
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
                "The given rotation must be a 3x3 matrix like object. Got this instead: " + str(input_array)
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

    def _isIdentity(self):
        """doc"""
        return np.allclose(self, np.identity(3))

    def getInverse(self):
        """:return: returns a copy of the inverted array"""
        return np.linalg.inv(self)

    def setRotationByPoints(self, origin, xCoordinate, xyPlaneCoordinate):
        """doc"""
        if not isinstance(origin, Translation):
            origin = Translation(origin)
        if not isinstance(xCoordinate, Translation):
            xCoordinate = Translation(xCoordinate)
        if not isinstance(xyPlaneCoordinate, Translation):
            xyPlaneCoordinate = Translation(xyPlaneCoordinate)

        xAxisLocal = xCoordinate - origin
        yxAxisLocal = xyPlaneCoordinate - origin
        if xCoordinate.distance(origin) < epsilon or xyPlaneCoordinate.distance(origin) < epsilon:
            raise GeometryError("Given points are not distinct from each other.")

        xAxisLocal = xAxisLocal / np.linalg.norm(xAxisLocal, 2)
        zAxisLocal = np.cross(xAxisLocal, yxAxisLocal)
        # check for linear dependency
        if np.linalg.norm(zAxisLocal, 2) < epsilon:
            raise ImproperParameterError("given vectors are linear dependent")
        zAxisLocal = zAxisLocal / np.linalg.norm(zAxisLocal, 2)

        yAxisLocal = np.cross(xAxisLocal, zAxisLocal) * -1
        yAxisLocal = yAxisLocal / np.linalg.norm(yAxisLocal, 2)

        self[:, 0] = xAxisLocal
        self[:, 1] = yAxisLocal
        self[:, 2] = zAxisLocal

    def getPointsByRotation(self, rotation, origin):
        """doc"""
        if not isinstance(origin, Translation):
            origin = Translation(origin)

        xAxisLocal = Translation(rotation[:, 0])
        yAxisLocal = Translation(rotation[:, 1])
        yCoordinate = yAxisLocal + origin
        xCoordinate = xAxisLocal + origin

        return [xCoordinate, yCoordinate]

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
            else:
                return ret
        except ValueError:
            # possibly multiplication with coordinatesystem
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

    def _setAngles(self, angles):
        """
        :param angles: iterable with at least 3 items: (x,y,z,[rotationtype])
        - the input angles have to be in radians"""
        if len(angles) == 4:
            alpha, beta, gamma, rotationType = angles[:4]
        elif len(angles) == 3:
            alpha, beta, gamma = angles[:3]
            rotationType = "rxyz"
        else:
            log.error("There must be 3 or 4 scalar parameters! Using identity rotation instead")
            alpha, beta, gamma, rotationType = 0, 0, 0, "rxyz"

        if np.any(np.array([alpha, beta, gamma]) > np.pi * 2):
            log.warning(
                "Rotation object will set angle that is bigger than 2*pi. Maybe the angles are not given in radians!"
            )

        self.setfield(euler_matrix(alpha, beta, gamma, rotationType)[:3, :3], np.float64)

        return self

    def _getAngles(self):
        """returns the 'rxyz' Euler angles"""
        return self.getAngles("rxyz")

    def getAngles(self, axis):
        """returns the Euler angles depending on the desired axis. See class description
        for details about the axis parameter."""
        return euler_from_matrix(self, axis)

    angles = property(fset=_setAngles, fget=_getAngles)

    isIdentity = property(fget=_isIdentity)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # alpha, beta, gamma, rotationType = np.pi*0.25, 0, np.pi*0.5, "rxyz"
    # myArr = trafo.euler_matrix(alpha, beta, gamma, rotationType)[:3, :3]
    # print()
