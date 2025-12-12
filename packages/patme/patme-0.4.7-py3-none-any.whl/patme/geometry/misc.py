# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
""" """
from operator import eq, ne

import numpy as np

from patme import epsilon
from patme.geometry.translate import Translation
from patme.service.exceptions import ImproperParameterError, InternalError


def PCA(data, correlation=False, sort=True):
    """Applies Principal Component Analysis to the data

    Method from
    https://github.com/daavoo/pyntcloud/blob/master/pyntcloud/utils/array.py
    MIT license

    Parameters
    ----------
    data: array
        The array containing the data. The array must have NxM dimensions, where each
        of the N rows represents a different individual record and each of the M columns
        represents a different variable recorded for that individual record.
            array([
            [V11, ... , V1m],
            ...,
            [Vn1, ... , Vnm]])

    correlation(Optional) : bool
            Set the type of matrix to be computed (see Notes):
                If True compute the correlation matrix.
                If False(Default) compute the covariance matrix.

    sort(Optional) : bool
            Set the order that the eigenvalues/vectors will have
                If True(Default) they will be sorted (from higher value to less).
                If False they won't.
    Returns
    -------
    eigenvalues: (1,M) array
        The eigenvalues of the corresponding matrix.

    eigenvector: (M,M) array
        The eigenvectors of the corresponding matrix.

    Notes
    -----
    The correlation matrix is a better choice when there are different magnitudes
    representing the M variables. Use covariance matrix in other cases.

    """

    mean = np.mean(data, axis=0)

    data_adjust = data - mean

    #: the data is transposed due to np.cov/corrcoef syntax
    if correlation:

        matrix = np.corrcoef(data_adjust.T)

    else:
        matrix = np.cov(data_adjust.T)

    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    if sort:
        #: sort eigenvalues and eigenvectors
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def areVectorsParallel(vector1, vector2):
    """checks if two vectors are parallel to each other

    >>> areVectorsParallel([0,0,2],[0,0,1])
    True
    >>> areVectorsParallel([0,0,2],[0,1,1])
    False
    >>> areVectorsParallel([0,0,0],[0,0,1])
    False
    """
    vector1, vector2 = np.array(vector1), np.array(vector2)
    if np.linalg.norm(vector1) < epsilon or np.linalg.norm(vector2) < epsilon:
        return False

    # normalize vectors
    vector1, vector2 = vector1 / vector1[np.argmax(np.abs(vector1))], vector2 / vector2[np.argmax(np.abs(vector2))]
    return np.linalg.norm(vector1 - vector2) < epsilon


def getGeometricCenterSimple(keypointList):
    """Returns the geometric center of self using the average of the min and
    max coordinates.

    >>> from patme.geometry.translate import Translation
    >>> keypointList = [Translation([0,a,(-1)**a*5]) for a in range(10)]
    >>> getGeometricCenterSimple(keypointList)
    Translation([0. , 4.5, 0. ])

    :param keypointList: list of Translation objects
    :return: instance of type Translation at the geometric center of the rib
    """
    pointArray = np.array([kp[:3] for kp in keypointList])
    center = (pointArray.max(axis=0) + pointArray.min(axis=0)) / 2
    return Translation(center)


def getAngleOnYZPlane(keypoint, referenceY=0.0, referenceZ=0.0):
    """calculating angle of keypoint on the y-z plane in reference to a
    optionally shifted coordinate system.

    :return: angle in degees[0,360]

    .. note:: Please refer to the CPACS definition of the fuselage coordinate system.
             These are the results for the CPACS definition::

                # results of getAngleOnYZPlane:
                #       y ^
                #  225    |    315
                #         |
                #     <---x---> z
                #         |
                #  135    |    45

         tan alpha = y / z
         coordinate system is rotated since angle=0 is on positive z-axis
         additionally the negative angles need to be shifted by 360deg

    >>> t1 = Translation([0,-1.,1.])
    >>> abs(getAngleOnYZPlane(t1))
    45.0
    >>> t1 = Translation([0,0.,1.])
    >>> abs(getAngleOnYZPlane(t1))
    0.0
    """

    alpha = np.arctan2(keypoint.y - referenceY, keypoint.z - referenceZ) * 180 / np.pi
    if alpha < epsilon:
        alpha += 360

    # subtract alpha by 360 since arctan2 calculates alpha in mathematically positive direction but
    # tigl calculates it in the negative direction
    return 360.0 - alpha


