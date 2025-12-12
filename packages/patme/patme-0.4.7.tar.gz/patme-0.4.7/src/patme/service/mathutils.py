# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Created on 16.06.2021

@author: schu_a1
"""
import numpy as np
from scipy.spatial import KDTree, cKDTree


def getUniqueListByThreshold(llist, threshold=1e-08):
    """doc"""
    newList = sorted(llist)
    removeIndexes = []
    elem = newList[0]
    for index, posX in enumerate(newList[1:]):
        if abs(posX - elem) < threshold:
            removeIndexes.append(index + 1)
        else:
            elem = posX

    for index in removeIndexes[::-1]:
        newList.pop(index)

    return newList


def cartprod(*arrays):
    """The method computes a cartesian product a multiple 1D-input arrays
    :param arrays: iterable of 1d-arrays
    :return: 2D array"""
    N = len(arrays)
    return np.transpose(np.meshgrid(*arrays, indexing="ij"), np.roll(np.arange(N + 1), -1)).reshape(-1, N)


def get2DSubArrayWithPregivenOrder(arr, columnValueOrder, columnNumber=0, returnMask=False):
    """
    The method creates an ordered 2D array with respect to a user defined order for a
    particular column of an input array. The value order do not need to contain all values
    from that column so that a reduced array can be returned.
    :param arr: 2D array
    :param columnValueOrder: Order
    :return: ordered 2D array
    """

    if columnNumber > arr.shape[1] - 1:
        raise Exception("Column number %s is greater than the number of columns for given array" % columnNumber)
    mask = np.in1d(arr[:, columnNumber], columnValueOrder)

    subArray = arr[mask]  # still 'unsorted'

    columnValueOrder = np.asarray(columnValueOrder)
    arr_is_sorted = (np.diff(arr[:, columnNumber]) == 1).all()
    query_ids_sorted = (np.diff(columnValueOrder) == 1).all()
    if arr_is_sorted and query_ids_sorted:
        ii = (columnValueOrder - int(arr[:, columnNumber][0])).astype(int)
    else:
        ii = None
        for treeImpl in [KDTree, cKDTree]:

            kdTree = treeImpl(subArray[:, columnNumber][:, np.newaxis])
            dd, ii = kdTree.query(columnValueOrder[:, np.newaxis])
            if np.all(np.isnan(dd)):
                ii = None
                continue
            else:
                break

        if ii is None:
            raise Exception("Unable to perform KDTree-based nearest neighbor search!")

    if returnMask:
        return subArray[ii], mask
    else:
        return subArray[ii]


def stack2DArrays(listWithArraysToStack, fillValue=0, use_dtype=np.float64):
    """This method stacks multiple 2D arrays to one complete array

    :param listWithArraysToStack: list with multiple 2D numpy arrays
    :param fillValue: Value which should be used when 2D input arrays are not all of the same
    column length so that entries are not set with values of the input array
    :param use_dtype: force numpy data type from use_dtype
    :return: stacked array"""
    numRows = sum(array.shape[0] for array in listWithArraysToStack)
    numCols = [array.shape[1] for array in listWithArraysToStack if len(array.shape) > 1]
    maxColumns = max(numCols, default=0)

    if numRows == 0 and maxColumns == 0:
        return np.array([])

    fullTable = np.empty((numRows, maxColumns), dtype=use_dtype)
    fullTable.fill(fillValue)
    i_min, i_max = 0, 0

    for table in listWithArraysToStack:

        if len(table.shape) < 2:
            continue

        i_max = i_min + table.shape[0]
        fullTable[i_min:i_max, : table.shape[1]] = table
        i_min = i_max

    return fullTable
