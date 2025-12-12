# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
The following conditions and Copyright is related to two functionalities of Transformation:
Transformation.setRotationByAxisAndAngle()
Transformation.estimateTransformationFromPointSets()

For detailed information please refer to '<http://www.lfd.uci.edu/~gohlke/code/transformations.py.html>'_ (23.01.2014).

References
----------
(1)  Matrices and transformations. Ronald Goldman.
     In "Graphics Gems I", pp 472-475. Morgan Kaufmann, 1990.
(2)  More matrices and transformations: shear and pseudo-perspective.
     Ronald Goldman. In "Graphics Gems II", pp 320-323. Morgan Kaufmann, 1991.
(3)  Decomposing a matrix into simple transformations. Spencer Thomas.
     In "Graphics Gems II", pp 320-323. Morgan Kaufmann, 1991.
(4)  Recovering the data from the transformation matrix. Ronald Goldman.
     In "Graphics Gems II", pp 324-331. Morgan Kaufmann, 1991.
(5)  Euler angle conversion. Ken Shoemake.
     In "Graphics Gems IV", pp 222-229. Morgan Kaufmann, 1994.
(6)  Arcball rotation control. Ken Shoemake.
     In "Graphics Gems IV", pp 175-192. Morgan Kaufmann, 1994.
(7)  Representing attitude: Euler angles, unit quaternions, and rotation
     vectors. James Diebel. 2006.
(8)  A discussion of the solution for the best rotation to relate two sets
     of vectors. W Kabsch. Acta Cryst. 1978. A34, 827-828.
(9)  Closed-form solution of absolute orientation using unit quaternions.
     BKP Horn. J Opt Soc Am A. 1987. 4(4):629-642.
(10) Quaternions. Ken Shoemake.
     http://www.sfu.ca/~jwa3/cmpt461/files/quatut.pdf
(11) From quaternion to matrix and back. JMP van Waveren. 2005.
     http://www.intel.com/cd/ids/developer/asmo-na/eng/293748.htm
(12) Uniform random rotations. Ken Shoemake.
     In "Graphics Gems III", pp 124-132. Morgan Kaufmann, 1992.
(13) Quaternion in molecular modeling. CFF Karney.
     J Mol Graph Mod, 25(5):595-604
(14) New method for extracting the quaternion from a rotation matrix.
     Itzhack Y Bar-Itzhack, J Guid Contr Dynam. 2000. 23(6): 1085-1087.
(15) Multiple View Geometry in Computer Vision. Hartley and Zissermann.
     Cambridge University Press; 2nd Ed. 2004. Chapter 4, Algorithm 4.7, p 130.
(16) Column Vectors vs. Row Vectors.
     http://steve.hollasch.net/cgindex/math/matrix/column-vec.html