def getNearestKeypoint(points, point):
    """This method returns the point from a specified point list next to the
    position of a specified point.
    All points have to be of a class that inherits the numpy array class."""

    tmpPoints = np.array(points, copy=True)
    allDists = np.linalg.norm(tmpPoints - point, axis=1)
    return points[np.argmin(allDists)]


def getRelativePositionOfProjectedPointOnLine(point, lineStartPoint, lineEndPoint):
    """Retrieve the relative distance of point Pp to the lineStartPoint. Pp is the point
    projection of point P on the straight line through the points lineStartPoint and
    lineEndPoint. The relative distance can also be < 0 or > 1, indicating that the
    projected point is not in between the given points.

            x P                 P     = point
                                Pp    = projected point
    o-------x-------o           Start = lineStartPoint
    Start   Pp      End         End   = lineEndPoint
    0-----alpha---->1

    >>> round(getRelativePositionOfProjectedPointOnLine([0,0,0], [-1,-1,-1], [1,1,1]), 1)
    0.5
    >>> round(getRelativePositionOfProjectedPointOnLine([-1,-1,-1], [-1,-1,-1], [1,1,1]), 1)
    0.0
    >>> round(getRelativePositionOfProjectedPointOnLine([1,1,1], [-1,-1,-1], [1,1,1]), 1)
    1.0
    >>> round(getRelativePositionOfProjectedPointOnLine([10,10,10], [-1,-1,-1], [1,1,1]), 1)
    5.5
    >>> round(getRelativePositionOfProjectedPointOnLine([-3,-3,-3], [-1,-1,-1], [1,1,1]), 1)
    -1.0
    >>> round(getRelativePositionOfProjectedPointOnLine([2,2,2], [0,0,0], [1,0,0]), 1)
    2.0

    :param point: array with 3d coordinate of point to be projected
    :param lineStartPoint: array with 3d coordinate of the line start point
    :param lineEndPoint: array with 3d coordinate of the line end point
    :return: relative distance between lineStartPoint and projection of point
    """
    point, lineStartPoint, lineEndPoint = np.array(point), np.array(lineStartPoint), np.array(lineEndPoint)
    alpha = np.dot(
        (point - lineStartPoint), (lineEndPoint - lineStartPoint) / np.linalg.norm(lineEndPoint - lineStartPoint) ** 2
    )
    return alpha


def getPointProjectedOnLine(lineStart, lineEnd, point, clipAlpha=True):
    """calculate the point that is projected from point to the line defined by lineStart and lineEnd

    :return: Pp - projected point

            x P                 P     = point
                                Pp    = projected point
    o-------x-------o           Start = lineStartPoint
    Start   Pp      End         End   = lineEndPoint
    0-----alpha---->1

    >>> getPointProjectedOnLine([0,0,0], [0,0,1], [1,0,0])
    array([0., 0., 0.])
    >>> getPointProjectedOnLine([0,0,0], [0,0,2], [1,0,1])
    array([0., 0., 1.])

    """
    point, lineStart, lineEnd = np.array(point), np.array(lineStart), np.array(lineEnd)
    alpha = getRelativePositionOfProjectedPointOnLine(point, lineStart, lineEnd)
    # limitation of alpha between 0 and 1
    # next position for distance calculation if clipAlpha equals true
    # else projection point is used for distance computation
    if clipAlpha:
        alpha = np.clip(alpha, 0, 1)
    projPoint = lineStart + alpha * (lineEnd - lineStart)
    return projPoint


