# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Provides functions for release automation
"""

import subprocess

from patme.service.logger import log


def hasTag(tagName, runDir="."):
    """Returns True if tagName is a tag in the loacal git"""
    output = subprocess.check_output(["git", "tag", "-l"], encoding="utf_8", cwd=runDir)
    return tagName in output


def gitTagAndPush(tagName):
    """create and push git tag"""
    if hasTag(tagName):
        log.error(f"Tag {tagName} already exists")
        return
    subprocess.call(["git", "tag", tagName])
    subprocess.call(["git", "push", "--tags"])
