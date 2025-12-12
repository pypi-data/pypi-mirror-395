# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Custom exceptions in order to specialize exception names and to catch tool-specific exceptions only.
"""


class CustomException(Exception):
    """This class defines and abstract exception class so that customized exceptions
    can be inherited."""

    def __init__(self, value):
        """doc"""
        self.value = value

    def __str__(self):
        """Returning the error message"""
        return repr(self.value)


class InternalError(CustomException):
    """classdocs"""


class ImproperParameterError(CustomException):
    """classdocs"""


class DelisSshError(CustomException):
    """classdocs"""


class GeometryError(CustomException):
    """classdocs"""