def getPointDistanceToLine(lineStart, lineEnd, point, clipAlpha=True):
    """Retrieve the absolute distance of point from the straight line through lineStart and
    lineEnd. The returned distance is the distance between P and Pp

            x P                 P     = point
                                Pp    = projected point
    o-------x-------o           Start = lineStartPoint
    Start   Pp      End         End   = lineEndPoint
    0-----alpha---->1

    >>> round(getPointDistanceToLine([-1,-1,-1], [1,1,1], [0,0,0]), 1)
    0.0
    >>> round(getPointDistanceToLine([0,0,0], [0,0,1], [2,0,-2], clipAlpha=False), 1)
    2.0
    >>> round(getPointDistanceToLine([-1,-1,-1], [1,1,1], [10,10,10], clipAlpha=False), 1)
    0.0

    :param lineStart: array with 3d coordinate of the line start point
    :param lineEnd: array with 3d coordinate of the line end point
    :param point: array with 3d coordinate of point to be projected
    :return: distance between point and the straight line through lineStart and lineEnd
    """
    point, lineStart, lineEnd = np.array(point), np.array(lineStart), np.array(lineEnd)
    projPoint = getPointProjectedOnLine(lineStart, lineEnd, point, clipAlpha)
    distance = np.linalg.norm(point - projPoint)
    if distance == np.nan:
        length = np.linalg.norm(lineStart, lineEnd)
        raise InternalError(
            "Got an error while calculating the distance of a point to a line. " + "The line-points coincide."
            if length < epsilon
            else ""
        )

    return distance


def isPointProjectionOnLineBetweenPoints(point, lineStartPoint, lineEndPoint):
    """Checks if the projection of point onto the straight line through lineStartPoint
    and lineEndPoint is between lineStartPoint and lineEndPoint. Both end points are
    included into the interval. For further information read the documentation of the
    function getRelativePositionOfProjectedPointOnLine()

    >>> isPointProjectionOnLineBetweenPoints([0,0,0], [-1,-1,-1], [1,1,1])
    True
    >>> isPointProjectionOnLineBetweenPoints([-1,-1,-1], [-1,-1,-1], [1,1,1])
    True
    >>> isPointProjectionOnLineBetweenPoints([1,1,1], [-1,-1,-1], [1,1,1])
    True
    >>> isPointProjectionOnLineBetweenPoints([10,10,10], [-1,-1,-1], [1,1,1])
    False
    >>> isPointProjectionOnLineBetweenPoints([-10,-10,-10], [-1,-1,-1], [1,1,1])
    False
    >>> isPointProjectionOnLineBetweenPoints([-0.5,-0.5,0.], [-1,-1,-1], [1,1,1])
    True

    :param point: array with 3d coordinate of point to be projected
    :param lineStartPoint: array with 3d coordinate of the line start point
    :param lineEndPoint: array with 3d coordinate of the line end point
    :return: True if projection of point is between lineStartPoint and lineEndPoint, else False
    """
    point, lineStartPoint, lineEndPoint = np.array(point), np.array(lineStartPoint), np.array(lineEndPoint)
    alpha = getRelativePositionOfProjectedPointOnLine(point, lineStartPoint, lineEndPoint)
    if alpha > -epsilon and alpha < 1 + epsilon:
        return True
    else:
        return False


