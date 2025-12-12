# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""
Created on Sep 21, 2011

@author: hein_fa
"""

import math

import numpy as np
from numpy.linalg import inv

from patme import epsilon
from patme.geometry.line import Line
from patme.geometry.misc import areVectorsParallel, getPointDistanceToLine
from patme.service.exceptions import ImproperParameterError, InternalError


class Intersection:
    """
    This class is intended to provide the functionality to intersect two linear curves with each other
    and to return the corresponding intersection point. The calculation of the intersection is limited to 2D
    due to the fact that spars, ribs and stringer are located within the areodynamic loft. Therefore, they
    categorical intersect each other. That means the z-coordinate of the points is dispensable for the
    intersection calculation. The first two position vectors from the first linear curve and the second two
    position vectors establish the second linear curve, respectively.


    """

    @staticmethod
    def getIntersection(lines=None, areas=None, plane="xy"):
        """doc"""
        if lines is None:
            lines = []
        if areas is None:
            areas = []

        if len(lines) == 2:
            return Intersection._intersectLines(*lines, plane=plane)
        elif len(areas) == 2:
            return Intersection._intersectAreas(*areas)
        elif len(lines) == 1 and len(areas) == 1:
            return Intersection._intersectLineArea(lines[0], areas[0])
        else:
            raise ImproperParameterError(
                "The specified parameters don't fit the specification of intersection instance"
            )

    @staticmethod
    def _intersectLines(line1, line2, plane="xy"):
        """This method generates vectorial equations from specified initial vectors (vector1, ...vector4).
        Afterwards, these two functions are intersected with each other. The resulting intersection point will be returned as result of this method.
        The generated equations will look like: f: xVector = aVectror+phi*bVector ; g: xVector = cVectror+chi*dVector. Subsequently, the xVector of
        f will be equalized with the xVector of g. The resulting coefficient matrix will be inverted and from left multiplied by the difference of aVector and cVector.
        Following system of equation should appear:
        aVector = vector1 ; bVector = vector2-vector1
        cVector = vector3 ; dVector = vector4-vector3

        |-                    -|          |- -|                           |-                   -|
        |bVector[0] -cVector[0]|          |phi|                           |dVector[0]-aVector[0]|
        |bVector[1] -cVector[1]|    *     |chi|            =              |dVector[1]-aVector[1]|
        |-                    -|          |- -|                           |-                   -|
        ->coeffMatrix                     ->vector function parameters    ->difference of position vector

        >>> from patme.geometry.translate import Translation
        >>> line1 = Line(Translation( [0., 0., 0.] ), Translation( [1., 0., 0.] ))
        >>> line2 = Line(Translation( [0., 0., 0.] ), Translation( [0., 1., 0.] ))
        >>> Intersection._intersectLines(line1, line2)
        Translation([0., 0., 0.])
        >>> line2 = Line(Translation( [0., 0., 0.] ), Translation( [0., 0., 1.] ))
        >>> Intersection._intersectLines(line1, line2, plane='xz')
        Translation([0., 0., 0.])
        >>> line2 = Line(Translation( [0., 0., 0.] ), Translation( [1., 0., 0.] ))
        >>> line1 is Intersection._intersectLines(line1, line2)
        True
        >>> line2 = Line(Translation( [0., 1., 0.] ), Translation( [1., 1., 0.] ))
        >>> print(Intersection._intersectLines(line1, line2))
        None
        """
        if plane not in ["xy", "xz", "yz"]:
            raise ImproperParameterError("plane not implemented: " + plane)
        else:
            coeff11 = getattr(line1.p2, plane[0]) - getattr(line1.p1, plane[0])
            coeff21 = getattr(line1.p2, plane[1]) - getattr(line1.p1, plane[1])
            coeff12 = getattr(line2.p2, plane[0]) - getattr(line2.p1, plane[0])
            coeff22 = getattr(line2.p2, plane[1]) - getattr(line2.p1, plane[1])

        if np.linalg.norm(np.cross([coeff11, coeff21], [coeff12, coeff22])) < epsilon:
            # line is parallel
            distance = getPointDistanceToLine(line1.p1, line1.p2, line2.p1)
            if distance < epsilon:
                return line1
            else:
                return None

        try:
            coeffMatrix = np.array([[coeff11, -coeff12], [coeff21, -coeff22]])
            coeffMatrixInv = inv(coeffMatrix)
        except:
            raise InternalError(
                "Can't calculate intersection! The matrix to be inverted is singular! Either the two vectors are parallel or the specified data is corrupted."
            )

        # ---CALCULATE UNKNOWN PARAMETERS
        if plane == "xy":
            vec = np.dot(coeffMatrixInv, (line2.p1 - line1.p1)[:2])
        elif plane == "xz":
            vec = np.dot(coeffMatrixInv, np.array([(line2.p1 - line1.p1)[0], (line2.p1 - line1.p1)[2]]))
        elif plane == "yz":
            vec = np.dot(coeffMatrixInv, (line2.p1 - line1.p1)[1:])

        # ---USE ONE OF THE UNKNOWN PARAMETERS TO CALCULATE THE INTERSECTION POINT
        return line1.p1 + vec[0] * (line1.p2 - line1.p1)

    @staticmethod
    def intersectLinesMethod2d(line1, line2):
        """method returns the intersection of two 2D lines with wing positions in xsi,eta coordinate system

        The coordinates are in xy-plane. It can also handle lines that are parallel

            returns a tuple: (xi, yi, valid, r, s), where
            (xi, yi) is the intersection
            r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
            s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
                valid == 0 if there are 0 or inf. intersections (invalid)
                valid == 1 if it has a unique intersection ON the segment"""

        # source: https://www.cs.hmc.edu/ACM/lectures/intersections.html
        # method is used for spar crossing. _intersectLines method should be investigated if
        # it can be used instead of this method for this purpose

        # the first line is pt1 + r*(pt2-pt1)
        # in component form:
        x1, y1 = line1.p1.x, line1.p1.y
        x2, y2 = line1.p2.x, line1.p2.y
        dx1 = x2 - x1
        dy1 = y2 - y1

        # the second line is ptA + s*(ptB-ptA)
        x, y = line2.p1.x, line2.p1.y
        xB, yB = line2.p2.x, line2.p2.y

        dx = xB - x
        dy = yB - y

        # we need to find the (typically unique) values of r and s
        # that will satisfy
        #
        # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
        #
        # which is the same as
        #
        #    [ dx1  -dx ][ r ] = [ x-x1 ]
        #    [ dy1  -dy ][ s ] = [ y-y1 ]
        #
        # whose solution is
        #
        #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
        #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
        #
        # where DET = (-dx1 * dy + dy1 * dx)
        #
        # if DET is too small, they're parallel
        #
        DET = -dx1 * dy + dy1 * dx

        if math.fabs(DET) < epsilon:
            return (0, 0, 0, 0, 0)

        # find the scalar amount along the "self" segment
        r = (1.0 / DET) * (-dy * (x - x1) + dx * (y - y1))

        # find the scalar amount along the input line
        s = (1.0 / DET) * (-dy1 * (x - x1) + dx1 * (y - y1))

        # return the average of the two descriptions
        xi = (x1 + r * dx1 + x + s * dx) / 2.0
        yi = (y1 + r * dy1 + y + s * dy) / 2.0
        return (xi, yi, 1, r, s)

    @staticmethod
    def _intersectAreas(plane1, plane2):
        """Calculate intersection of two planes.

        :return: If the planes cross each other, a line instance is returned. If the
            planes are coincident, the first plane is returned. If the planes have the same
            normal direction but the planes do not coincide, None is returned.

        >>> from patme.geometry.plane import Plane
        >>> plane1, plane2 = Plane(), Plane()
        >>> plane1 = plane1.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> plane2 = plane2.generatePlane([0,0,0], planeNormalVector = [0,1,0])
        >>> print(Intersection._intersectAreas(plane1, plane2))
        [0. 0. 0.], [-1.  0.  0.]
        >>> plane2 = plane2.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> plane1 is Intersection._intersectAreas(plane1, plane2)
        True
        >>> plane2 = plane2.generatePlane([0,0,1], planeNormalVector = [0,0,1])
        >>> print(Intersection._intersectAreas(plane1, plane2))
        None
        """
        # get direction of resulting line
        directionVector = np.cross(plane1.planeNormalVector, plane2.planeNormalVector)
        if np.linalg.norm(directionVector) < epsilon:
            # normal vectors are parallel to each other
            if plane1.getDistanceToPoint(plane2.planePositioningVector) < epsilon:
                # planes are coincident
                return plane1
            else:
                return None

        # =======================================================================
        # get base vector of the desired line
        # This is done by using the plane orientation vector that is not parallel to the other plane.
        # Then the intersection of a line with this orientation vector and the other plane is calculated.
        # =======================================================================

        lineToIntersect = Line(
            plane1.planePositioningVector,
            plane1.planePositioningVector + plane1.planeOrientationVector1,
        )
        intersectionPoint = Intersection.getIntersection([lineToIntersect], [plane2])
        if intersectionPoint is None or intersectionPoint is lineToIntersect:
            # orientation vector1 is parallel to the other plane
            lineToIntersect = Line(
                plane1.planePositioningVector,
                plane1.planePositioningVector + plane1.planeOrientationVector2,
            )
            intersectionPoint = Intersection.getIntersection([lineToIntersect], [plane2])

        return Line(intersectionPoint, (intersectionPoint + directionVector))

    @staticmethod
    def _intersectLineArea(line, plane):
        """doc

        >>> from patme.geometry.translate import Translation
        >>> from patme.geometry.plane import Plane
        >>> plane = Plane()
        >>> plane = plane.generatePlane([0,0,0], planeNormalVector = [0,0,1])
        >>> Intersection._intersectLineArea(Line(Translation([0,0,0]),Translation([0,0,1])), plane)
        Translation([0., 0., 0.])
        >>> print(Intersection._intersectLineArea(Line(Translation([0,0,1]),Translation([1,0,1])), plane))
        None
        >>> line = Line(Translation([0,0,0]),Translation([1,0,0]))
        >>> line is Intersection._intersectLineArea(line, plane)
        True
        """
        # check if line is parallel to plane
        usedVector = (
            plane.planeOrientationVector2
            if areVectorsParallel(plane.planeOrientationVector1, line.vector)
            else plane.planeOrientationVector1
        )
        crossProduct = np.cross(usedVector, line.vector)

        if areVectorsParallel(crossProduct, plane.planeNormalVector):
            # line is parallel to plane
            distance = np.linalg.norm(
                np.dot(plane.planeNormalVector, (line.p1 - plane.planePositioningVector))
            ) / np.linalg.norm(plane.planeNormalVector)
            if -1.0 * epsilon <= distance <= epsilon:
                # Line lays within plane. Infinite number of intersection point calculable.
                return line
            else:
                return None
        else:
            phi = np.dot(plane.planeNormalVector, (plane.planePositioningVector - line.p1)) / np.dot(
                plane.planeNormalVector, line.vector
            )
            intersectionPoint = line.p1 + phi * line.vector

            return intersectionPoint


if __name__ == "__main__":

    import doctest

    doctest.testmod()
