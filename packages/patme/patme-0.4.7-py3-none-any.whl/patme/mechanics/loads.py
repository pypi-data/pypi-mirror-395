# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

from collections import OrderedDict
from enum import IntEnum

import numpy as np
from scipy.linalg import block_diag

from patme import epsilon
from patme.geometry.rotate import Rotation
from patme.geometry.translate import Translation
from patme.service.exceptions import ImproperParameterError, InternalError
from patme.service.stringutils import indent

loadComponentNames = ["fx", "fy", "fz", "mx", "my", "mz"]
loadComponentUpperNames = ["Fx", "Fy", "Fz", "Mx", "My", "Mz"]
loadcomponentToIndex = dict(
    [
        (name, compIndex)
        for compIndex, name in list(enumerate(loadComponentNames)) + list(enumerate(loadComponentUpperNames))
    ]
)


class PointTypeOfLoad(IntEnum):

    keypoint = 1
    meshNode = 2


class Loads(list):
    """This class serves as collection of several single loads."""

    def __init__(self, *args, **kwargs):
        """doc"""
        list.__init__(self, *args, **kwargs)

    def getLoad(self, point=None, rotation=None):
        """Sums up all loads referencing to a point and rotation.

        :param point: object of type Translation (defaultes to aircraft coordinate system [0,0,0])
        :param rotation: object of type Rotation (defaultes to aircraft coordinate system )"""
        if point is None:
            point = Translation((0.0, 0.0, 0.0))

        loadSum = Load(point=point)
        for load in self:
            loadSum += load.getLoad(point)

        return loadSum

    def getCutLoads(self):
        """Retruns an instance of Loads with cutloads of self

        >>> from patme.geometry.translate import Translation
        >>> loads = Loads([Load([1*loadFactor,2*loadFactor,0,0,0,0], point = Translation([loadFactor,0,0])) for loadFactor in [1,2,3]])
        >>> cutLoads = loads.getCutLoads()
        >>> print(cutLoads)
        [Load([ 6., 12.,  0.,  0.,  0., 16.]), Load([ 5., 10.,  0.,  0.,  0.,  6.]), Load([3., 6., 0., 0., 0., 0.])]
        """
        cutLoads = Loads()
        if not self:
            return cutLoads

        cutLoads.append(self[-1])
        for load in self[-2::-1]:  # reversed without last original element
            cutLoads.append(load + cutLoads[-1].getLoad(load.point))

        return cutLoads[::-1]

    def removeZeroLoads(self):
        """Removes loads from self that are zero"""
        loadIndexesToRemove = [ix for ix, load in enumerate(self) if np.allclose(load, np.zeros(6))]
        for loadIndex in loadIndexesToRemove[::-1]:
            self.pop(loadIndex)

    def getLoadsMovedToTranslations(self, translations):
        """This method copies the given loads to the respectively nearest
        translation object of the component(wing or fuselage) and
        returns a list of these loads with damPoints as load.point"""
        translation2NewLoadDict = OrderedDict()

        # create initial load at each damPoint
        cls = self[0].__class__ if self else Load
        for point in translations:
            translation2NewLoadDict[point] = cls(point=point)

        for load in self:
            nearestIndex = np.argmin(np.linalg.norm(np.array(translations) - [load.point], axis=1))
            newLoad = load.copy()
            # move load
            newLoad.point = translations[nearestIndex]
            # add load to existing loads at dam-axis
            translation2NewLoadDict[translations[nearestIndex]] += newLoad

        return Loads(list(translation2NewLoadDict.values()))

    @staticmethod
    def massesToLoads(masses, acceleration=Translation([0.0, 0.0, 1.0])):
        """converts masses to loads with the given acceleration"""
        loads = Loads()
        for mass in masses:
            load = list(acceleration * mass.mass) + [0.0, 0.0, 0.0]
            loads.append(Load(load, point=mass.coG))
        return loads

    def getInfoString(self):
        """returns a string with the loads and ref points"""
        body = [[load.tolist() + load.point.tolist()] for load in self]
        header = loadComponentNames
        return indent([header] + body, hasHeader=True)

    def __iadd__(self, otherLoads):
        """Adds the other Loads to the loads in self.

        Condition: the length and points of both load lists must be equal or one of
        the load lists must be empty."""
        if len(otherLoads) == 0:
            return self
        elif len(self) == 0:
            self.extend(otherLoads)
            return self
        elif len(self) != len(otherLoads):
            raise ImproperParameterError("The given Loads lists are not of equal length!")

        for load, otherLoad in zip(self, otherLoads):
            if not np.allclose(load.point, otherLoad.point):
                raise ImproperParameterError("The given Loads do not share the same locations!")
            load += otherLoad
        return self