def isPointOnLineBetweenPoints(point, lineStartPoint, lineEndPoint):
    """Checks if point is located on a straight line between the given points lineStartPoint and
    lineEndPoint including these points.

    >>> isPointOnLineBetweenPoints([0,0,0], [-1,-1,-1], [1,1,1])
    True
    >>> isPointOnLineBetweenPoints([-1,-1,-1], [-1,-1,-1], [1,1,1])
    True
    >>> isPointOnLineBetweenPoints([1,1,1], [-1,-1,-1], [1,1,1])
    True
    >>> isPointOnLineBetweenPoints([10,10,10], [-1,-1,-1], [1,1,1])
    False
    >>> isPointOnLineBetweenPoints([-10,-10,-10], [-1,-1,-1], [1,1,1])
    False
    >>> isPointOnLineBetweenPoints([-10,-10,0], [-1,-1,-1], [1,1,1])
    False

    :param point: 1x3 array containing a 3D coordinate of the point to be checked
    :param lineStartPoint: 1x3 array containing a 3D coordinate of the line start point
    :param lineStartPoint: 1x3 array containing a 3D coordinate of the line end point
    :return: True if point is on straight line between lineStartPoint and lineEndPoint, else False
    """
    point, lineStartPoint, lineEndPoint = np.array(point), np.array(lineStartPoint), np.array(lineEndPoint)
    # check if lineStartPoint and lineEndPoint are not equal
    if all(np.abs(lineStartPoint - lineEndPoint) < epsilon):
        raise ImproperParameterError("lineStartPoint and lineEndPoint must not be coincidental")
    # check if point is coincident with lineStartPoint or lineEndPoint
    if all(np.abs(lineStartPoint - point) < epsilon) or all(np.abs(lineEndPoint - point) < epsilon):
        return True
    # check if point is not on straight line through lineStartPoint and lineEndPoint
    if getPointDistanceToLine(lineStartPoint, lineEndPoint, point, clipAlpha=False) > epsilon:
        return False
    # check if point is in between lineStartPoint and lineEndPoint
    if isPointProjectionOnLineBetweenPoints(point, lineStartPoint, lineEndPoint):
        return True
    return False


def getLineLoop(lines, startLine=None):
    """retuns a list of lines in the correct order"""

    def isAdjacentLine(line, otherLine):
        return bool({line.p1, line.p2} & {otherLine.p1, otherLine.p2})

    if len(lines) == 1:
        return lines, [1]

    linesCopy = lines[:]
    if startLine is not None:
        ix = linesCopy.index(startLine)
        if ix == -1:
            firstLine = linesCopy[0]
        else:
            firstLine = linesCopy[ix]
    else:
        firstLine = linesCopy[0]

    loop = [firstLine]
    linesCopy.remove(firstLine)

    curLine = None
    adjLines = [line for line in linesCopy if isAdjacentLine(line, loop[0])]
    if adjLines:
        curLine = next((line for line in adjLines if line.p1 == loop[0].p2), None)
        if not curLine:
            curLine = next((line for line in adjLines if line.p2 == loop[0].p2), None)
            if not curLine:
                raise Exception("No matching adjacent line found for line %s" % loop[0].id)
    else:
        raise Exception("No matching adjacent line found for line %s" % loop[0].id)

    loop.append(curLine)

    linesCopy.pop(linesCopy.index(curLine))
    while len(linesCopy) > 0:
        nextLineIx = next(i for i, line in enumerate(linesCopy) if isAdjacentLine(line, curLine))
        loop.append(linesCopy[nextLineIx])
        curLine = linesCopy[nextLineIx]
        linesCopy.pop(nextLineIx)

    lineOrientation = [1]
    cmpFuncDict = {-1: eq, 1: ne}
    for i, line in enumerate(loop[1:], 1):

        cmpFunc = cmpFuncDict[lineOrientation[i - 1]]

        prevLinePoints = loop[i - 1].keypoints[:: lineOrientation[i - 1]]

        if cmpFunc(line.p1.id, prevLinePoints[-1].id):
            muliplier = -1
        else:
            muliplier = 1

        lineOrientation.append(lineOrientation[i - 1] * muliplier)

    return loop, lineOrientation


def getAngleBetweenVectors(vector1, vector2):
    """calcuclates the angle [°] between two vectors

    >>> angle = getAngleBetweenVectors([1,0,0],[0,1,0])
    >>> round(angle,1)
    90.0
    >>> angle = getAngleBetweenVectors([1,0,0],[1,1,0])
    >>> round(angle,1)
    45.0
    >>> angle = getAngleBetweenVectors([1,0,0],[1,0,0])
    >>> round(angle,1)
    0.0
    """
    vector1, vector2 = np.array(vector1), np.array(vector2)

    nominator = np.dot(vector1, vector2)
    denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    fraction = nominator / denominator
    if abs(fraction - 1) < epsilon:
        angleRad = 0.0
    elif abs(fraction + 1) < epsilon:
        angleRad = np.pi
    else:
        angleRad = np.arccos(fraction)
    angle = np.degrees(angleRad)
    return angle
