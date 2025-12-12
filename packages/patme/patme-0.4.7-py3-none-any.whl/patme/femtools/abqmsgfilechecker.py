# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""Checks for the abaqus message file"""

from patme.service.logger import log


def getElementsWithLargestResForces(msgString):
    """Check Abq message file for largest residual force

    ABAQUS prints information to the msg-file which could be useful to identify the reasons
    for divergence. One kind of information is at which node of which instance the highes
    residual force occurs per iteration. The script extracts all nodes (and their instances)
    which are at least once the nodes with the highest residual force. The result is plotted
    to a txt-file of the form:

    Input Example:

    .. code-block:: none

        <Instance_Name 2>
        <Node nr 1>, <node nr 2>, ...
        <Instance_Name 2>
        <Node nr 1>, <node nr 2>, ...

    :param msgString: string of the message file
    :return: string, overview about elements with largest residual forces
    """
    lines = msgString.split("\n")

    elementList = list(list())
    instanceList = list()

    lineNo = -1
    for line in lines:
        lineNo = lineNo + 1
        if "LARGEST RESIDUAL FORCE" in line:
            words = line.split()
            element = list()
            element.append(int(words[6]))

            nextLine = lines[lineNo + 1]
            words = nextLine.split()
            instanceName = words[1]

            if instanceName in instanceList:
                index = instanceList.index(instanceName)
                if element[0] not in elementList[index]:
                    elementList[index].append(element[0])
            else:
                instanceList.append(instanceName)
                elementList.append(element)

    outString = ""
    for instanceName in instanceList:
        outString += instanceName + "\n"
        index = instanceList.index(instanceName)
        outString += "\n".join(["%s, " % item for item in elementList[index]] + [""])
    log.info("Elements with largest residual force:\n" + outString)
    return outString


def getOverconstrainedNodes(msgString):
    """ "Check abq message file for overconstrained nodes

    ABAQUS prints information to the msg-file which could be useful to identify the reasons
    for divergence. Sometimes overconstraints exists in the model (nodes are constrains by
    too many constraints). These overconstraints are identified by PIVOT messages. This scripts
    extracts all nodes (and the instances they belong to) for which pivots are idendified.

    Input Example:

    .. code-block:: none

        ***WARNING: SOLVER PROBLEM.  ZERO PIVOT WHEN PROCESSING A (TIED) CONTACT
        CONSTRAINT D.O.F. 1 FOR SLAVE NODE 3288 INSTANCE MANDREL1_LAYER_9.
        THIS MAY BE DUE TO THE UNIT USED FOR THE DISPLACEMENT DIFFERS BY
        MORE THAN 10 ORDER OF MAGNITUDE THAN THE UNIT USED FOR THE
        MATERIAL STIFFNESS.  IF THIS IS THE CASE, PLEASE USE A DIFFERENT
        UNIT SYSTEM.

    :param msgString: string of the message file
    :return: string, overview about overconstraint nodes
    """

    lines = msgString.split("\n")

    nodeList = list(list())
    instanceList = list()

    lineNo = -1
    for line in lines:
        lineNo = lineNo + 1
        if "PIVOT" in line:
            nextLine = lines[lineNo + 1]
            if "D.O.F." in nextLine and "NODE" in nextLine and "INSTANCE" in nextLine:
                words = nextLine.split()
                node = words[6]
                try:  # instance name mentioned in next line; maybe too long for current line --> take first word of next line
                    instanceName = words[8]
                except IndexError:
                    overNextLine = lines[lineNo + 2]
                    overNextWords = overNextLine.split()
                    instanceName = overNextWords[0]

            if instanceName in instanceList:
                index = instanceList.index(instanceName)
                if node not in nodeList[index]:
                    nodeList[index].append(node)
            else:
                instanceList.append(instanceName)
                nodeList.append([node])

    outString = ""
    # nodes and their instances are written to the given file
    for instanceName in instanceList:
        outString += instanceName + "\n"
        index = instanceList.index(instanceName)
        outString += "\n".join(["%s, " % item for item in nodeList[index]] + [""])
    log.info("Overconstrained nodes:\n" + outString)
    return outString


if __name__ == "__main__":
    # please provide name of abaqus message file
    filename = "Job_NGT-BIT-small_Solid3D_C3D8R_noDamage_TiedContact.msg"
    with open(filename) as f:
        msgString = f.read()
    getElementsWithLargestResForces(msgString)

    # please provide name of abaqus message file
    filename = "Job_NGT-BIT-small_Solid3D_C3D8R_noDamage_TiedContact.msg"
    with open(filename) as f:
        msgString = f.read()
    getOverconstrainedNodes(msgString)
