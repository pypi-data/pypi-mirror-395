# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Utilities on system level.
"""
import os
import re
import shutil
import subprocess
import tarfile
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime

from patme.service.logger import log, resetLoggerToNewRunDir


def dos2unix(filename):
    """doc"""
    with open(filename, "rb") as f:
        stream = f.read()

    stream = stream.decode().replace("\r\n", "\n")
    with open(filename, "wb") as f:
        f.write(stream.encode())


def searchForWordsWithinFile(filename=None, words=None):
    """doc"""
    if not filename:
        filename = ""

    if isinstance(words, list):
        words = re.compile("(%s)" % "|".join(words), re.RegexFlag.MULTILINE)

    if os.path.exists(filename):
        with open(filename, "rb") as f:
            wordMatches = words.finditer(f.read().decode(errors="replace"))
            if wordMatches:
                return [match.group() for match in wordMatches]
        return None
    else:
        log.error('Filename "%s" not found.' % filename)
        return None


def checkForLibraryInPaths(library, pathsToCheck):
    """Checks if library is found in any of the path set in global PATH variable.
    If the library is found the base directory is returned"""
    for path in pathsToCheck:
        if os.path.isdir(path) and os.path.exists(path) and library in os.listdir(path):
            return path

    return None


@contextmanager
def changeDirTemporary(newDir):
    """Method to change the directory temporarily to do some things and change back to the original directory
    after some things are done.
    Example:

    >>> import os
    >>> currentDir = os.getcwd()
    >>> with changeDirTemporary(os.path.join(currentDir, '..')): changedDir = os.getcwd()
    >>> currentDirNew = os.getcwd()
    >>> currentDir == currentDirNew
    True
    >>> currentDir != changedDir
    True
    >>> #print(currentDir,changedDir,currentDirNew)
    >>> with changeDirTemporary(None): changedDir = os.getcwd()
    >>> currentDirNew = os.getcwd()
    >>> currentDir == currentDirNew
    True
    >>> currentDir == changedDir
    True
    >>> #print(currentDir,changedDir,currentDirNew)

    """
    if newDir is None:
        yield
        return
    tmpDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(tmpDir)


def getTimeString(useMilliSeconds=False):
    """returns a time string of the format: yyyymmdd_hhmmss"""
    dt = datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S") + (f"_{dt.microsecond}" if useMilliSeconds else "")


def makeAllDirs(directory):
    absPath = os.path.abspath(directory)
    for i in range(0, absPath.count(os.sep))[::-1]:
        # Split path into subpaths beginning from the top of the drive
        subPath = absPath.rsplit(os.sep, i)[0]
        if not os.path.exists(subPath):
            os.makedirs(subPath)


def getRunDir(baseName="tmp", runDirExtension="", moveLogFilesToRunDir=True, basePath=".", useMilliSeconds=False):
    """Creates a folder that will be used as directory for the actual run.

    The created folder has this name::

        basePath/<baseName>_<timestamp><runDirExtension>

    :param runDirExtension: optional string appended to the folder name. Defaults to ''
    :param moveLogFilesToRunDir: Flag if the log files should be put in this directory.
    :param basePath: working directory where folder shall be created.
    :param useMilliSeconds: include milliseconds to the run dir name or not
    :returns: absolute path to the new folder

    Example::

        >> getRunDir('foo', '_bar', False, False, 'foobar')
        foobar/foo_20170206_152323_bar

    """
    while True:
        runDir = os.path.join(basePath, baseName + "_" + getTimeString(useMilliSeconds)) + runDirExtension
        if os.path.exists(runDir):
            log.warning("runDir already exists. Wait 1s and retry with new timestring.")
            time.sleep(1)
        else:
            makeAllDirs(runDir)
            break

    if moveLogFilesToRunDir:
        resetLoggerToNewRunDir(runDir)

    return runDir


def getGitInformation(wcDirectory=None):
    """Return information of the state of this git repository if it is present.

    :param wcDirectory: main directory of the git clone
    :return: tuple (description of the actual version and commit, has local modifications)
        describe is either something like "0.2.0" if the tag-commit is active or
        "0.1.1-31-g23a6851" describing
        0.1.1:      last tag name
        31:         number of commits since this tag
        23a6851:    actual commit
    """
    gitBin = shutil.which("git")
    if gitBin is None:
        return ("No git binary found", "No git binary found")

    with changeDirTemporary(wcDirectory):
        p = subprocess.run(
            [gitBin, "describe", "--tags"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # use text=True for python >= 3.7

        describe = p.stderr if p.stdout == b"" else p.stdout
        describe = describe.decode("utf-8").strip()

        p = subprocess.run(
            [gitBin, "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # use text=True for python >= 3.7

        status = p.stderr if p.stdout == b"" else p.stdout
        status = status.decode("utf-8").strip()

    if "not a git repository" in describe:
        return ("not a git repository", "not a git repository")
    hasLocalModifications = "Changes to be committed" in status or "Changes not staged for commit" in status
    return describe, hasLocalModifications


def getFormattedTimeStampForFile(ffile):
    return int(datetime.fromtimestamp(os.path.getmtime(ffile)).strftime("%Y%m%d%H%M"))


def compressFilesInDir(
    direc, regEx, zipFilename=None, thresholdMB=0, olderThan=0, removeOrigFiles=False, autoCRCCheck=True
):
    """Compresses files in a given directory with a given minimal file size and a modification time.

    The resulting file archive is a general zip file.

    :param direc: Directory where several files should be compressed
    :param regEx: Regular expression which the filenames should match to compress
    :param zipFilename: Filename of the Zip-file to store files. If it is None, all matching files in a directory.
        will be compressed as seperate files with the original filename and the new .zip ending
    :param thresholdMB: Minimum file size in megabytes for compression to exclude very small files.
    :param olderThan: Timestamp (Format '%Y%m%d%H%M') to exclude files from compression which are generated in the shorter past.
        Timestamp can be helpful to avoid compressing files which may be needed again in a long term process.
    :param removeOrigFiles: Flag if original files should be deleted if they were compressed successfully
    :param autoCRCCheck: Flag if created zip files should be checked by CRC algorithm

    """

    direc = os.path.abspath(direc)
    p = re.compile(regEx)
    thresholdBytes = int(thresholdMB * 1024**2)

    for root, __, files in os.walk(direc, topdown=True):
        compressDict = {}
        for name in files:
            filenameWithRoot = os.path.join(root, name)
            getLastModifiedTime = getFormattedTimeStampForFile(filenameWithRoot)

            if int(olderThan) > 0 and getLastModifiedTime > int(olderThan):
                continue

            if p.match(name) and os.stat(filenameWithRoot).st_size > thresholdBytes:
                if not zipFilename:
                    newZiPFile = os.path.join(root, name + ".zip")
                else:
                    newZiPFile = os.path.join(root, zipFilename)

                with zipfile.ZipFile(newZiPFile, "a", zipfile.ZIP_DEFLATED, allowZip64=True) as myzip:
                    myzip.write(filenameWithRoot, name)

                if compressDict.get(newZiPFile, None):
                    compressDict[newZiPFile].append(filenameWithRoot)
                else:
                    compressDict[newZiPFile] = [filenameWithRoot]

        if autoCRCCheck:
            for zFile, cFiles in list(compressDict.items()):
                with zipfile.ZipFile(zFile, "r", allowZip64=True) as myzip:
                    if myzip.testzip():
                        print("Something went wrong with zip file creation: ", zFile)
                        raise
                    elif removeOrigFiles:
                        for ffile in cFiles:
                            os.remove(ffile)


def tarGzDirectory(directory, tarFileName):
    """put a directory in a targz"""
    if not os.path.isabs(tarFileName):
        tarFileName = os.path.join(directory, tarFileName)
    directory = os.path.abspath(directory)
    if os.path.exists(tarFileName):
        os.remove(tarFileName)

    with tarfile.open(tarFileName, "x:gz") as tarFileDescriptor:
        for fileOrDir in os.listdir(directory):
            tarFileDescriptor.add(os.path.join(directory, fileOrDir), arcname=fileOrDir)

    return tarFileName


def zipDirectory(directory, zipFileName):
    """Puts all files in the given directory to a zip file in the same dir

    Attention: Extracting of empty (sub)directories does not work with python's zipfile module

    :param directory: directory that will be zipped
    :param zipFileName: name of the zip file that is created. If it as an abs path, then it is
        used directly. If it has a relative path, it is used relative to directory.
    """
    if not os.path.isabs(zipFileName):
        zipFileName = os.path.join(directory, zipFileName)
    directory = os.path.abspath(directory)
    if os.path.exists(zipFileName):
        os.remove(zipFileName)
    with zipfile.ZipFile(zipFileName, "x") as zipFileDescriptor:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file != os.path.basename(zipFileName):
                    fullFileName = os.path.join(root, file)
                    fileInZipName = os.path.join(os.path.relpath(root, directory), file)
                    zipFileDescriptor.write(fullFileName, fileInZipName)
            for directory in dirs:  # add folder in order to also have empty folders added
                with changeDirTemporary(root):
                    zif = zipfile.ZipInfo(os.path.join(directory))
                    zif.external_attr = 16
                    zipFileDescriptor.writestr(zif, "")


if __name__ == "__main__":
    pass
    # print(getRunDir('foo', '_bar', False, False, 'foobar'))
#     directory = 'D:\\freu_se\\DELiS\\tmp\\delis_20170206_143544_functionCreator\\abq_abq'
#     tarFileName = 'a.tar.gz'
#     if os.path.exists(os.path.join(directory, tarFileName)):
#         os.remove(os.path.join(directory, tarFileName))
#     tarGzDirectory(directory, tarFileName)
