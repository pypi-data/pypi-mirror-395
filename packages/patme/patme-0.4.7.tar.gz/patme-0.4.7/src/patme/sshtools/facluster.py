# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Connect via python to the FA cluster using ssh, submit commands, move inputs/outputs to and from the cluster.

**Scenario**

To connect to the institute cluster and submit a job, two things need to be done.
First the input files must be copied to the cluster.

``\\\\cluster.fa.bs.dlr.de\\<username>\\``

Secondly, when all required files are available on the cluster,
the cluster command (see cluster documentation) needs to be sent using a secure connection.
This is done via ssh using the rsa-public/privat-key algorithm.

**Connect for the first time**

- Create a public+private key using ssh-keygen
- Put the private key to the location specified in patme.sshtools.sshcall.privateKeyFileConfig
  or adapt this variable at runtime.
- Append the public key to "~/.ssh/authorized_keys" on the remote computer

**HowTo connect to the a host**

    >> sshCluster('echo hello world')
    'hello world\\n'

"""

from time import sleep, time

from patme.service.exceptions import DelisSshError
from patme.service.logger import log
from patme.sshtools import sshcall


def _getClusterAuthentication():
    """Returns the hostname, host key string and private key file information for a cluster call.

    A description to these objects can be found in service.sshremotecall.callSSH"""
    hostname = "cluster.fa.bs.dlr.de"
    #     hostname = '129.247.54.37' # in vpn, the host name is not reachable
    bsfalxclusterKeyString = "AAAAB3NzaC1yc2EAAAADAQABAAABAQDIibHwDzn+UQFI3PRve7YSUdj72lBAG4ARvzrbXNOZJ04/nFMlS5vee8AB+EWOqMj56xa4fWX2BOcBfpI69dp0oDMWuotqLKUpRIQoSlYeE7wZ34KXr2F3nEZ9Zm8Y0OWCGVPgO3euLiBz6Rt+veuNN2A/2EyBM36Ij8T9czNHzOqjR6lpkqPVDC2Rdfjiytvy+iMYnGR1wTNqjPlfLHz4YTWM4dF/H8pd1SQ0maNKXCH9Fr4zPV6uxMJURzm+wjPC+ccG/On3jCsGxxjyVQ3PnHwPrK0Pds0yFZ00Kf/y9lpHaP1yjD955NB7cINhCZKenTl8gdYZ6u7Qub+OV2kJ"
    """this is the key from the file "~/.ssh/known_hosts" used by openssh on a linux machine"""
    sshcall.checkPrivatePublicKey()
    return hostname, bsfalxclusterKeyString, sshcall.privateKeyFileConfig


def sshClusterJob(
    remoteCommand, printOutput=True, checkInterval=5, time2WaitForJob=30, monitorNodeUsage=False, **kwargs
):
    """Submit a job to the institute cluster via ssh and return when terminated.

    After job submission, a connection to the cluster is established every 'checkInterval' seconds
    to check if the job's status is already set to 'COMPLETED'.

    :param remoteCommand: String with command for cluster. The arguments for the queuing
                          system must not contain the option '-i' to wait for job
                          completion.
    :param printOutput: True (default) will print output created by the ssh call.
    :param checkInterval: Time period in seconds between job completion checks
    :param time2WaitForJob: After job submission it might take some time for the cluster to
                            add the job to the queue. Enter max seconds [int] to wait.

    :return: int, job id
    """
    retVal = sshCluster(remoteCommand, printOutput=printOutput)
    errorMsg = lambda remoteCommand, retVal: f"remote command: {remoteCommand}\nreturn value: {retVal}"
    if not retVal or (retVal and "Submitted batch job" not in retVal):
        raise DelisSshError(
            "Job submission to cluster failed or maybe the arguments "
            + "for the cluster contained the option -i\n"
            + errorMsg(remoteCommand, retVal)
        )
    try:
        jobId = int(retVal.split()[-1])
    except:
        raise DelisSshError("Could not extract job id for cluster job submission.\n" + errorMsg(remoteCommand, retVal))

    log.info("Job enqueued. JobId: %s" % jobId)
    usageWarningDone = False
    while not clusterJobEnded(jobId, time2WaitForJob):
        if monitorNodeUsage:
            if not usageWarningDone:
                nodeName = getNodeOfJob(jobId)
                usageWarningDone = printNodeUtilization(nodeName, usageWarningDone)
        sleep(checkInterval)
    return jobId


def sshCluster(remoteCommand, printOutput=True, **kwargs):
    """Submit a job to the institute cluster via ssh.

    The method does not
    wait for the completion of the cluster call. Please use sshClusterJob instead.

    :param remoteCommand: String with command for cluster
    :param printOutput: True (default) will print output created by the ssh call.
    """
    hostname, bsfalxclusterKeyString, privateKeyFile = _getClusterAuthentication()
    return sshcall.callSSH(
        hostname, remoteCommand, privateKeyFile, None, bsfalxclusterKeyString, printOutput=printOutput
    )


def clusterJobEnded(jobId, time2WaitForJob=30, printOutput=False):
    """Checks if jobId is still listed in the cluster queue.

    :param jobId: Id of job running on the cluster <int>
    :param time2WaitForJob: After job submission it might take some time for the cluster to
                            add the job to the queue. Enter max seconds [int] to wait.
    :param printOutput: Flag if the ssh output should be output. Defaults to True
    :return: True if job with jobId still exists in the queue, else False
    :raise DelisSshError: in case job is neither running nor completed successfully
    """
    status = clusterJobStatus(jobId, printOutput=printOutput)
    if not status and time2WaitForJob:
        startTime = time()
        while not status:
            status = clusterJobStatus(jobId, printOutput=printOutput)
            if time() - startTime > time2WaitForJob:
                raise DelisSshError("Could not obtain status of cluster job with id %s" % jobId)
    if not status:
        raise DelisSshError("Job with id %s not found in cluster job history." % jobId)
    elif "PENDING" == status:
        log.debug("Job execution on cluster is waiting for resources.")
        return False
    elif status in ["RESIZING", "RUNNING", "REQUEUED"]:
        return False
    elif "FAILED" == status:
        log.debug("Job with id %s failed" % jobId)
        return True
    elif "CANCELLED" == status:
        log.debug("Job with id %s was cancelled." % jobId)
        return True
    elif "COMPLETED" == status:
        return True
    else:
        raise DelisSshError('Unknown cluster status: "%s"' % status)


def clusterJobStatus(jobId, printOutput=False):
    """Checks if cluster process with id "jobID" is pending.

    :param jobId: id of cluster process (int)
    :return: True if state is pending, else False
    """
    sacct = sshCluster("sacct -o state -n -j " + str(jobId), printOutput=printOutput)
    return sacct.split("\n")[0].replace("+", "").strip()


def copyClusterFilesSCP(files, srcBaseDir=".", destBaseDir=".", mode="put", keytype="ssh-rsa", port=None, **kwargs):
    hostname, bsfalxclusterKeyString, privateKeyFile = _getClusterAuthentication()
    sshcall.copyFilesSCP(
        files, hostname, privateKeyFile, None, srcBaseDir, destBaseDir, bsfalxclusterKeyString, mode, keytype, port
    )


def _wrapSshCluster(*args, **kwargs):
    """This method wraps the sshCluster routine to prevent python cyclic imports"""
    retries = 3
    for retry in range(retries):
        try:
            result = sshCluster(*args, **kwargs)
            break
        except Exception as e:
            if retry < retries:
                log.error(f"Got an error while calling the cluster (retry in 60s): {e}")
                time.sleep(60)
            else:
                raise
    return result


def numberOfClusterJobsAvailable(exclusiveNode=False):
    """Checks and returns the number of available jobs on the FA cluster.

    :param exclusiveNode: if True, number of cluster jobs is given, that can allocate
                          a complete node. The default is False

    :returns: Returns the number of jobs that can be executed on the cluster.
    """
    clusterCommand = 'sinfo -h -o "%t %N";'
    clusterCommand += 'squeue -h -t RUNNING,COMPLETING -o "%N"'
    clusterOutput = _wrapSshCluster(clusterCommand, printOutput=False).split("\n")

    # STATE NODELIST        <- this line does not appear in clusterOutput
    # mix node[1,3]         <- these nodes have one or more active jobs
    # alloc node5           <- these nodes are exclusively used
    # idle node[2,4,6]      <- these nodes are awaiting jobs (up to 2)
    # NODELIST              <- this line does not appear in clusterOutput
    # node5                 <- job on node5
    # node1
    # node3
    # node3

    mixNodes = _splitNodes([line.split()[1][4:].strip("[]") for line in clusterOutput if "mix" in line])
    idleNodes = _splitNodes([line.split()[1][4:].strip("[]") for line in clusterOutput if "idle" in line])
    nodeNumbersOfActiveJobs = [int(line[4:].strip()) for line in clusterOutput if line.startswith("node")]

    numberOfPosssibleJobs = 0
    if exclusiveNode:
        numberOfPosssibleJobs = len(idleNodes)
    else:
        for mixNode in mixNodes:
            if nodeNumbersOfActiveJobs.count(mixNode) < 2:
                numberOfPosssibleJobs += 1
        numberOfPosssibleJobs += len(idleNodes) * 2
    return numberOfPosssibleJobs


def _splitNodes(nodes):
    """parses the nodes string and returns a list of node numbers

    Example:

    >>> inputString = ['1,4', '2-3,5-6']
    >>> _splitNodes(inputString)
    [1, 2, 3, 4, 5, 6]
    """
    outputNodes = []
    for nodesString in nodes:
        groups = nodesString.split(",")
        for group in groups:
            groupMembers = group.split("-")
            if len(groupMembers) > 1:
                outputNodes.extend(range(int(groupMembers[0]), int(groupMembers[1]) + 1))
            else:
                outputNodes.append(int(groupMembers[0]))
    return list(set(outputNodes))


def numberOfIdleClusterNodes():
    """returns the number of idle cluster nodes

    cluster call returns: "3/3" which is Allocated/Idle

    Attention: This is not the number of possible cluster jobs, since 2 jobs can be run
    at each node. If zero nodes are idle, there may be still the opportunity to start
    a job right away.
    """
    clusterOutput = _wrapSshCluster('sinfo -h -e -o "%A"', printOutput=False)
    return int(clusterOutput.split("/")[-1])


def getNodeUtilization(nodeName="head"):
    """Returns the utilization of the cluster head (default) or of one of its nodes.
    The information is retrieved using the commands vmstat and df. The keys of the
    returned dictionary are described in the following.

    Processes
        r: The number of processes waiting for run time.
        b: The number of processes in uninterruptible sleep.
    RAM Memory
        swpd: The amount of virtual memory used. (in MB)
        free: The amount of idle memory. (in MB)
        buff: The amount of memory used as buffers. (in MB)
        cache: The amount of memory used as cache. (in MB)
    Swap Memory
        si: Amount of memory swapped in from disk (in MB/s).
        so: Amount of memory swapped to disk (in MB/s).
    IO
        bi: Blocks received from a block device (blocks/s).
        bo: Blocks sent to a block device (blocks/s).
    System
        in: The number of interrupts per second, including the clock.
        cs: The number of context switches per second.
    CPU
        These are percentages of total CPU time.
        us: Time spent running non-kernel code. (user time, including nice time)
        sy: Time spent running kernel code. (system time)
        id: Time spent idle. Prior to Linux 2.5.41, this includes IO-wait time.
        wa: Time spent waiting for IO. Prior to Linux 2.5.41, shown as zero.
    HDD Memory
        1K-blocks: Total size of storage memory (in KB)
        Used: Total size of used storage memory (in KB)
        Available: Total size of available storage memory (in KB)
        Use%: Relative usage of storage memory (in %)

    :param nodeName: Name of the node (node1, ...) of which the information is to
                     be retrieved. The default is "head".
    :return: Dictionary with utilization information.
    """
    nodeCmdString = ""
    filesystem = "/home"
    if nodeName != "head":
        nodeCmdString = "ssh " + nodeName + " "
        filesystem = "/dev/sda3"
    remoteCmd = nodeCmdString + "vmstat -S M;"
    remoteCmd += nodeCmdString + "df -l -k"
    remoteCmdOutput = _wrapSshCluster(remoteCmd, printOutput=False).split("\n")
    vmstatDict = dict(zip(remoteCmdOutput[1].split(), [float(item) for item in remoteCmdOutput[2].split()]))
    dfData = [row for row in remoteCmdOutput if row.startswith(filesystem)][0]
    dfDict = dict(zip(remoteCmdOutput[3].split()[1:-1], [float(item.strip("%")) for item in dfData.split()[1:-1]]))
    vmstatDict.update(dfDict)
    return vmstatDict


def printNodeUtilization(self, nodeName, printOnCriticalUtilization=False):
    """Prints the utilization of a cluster node

    :param nodeName: name of the cluster node to inspect
    :param printOnCriticalUtilization: Flag if only on a critical utilization, the routine should print anything
    :return: Flag if a usage warning was emit
    :raise DelisSshError: if nodeName could not be found
    """
    if printOnCriticalUtilization:
        logMethod = log.warn
    else:
        logMethod = log.info
    usageWarningDone = False
    if nodeName:
        utilizationInfo = getNodeUtilization(nodeName=nodeName)
        freeRam = (utilizationInfo["free"] + utilizationInfo["cache"]) / 1024
        freeHdd = utilizationInfo["Available"] / 1024 / 1024
        if freeHdd < 2 or not printOnCriticalUtilization:
            logMethod("HDD memory utilization of node %s critical. This may cause problems." % nodeName)
            usageWarningDone = True
        if freeRam < 2 or not printOnCriticalUtilization:
            logMethod("RAM memory utilization of node %s critical. This may cause problems." % nodeName)
            usageWarningDone = True
    else:
        raise DelisSshError(
            'Utilization of the used cluster node %s cannot be performed: Node "" not found.' % nodeName
        )
    return usageWarningDone


def getNodeOfJob(jobId):
    """Returns the name of the node on which the job with id "jobId" is being executed on.

    :param jobId: Id of cluster process (int)
    :return: Name of node ("node1", "node2", ...) or None if jobId is not found.
    """
    node = None
    try:
        node = _wrapSshCluster("squeue | grep " + str(jobId), printOutput=False).split()[7]
    except:
        log.warning("Node not found, because jobID not found in cluster queue")
    return node


if __name__ == "__main__":
    from patme.sshtools import sshcall

    sshcall.privateKeyFileConfig = None
    sshCluster("echo foobar")
