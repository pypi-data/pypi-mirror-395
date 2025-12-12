# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Functions for string formatting.
"""
import functools
import io
import itertools
import logging
import math
import re
import sys

import numpy as np

try:
    from tqdm import tqdm

    HAS_TQDM = True
except:
    HAS_TQDM = False


class ProgressBar:
    """This class produces a progress bar in the console that also works in the eclipse console.
    It is intended for iterated procedures where each iteration step takes almost the
    same time. Every call to ``ProgressBar.append`` appends one progress item
    in the progress bar.

    .. note::
            The progress bar does not work if you do other prints during filling the progress bar

    Example::

        pb = ProgressBar(50)
        for i in range(50): pb.append()
        pb.end()

    Result::

         [                         ]
          #########################

    """

    def __init__(self, numberOfItems, logLevel=logging.INFO, baseLogger=None):
        """initializes a progress bar

        :param numberOfItems: number of items that are iterated"""
        # spaces in front of progress bar at each line
        self.preSpaces = "                                 "

        if not HAS_TQDM:

            # the progress bar should be 80 elements thick at maximum
            self.maxLength = 80 - len(self.preSpaces)
            self.count = 0
            self.printEveryXItem = int(numberOfItems) // self.maxLength + 1
            self.logLevel = logLevel
            self.baseLogger = baseLogger

            if not self.isBlocked:
                itemsToInsert = " " * (numberOfItems // self.printEveryXItem)
                sys.stdout.write(f"{self.preSpaces}[{itemsToInsert}]\n {self.preSpaces}")
                sys.stdout.flush()

        else:
            self._tqdm = tqdm(
                desc=self.preSpaces, total=numberOfItems, bar_format="{desc}{percentage:3.0f}%|{bar:30}| Total: {total}"
            )

    def append(self):
        """doc"""
        if not HAS_TQDM:
            if not self.isBlocked:
                if self.count % self.printEveryXItem == 0:
                    sys.stdout.write("#")
                    sys.stdout.flush()
                self.count += 1
        else:
            self._tqdm.update()

    def end(self):
        """doc"""
        if not HAS_TQDM:
            if not self.isBlocked:
                sys.stdout.write("\n")
                sys.stdout.flush()
        else:
            self._tqdm.close()

    def _isBlocked(self):
        """doc"""
        if (self.baseLogger is None) or not hasattr(self.baseLogger, "logLevel"):
            return False
        else:
            return self.logLevel < self.baseLogger.logLevel

    isBlocked = property(fget=_isBlocked)


def breakStringIntoMultlineString(
    fullString, intendationLengthLeft=0, setContinuationChar=False, maximumLineLength=72, pattern="[,]"
):
    """
    Formats a string to match a given maximum line length. Furthermore, all newlines
    starts with an intendation if specified.(Necessary for several NASTRAN cards)

    :param fullString: String to be splitted
    :param intendationLengthLeft: Intendation length for new lines (beginning at the second line for long string)
    :param setContinuationChar: Flag if continuation character should be added when new line is needed
           (may be used in Nastran)
    :param pattern: Regular expression with all possible characters to search
           within the 'fullString' where the string can be splitted. Please refer to the documentation
           of the python 're' library
    :return: formatted multiline string that matches maximum line length
    """
    firstRowOffset = intendationLengthLeft
    if setContinuationChar:
        breakStr = "+\n%s+" % (" " * intendationLengthLeft)
    else:
        breakStr = "\n%s" % (" " * intendationLengthLeft)

    formattedString = ""
    while len(fullString) > maximumLineLength:
        lineLength = maximumLineLength - firstRowOffset
        indexes = [m.start() for m in re.finditer(pattern, fullString) if m.start() < lineLength]
        if indexes:
            nearestIx = max(indexes)
        else:
            nearestIx = next(m.start() for m in re.finditer(pattern, fullString) if m.start() > lineLength)

        formattedString += fullString[: nearestIx + 1] + breakStr
        fullString = fullString[nearestIx + 1 :]

        firstRowOffset = 0

    # add remaining substring which fits into the last line
    formattedString += fullString
    return formattedString


def createRstTable(inputMatrix, numberOfHeaderLines=1):
    """Returns a string containing a well formatted table that can be used in rst-documentation.

    :param inputMatrix: A sequence of sequences of items, one sequence per row.
    :param numberOfHeaderLines: number of lines that are used as header. the header is printed bold.
    :return: string containing well formatted rst table

    Example::

        >>> from patme.service.stringutils import createRstTable
        >>> a=[]
        >>> a.append(['','major','minor','revision'])
        >>> a.append(['Example','13','2','0'])
        >>> a.append([  'Explanation','New feature, incompatibe to prev versions','New feature, compatible to prev versions','Patch/Bugfix'])
        >>> print(createRstTable(a))
        +-------------+-------------------------------------------+------------------------------------------+--------------+
        |             | major                                     | minor                                    | revision     |
        +=============+===========================================+==========================================+==============+
        | Example     | 13                                        | 2                                        | 0            |
        +-------------+-------------------------------------------+------------------------------------------+--------------+
        | Explanation | New feature, incompatibe to prev versions | New feature, compatible to prev versions | Patch/Bugfix |
        +-------------+-------------------------------------------+------------------------------------------+--------------+
    """
    tableString = indent(inputMatrix, separateRows=True, hasHeader=True, headerChar="-", prefix="| ", postfix=" |")
    tableLines = tableString.splitlines()
    # get second row to extract the position of '|'
    pipePositions = []
    line = tableLines[1]
    for index, character in enumerate(line):
        if character == "|":
            pipePositions.append(index)

    # alter tableLines containing text
    for halfLineNumber, line in enumerate(tableLines[::2]):
        for index in pipePositions:
            line = line[:index] + "+" + line[index + 1 :]
        tableLines[halfLineNumber * 2] = line

    tableLines[2 * numberOfHeaderLines] = tableLines[2 * numberOfHeaderLines].replace("-", "=")
    return "\n".join(tableLines)


def indentDataFrame(df, *args, **kwargs):
    """Indents a pandas data frame. All other parameters can be seen in indent()"""
    outList = [list(df)] + df.values.tolist()
    dfIndex = [""] + df.index.tolist()
    outList = [[indexItem] + line for indexItem, line in zip(dfIndex, outList)]
    return indent(outList, *args, **kwargs)


def indent(
    rows,
    hasHeader=False,
    headerChar="-",
    delim=" | ",
    justify="left",
    separateRows=False,
    prefix="",
    postfix="",
    wrapfunc=lambda x: wrap_npstr(x),
    header=None,
    colHeader=None,
):  # lambda x:x):
    """
    Indents a table by column.

    :param rows: A sequence of sequences of items, one sequence per row.

    :param hasHeader: True if the first row consists of the columns' names.

    :param headerChar: Character to be used for the row separator line
      (if hasHeader==True or separateRows==True).

    :param delim: The column delimiter.

    :param justify: Determines how are data justified in their column.
      Valid values are 'left','right' and 'center'.

    :param separateRows: True if rows are to be separated by astr
     line of 'headerChar's.

    :param prefix: A string prepended to each printed row.

    :param postfix: A string appended to each printed row.

    :param wrapfunc: A function f(text) for wrapping text; each element in
      the table is first wrapped by this function.

    :param header: header for a table. Will be inserted before rows

    :param colHeader: column header for a table. Will be inserted before rows

    remark:

    :Author: George Sakkis
    :Source: http://code.activestate.com/recipes/267662/
    :License: MIT (http://code.activestate.com/help/terms/)
    """

    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [str(wrapfunc(item)).split("\n") for item in row]
        return [[substr or "" for substr in item] for item in map(lambda *x: x, *newRows)]

    if header is not None:
        hasHeader = True
        rows = [header] + [row for row in rows]

    if colHeader is not None:
        if header is not None:
            colHeader = [""] + list(colHeader)
        rows = [[colHead, headerChar] + list(row) for colHead, row in zip(colHeader, rows)]

    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = list(itertools.zip_longest(*(row[0] for row in logicalRows)))
    # get the maximum of each column by the string length of its items
    maxWidths = [max(len(str(item)) for item in column) for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + len(delim) * (len(maxWidths) - 1))
    # select the appropriate justify method
    justify = {"center": str.center, "right": str.rjust, "left": str.ljust}[justify.lower()]
    output = io.StringIO()
    if separateRows:
        print(rowSeparator, file=output)
    for physicalRows in logicalRows:
        for row in physicalRows:
            outRow = prefix + delim.join([justify(str(item), width) for (item, width) in zip(row, maxWidths)]) + postfix
            print(outRow, file=output)
        if separateRows or hasHeader:
            print(rowSeparator, file=output)
            hasHeader = False
    return output.getvalue()


# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061


def wrap_npstr(text):
    """A function to distinguisch between np-arrays and others.
    np-arrays are returned as string without newline symbols that are usually returned by np.ndarray.__str__()
    """
    if isinstance(text, np.ndarray):
        text = str(text).replace("\n", "").replace("   ", ", ").replace("  -", ", -")
    return text


def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return functools.reduce(
        lambda line, word, width=width: "%s%s%s"
        % (line, " \n"[(len(line[line.rfind("\n") + 1 :]) + len(word.split("\n", 1)[0]) >= width)], word),
        text.split(" "),
    )


def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
    words longer than width are split."""
    wordRegex = re.compile(r"\S{" + str(width) + r",}")
    return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(), width), text), width)


