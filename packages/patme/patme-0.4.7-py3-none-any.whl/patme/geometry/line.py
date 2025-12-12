# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT


from operator import attrgetter

import numpy as np

from patme import epsilon
from patme.geometry.translate import Translation
from patme.service.exceptions import InternalError


class Lines(list):
    """doc"""

    def sort(self, cmp=None, key=None, reverse=False, attribute=None):
        """doc"""
        if key == None:
            try:
                # make attribute an iterable item if needed
                a = attribute[0]
                if isinstance(attribute, str):
                    raise
            except:
                attribute = [attribute]
            key = attrgetter(*attribute)
        list.sort(self, key=key, reverse=reverse)


class Line:
    """classdocs"""

    # Attention: when changing parameters, please also edit them in model.mechanicalproperties.Beam.__init__
    def __init__(self, point1=None, point2=None, lineID=None, doZeroLengthCheck=True):
        """Creates a line based on two points

        :param point1: first point, should be instance of model.geometry.translate.Translation
        :param point2: first point, should be instance of model.geometry.translate.Translation
        :param lineID: id of the point used in FEM
        :param connectVertex: Flag if common neighbors of point1 and point2 should be connected with the new line
        :param doZeroLengthCheck: geometrical lines should not have a length of zero. Hence an exception is risen in this case.
            If a length of zero is on purpose (e.g. to constrain two nodes), this flag should be set to False
        """
        # init ac graph vertex
        if point1 is point2:
            raise InternalError("The same points are given as point1 and point2.")

        self._keypoints = []
        if point1 is not None and point2 is not None:
            self._keypoints = [point1, point2]

        # check if lines have a length higher than zero
        if doZeroLengthCheck and self._keypoints and self.length < epsilon:
            raise InternalError(f"The given line has a length of zero! line, length: {lineID}, {self.length}")

        self.id = lineID
        self.cutout = None

    def copy(self, old2NewDict, copyProperties):
        """returns a copy of this instance.
        :param old2NewDict: references attributes of self with the newly created instances to
            reestablish the connections between instances
        :param copyProperties: Flag if sheetproperties and profiles should be copied or
            if the references should be kept.
        """
        return self.__class__(old2NewDict[self.p1], old2NewDict[self.p2], lineID=self.id)

    def __str__(self):
        """doc"""
        if self._keypoints:
            return ", ".join(str(k) for k in self._keypoints)
        else:
            return ""

    def _getp1(self):
        """doc"""
        self._checkKeypoints()
        return self.keypoints[0]

    def _getp2(self):
        """doc"""
        self._checkKeypoints()
        return self.keypoints[-1]

    def _getxLesser(self):
        """Returns the lesser x-coordinate of the two keypoints."""
        self._checkKeypoints()
        return min(self.p1.x, self.p2.x)

    def _getyLesser(self):
        """Returns the lesser y-coordinate of the two keypoints."""
        self._checkKeypoints()
        return min(self.p1.y, self.p2.y)

    def _getzLesser(self):
        """Returns the lesser z-coordinate of the two keypoints."""
        self._checkKeypoints()
        return min(self.p1.z, self.p2.z)

    def _getxGreater(self):
        """Returns the greater x-coordinate of the two keypoints."""
        self._checkKeypoints()
        return max(self.p1.x, self.p2.x)

    def _getyGreater(self):
        """Returns the greater y-coordinate of the two keypoints."""
        self._checkKeypoints()
        return max(self.p1.y, self.p2.y)

    def _getzGreater(self):
        """Returns the greater z-coordinate of the two keypoints."""
        self._checkKeypoints()
        return max(self.p1.z, self.p2.z)

    def _getLength(self):
        """doc"""
        return self.p1.distance(self.p2)

    def _getKeypoints(self):
        """doc"""
        return self._keypoints

    def _checkKeypoints(self):
        """This method raises an InternalError if there are not exactly 2 keypoints."""
        if len(self.keypoints) != 2:
            raise InternalError("There are not exactly 2 keypoints for line %s" % repr(self))

    def _getVector(self):
        """Retruns the vector of the line as p2=p1+vector"""
        return self.p2 - self.p1

    def _getNormalizedVector(self):
        """Retruns the vector of the line as p2=p1+vector"""
        vector = self.vector
        return vector / np.linalg.norm(vector)

    def _getMeanPoint(self):
        """Retruns the mean of both points: mean(self.p1, self.p2)"""
        return Translation(np.mean([self.p2, self.p1], 0))

    keypoints = property(fget=_getKeypoints)
    p1 = property(fget=_getp1)
    p2 = property(fget=_getp2)
    xLesser = property(fget=_getxLesser)
    """Returns the lesser x-coordinate of the two keypoints."""
    yLesser = property(fget=_getyLesser)
    """Returns the lesser y-coordinate of the two keypoints."""
    zLesser = property(fget=_getzLesser)
    """Returns the lesser z-coordinate of the two keypoints."""
    xGreater = property(fget=_getxGreater)
    """Returns the greater x-coordinate of the two keypoints."""
    yGreater = property(fget=_getyGreater)
    """Returns the greater y-coordinate of the two keypoints."""
    zGreater = property(fget=_getzGreater)
    """Returns the greater z-coordinate of the two keypoints."""
    length = property(fget=_getLength)
    """Returns the length of the line (2-norm)"""
    vector = property(fget=_getVector)
    """Returns the vector of the line as p2=p1+vector"""
    meanPoint = property(fget=_getMeanPoint)
    """Returns the mean of the two points: mean(self.p1, self.p2)"""
    normalizedVector = property(fget=_getNormalizedVector)
    """Returns the mean of the two points: mean(self.p1, self.p2)"""


def computePointsOnBezierCurve(bezierKnots, s_vals):
    """doc"""
    from scipy.special import binom

    npbezierKnots = np.array(bezierKnots)
    degree = npbezierKnots.shape[0] - 1

    kVals = np.arange(degree + 1)
    tmp = np.power(1 - s_vals[:, np.newaxis], degree - kVals)
    tmp2 = np.power(s_vals[:, np.newaxis], kVals)

    binomStuff = binom([degree] * kVals.size, kVals)
    res = binomStuff * tmp * tmp2
    evaluatedPoints = np.dot(npbezierKnots.T, res.T).T
    return evaluatedPoints
