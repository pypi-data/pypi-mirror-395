# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT
"""methods for 2d shapes"""

import numpy as np

from patme import epsilon
from patme.geometry.rotate import Rotation


def getSuperEllipseCoords(
    halfAxisHoriz, halfAxisVert, ellipseParamHoriz, ellipseParamVert, ellipseRotationAngle, samplePointsEllipse
):
    """

    :param halfAxisHoriz: horizontal half axis
    :param halfAxisVert: vertical half axis
    :param ellipseParamHoriz: horizontal ellipse power parameter
    :param ellipseParamVert: vertical ellipse power parameter
    :param ellipseRotationAngle: rotation in deg of the ellipse
    :param samplePointsEllipse: number of sample points of the ellipse
    :return: np array of shape (samplePointsEllipse, 2) with ellipse coords
    """
    ellipse = np.ones((samplePointsEllipse, 3))

    angles = np.linspace(0, 2 * np.pi, samplePointsEllipse, endpoint=False)

    ellipse[:, 0] = _calcPowerForEllipse(np.cos, halfAxisHoriz, angles, ellipseParamHoriz)
    ellipse[:, 1] = _calcPowerForEllipse(np.sin, halfAxisVert, angles, ellipseParamVert)

    # rotate ellipse
    if abs(ellipseRotationAngle) > epsilon:
        rot = Rotation()
        rot.angles = (0, 0, np.deg2rad(ellipseRotationAngle))
        ellipse = np.dot(rot, ellipse.T).T
    ellipse = ellipse[:, :2]

    return ellipse


def _calcPowerForEllipse(sinOrCosFunc, halfAxis, angles, ellipseParameter):
    """The power calculation for negative values does not work for float exponents. Use a workaround for it."""
    sinOrCos = sinOrCosFunc(angles)
    sinOrCosIsNeg = sinOrCos < 0.0
    sinOrCos[sinOrCosIsNeg] *= -1
    ellipse = halfAxis * np.power(sinOrCos, 2.0 / ellipseParameter)
    ellipse[sinOrCosIsNeg] *= -1
    return ellipse