def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
    It doesn't split the text in words."""
    return "\n".join([text[width * i : width * (i + 1)] for i in range(int(math.ceil(1.0 * len(text) / width)))])


def printMatrix(matrix):
    '''Prints a 2D array with space as separator

    :return: string with matrix entries separated by " "'''
    return indent(matrix, delim="  ", prefix="|", postfix="|")


if __name__ == "__main__":

    import doctest

    doctest.testmod()

    if 0:
        labels = ["First Name", "Last Name", "Age", "Position"]
        data = """John,Smith,24,Software Engineer
               Mary,Brohowski,23,Sales Manager
               Aristidis,Papageorgopoulos,28,Senior Reseacher"""
        rows = [row.strip().split(",") for row in data.splitlines()]

        print("Without wrapping function\n")
        print(indent([labels] + rows, hasHeader=True))
        # test indent with different wrapping functions
        width = 10
        for wrapper in (wrap_always, wrap_onspace, wrap_onspace_strict):
            print("Wrapping function: %s(x,width=%d)\n" % (wrapper.__name__, width))
            print(
                indent(
                    [labels] + rows,
                    hasHeader=True,
                    separateRows=True,
                    prefix="| ",
                    postfix=" |",
                    wrapfunc=lambda x: wrapper(x, width),
                )
            )

        # output:
        #
        # Without wrapping function
        #
        # First Name | Last Name        | Age | Position
        # -------------------------------------------------------
        # John       | Smith            | 24  | Software Engineer
        # Mary       | Brohowski        | 23  | Sales Manager
        # Aristidis  | Papageorgopoulos | 28  | Senior Reseacher
        #
        # Wrapping function: wrap_always(x,width=10)
        #
        # ----------------------------------------------
        # | First Name | Last Name  | Age | Position   |
        # ----------------------------------------------
        # | John       | Smith      | 24  | Software E |
        # |            |            |     | ngineer    |
        # ----------------------------------------------
        # | Mary       | Brohowski  | 23  | Sales Mana |
        # |            |            |     | ger        |
        # ----------------------------------------------
        # | Aristidis  | Papageorgo | 28  | Senior Res |
        # |            | poulos     |     | eacher     |
        # ----------------------------------------------
        #
        # Wrapping function: wrap_onspace(x,width=10)
        #
        # ---------------------------------------------------
        # | First Name | Last Name        | Age | Position  |
        # ---------------------------------------------------
        # | John       | Smith            | 24  | Software  |
        # |            |                  |     | Engineer  |
        # ---------------------------------------------------
        # | Mary       | Brohowski        | 23  | Sales     |
        # |            |                  |     | Manager   |
        # ---------------------------------------------------
        # | Aristidis  | Papageorgopoulos | 28  | Senior    |
        # |            |                  |     | Reseacher |
        # ---------------------------------------------------
        #
        # Wrapping function: wrap_onspace_strict(x,width=10)
        #
        # ---------------------------------------------
        # | First Name | Last Name  | Age | Position  |
        # ---------------------------------------------
        # | John       | Smith      | 24  | Software  |
        # |            |            |     | Engineer  |
        # ---------------------------------------------
        # | Mary       | Brohowski  | 23  | Sales     |
        # |            |            |     | Manager   |
        # ---------------------------------------------
        # | Aristidis  | Papageorgo | 28  | Senior    |
        # |            | poulos     |     | Reseacher |

        a = [
            ["", "BC for Design", "BC for testing"],
            ["Beos 4", -77879, -37020],
            ["Beos 5", -134117, -84489],
            ["Abaqus Linear", "", ""],
            ["Abaqus NonLinear", "", ""],
            ["Test result", "", -100000],
        ]
        print(createRstTable(a))
