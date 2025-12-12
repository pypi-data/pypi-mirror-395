# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Created on 25.01.2017

@author: freu_se
"""
import getpass
import os
import re
import shutil
import subprocess
import tarfile
import zlib
from datetime import datetime

from patme.service.duration import Duration
from patme.service.logger import log
from patme.service.systemutils import dos2unix, tarGzDirectory
from patme.sshtools.cara import copyClusterFilesSCP, get_default_slurm_args, sshCluster, sshClusterJob
from patme.sshtools.sshcall import callSSH

duration = Duration()


class ClusterCaller:
    """This class represents a general interface to call several fe and other functions on the cluster.

    The remote jobs are performed by copying the files of the local input directory to the
    cluster on "\\\\cluster.fa.bs.dlr.de\\<username>\\job\\<runDirName>".
    Then the program creates an ssh connection to the cluster. More information about
    the ssh connection can be found in service.utilities.callSSH.
    After the completion of the job the result is copied back to the local runDir.

    :param runDir: absolute or relative path to the folder where the fe run should be executed
    """

    REMOTE_SCRIPT = "run_sbatch.sh"

    clusterFuncDict = {
        "cara": {
            "copyClusterFilesSCP": copyClusterFilesSCP,
            "sshCluster": sshCluster,
            "sshClusterJob": sshClusterJob,
        },
    }

    def __init__(self, runDir, **kwargs):
        self.runDir = runDir
        self.remoteBaseDir = None
        """Directory where files will be copied remotely. Defaults to solverName in runRemote
        remoteRunDir = ~/remoteBaseDir/self.runDir[-1]"""
        self.remoteCmds = None
        self.preCommands = []
        """List of commands that are sent to the cluster prior to the remote command.
        It is intended to setup the environment for the call that will be done
        """
        self.ignorePatternsHostToLocal = {".svn"}
        """Files and folders that shall not copied from the cluster to the local machine on remote runs."""

        self.reuseResults = False
        """If True, the resulting tar.gz file is also extracted on the remote machine.
        This way, the result folder can be reused on a next remote call without copying inputs."""

        self._clusterName = kwargs.pop("clusterName", "cara")
        self.__checkClusterName(self._clusterName)

        self.docker_container = kwargs.pop("docker_container", None)

        if "wsl" in self.clusterName:
            self.remoteCmds = [
                "bash",
                "-i",
                self.REMOTE_SCRIPT,
            ]
        elif "cara" in self.clusterName:
            self.preCommands.append(f"chmod a+x {self.REMOTE_SCRIPT}")
            self.remoteCmds = [
                "sbatch",
                self.REMOTE_SCRIPT,
            ]

    def _getClusterFunc(self, funcName):
        """doc"""
        if self.clusterName not in self.clusterFuncDict:
            raise Exception(f"Unknown cluster {self.clusterName}")

        if funcName not in self.clusterFuncDict[self.clusterName]:
            raise Exception(f"Unknown cluster func {funcName}")

        return self.clusterFuncDict[self.clusterName][funcName]

    def runRemote(self, copyFilesLocalToHost=True, jobName="job", **kwargs):
        """doc"""
        log.info(f"call {self.solverName} remotely on '{self.clusterName}'")

        remoteRunDir = kwargs.get("remoteRunDir", None)
        if not remoteRunDir:
            ws_dir_name, remoteRunDir = self.getRemoteRunDir(**kwargs)

        if self.docker_container is not None:
            basedir = os.path.basename(remoteRunDir)
            docker_mnt_dir = f"/mnt/{basedir}"
            self.addClusterSpecificBatchCmds(jobName, docker_mnt_dir)
        else:
            self.addClusterSpecificBatchCmds(jobName, remoteRunDir)

        # copy rundir to network folder
        if copyFilesLocalToHost:
            log.info(f"Copy files to remote machine '{self.clusterName}'")
            with log.switchLevelTemp(log.WARN):
                self._transferInputToCluster(remoteRunDir, **kwargs)

        # Replace <jobName> two times since it used two times in the command list
        remoteCmds = [re.sub("<jobName>", jobName, elem) for elem in self.remoteCmds]

        # change to run dir of fe call
        remoteCmdsJoin = " ".join(remoteCmds)
        if "wsl" not in self.clusterName:
            command = f"cd {remoteRunDir};{remoteCmdsJoin}"
        else:
            if self.docker_container is not None:
                if ".sh" not in remoteCmds[-1]:
                    raise Exception("Test")

                remoteCmds[-1] = f"{docker_mnt_dir}/{remoteCmds[-1]}"
                remoteCmds[0] = (
                    f"docker run -w {docker_mnt_dir} -it -v {remoteRunDir}:{docker_mnt_dir} {self.docker_container} "
                )
                command = " ".join(remoteCmds)
            else:
                command = remoteCmdsJoin

        if self.preCommands:
            precmd = ";".join(self.preCommands)
            command = f"{precmd};{command}"

        log.debug(f'Call "{self.solverName}" with the following command:')
        log.debug(f"{command}", longMesageDelim=";")

        if "cara" in self.clusterName:
            # =======================================================================
            # run remote
            # =======================================================================
            if self.clusterName not in self.clusterFuncDict:
                raise Exception(f"Unknown cluster {self.clusterName}")

            sshClusterFunc = self._getClusterFunc("sshClusterJob")

            jobId = sshClusterFunc(command, printOutput=False, **kwargs)
        else:

            jobId = "WSL_NOJOBID"
            remoteRunDirAsWinPath = self.__getWSLRemoteDirAsWinPath(remoteRunDir)
            wsl_cmd = f"wsl --cd {remoteRunDirAsWinPath} {command}"
            p = subprocess.run(wsl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        log.debug(f"Transfer files from remote to local working dir")
        with log.switchLevelTemp(log.WARN):
            self._transferFromCluster(remoteRunDir, jobId, **kwargs)

        self.cleanRemoteDir(ws_dir_name, remoteRunDir, **kwargs)

        log.info(f"Remote call {self.solverName} with jobId {str(jobId)} done")

    def cleanRemoteDir(self, ws_name, remoteRunDir, **kwargs):
        """Clean scratch directory and release scratch"""
        if self.clusterName == "cara":

            from patme.sshtools.cara import _getClusterAuthentication

            hostname, hostKeyString, privateKey = _getClusterAuthentication()
            username = kwargs.get("username", getpass.getuser())
            cmd = f"rm -rf {remoteRunDir}/*;ws_release {ws_name}"
            _ = callSSH(hostname, cmd, privateKey, hostKeyString=hostKeyString, username=username, printOutput=False)

        elif "wsl" in self.clusterName:

            shutil.rmtree(self.__getWSLRemoteDirAsWinPath(remoteRunDir))

    def getRemoteRunDir(self, **kwargs):
        """doc"""
        if self.clusterName == "cara":

            from patme.sshtools.cara import _getClusterAuthentication

            hostname, hostKeyString, privateKey = _getClusterAuthentication()
            username = kwargs.get("username", getpass.getuser())
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            ws_dir_name = f"run_{timestamp}"
            cmd = f"ws_allocate {ws_dir_name}"
            log.info("Allocate workspace: " + ws_dir_name)
            with log.switchLevelTemp(log.WARN):
                scratch_dir = callSSH(
                    hostname, cmd, privateKey, hostKeyString=hostKeyString, username=username, printOutput=False
                )

            remoteRunDir = scratch_dir.strip()

        elif "wsl" in self.clusterName:

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            ws_dir_name = f"run_{timestamp}"
            remoteRunDir = f"~/tmp/{ws_dir_name}"
            os.makedirs(self.__getWSLRemoteDirAsWinPath(remoteRunDir))

        else:
            raise Exception(f"Cluster with name {self.clusterName} not supported!")

        return ws_dir_name, remoteRunDir

    def _transferInputToCluster(self, remoteRunDir, **kwargs):
        """Transfer the input to the cluster by performing 4 steps.

        1. tar.gz the whole input directory
        2. transfer this tarfile to the cluster via sftp
        3. extract the file on the cluster
        4. remove the tarfiles on both ends
        """
        log.info(f"Copy files to remote machine: {remoteRunDir}")
        tarFileName = "clusterInput.tar.gz"
        tarFileNameFull = tarGzDirectory(self.runDir, tarFileName)

        if "cara" in self.clusterName:
            username = kwargs.get("username", getpass.getuser())
            if self.clusterName not in self.clusterFuncDict:
                raise Exception(f"Unknown cluster {self.clusterName}")

            clusterFuncCopy = self._getClusterFunc("copyClusterFilesSCP")
            sshClusterFunc = self._getClusterFunc("sshCluster")

            clusterFuncCopy(
                [tarFileName], srcBaseDir=self.runDir, destBaseDir=remoteRunDir, mode="put", username=username
            )

            # unzip files at cluster and remove zip files on both sides
            extract = [f"cd {remoteRunDir}", f"tar -xf {tarFileName}", f"rm {tarFileName}"]

            sshClusterFunc(";".join(extract), printOutput=False, username=username)

        elif "wsl" in self.clusterName:

            remoteRunDirAsWinPath = self.__getWSLRemoteDirAsWinPath(remoteRunDir)
            shutil.copy(tarFileNameFull, remoteRunDirAsWinPath)

            cmd = f"wsl --cd {remoteRunDir} tar -xf {tarFileName} -C .;rm {tarFileName}"
            subprocess.run(cmd, shell=True)

        else:
            raise NotImplementedError(f"Unknown cluster name or wsl: {self.clusterName}")

        os.remove(os.path.join(self.runDir, tarFileName))

        log.debug(f"Copy files to remote machine '{self.clusterName}' done")

    def __getWSLRemoteDirAsWinPath(self, remoteDir):
        """doc"""
        p = subprocess.run(["wsl", "wslpath", "-w", remoteDir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.decode().strip()

    def _transferFromCluster(self, remoteRunDir, jobId, **kwargs):
        """Transfer the calculation result from the cluster by performing these steps.

        1. copy the result tar.gz file to self.runDir
        2. extract the file locally
        3. extract tar file remotely if the remote folder should be reused
        4. remove the tarfile locally
        4.1 optionally extract tarfile remotely to reuse the calculation results
        5. remove the tarfile remote"""

        def getFileAndExtract(tarFileName, tarFileNamePath, remoteRunDir, copyFunc, username=None):
            """doc"""
            copyFunc([tarFileName], remoteRunDir, self.runDir, "get", username=username)

            with tarfile.open(tarFileNamePath) as f:
                f.extractall(self.runDir, filter="data")

        if "wsl" in self.clusterName:

            remoteRunDirAsWinPath = self.__getWSLRemoteDirAsWinPath(remoteRunDir)
            dir_creation_time = os.path.getctime(remoteRunDirAsWinPath)
            for dirpath, _, filenames in os.walk(remoteRunDirAsWinPath):
                for filename in filenames:

                    filepath = os.path.join(dirpath, filename)
                    try:
                        file_mtime = os.path.getmtime(filepath)
                        # Compare the file's modification time with the directory's creation time
                        if file_mtime > dir_creation_time:
                            rel_dir = os.path.relpath(dirpath, remoteRunDirAsWinPath)
                            dirInRunDir = os.path.join(self.runDir, rel_dir)
                            os.makedirs(dirInRunDir, exist_ok=True)
                            shutil.copy(filepath, dirInRunDir)

                    except FileNotFoundError:
                        # Skip files that might disappear during walk
                        continue

        else:
            username = kwargs.get("username", getpass.getuser())
            copyFunc = self._getClusterFunc("copyClusterFilesSCP")
            sshClusterFunc = self._getClusterFunc("sshCluster")

            try:
                log.info("copy result from cluster")
                tarFileName = f"cluster.r{jobId}.tar.gz"
                tarFileNamePath = os.path.join(self.runDir, tarFileName)

                try:
                    getFileAndExtract(tarFileName, tarFileNamePath, remoteRunDir, copyFunc, username=username)

                except tarfile.ReadError:
                    msg = "Could not open the result tar file. "
                    msg += "Probably the calculation was cancelled."
                    log.error(msg)
                    return  # retruning to make a local calculation possible

                except zlib.error:
                    msg = "Got error while extracting result file. "
                    msg += "Try again to copy and extract"
                    log.error(msg)
                    try:
                        getFileAndExtract(tarFileName, tarFileNamePath, remoteRunDir)
                    except tarfile.ReadError:
                        msg = "Could not open the result tar file. "
                        msg += "Probably the calculation was cancelled."
                        log.error(msg)
                        return  # retruning to make a local calculation possible

                os.remove(tarFileNamePath)

                cleanupCommand = f"cd {remoteRunDir}"
                if self.reuseResults:
                    cleanupCommand += f";tar -xf {tarFileName}"

                cleanupCommand += f";rm {tarFileName}"

                sshClusterFunc(cleanupCommand, printOutput=False, username=username)
                log.debug("copy result from cluster done")

            except OSError as exception:

                msg = "Retrieved IOError when copying results from remote computer. "
                msg += "Maybe some items are not copied properly. "
                msg += "See debug.log for more details."

                log.warning(msg)
                log.debug("error message to the above warning: " + str(exception))

    def addClusterSpecificBatchCmds(self, jobName, remoteRunDir, **kwargs):
        """Create bash cmds which for remote sbatch call"""
        runScriptCmds = ["#!/bin/bash"]
        if self.clusterName == "cara":

            slurm_args = get_default_slurm_args()
            cara_partion = os.environ.get("CARA_PARTITION", slurm_args["partition"])
            slurm_args["partition"] = cara_partion
            if cara_partion == "ppp":
                slurm_args["ntasks"] = "1"

            slurm_args["output"] = f"{jobName}.log"

            for sarg, sval in slurm_args.items():
                if f"--{sarg}" in self.remoteCmds:
                    continue
                cmd = f"#SBATCH --{sarg}"
                cmd += "" if not sval else f"={sval}"
                runScriptCmds.append(cmd)

            runScriptCmds += [
                ". /usr/share/lmod/lmod/init/sh",
                ". /etc/profile.d/10-dlr-modulepath.sh",
                "module --force purge",
                'curtime=$(date +"%Y-%m-%d %H:%M:%S")',
                # find can only distinguish between timestamps which have seconds as highest precision
                "sleep 1s",
            ]

        runScriptCmds += [f"cd {remoteRunDir}"]
        runScriptCmds += self.generateSolverSpecificRemoteCmds(jobName)
        runScriptCmds += [f"touch {jobName}.log"]
        if self.clusterName == "cara":
            runScriptCmds += [
                'tarFile="cluster.r$SLURM_JOB_ID.tar.gz"',
                'tar -czf $tarFile -C . $(find . -newermt "$curtime" -type f)',
            ]

        runScriptFile = os.path.join(self.runDir, self.REMOTE_SCRIPT)
        with open(runScriptFile, "w") as f:
            f.write("\n".join(runScriptCmds))

        dos2unix(runScriptFile)

    def __checkClusterName(self, cname):
        if not re.search("cara|wsl", cname):
            raise NotImplementedError(f"No remote caller implemented for cluster '{cname}'")

    def _getClusterName(self):
        return self._clusterName

    def _setClusterName(self, cname):
        self.__checkClusterName(cname)
        self._clusterName = cname

    clusterName = property(fget=_getClusterName, fset=_setClusterName)


class PythonModuleCaller(ClusterCaller):
    """This class handles calling target functions like those in buckling.bucklingtargetfunction on the cluster"""

    def __init__(self, runDir, jobCommands):
        """
        :param jobCommands: list with strings defining the command to call a python script excluding the leading python executable
        """
        ClusterCaller.__init__(self, runDir)
        self.solverName = "python35"
        clusterCmds = ["py35", "-d", "-O", "tgz", "-J", "<jobName>"]
        self.remoteCmds = clusterCmds + jobCommands
        self.preCommands = [". ${HOME}/.profile;echo PYTHONPATH:${PYTHONPATH}"]


class MatlabCaller(ClusterCaller):
    """This class handles calling target functions like those in buckling.bucklingtargetfunction on the cluster"""

    solverName = "matlab"

    def __init__(self, runDir, jobCommands):
        """
        :param jobCommands: list with strings defining the command to call a matlab script excluding the leading matlabe executable
        """
        ClusterCaller.__init__(self, runDir)
        clusterCmds = ["mat2013a", "-d", "-O", "tgz", "-J", "<jobName>", "--", "-r"]
        self.remoteCmds = clusterCmds + jobCommands
