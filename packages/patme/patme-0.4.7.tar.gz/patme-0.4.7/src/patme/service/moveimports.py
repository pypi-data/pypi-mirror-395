# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

r"""
Adapts the import statements if a package/module/moduleattribute is moved to another location

When something is moved to another location, many import statements may have to be modified.
With this package, the modifications can be automatically performed in a defined scope.
These are the actions performed:

- The files with matches are adapted accordingly.
  E.g the package/module/attribute "foobar" is moved to the new location "newpackage"::

    import oldpackage.foobar
    from oldpackage import foobar

    # is turned into

    import newpackage.foobar
    from newpackage import foobar

- An overview of the matches is printed
- This overview is also put in the file "movedImports.txt" in the sourcePaths

Usage::

    # define attributeName --> newPackage/Module
    changedVariablesDict = OrderedDict([('DelisSshError', 'patme.service.exceptions')])

    # run with source locations defined
    moveIt([r"C:\eclipse_projects\DELiS\src"], changedVariablesDict, False)

.. note::

    Does not work with imports spanning several lines
"""

import glob
import os
import re
from collections import OrderedDict

from patme.service.logger import log

# regex pattern strings that will be extended (at {}) with the newPackage and attribute names
patternStrings = [
    # import x.y
    r"""^                          # immediately after newline plus optional whitespaces
        (\ *?import\ (?!{}))       # optional whitespaces + import statement + exclude the match if the attribute is already in the new package
        (.*?)                      # preceding packages/module
        ({})                       # the actual variable
        (.*?)                      # as-statement, comments etc.
        $""",
    # from x import y
    r"""^                          # immediately after newline
        (\ *?from\ (?!{}))         # optional whitespaces + from statement + exclude the match if the attribute is already in the new package
        (.+?\ )                    # preceding packages/module
        (import\ )                 # import statement
        ({})                       # the actual variable
        (\ *?\#.*|\ ?as\ .*|\ *?)? # as-statement, comments etc.
        $""",
    # from x import y, z
    r"""^                          # immediately after newline
        (\ *?from\ (?!{}))         # optional whitespace + from statement + exclude the match if the attribute is already in the new package
        (.+?\ )                    # preceding packages/module
        (import\ )                 # import statement
        (.+?\ *)?                  # preceding imported variables
        (,\ *{}|{}\ *,\ *)         # the actual variable
        (.+?)?                     # following imported variables
        (\ *?\#.*)?                # comments etc
        $""",
    # from x.y import z
    r"""^                          # immediately after newline
        (\ *?from\ (?!{}))         # optional whitespaces + import statement + exclude the match if the attribute is already in the new package
        (.+?\.)                    # preceding packages/module
        ({})\                      # the actual variable
        (import\ .*)               # import statement and all the rest
        $""",
]

# regex replacement strings
replacements = [
    r"\g<1>{}\g<3>\g<4>",
    r"\g<1>{}\g<3>\g<4>\g<5>",
    r"\g<1>\g<2>\g<3>\g<4>\g<6>\g<7>\n\g<1>{}\g<3>{}",
    r"\g<1>{}\g<3> \g<4>",
]

replacementNewPackagePostfixes = [".", " ", " ", "."]


def moveIt(sourcePaths, changedVariablesDict, doTestrun=False, blacklist=None):
    """
    Main entry function of the module - see module description

    :param sourcePaths: list with paths to search for python files
    :param changedVariables: variable name --> new variable location
    :param doTestrun: Flag if no file should be changed.
                      Then only the matches are printed
    :param blacklist: List with packages after import/from statement that should be blacklisted.
                      E.g. in the following example if ``import logging as log`` should not be adapted,
                      the blacklist would be ['logging']::

                          import logging as log
                          from patme.service.logger import log
    """

    matchLines = []

    for sourcePath in sourcePaths:
        for ffile in glob.glob(os.path.join(sourcePath, "**", "*.py"), recursive=True):
            with open(ffile) as f:
                stream = f.read()
                matchLines += checkAndReplaceFile(stream, ffile, changedVariablesDict, doTestrun, blacklist)

    outFile = os.path.join(sourcePath, "movedImports.txt")
    if matchLines:
        msg = "\n".join([""] + matchLines)
    else:
        msg = "No matches found!"
    log.info(msg)
    with open(outFile, "w") as g:
        g.write(msg)


def checkAndReplaceFile(fileString, fileName, changedVariablesDict, doTestrun=False, blacklist=None):
    """check a file for matching lines and replace them accordingly

    :return: list with strings containing matching information"""

    fileString, matchLines = checkAndReplaceString(fileString, fileName, changedVariablesDict, blacklist)
    if not doTestrun:
        with open(fileName, "w") as g:
            g.write(fileString)

    return matchLines


def checkAndReplaceString(fileString, fileName, changedVariablesDict, blacklist=None):
    """check a string for matching lines and replace them accordingly

    :return: tuple (replacedFileString, matchLines)"""

    matchLines = []
    for variableName, newPackage in changedVariablesDict.items():
        if variableName == "":
            continue
        for patternStr, replacement, repPostfix in zip(patternStrings, replacements, replacementNewPackagePostfixes):
            pattern = _getPattern(patternStr, variableName, newPackage, blacklist)

            match = pattern.search(fileString)
            if match:
                # documentation
                matchLines += ["#########################", fileName]
                for allMatches in pattern.findall(fileString):
                    matchLines.append("".join(allMatches))

                # replacement
                replacementStr = _getReplacement(replacement, newPackage, repPostfix, variableName)
                fileString = pattern.sub(replacementStr, fileString)
    return fileString, matchLines


def _getPattern(patternString, variableName, newPackage, blacklist=None):
    """create a regex pattern including the variable and new package name"""
    if blacklist is None:
        blacklist = newPackage
    else:
        blacklist = "|".join([newPackage] + blacklist)
    patternString = patternString.format(blacklist, variableName, variableName)
    pattern = re.compile(patternString, re.RegexFlag.MULTILINE + re.RegexFlag.VERBOSE)
    return pattern


def _getReplacement(replacement, newPackage, replacementPostfix, variableName=None):
    """create a regex replacement string including the variable and new package name"""
    if newPackage[-1] != replacementPostfix:
        newPackage += replacementPostfix
    return replacement.format(newPackage, variableName)


def stringMatchesPatterns(inputStr, variableName, newPackage, blacklist=None):
    """check if a given string matches the patterns defined"""
    matches = []
    for patternStr, _, _ in zip(patternStrings, replacements, replacementNewPackagePostfixes):
        pattern = _getPattern(patternStr, variableName, newPackage, blacklist)

        matches.append(pattern.search(inputStr))

    return any(matches)


if __name__ == "__main__":
    if 0:
        # test single lines
        res = stringMatchesPatterns(
            "from delismm.service.utilities import log", "log", "patme.service.logger", ["logging"]
        )
        print(res)
    else:
        # test and modify imports
        changeVar = OrderedDict(
            [
                ("copyClusterFilesSFTP", "patme.sshtools.facluster"),
                ("", ""),
            ]
        )
        sourcePaths = [
            r"C:\PycharmProjects\DELiS\src",
            r"C:\PycharmProjects\DELiS\test",
            r"C:\PycharmProjects\delismm\src",
            r"C:\PycharmProjects\delismm\test",
            r"C:\eclipse_projects\andecs\src",
            r"C:\eclipse_projects\andecs\test",
        ]
        moveIt(sourcePaths, changeVar, False)
