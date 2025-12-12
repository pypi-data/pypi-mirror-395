# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT


import numpy as np

from patme.geometry.translate import Translation


class Area:
    def __init__(self, lines=None, areaID=None, **kwargs):
        """doc"""
        self.cutout = None
        self._surfaceArea = None
        self._centerOfArea = None
        self.id = areaID
        self.splitAreaIDs = []
        if not lines:
            lines = []

        self._lines = lines
        self.innerLines = kwargs.get("innerLines", [])

    def toggleLineOrder(self):
        """changes the order of each line: first line will be last line etc."""
        raise Exception("Not implemented")

    def toggleLineDirection(self):
        """changes the direction of the lines: first line stays intact, second line will be last line etc."""
        raise Exception("Not implemented")

    def _getKeypoints(self):
        """doc"""
        keypts = []
        for line in self.lines:
            for pt in line.keypoints:
                if pt not in keypts:
                    keypts.append(pt)
        return keypts

    def _getSurfaceArea(self):
        """Split area in triangles and calculate their surface area(flaecheninhalt).
        assumption: concave area(which is not checked automatically)

        The distances are calculated. With this, the angle gamma can be calculated
        which encloses the two smallest lines. Then, the surface area for this triangle
        is calculated.
        Calculates also the center of area during surface area calculation. These centers
        are cumulated to the total center of area."""
        if self._surfaceArea is None:
            if len(self.lines) < 3:
                self._surfaceArea = 0.0
                self._centerOfArea = Translation()
            else:
                keypoints = self.keypoints
                midKeypoint = keypoints[0]
                lastKeypoint = keypoints[1]
                totalSurfaceArea = 0.0
                centerOfArea = np.zeros(3)
                for keypoint in keypoints[2:]:
                    distances = sorted(
                        [
                            midKeypoint.distance(lastKeypoint),
                            lastKeypoint.distance(keypoint),
                            keypoint.distance(midKeypoint),
                        ]
                    )

                    # source: http://de.wikipedia.org/wiki/Dreiecksfl%C3%A4che#Zwei_Seitenl.C3.A4ngen_und_eingeschlossener_Winkel_gegeben
                    gamma = np.arccos(
                        (distances[0] ** 2 + distances[1] ** 2 - distances[-1] ** 2) / (2 * distances[0] * distances[1])
                    )
                    surfaceArea = 0.5 * distances[0] * distances[1] * np.sin(gamma)
                    totalSurfaceArea += surfaceArea
                    centerOfArea += np.mean([midKeypoint, lastKeypoint, keypoint], 0) * surfaceArea
                    lastKeypoint = keypoint

                self._surfaceArea = totalSurfaceArea
                self._centerOfArea = Translation(centerOfArea / totalSurfaceArea)

        return self._surfaceArea

    def getCenterOfArea(self):
        """Returns a translation which is the mean of all keypoints"""
        return np.sum(self.keypoints, 0) / len(self.keypoints)

    def commonLine(self, otherArea):
        """doc"""
        commonLines = set(self.lines) & set(otherArea.lines)
        if commonLines != set():
            return commonLines.pop()
        return None

    def _getCenterOfArea(self):
        """see _getSurfaceArea"""
        if self._centerOfArea is None:
            self.surfaceArea
        return self._centerOfArea

    def _getLines(self):
        return self._lines

    def _setLines(self, value):
        self._lines = value

    def _getNormalDirection(self):
        l1, l2 = self.lines[:2]
        p1 = (set(l1.keypoints) & set(l2.keypoints)).pop()
        p0 = set(l1.keypoints).difference({p1}).pop()
        p2 = set(l2.keypoints).difference({p1}).pop()
        return Translation(np.cross(p1 - p0, p2 - p0))

    normalDirection = property(fget=_getNormalDirection)
    """Returns normal direction of self"""

    lines = property(fget=_getLines, fset=_setLines)
    keypoints = property(fget=_getKeypoints)
    surfaceArea = property(fget=_getSurfaceArea)
    """flaecheninhalt"""
    centerOfArea = property(fget=_getCenterOfArea)
    """Calculates the center of area during surface area calculation. These centers
    are cumulated to the total center of area."""