class Load(np.ndarray):
    """This class represents a Load that is defined by a vector of length 6 (fx,fy,fz,mx,my,mz).
    The load vector is included in a numpy array and can be accessed and altered like this::

        >>> from patme.mechanics.loads import Load
        >>> load=Load([1,0,0,0,0,0])
        >>> load
        Load([1., 0., 0., 0., 0., 0.])
        >>> load.point
        Translation([0., 0., 0.])
        >>> load.rotation
        Rotation([[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])

    The load can be moved and rotated by the ``point`` and ``rotation`` properties::

        >>> # translate the load
        >>> # getting a copy of the point object, move it 2[m] in y-direction and
        >>> # move the load - the result is a newly added moment
        >>> p=load.point
        >>> p
        Translation([0., 0., 0.])
        >>> p2=p+[0,2,0]
        >>> p2
        Translation([0., 2., 0.])
        >>> load.point = p2
        >>> load
        Load([1., 0., 0., 0., 0., 2.])

        >>> # rotate the load
        >>> # getting a copy of the rotation, rotate it by 90 degress around the z-axis
        >>> # and rotate the load
        >>> load=Load([1,0,0,0,0,0])
        >>> r=load.rotation
        >>> r
        Rotation([[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]])
        >>> r2 = Rotation()
        >>> r2.angles = [0.,0.,np.pi/2]
        >>> r2
        Rotation([[ 6.123234e-17, -1.000000e+00,  0.000000e+00],
                  [ 1.000000e+00,  6.123234e-17, -0.000000e+00],
                  [ 0.000000e+00,  0.000000e+00,  1.000000e+00]])
        >>> load.rotation = r2
        >>> load
        Load([ 6.123234e-17, -1.000000e+00,  0.000000e+00,  0.000000e+00,
               0.000000e+00,  0.000000e+00])

    The point and rotation properties always reference to the aircraft coordinate system.
    Thus one can not operate with them directly - a new point or rotation has
    to be calculated outside of the loads class and applied to the load as
    shown in the description above.

    """

    def __new__(cls, input_array=None, point=Translation(), rotation=Rotation(), pointTypeOfLoad=None):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        if input_array is None:
            input_array = np.zeros(6)

        if not hasattr(input_array, "shape"):
            input_array = np.asarray(input_array, dtype=np.float64)

        if not input_array.shape == (6,):
            raise ImproperParameterError(
                "The given load must be a vector with 6 elements. " + "Got this instead: " + str(input_array)
            )

        obj = input_array.view(cls)
        # add the new attribute to the created instance
        if not isinstance(point, Translation):
            point = Translation(point)
        obj._point = point

        if not isinstance(rotation, Rotation):
            rotation = Rotation(rotation)
        obj._rotation = rotation

        obj._pointTypeOfLoad = pointTypeOfLoad
        if pointTypeOfLoad is None:
            obj._pointTypeOfLoad = PointTypeOfLoad.keypoint

        # Finally, we must return the newly created object:
        return obj

    def getPickleLoadProperties(self):
        """returns the properties that are not pickled automatically."""
        return (
            self._point,
            self._point.id,
            self._point.cutout,
            self._point.refType,
            self._rotation,
            self._pointTypeOfLoad,
        )

    def setPickleLoadProperties(self, loadProperties):
        """sets the properties that are not pickled automatically."""
        (
            self._point,
            self._point.id,
            self._point.cutout,
            self._point.refType,
            self._rotation,
            self._pointTypeOfLoad,
        ) = loadProperties

    def __array_finalize__(self, obj):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self._point = getattr(obj, "_point", Translation())
        """Reference position of type model.geometry.translation.Translation in reference to the aircraft coordinate system"""

        self._rotation = getattr(obj, "_rotation", Rotation())
        """Reference rotation of type model.geometry.rotation.Rotation in reference to the aircraft coordinate system"""

        self._pointTypeOfLoad = getattr(obj, "_pointTypeOfLoad", PointTypeOfLoad.keypoint)
        """Type of point where load is applied, either geometric keypoint or mesh node"""

    def copy(self):
        """returns a copy of self"""
        return self.getLoad()

    def getLoad(self, point=None, rotation=None):
        """returns a copy of the load in reference to optionally differing point and rotation"""
        ret = np.ndarray.copy(self)
        if point is None:
            newPoint = self.point.copy()
        else:
            newPoint = Translation(point).copy()

        if rotation is None:
            newRotation = self.rotation.copy()
        else:
            newRotation = Rotation(rotation).copy()

        ret.point = newPoint
        ret.rotation = newRotation
        return ret

    def getLoadMirrored(self, plane="xz"):
        """returns a copy of this load mirrored at the given global plane

        :param plane: one of 'xz','xy','yz'
        """
        if not self.rotation.isIdentity:
            NotImplementedError("Mirroring a rotated load is actuallay unsupported. Please contact the developer.")

        mirrorMask = np.ones(6)
        if plane == "xy":
            mirrorMask[2:5] = -1
        elif plane == "xz":
            mirrorMask[[1, 3, 5]] = -1
        elif plane == "yz":
            mirrorMask[[0, 4, 5]] = -1
        else:
            raise InternalError("got wrong parameter for plane: %s" % plane)

        newLoad = self.copy()
        # mirror load
        newLoad *= mirrorMask
        # mirror the reference point without changing the load itself
        newLoad._point = self.point * mirrorMask[:3]

        return newLoad

    def _getMomentsDueToNewPoint(self, point):
        """this method calculates the moments resulting from moving a force vector.
        It is only used with identity rotation!"""
        # moments due to translation
        return np.cross(self[:3], np.array(point) - self.point)

    def _setPoint(self, newPoint):
        """resets the reference point of the load. Thus the load is rotated back to
        the aircraft coordinate system rotation to calculate the correct moments due to
        the newPoint. Then it is rotated back to the original rotation."""
        if not self.rotation.isIdentity:
            originalRotation = self.rotation
            self.rotation = Rotation()

        if np.linalg.norm(self._point - newPoint) > epsilon:
            self[3:6] += self._getMomentsDueToNewPoint(newPoint)
        self._point = newPoint

        if not self.rotation.isIdentity:
            self.rotation = originalRotation

    def _getPoint(self):
        """returns the reference point

        Attention: altering this point object will not affect the loads like"""
        return self._point

    def _getPositionX(self):
        """returns the x-coordinate of the loads point. (Used for sorting loads)"""
        return self._point.x

    def _setRotation(self, newRotation):
        """rotates the load back to and identity rotation and then to newRotation"""

        # rotate to identity: inverse(oldRotation)*forces .....
        if not self._rotation.isIdentity:
            rotInv = np.linalg.inv(self._rotation)
            self[:] = self[:] @ block_diag(rotInv, rotInv)
            # @ operator is equivalent to np.dot and represents matrix-vector multiplication

        # rotate to new rotation: newRotation*forces ....
        if not newRotation.isIdentity:
            self[:] = self[:] @ block_diag(newRotation, newRotation)

        self._rotation = newRotation

    def _getRotation(self):
        """returns a copy of the object's rotation attribute"""
        return self._rotation

    def __str__(self):
        """doc"""
        return ", ".join(self.astype(str))

    def _getFX(self):
        return self[0]

    def _getFY(self):
        return self[1]

    def _getFZ(self):
        return self[2]

    def _getMX(self):
        return self[3]

    def _getMY(self):
        return self[4]

    def _getMZ(self):
        return self[5]

    def _setFX(self, fx):
        self[0] = fx

    def _setFY(self, fy):
        self[1] = fy

    def _setFZ(self, fz):
        self[2] = fz

    def _setMX(self, mx):
        self[3] = mx

    def _setMY(self, my):
        self[4] = my

    def _setMZ(self, mz):
        self[5] = mz

    fx = property(fget=_getFX, fset=_setFX)
    fy = property(fget=_getFY, fset=_setFY)
    fz = property(fget=_getFZ, fset=_setFZ)
    mx = property(fget=_getMX, fset=_setMX)
    my = property(fget=_getMY, fset=_setMY)
    mz = property(fget=_getMZ, fset=_setMZ)

    point = property(fset=_setPoint, fget=_getPoint)
    rotation = property(fset=_setRotation, fget=_getRotation)
    positionX = property(fget=_getPositionX)


if __name__ == "__main__":
    if 0:
        f = Flow()
        f.machNumber = 0.0
        heightsFt = np.array([5000, 6000, 7000, 8000, 9000, 10000, 39000])
        heights = heightsFt * 0.3048
        pressures = []

        for height in heights:
            f.h = height
            f._p = None
            pressures.append(f.staticPressure)
        pressures = np.array(pressures)
        dPs = pressures - pressures[-1]
        print(
            indent(
                [["height[ft]", "height[m]", "pressure[Pa]", "dP[Pa]"]] + list(zip(heightsFt, heights, pressures, dPs))
            )
        )

    elif 1:
        import doctest

        doctest.testmod()  # verbose=True
