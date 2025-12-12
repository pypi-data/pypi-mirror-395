# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""Create RCE components and publish them on an rce toolserver.

This script is meant for the deployment of tools in various versions and configuration variants.
To create all inputs to the main function, one must create one tool configuration using the rce- "integrate tool" wizard first.
Then, extract all neccessary information (toolInput, toolOutput, preScript, postScript, runCmd) from the configuration file.

Perform the following

- Create documentation pdf
- Clone the respective git tag
- Create the RCE-Component:
    - Create the configuration folder, file and documentation
    - Upload configuration to the toolserver (using file shares)
    - Publish the component in RCE to "public"

Prerequisites and restrictions:

- The RCE-toolserver must be accessible via ssh
- The Configuration (in the rc-profile dir) of the RCE-toolserver must be accessible via file share
- Only "common" components creatable - no "cpacs" components
- In the folder "toolDirToolserver" (parameter of releaseCreatorMain), there should be a subdirectory called "programName"
  for the nightly version. This folder must be created by the user when createNightly=True.
  In "toolDirToolserver", tag folders will be created using "versionString" as folder name.
"""

import os
import shutil
import subprocess
import sys

from patme.buildtools.release import hasTag
from patme.service.exceptions import ImproperParameterError
from patme.service.logger import log
from patme.sshtools.sshcall import callSSH


def releaseCreatorMain(
    # program settings
    versionString,
    programDir,
    programName,
    gitRepo,
    iconPath,
    description,
    # rce tool settings
    runCmd,
    preScript,
    postScript,
    rceInputs,
    rceOutputs,
    toolProperties,
    # doc settings
    docCommand,
    docResultPdfPath,
    # remote settings
    username,
    privateKeyFile,
    hostnameRce10,
    hostKeyStringRce10,
    portRce10,
    toolDirToolserver,
    toolDirToolserverRemote,
    configDirToolserver,
    # run behavior
    createDoc=True,
    cloneTag=True,
    createRceConfig=True,
    createNightly=False,
):
    """Main function for creating the whole configuration

    :param versionString: version
    :param programDir: directory of the local program
    :param programName: name of the program
    :param gitRepo: https address of git repository
    :param icoPath: name and path (relative to programDir) to the programs icon. May be None
    :param description: description of the program

    :param runCmd: command to run the tool on the rce toolserver
    :param preScript: pre command on rce toolserver
    :param postScript: post command on rce toolserver
    :param rceInputs: inputs of the rce component
    :param rceOutputs: outputs of the rce component
    :param toolProperties: string, section toolProperties in rce configuration

    :param docCommand: setup.py command to create doc
    :param docResultPdfPath: name and path (relative to programDir) with the created pdf file. If None, no documentation will be included.

    :param username: username to login to rce using ssh
    :param privateKeyFile: path to the private key for ssh access
    :param hostnameRce10: hostname of the computer running the toolserver
    :param hostKeyStringRce10: ssh host key for authentication
    :param portRce10: port of the rce server
    :param toolDirToolserver: local path to tool on toolserver.
    :param toolDirToolserverRemote: remote path to tool on toolserver
    :param configDirToolserver: tool directory on toolserver (local path to remote machine)

    :param createDoc: flag if the documentation should be created. Otherwise, the documentaion must be created manually.
    :param cloneTag: flag if the tag folder should be created. Otherwise the folder must be created manually.
    :param createRceConfig: flag if the rce configuration folder/file should be created
    :param createNightly: flag if the nightly configuration should be created. Has only effect, if createRceConfig=True
    """
    if not hasTag(versionString, programDir):
        raise ImproperParameterError(f'There is no tag "{versionString}" in {programName} in folder {programDir}')

    connectInfo = (username, privateKeyFile, hostnameRce10, hostKeyStringRce10, portRce10)
    rceInfo = description, runCmd, preScript, postScript, rceInputs, rceOutputs, docResultPdfPath, toolProperties

    # ===============================================================================================
    # create documentation
    # ===============================================================================================
    if createDoc:
        log.infoHeadline("Making documentation")
        subprocess.call([sys.executable, "setup.py", docCommand], cwd=programDir)

    # ===========================================================================
    # create a clone of the tag on the toolserver
    # ===========================================================================
    tagPath = os.path.join(toolDirToolserverRemote, versionString)
    if cloneTag:
        if os.path.exists(tagPath):
            log.info(f"Not performing git clone: tag already exists at: {tagPath}")
        else:
            os.makedirs(tagPath)
            gitBin = shutil.which("git")
            cloneCmd = [gitBin, "clone", "--depth", "1", "--branch", versionString, gitRepo, tagPath]
            subprocess.run(cloneCmd, stdout=sys.stdout)

    # ===========================================================================
    # rce tool configuration
    # ===========================================================================
    if createRceConfig:
        createToolConfigurations(
            toolDirToolserver,
            versionString,
            programName,
            programDir,
            connectInfo,
            configDirToolserver,
            iconPath,
            rceInfo,
            createNightly,
        )


def createToolConfigurations(
    toolDirToolserver,
    versionString,
    programName,
    programDir,
    connectInfo,
    configDirToolserver,
    iconPath,
    rceInfo,
    createNightly,
    rceVersion="rce10",
):
    """Creates the configuration files for RCE"""
    if rceVersion == "rce10":
        createToolConfiguration = createRCE10ToolConfiguration
    else:
        raise Exception(f'RCE version "{rceVersion}" not supported')

    toolDir = os.path.join(toolDirToolserver, versionString).replace(
        "\\", "\\\\"
    )  # using 4backslashes since it is parsed by python 2 times
    createToolConfiguration(
        versionString, programName, programDir, toolDir, connectInfo, configDirToolserver, iconPath, rceInfo
    )

    if createNightly:
        toolDir = os.path.join(toolDirToolserver, programName).replace("\\", "\\\\")
        createToolConfiguration(
            "nightly", programName, programDir, toolDir, connectInfo, configDirToolserver, iconPath, rceInfo
        )


def createRCE10ToolConfiguration(
    versionString, programName, programDir, toolDir, connectInfo, configDirToolserver, iconPath, rceInfo
):
    """Create the RCE8 configuration folder and all necessary files"""

    username, privateKeyFile, hostnameRce10, hostKeyStringRce10, portRce10 = connectInfo
    # create configuration dir
    versionName = programName + "_" + versionString  # e.g. results in str: DELiS_14.7.2
    rceConfigToolserver = os.path.join(configDirToolserver, versionName)
    log.info(f"Create rce tool configurations in folder {rceConfigToolserver}")
    if not os.path.exists(os.path.join(rceConfigToolserver, "docs")):
        os.makedirs(os.path.join(rceConfigToolserver, "docs"))

    # ===========================================================================
    # create conf dir, write conf
    # ===========================================================================
    docResultPdfPath = rceInfo[-2]
    if docResultPdfPath is not None:
        docFile = os.path.join(programDir, docResultPdfPath)
        if os.path.exists(docFile):
            shutil.copy2(docFile, os.path.join(rceConfigToolserver, "docs"))
        else:
            log.warning("The documentation pdf is not existing: " + docFile)
            docResultPdfPath = ""
    else:
        docResultPdfPath = ""
    shutil.copy2(os.path.join(programDir, iconPath), rceConfigToolserver)
    # write Config
    configString = getRCE10ConfigString(versionName, versionString, toolDir, os.path.basename(iconPath), rceInfo)
    with open(rceConfigToolserver + "/configuration.json", "w") as f:
        f.write(configString)

    # ===========================================================================
    # publish RCE component
    # ===========================================================================
    log.info(f"publish RCE component {versionName}")
    remoteCommand = f"components set-auth common/{versionName} public"
    output = callSSH(hostnameRce10, remoteCommand, privateKeyFile, username, hostKeyStringRce10, port=portRce10)
    if not "Set access authorization for component id" in output:
        log.error("Publish component failed")


def getRCE10ConfigString(versionName, versionString, toolDir, iconFilename, rceInfo):
    description, runCmd, preScript, postScript, rceInputs, rceOutputs, docResultPdfPath, toolProperties = rceInfo

    return (
        '''{
  "commandScriptLinux" : "",
  "commandScriptWindows" : "'''
        + runCmd
        + '''",
  "copyToolBehavior" : "never",
  "deleteWorkingDirectoriesNever" : true,
  "documentationFilePath" : "'''
        + os.path.basename(docResultPdfPath)
        + """",
  "enableCommandScriptWindows" : true,
  "groupName" : "DLR-FA",
  "iconHash" : "bbca83a88b19e9c05524ec3f5df1553b",
  "iconModified" : 1482484234043,
  "imitationScript" : "",
  "imitationToolOutputFilename" : "",
  "inputs" : [ """
        + rceInputs
        + """ ],
  "isActive" : true,
  "launchSettings" : [ {
    "limitInstallationInstancesNumber" : "10",
    "limitInstallationInstances" : "true",
    "rootWorkingDirectory" : "D:\\\\DELiS_tools\\\\tmp\\\\"""
        + versionName
        + '''",
    "host" : "RCE",
    "toolDirectory" : "'''
        + toolDir
        + '''",
    "version" : "'''
        + versionString
        + """"
  } ],
  "outputs" : [ """
        + rceOutputs
        + ''' ],
  "postScript" : "'''
        + postScript
        + '''",
  "preScript" : "'''
        + preScript
        + '''",
  "toolDescription" : "'''
        + description
        + '''",
  "toolIconPath" : "'''
        + iconFilename
        + '''",
  "toolIntegrationVersion" : 1,
  "toolIntegratorE-Mail" : "sebastian.freund@dlr.de",
  "toolIntegratorName" : "Sebastian Freund",
  "toolName" : "'''
        + versionName
        + """",
  "toolProperties" : {"""
        + toolProperties
        + """},
  "uploadIcon" : true,
  "useIterationDirectories" : true
}"""
    )


if __name__ == "__main__":
    from patme import name, programDir, version

    iconPath = "doc/icon.png"
    rceRunCommand = 'rem setting paths  \\r\\nD:\\\\DELiS_tools\\\\delis_3rd_party\\\\64\\\\delis_vars.bat  \\r\\nC:\\\\Miniconda3\\\\envs\\\\py36\\\\python.exe src\\\\delis\\\\main\\\\aircraftmain.py --configFile=\\"${in:optionalConfigFileName}\\"'

    username = "default"
    password = "default"
    hostnameRce10 = "fa-jenkins2.intra.dlr.de"
    portRce10 = 31008
    hostKeyStringRce10 = "AAAAB3NzaC1yc2EAAAADAQABAAABAQCI1DvxZ3gC9437WjXebxZ5HOjru51ur0OlTgHAbHiPpIue\ng0F231NpRs/4Q8TvhkJpepb83EfE2xMyaZNIW6vf8BoKB+Jz7VEi609pI5aNzLdnrRCPXXUIdcLv\neMOvS1vez+KREp+5rLbvPvUfFwkOk0jvT95aFFgFnqoLu/zxIEvKN7TIR9z1S1Gy98Y7h4UHHYrV\nn156nvbnU2sMhwH7Lzl7zGbn+nYPki5oFXxloSJiwHbjPIYGqKGp0tzuV8bCmJUTt9q9SknCi3jY\n40TlXl25vRjjF7oLuIaFFWcYPSBp0nSgkJyGK3Cc3zv1hkztrZ19yzD8a6tDCZFzV+ht"

    docCommand = "doc_latex"
    docResultPdfPath = f"build/sphinx/latex/{name}.pdf"

    toolDirToolserver = "D:\\DELiS_tools\\DELiS_git"
    configDirToolserver = (
        "\\\\fa-jenkins2\\DELiS_tools\\RCE\\Profiles\\RCE10_stm_toolserver\\integration\\tools\\common"
    )
    # configDirToolserver = 'C:\\RCE\\Profiles\\RCE10_client\\integration\\tools\\common'

    toolDirToolserverRemote = "\\\\fa-jenkins2\\DELiS_tools\\DELiS_git"

    releaseCreatorMain(
        version,
        programDir,
        name,
        "https://gitlab.dlr.de/fa_sw/patme.git",
        iconPath,
        "description",
        rceRunCommand,
        # doc settings
        docCommand,
        docResultPdfPath,
        # remote settings
        username,
        password,
        hostnameRce10,
        hostKeyStringRce10,
        portRce10,
        toolDirToolserver,
        toolDirToolserverRemote,
        configDirToolserver,
    )
