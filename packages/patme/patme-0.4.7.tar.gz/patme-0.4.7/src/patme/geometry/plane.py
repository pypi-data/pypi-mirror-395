# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""
documentation
"""
import numpy as np

from patme import epsilon
from patme.geometry.intersect import Intersection
from patme.geometry.line import Line
from patme.geometry.rotate import Rotation
from patme.geometry.translate import Translation
from patme.service.exceptions import GeometryError, ImproperParameterError, InternalError
from patme.service.logger import log


class Plane:
    """this class represents the mathematical description of a plane.

    It provides necessary methods for calculating intersection points and other stuff.
    A positioning point and the plane normal vector is necessary to establish the plane.


    >>> plane = Plane()
    >>> plane = plane.generatePlane([3,0,0], planeNormalVector = [0,0,1])
    >>> plane.planeNormalVector
    Translation([0., 0., 1.])
    >>> plane.planePositioningVector
    Translation([3, 0, 0])
    >>> plane.getProjectedPoints([[2,0,0]])
    array([[2., 0., 0.]])
    """

    def __init__(self, *args, **kwargs):
        """
        :param refPlane: string, optional if a standard projection plane is to be used ('xy', 'xz' and 'yz' possible)
        :param planeID: string, specifying the id of the projection plane

        """
        self._n = None
        self._position = None
        self._planeOrientationVector1 = None
        self._planeOrientationVector2 = None

        refPlane = kwargs.pop("refPlane", None)

        if refPlane:

            allowedRefPlanes = ["xy", "xz", "yz"]
            if refPlane not in allowedRefPlanes:
                raise ImproperParameterError(
                    f'Parameter "refPlane" is "{refPlane}" but must be one of {allowedRefPlanes}'
                )

            self.planePositioningVector = np.zeros(3)

            baseVector = np.eye(3)
            self._planeOrientationVector1, self._planeOrientationVector2 = (
                baseVector["xyz".index(axis), :] for axis in refPlane
            )

            self.generatePlane(self._position, self._planeOrientationVector1, self._planeOrientationVector2)

        self.planeID = kwargs.pop("planeID", None)

        if not self.planeID and refPlane:
            self.planeID = f"Plane_{refPlane}"

        for key in kwargs:
            if not hasattr(self, key):
                log.warning(f'Setting unknown key "{key}" in class {self.__class__} with name "{str(self)}"')
            setattr(self, key, kwargs[key])

    def copy(self):
        """doc"""
        return Plane(
            planeID=f"{self.planeID}_copy",
            _planeOrientationVector1=self.planeOrientationVector1,
            _planeOrientationVector2=self.planeOrientationVector2,
            _position=self._position,
            _n=self._n,
        )

    def to_occ(self):
        """doc"""
        try:
            from OCC.gp import gp_Ax3, gp_Dir, gp_Pln, gp_Pnt
        except ImportError:
            from OCC.Core.gp import gp_Ax3, gp_Dir, gp_Pln, gp_Pnt

        origPos = gp_Pnt(*self._position)
        normal = gp_Dir(*self.planeNormalVector)
        Vx = gp_Dir(*self.planeOrientationVector1)
        ax = gp_Ax3(origPos, normal, Vx)
        return gp_Pln(ax)

    def getDistanceToPoint(self, point):
        """
        this function is intended to calculate the distance from this plane to the given point p
        d(P,E)=abs(n*p-d)/abs(n) with E: n*x = n*a = d

        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> plane.getDistanceToPoint([0,0,10])
        10.0
        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,0], planeNormalVector = [1,1,1])
        >>> '{:03.1f}'.format(plane.getDistanceToPoint([1,1,1])**2)
        '3.0'

        :param point: instance of type Translation(), specifying the point, from which the distance to the plane shall be calculated
        """
        distanceNominator = abs(
            np.dot(point, self.planeNormalVector) - np.dot(self.planeNormalVector, self.planePositioningVector)
        )
        return distanceNominator / np.linalg.norm(self.planeNormalVector)

    @staticmethod
    def fromPointCloud(points):
        from patme.geometry.misc import PCA

        _, v = PCA(points)
        point = np.mean(points, axis=0)
        return Plane().generatePlane(point, planeNormalVector=v[:, 2])

    def generatePlane(
        self, positioningPoint=None, orientationPoint1=None, orientationPoint2=None, planeNormalVector=None
    ):
        """
        :param positioningPoint: instance of type Translation(), specifying a point within the projection plane
        :param orientationPoint1: instance of type Translation(), specifying an orientation vector within the projection plane
        :param orientationPoint2: instance of type Translation(), specifying an orientation vector within the projection perpendicular to orientationPoint1
        """

        if positioningPoint is not None and orientationPoint1 is not None and orientationPoint2 is not None:
            self.planePositioningVector = Translation(positioningPoint)
            self._planeOrientationVector1 = np.asarray(orientationPoint1) - self.planePositioningVector
            self._planeOrientationVector2 = np.asarray(orientationPoint2) - self.planePositioningVector

            # Ebenennormalenvektor bestimmen
            # n = planeOrientationVector1 x planeOrientationVector2
            # n*(x-planePositionVector) = 0
            self.planeNormalVector = np.cross(self._planeOrientationVector1, self._planeOrientationVector2)

        elif positioningPoint is not None and planeNormalVector is not None:
            self.planePositioningVector = Translation(positioningPoint)
            self.planeNormalVector = planeNormalVector

            self.setPlaneOrientationVectors()

        else:
            raise InternalError("At least one point for a proper plane definition is missing.")

        self.normalizeVectors()

        return self

    def getIntersection(self, lines=None, areas=None):
        """This method is intended to return the intersection of the provided input with itself.
        Depending on the input this method returns an instance of Translation or an
        instance of Line

        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> plane.getIntersection(lines = [Line(Translation([0,0,0]),Translation([0,0,1]))])
        Translation([0., 0., 0.])
        """
        if lines is None:
            lines = []
        if areas is None:
            areas = []

        if lines:
            return Intersection.getIntersection(lines=lines, areas=[self])
        elif areas:
            areas.insert(0, self)
            return Intersection.getIntersection(areas=areas)
        else:
            raise ImproperParameterError("No line or area specified for intersection.")

    def getIntersectionPointOfVetor(self, vectorPoint, vectorOrienation):
        """Calculates the intersection point of a vector with this plane. The vector must not be parallel to the plane

        :return: Translation defining the intersection point
        :raises GeometryError: in case vector is parallel to plane

        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> plane.getIntersectionPointOfVetor([0,0,0],[0,0,1])
        Translation([0., 0., 0.])
        """
        line = Line(Translation(vectorPoint), Translation(vectorPoint) + vectorOrienation)
        result = Intersection.getIntersection(lines=[line], areas=[self])

        if result is None:
            raise GeometryError("Line is parallel to plane and not coincident")
        if result is line:
            raise GeometryError("Line is parallel and coincident to plane")

        return Translation(result)

    def getProjectedPoints(self, points=None, transformIntoPlaneCoordinates=False):
        """This method is intended to provide the functionality of orthogonal projection of points and lines onto a plane.

        :param points: list of points to be projected
        :param transformIntoPlaneCoordinates: Flag, if the resulting points should be absolute or in the plane
            coordinate system including the plane's rotation

        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,1], planeNormalVector = [0,0,1])
        >>> plane.getProjectedPoints([[1,0,3],[0,1,3]])
        array([[1., 0., 1.],
               [0., 1., 1.]])
        >>> plane = plane.generatePlane([0,0,1], planeNormalVector = [0,0,1])
        >>> plane.getProjectedPoints([[1,0,3],[0,1,3]], transformIntoPlaneCoordinates=True)
        array([[1., 0., 0.],
               [0., 1., 0.]])

        .. figure:: ../../bilder/reference/IMG7254.PNG
            :width: 250pt
            :align: center

        Common equation of plane:

        .. math::
            \\\\
            \\vec{e} = \\vec{ap}+\\lambda\\cdot\\vec{rv_{1}}+\\mu\\cdot\\vec{rv_{1}}

        Common equation of linear function:

        .. math::
            \\\\
            \\vec{x_{g}} = \\vec{p}+\\omega\\cdot\\vec{rv_{g}}

        Common equation of projection of the linear function:

        .. math::
            \\\\
            \\vec{x_{s}} = \\vec{p_{s}}+\\omega\\cdot\\vec{rv_{gs}}

        Common equations for supporting functions:

        .. math::
            \\\\
            \\vec{x_{h1}} = \\vec{p}+\\sigma\\cdot\\vec{n},\\, with\\; \\vec{n}\\; the\\; normal\\; vector\\; of\\; \\vec{e}
            \\\\
            \\vec{x_{h2}} = \\vec{q}+\\eta\\cdot\\vec{n},\\, with\\; \\vec{n}\\; the\\; normal\\; vector\\; of\\; \\vec{e}

    """
        # Hilfsgeradeen aufstellen
        # h1(omega) = functionPositionVector + omega*self.planeNormalVector

        # Gleichungssystem loesen:
        # Solve ``-sigma*n_1+lambda*rv1_1+mu*rv2_1 = p_1-ap_1``
        #       ``-sigma*n_2+lambda*rv1_2+mu*rv2_2 = p_2-ap_2``
        #       ``-sigma*n_3+lambda*rv1_3+mu*rv2_3 = p_3-ap_3``

        # h1(omega) = E(alpha,beta)
        if len(points) == 1:
            pointsArray = np.array([points[0]])
        else:
            pointsArray = np.array(points, copy=True)

        rechteSeiten = pointsArray - np.array(self.planePositioningVector)

        koeffMat = np.array(
            [-1 * self.planeNormalVector[:3], self._planeOrientationVector1[:3], self._planeOrientationVector2[:3]]
        ).T

        # [sigma, lambda, mu]
        unknownParms = np.linalg.solve(koeffMat, rechteSeiten.T)

        # evaluate supporting function to get intersection point
        planeNormals = np.outer(self.planeNormalVector, np.ones(pointsArray.shape[0]))

        newPoints = pointsArray + (unknownParms[0, :] * planeNormals).T

        if transformIntoPlaneCoordinates:
            newPoints -= self.planePositioningVector
            unknownParms = np.linalg.lstsq(self.rotation, newPoints.T, rcond=None)[0]
            newPoints = unknownParms.T

        return newPoints

    def setPlaneOrientationVectors(self):
        """doc"""
        # create a vector deviating a bit from normal vector
        newVector = None
        for translation in np.eye(3, 3):
            newVector = self.planeNormalVector + translation
            auxVector = np.cross(self.planeNormalVector, newVector)

            # check whether new vector is linear independent from plane normal vector
            vectorMatrix = np.array([self.planeNormalVector, newVector, auxVector])

            if np.linalg.det(vectorMatrix.T) > epsilon:
                # vectors are linear independent - no new vector has to be created
                break

        # calculate part of newVector parallel to plane normal vector
        nParallelVec = (
            np.dot(self.planeNormalVector, newVector)
            / np.dot(self.planeNormalVector, self.planeNormalVector)
            * self.planeNormalVector
        )

        # calculate first vector in plane
        self._planeOrientationVector1 = Translation(newVector - nParallelVec)

        # calculate second vector in plane
        self._planeOrientationVector2 = Translation(np.cross(self.planeNormalVector, self._planeOrientationVector1))

        self.planeNormalVector = Translation(np.cross(self._planeOrientationVector1, self._planeOrientationVector2))

    def getNearestPointFromList(self, pointList):
        """Returns the point of list pointList which is closest to the plane.

        :param pointList: list of keypoints (or 3D coordinates)
        :return: the point of pointList closest to the plane
        """
        distancesToPlane = np.array([self.getDistanceToPoint(np.array(point)) for point in pointList])
        return pointList[np.argmin(distancesToPlane)]

    @staticmethod
    def fromTransformation(rotation, position):
        """doc"""
        refPos1 = position + rotation[:, 0] / np.linalg.norm(rotation[:, 0])
        refPos2 = position + rotation[:, 1] / np.linalg.norm(rotation[:, 1])
        return Plane().generatePlane(position, refPos1, refPos2)

    def makeOrthogonal(self, adaptVectorNum=1):
        """doc"""
        # adapt orientation vector to get orthogonal vectors
        if adaptVectorNum not in [1, 2]:
            log.warning(
                "Only [1,2] are valid numbers for parameter 'adaptVectorNum' in function Plane.makeOrthogonal. Set to 1"
            )
            adaptVectorNum = 1

        if adaptVectorNum == 1:
            self._planeOrientationVector1 = Translation(np.cross(self.planeOrientationVector2, self.planeNormalVector))
        else:
            self._planeOrientationVector2 = Translation(np.cross(self.planeNormalVector, self.planeOrientationVector1))

    def normalizeVectors(self):
        """doc"""
        self.planeNormalVector /= np.linalg.norm(self.planeNormalVector)
        self._planeOrientationVector1 /= np.linalg.norm(self._planeOrientationVector1)
        self._planeOrientationVector2 /= np.linalg.norm(self._planeOrientationVector2)

    def plot(self, axes=None):
        """doc"""
        import matplotlib.pyplot as plt

        copyPlane = self.copy()
        copyPlane.makeOrthogonal(2)

        xx, yy = np.meshgrid(np.linspace(-2, 2, 21), np.linspace(-2, 2, 21))
        allPoints = np.c_[xx.ravel(), yy.ravel()]

        from scipy.spatial import Delaunay

        tri = Delaunay(allPoints)

        allPoints = np.c_[allPoints, np.zeros(allPoints.shape[0])]
        newPoints = (self.rotation * allPoints.T).T + self.planePositioningVector

        if not axes:
            axes = plt.figure().gca(projection="3d")

        axes.set_aspect("equal")
        axes.plot_trisurf(
            newPoints[:, 0], newPoints[:, 1], newPoints[:, 2], linewidth=0, triangles=tri.simplices, alpha=0.2
        )

        return axes

    def switchAxes(self):
        """doc"""
        tmpVector1 = self.planeOrientationVector1
        self._planeOrientationVector1 = np.copy(self.planeOrientationVector2)
        self._planeOrientationVector2 = np.copy(tmpVector1)
        self.planeNormalVector = np.cross(self._planeOrientationVector1, self._planeOrientationVector2)

    def _hasOrthogonalBase(self):
        """doc"""
        dotProduct = self.planeOrientationVector1 @ self.planeOrientationVector2
        norm = np.linalg.norm(self.planeOrientationVector1) * np.linalg.norm(self.planeOrientationVector2)
        return abs(dotProduct / norm) < 1e-08

    def _getRotation(self):
        """doc"""
        if not self.hasOrthogonalBase:
            return None
        else:
            return Rotation(
                np.array([self.planeOrientationVector1, self.planeOrientationVector2, self.planeNormalVector]).T
            )

    def __str__(self):
        """doc"""
        if self.planeID:
            return self.planeID

        return object.__str__(self)

    def _getNormalVector(self):
        """doc"""
        return self._n

    def _setNormalVector(self, normalVector):
        """doc"""
        self._n = Translation(normalVector / np.linalg.norm(normalVector))

    def _getPositionVector(self):
        """doc"""
        return self._position

    def _setPositionVector(self, positioningVector):
        """doc"""
        self._position = Translation(positioningVector)

    def _getplaneOrientationVector1(self):
        """doc"""
        return self._planeOrientationVector1

    def _getplaneOrientationVector2(self):
        """doc"""
        return self._planeOrientationVector2

    planeNormalVector = property(fget=_getNormalVector, fset=_setNormalVector)
    # normal vector of the plane
    planeOrientationVector1 = property(fget=_getplaneOrientationVector1)
    planeOrientationVector2 = property(fget=_getplaneOrientationVector2)
    planePositioningVector = property(fget=_getPositionVector, fset=_setPositionVector)
    hasOrthogonalBase = property(fget=_hasOrthogonalBase)
    rotation = property(fget=_getRotation)


if __name__ == "__main__":

    plane = Plane().generatePlane(np.array([1, 1, 1]), planeNormalVector=[2, 4, 3])
    plane2 = plane.copy()
    numPoints = 10
    testPoints = np.random.rand(numPoints * 3).reshape((10, 3)) * 10
    newPoint = plane.getProjectedPoints(testPoints, True)

#
#     from mpl_toolkits.mplot3d import axes3d
#     import matplotlib.pyplot as plt
#
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     ax.scatter(xs = newPoint[:,0], ys = newPoint[:,1], zs = newPoint[:,2], marker="o", label='Data points')
#     #plane.plot(ax)
#     plt.show()
#
#     #plane = plane.generatePlane([0,0,0], planeNormalVector = [0,0,1])
#     #print(plane.getIntersection(lines = [Line(Translation([0,0,0]),Translation([0,0,1]))]))
#
# #     import doctest
# #     doctest.testmod()