"""
# Copyright (c) 2006-2014, Christoph Gohlke
# Copyright (c) 2006-2014, The Regents of the University of California
# Produced at the Laboratory for Fluorescence Dynamics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import warnings

import numpy as np

from patme import epsilon
from patme.geometry.plane import Plane
from patme.geometry.rotate import Rotation
from patme.geometry.scale import Scaling
from patme.geometry.translate import Translation
from patme.service.exceptions import ImproperParameterError, InternalError
from patme.service.logger import log


class Transformation(np.ndarray):
    """
    This class describes a Transformation in 3D space which is represented by a 3x3 matrix.

    With this class coordinate transformations in 3D space can be created and operations may be performed.
    For that purpose the class inherits from np.ndarray which is a class for storing
    matrix values and performing operations on them. For further details on np.ndarray
    please refer to the numpy/scipy documentation.

    Transformations are represented by a 4x4 matrix. A transformation is composed of
    a rotation matrix r_ii, a translation t_i, a scaling s_i and a projection p_i the following way::

        [[ s_1*r_11,  r_21,  r_31,  t_1],
         [ r_12,  s_2*r_22,  r_32,  t_2],
         [ r_13,  r_23,  s_3*r_33,  t_3],
         [ p_1 ,  p_2 ,  p_3 ,   1 ]]

    Actually Scalings are not actively supported in this class. Thus is it still
    mathematically possible.

    Transformations can be created and used in the following ways::

        >>> import numpy as np
        >>> from patme.geometry.coordinatesystem import Transformation
        >>> from patme.geometry.translate import Translation
        >>> from patme.geometry.rotate import Rotation
        >>> t = Translation([5,2,0])
        >>> # creating identity transformation
        >>> tr = Transformation()
        >>> tr
        Transformation([[1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 1., 0.],
                        [0., 0., 0., 1.]])
        >>> # setting a translation
        >>> tr.translation = t
        >>> tr
        Transformation([[1., 0., 0., 5.],
                        [0., 1., 0., 2.],
                        [0., 0., 1., 0.],
                        [0., 0., 0., 1.]])

        >>> ####################### adding a translation
        >>> tr.addTranslation(t)
        >>> tr
        Transformation([[ 1.,  0.,  0., 10.],
                        [ 0.,  1.,  0.,  4.],
                        [ 0.,  0.,  1.,  0.],
                        [ 0.,  0.,  0.,  1.]])

        >>> ####################### setting a rotation
        >>> rx = Rotation()
        >>> rx.angles = (np.pi/2,0,0)
        >>> ry = Rotation()
        >>> ry.angles = (0,np.pi/2,0)
        >>> tr.rotation = rx
        >>> tr.round() + 0 # ".round()" avoids long floats and "+ 0" turns all -0 in 0
        Transformation([[ 1.,  0.,  0., 10.],
                        [ 0.,  0., -1.,  4.],
                        [ 0.,  1.,  0.,  0.],
                        [ 0.,  0.,  0.,  1.]])
        >>> # adding a rotation
        >>> tr.addRotation(ry)
        >>> tr.round() + 0
        Transformation([[ 0.,  0.,  1., 10.],
                        [ 1.,  0.,  0.,  4.],
                        [ 0.,  1.,  0.,  0.],
                        [ 0.,  0.,  0.,  1.]])
        >>> # concatenation of transformations
        >>> tr2 = Transformation()
        >>> tr2.translation = [0,0,1]
        >>> tr3 = tr*tr2
        >>> tr3.round() + 0
        Transformation([[ 0.,  0.,  1., 11.],
                        [ 1.,  0.,  0.,  4.],
                        [ 0.,  1.,  0.,  0.],
                        [ 0.,  0.,  0.,  1.]])
        >>> # inverting transformation
        >>> tr3inv = tr3.getInverse()
        >>> tr3inv.round() + 0
        Transformation([[  0.,   1.,   0.,  -4.],
                        [  0.,   0.,   1.,   0.],
                        [  1.,   0.,   0., -11.],
                        [  0.,   0.,   0.,   1.]])
        >>> (tr3*tr3inv).round() + 0 # retruns identity matrix
        Transformation([[1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 1., 0.],
                        [0., 0., 0., 1.]])

        >>> ####################### transformation of translations
        >>> # MOST IMPORTANT !!!
        >>> tr3*t
        Translation([11.,  9.,  2.])
        >>> t1 = tr3inv * (tr3 * t)
        >>> t1.round()
        Translation([5., 2., 0.])

        >>> ####################### setting a scaling
        >>> sx = Scaling()
        >>> sx.factors = (2.0,1.0,1.0)
        >>> sxyz = Scaling()
        >>> sxyz.factors = (2.0,2.0,2.0)
        >>> tr.scaling = sx # also resets the rotation
        >>> tr
        Transformation([[ 2.,  0.,  0., 10.],
                        [ 0.,  1.,  0.,  4.],
                        [ 0.,  0.,  1.,  0.],
                        [ 0.,  0.,  0.,  1.]])
        >>> # adding a scaling
        >>> tr.addScaling(sxyz)
        >>> tr
        Transformation([[ 4.,  0.,  0., 10.],
                        [ 0.,  2.,  0.,  4.],
                        [ 0.,  0.,  2.,  0.],
                        [ 0.,  0.,  0.,  1.]])
    """

    __hash__ = object.__hash__
    """hash reimplementation due to definition of __eq__. See __hash__ doc for more details.
    https://docs.python.org/3.4/reference/datamodel.html#object.__hash__"""

    def __new__(cls, input_array=None, tId=None, description=None):
        """constructing np.ndarray instance. For more information see
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#basics-subclassing"""
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        if input_array is None:
            input_array = np.identity(4, dtype=np.float64)
        if not hasattr(input_array, "shape"):
            input_array = np.asarray(input_array)
        if not input_array.shape == (4, 4):
            raise ImproperParameterError(
                "The given transformation must be a 4x4 matrix like object. Got this instead: " + str(input_array)
            )
        obj = input_array.view(cls)
        return obj

    def setTransformation(self, t=None, r=None, s=None, t_id=None):
        """doc"""
        if np.any(t):
            self[:3, 3] = t * 1

        #        # scale the transformation matrix
        #        # get scaling in each dimension and perform a matrix multiplication
        #        sc1 = trafo.scale_matrix(s.vals.x, None, [1, 0, 0])
        #        sc2 = trafo.scale_matrix(s.vals.y, None, [0, 1, 0])
        #        sc3 = trafo.scale_matrix(s.vals.z, None, [0, 0, 1])
        #        self = np.dot(np.dot(sc1, sc2), np.dot(sc3, self))

        if np.any(r):
            self[:3, :3] = r
        if np.any(s):
            self.addScaling(s)
        if t_id:
            self.id = t_id

    def isIdentity(self):
        """doc"""
        return np.allclose(np.identity(4, dtype=np.float64), self, atol=epsilon)

    def getInverse(self):
        """invert Transformation
        Rotation = R^transpose and Position = -R^transposed*p"""
        ret = Transformation()
        rT = self.rotation.T
        sT = self.scaling.getInverse()
        ret[:3, :3] = rT * sT
        ret[:3, 3] = (rT * self.translation) * -1
        return ret

    def __invert__(self):
        """invert Coordinatesystem
        Rotation = R^Transponiert und Position = -R^Transponiert*p"""
        self[:, :] = self.getInverse()

    def __mul__(self, other):
        """doc"""
        if other is None:
            raise ImproperParameterError("Got None for multiplication with transformation")

        otherOrg = other
        other = np.asarray(other)
        if other.shape == (3,):
            other = np.array([other[0], other[1], other[2], 1.0])
            cls = otherOrg.__class__
            if cls is np.ndarray:
                cls = np.array
            return cls((self @ other)[:3])

        elif other.shape == (4,):
            return np.array(self @ other)

        elif other.shape == (4, 4):
            return self @ other

        elif other.shape[0] == 3:
            # input is interpreted as array comprising of Translations
            other = np.insert(other, 3, 1, axis=0)
            return np.array(self @ other)[:3, :]

        elif other.shape[0] == 4:
            return np.array(np.dot(self, other))

        elif other.shape[1] == 3:
            other = np.insert(other, 3, 1, axis=1)
            other = np.transpose(other)
            return np.transpose(np.array(np.dot(self, other)))[:, :3]

        elif other.shape[1] == 4:
            other = np.transpose(other)
            return np.transpose(np.array(np.dot(self, other)))

        # elif other.shape[1] == 3:
        #    other = np.insert(other, 3, 1, axis=1)
        #    return np.array(self @ other.T).T[:,:3]

        # elif other.shape[1] == 4:
        #    return np.array(np.dot(self, other.T)).T
        else:
            raise ImproperParameterError(
                "only array sizes of 3, 4, 4x4, 3xn and 4xn are supported. Got instead: " + str(other.shape)
            )

    def __imul__(self, other):
        """doc"""
        return self * other

    def __eq__(self, other):
        """doc"""
        try:
            return np.allclose(self, other)
        except TypeError:
            return False

    def addTranslation(self, t):
        """doc"""
        if np.array(t).shape != (3,):
            log.error(
                'Could not set translation "%s". An iterable with 3 scalars or an object of type Translation is needed!'
                % t
            )
        self[:3, 3] += t[:]

    def addRotation(self, rot):
        """doc"""
        if np.array(rot).shape != (3, 3):
            raise ImproperParameterError(
                'Could not set rotation "%s". An iterable with 3x3 scalars or an object of type Rotation is needed!'
                % rot
            )
        self[:3, :3] = np.dot(self[:3, :3], rot)

    def addScaling(self, scal):
        """doc"""
        if np.array(scal).shape != (3, 3):
            raise ImproperParameterError(
                'Could not set scaling "%s". An iterable with 3x3 scalars or an object of type Scaling is needed!'
                % scal
            )
        self[:3, :3] = np.dot(self[:3, :3], scal)

    def setRotationByAxisAndAngle(self, axis, angle):
        """This method converts a rotation around a specified axis by a specified angle into rotation matrix.
        The mathematical algorithm can be found in [Wiki2013]_ and also in [Tayl2013]_.

        :param axis: instance of L{Translation}, specifying the rotational axis to be rotated about
        :param angle: float, variable specifying the rotating angle in degrees about the axis
                    .. note:: The angle is being transformed into radians.

        .. _[Wiki2013]: http://en.wikipedia.org/wiki/Rotation_matrix#cite_ref-2 (08.10.2013)
        .. _[Tayl1994] Taylor, Camillo; Kriegman (1994). "Minimization on the Lie Group SO(3) and Related Manifolds". Technical Report. No. 9405 (Yale University).
        """

        if np.array(axis).shape != (3,):
            log.error("Could not set rotation. An iterable with 3 scalars or an object of type Translation is needed!")

        if not (isinstance(angle, float) or isinstance(angle, int)):
            log.error("Could not set rotation. An angle in radiant of type float is needed!")

        angle *= np.pi / 180.0
        unitVector = axis / np.linalg.norm(axis)
        sinAngle, cosAngle = np.sin(angle), np.cos(angle)

        r = np.diag(cosAngle + unitVector[:3] ** 2 * (1.0 - cosAngle))

        r[0, 1] = unitVector[0] * unitVector[1] * (1.0 - cosAngle) - unitVector[2] * sinAngle
        r[1, 0] = unitVector[0] * unitVector[1] * (1.0 - cosAngle) + unitVector[2] * sinAngle

        r[0, 2] = unitVector[0] * unitVector[2] * (1.0 - cosAngle) + unitVector[1] * sinAngle
        r[2, 0] = unitVector[0] * unitVector[2] * (1.0 - cosAngle) - unitVector[1] * sinAngle

        r[1, 2] = unitVector[1] * unitVector[2] * (1.0 - cosAngle) - unitVector[0] * sinAngle
        r[2, 1] = unitVector[1] * unitVector[2] * (1.0 - cosAngle) + unitVector[0] * sinAngle

        self.rotation = r

    def getAxisAndAngleByRotation(self):
        """This method is intended to decompose the transformation instance into one rotation axis and a corresponding rotation angle.
        The mathematical algorithm can be found in [Wiki2013]_.

        :returns: tuple, containing the rotation axis as Translation and the rotation angle in radians

        .. _[Wiki2013]: http://en.wikipedia.org/wiki/Rotation_matrix#cite_ref-2 (08.10.2013)
        """

        def getAxis(rotationMatrix):

            rotMatEigenResult = np.linalg.eig(rotationMatrix)
            # ---FIND MATRIX EIGENVALUE EQUAL TO 1
            if not complex(1.0) in rotMatEigenResult[0]:
                raise InternalError("Result of eigenanalysis of rotation matrix contains no eigenvalue equal to 1.")
            else:
                for i in [0, 1, 2]:
                    if rotMatEigenResult[0][i] == complex(1.0):
                        eigenValueIndex = i

            # ---X-COORDINATE
            xReal = rotMatEigenResult[1][0][eigenValueIndex].real
            xImag = rotMatEigenResult[1][0][eigenValueIndex].imag
            if xImag > epsilon:
                raise InternalError("Rotation axis x-coordinate is complex.")

            yReal = rotMatEigenResult[1][1][eigenValueIndex].real
            yImag = rotMatEigenResult[1][1][eigenValueIndex].imag
            if yImag > epsilon:
                raise InternalError("Rotation axis y-coordinate is complex.")

            zReal = rotMatEigenResult[1][2][eigenValueIndex].real
            zImag = rotMatEigenResult[1][2][eigenValueIndex].imag
            if zImag > epsilon:
                raise InternalError("Rotation axis z-coordinate is complex.")

            return Translation([xReal, yReal, zReal])

        rotationMatrix = self.getRotation()
        # ---DETERMINE AXIS
        # the roation axis has to be an eigenvector of the rotation matrix
        # the axis is equivalent to the eigenvector belonging to the first eigenvalue of the matrix
        with warnings.catch_warnings():

            warnings.simplefilter("ignore")
            axis = getAxis(rotationMatrix)

        # ---DETERMINE ANGLE
        # ---RETRIEVE VECTOR PERPENDICULAR TO AXIS
        tmpPlane = Plane().generatePlane(positioningPoint=Translation([0.0, 0.0, 0.0]), planeNormalVector=axis)
        axisPerpendiculaVector = tmpPlane.planeOrientationVector1

        rotatedAxisPerpendiculaVector = rotationMatrix * axisPerpendiculaVector
        arcos = np.dot(axisPerpendiculaVector, rotatedAxisPerpendiculaVector)
        arcos = arcos / (np.linalg.norm(axisPerpendiculaVector) * np.linalg.norm(rotatedAxisPerpendiculaVector))

        return (axis, np.arccos(arcos))

    def estimateTransformationFromPointSets(self, fromPoints, toPoints):
        r"""
        This method is intended for superimposing arrays of 3D homogeneous coordinates.
        It calculates the Transformation representing the transformation of the fromPoints into
        the corresponding toPoints.

        :param fromPoints: list, containing at least three instances of Translation
        :param toPoints: list, containing at least three instances of Translation corresponding to the points within the list toPoints

        :returns: self, with translation, rotation and scaling set adequately


        :Author:
          `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`_

        :Editor:
          `Falk Heinecke 23.01.2014`

        :Organization:
          Laboratory for Fluorescence Dynamics, University of California, Irvine

        :Version: 2013.06.29

        Requirements
        ------------
        * `CPython 2.7 or 3.3 <http://www.python.org>`_
        * `Numpy 1.7 <http://www.numpy.org>`_
        * `Transformations.c 2013.01.18 <http://www.lfd.uci.edu/~gohlke/>`_
          (recommended for speedup of some functions)

        Return affine transform matrix to register two point sets.

        v0 and v1 are shape (ndims, \*) arrays of at least ndims non-homogeneous
        coordinates, where ndims is the dimensionality of the coordinate space.

        A rigid/Euclidean transformation matrix is returned.

        Similarity and Euclidean transformation matrices
        are calculated by minimizing the weighted sum of squared deviations
        (RMSD) according to the algorithm by Kabsch [8].

        Example:

        >>> v0 = [Translation([1., 0., 0.]), Translation([0., 1., 0.]), Translation([0., 0., 1.])]
        >>> v1 = [Translation([2., 0., 0.]), Translation([1., 1., 0.]), Translation([1., 0., 1.])]
        >>> tr = Transformation().estimateTransformationFromPointSets(v0, v1)
        >>> tr.round().astype(int)
        Transformation([[1, 0, 0, 1],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        """

        fromPoints = np.array(fromPoints, dtype=np.float64, copy=True)
        toPoints = np.array(toPoints, dtype=np.float64, copy=True)
        # points need to be stored as columns within the array
        fromPoints = np.transpose(fromPoints)
        toPoints = np.transpose(toPoints)

        ndims = fromPoints.shape[0]
        if ndims < 2 or fromPoints.shape[1] < ndims or fromPoints.shape != toPoints.shape:
            raise ValueError("input arrays are of wrong shape or type")

        # move centroids to origin
        t0 = -np.mean(fromPoints, axis=1)
        M0 = np.identity(ndims + 1)
        M0[:ndims, ndims] = t0
        fromPoints += t0.reshape(ndims, 1)
        t1 = -np.mean(toPoints, axis=1)
        M1 = np.identity(ndims + 1)
        M1[:ndims, ndims] = t1
        toPoints += t1.reshape(ndims, 1)

        # Rigid transformation via SVD of covariance matrix
        u, s, vh = np.linalg.svd(np.dot(toPoints, fromPoints.T))
        # rotation matrix from SVD orthonormal bases
        R = np.dot(u, vh)
        if np.linalg.det(R) < 0.0:
            # R does not constitute right handed system
            R -= np.outer(u[:, ndims - 1], vh[ndims - 1, :] * 2.0)
            s[-1] *= -1.0
        # homogeneous transformation matrix
        M = np.identity(ndims + 1)
        M[:ndims, :ndims] = R

        if 1:  # scale:
            # Affine transformation; scale is ratio of RMS deviations from centroid
            fromPoints *= fromPoints
            toPoints *= toPoints
            M[:ndims, :ndims] *= np.sqrt(np.sum(toPoints) / np.sum(fromPoints))

        # move centroids back
        M = np.dot(np.linalg.inv(M1), np.dot(M, M0))
        M /= M[ndims, ndims]

        self.rotation = M[:3, :3]
        self.translation = M[:3, 3]

        return self

    def mirror(self):
        """Method to create a new coordinate system object with mirroring the axis
        on the x-z plane."""
        transformation = Transformation(
            [
                [1, -1, 1, 1],
                [-1, 1, -1, -1],
                [1, -1, 1, 1],
                [0, 0, 0, 1],
            ]
        )

        return np.multiply(self.copy(), transformation)

    def _setTranslation(self, translation):
        """doc"""
        if not np.array(translation).shape == (3,):
            raise ImproperParameterError(
                'Could not set translation "%s".'
                + " An iterable with 3 scalars or an object of type Translation is needed!" % translation
            )
        self[:3, 3] = translation[:]

    def _getTranslation(self):
        """doc"""
        return np.array(self[:3, 3])

    def _setRotation(self, rot):
        """doc"""
        if not np.array(rot).shape == (3, 3):
            raise ImproperParameterError(
                'Could not set rotation "%s".'
                + " An iterable with 3x3 scalars or an object of type Rotation is needed!" % rot
            )
        self[:3, :3] = rot

    def _getRotation(self):
        """doc"""
        scaleFactors = 1.0 / np.outer(self.scaling.factors[:3], np.ones(3))
        return Rotation(np.multiply(self[:3, :3], scaleFactors))

    def _setScaling(self, scal):
        """doc"""
        if np.array(scal).shape != (3, 3):
            raise ImproperParameterError(
                'Could not set scaling "%s".'
                + " An iterable with 3x3 scalars or an object of type Scaling is needed!" % scal
            )
        self[:3, :3] = scal

    def _getScaling(self):
        """doc"""
        scaling = Scaling()
        scaling.factors = (np.linalg.norm(self[0, :3]), np.linalg.norm(self[1, :3]), np.linalg.norm(self[2, :3]))

        return scaling

    def getReflectedCoordinateSystem(self, reflectionType):
        """this routine reflects the respective coordinatesystem by the given reflection Type
        reflectionType "xAxis" generates a reflection about the x-axis
        reflect = [[1,0.,0.],
                   [0.,-1, 0.],
                   [0.,0.,1]]
        reflectionType "yAxis" generates a reflection about the y-axis
        reflect = [[-1,0.,0.],
                   [0.,1, 0.],
                   [0.,0.,1]]
        reflectionType "zAxis" generates a reflection about the z-axis
        reflect = [[1,0.,0.],
                   [0.,1, 0.],
                   [0.,0.,-1]]
        """

        idxToReflectedDict = {"xAxis": 1, "yAxis": 0, "zAxis": 2}
        if reflectionType in idxToReflectedDict.keys():
            reflect = np.identity(3, np.float64)
            idx = idxToReflectedDict[reflectionType]
            reflect[idx, idx] *= -1
        else:
            raise ImproperParameterError("the reflection Type is not correct: " + reflectionType)

        if not np.array(reflect).shape == (3, 3):
            log.error(
                'Could not set reflection "%s". An iterable with 3x3 scalars or an object of type Reflection is needed!'
                % reflect
            )
        self[:3, :3] = np.dot(self[:3, :3], reflect)
        self[:3, 3] = np.dot(self[:3, 3], reflect)

        return self

    translation = property(fset=_setTranslation, fget=_getTranslation)
    rotation = property(fset=_setRotation, fget=_getRotation)
    scaling = property(fset=_setScaling, fget=_getScaling)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
