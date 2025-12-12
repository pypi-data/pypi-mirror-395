# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Calling Analysis

Several finite element solvers can be used to solve different kinds of structural problems.
Currently, interfaces to Ansys, Nastran and Abaqus are provided. They all base on a general
python interface which provide convenient methods to establish a fe solver call whithout taking effort
e.g. in file I/O or error handling. This is all done by the general interface.
For example,running an linear static analysis in Ansys with a beforehand written file Model.mac
will be instantiated as follows::

    from patme.femtools.fecall import AnsysCaller
    ansCall = AnsysCaller(feFilename = "Model.mac")
    ansCall.run(doRemoteCall = False, jobName = "testJobName")

If Abaqus or Nastran are used as external fe solver, the approach is similiar and the input file and caller object
need to be changed. Within a run() call, the user can also define if the calculation shall be done locally
or one the FA-Cluster in remote mode.

"""
import argparse
import getpass
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
import time

from numpy import array

from patme.service.duration import Duration
from patme.service.exceptions import DelisSshError, ImproperParameterError, InternalError
from patme.service.logger import log
from patme.service.systemutils import dos2unix, searchForWordsWithinFile
from patme.sshtools.clustercaller import ClusterCaller
from patme.sshtools.sshcall import callSSH

duration = Duration()

femUsedCores = 2
"""Number of the cores used for an fem calculation. Defaults to 2. If you change this for abaqus
runs, please also recognize the STM-rules for abaqus usage."""
ansysPath = "C:\\Program Files\\ANSYS Inc\\v192\\ansys\\bin\\winx64\\ANSYS192.EXE"
ansysLicense = "ansys"
"""Ansys license. Some possible values are (ansys, anshpc)"""
nastranPath = "C:\\MSC.Software\\MSC_Nastran\\20190\\bin\\nastran.exe"
abaqusPath = "C:\\SIMULIA\\Commands\\abaqus.bat"
"""path to abaqus.bat"""

RE_MULTILINE = re.RegexFlag.MULTILINE


class ResultLogFileChecker:
    """checks result log files for errors"""

    def __init__(self):
        self.maxErrors = 0

    def getErrorFileAndErrorPattern(self, jobName):
        """must be implemented in sub class"""
        raise NotImplementedError("This method must be implemented in a subclass")

    def checkResultLogFile(self, jobName):
        """returns true if no specified errors are found"""
        errorFileName, errorPattern = self.getErrorFileAndErrorPattern(jobName)
        if not os.path.exists(errorFileName):
            log.info(f"{errorFileName} not found. Try {jobName}_err.log")
            errorFileName = os.path.join(self.runDir, f"{jobName}_err.log")

        if not os.path.exists(errorFileName):
            log.error(f"Did not find given error file {errorFileName}")
            return None
        else:

            matches = searchForWordsWithinFile(errorFileName, errorPattern)
            if len(matches) > self.maxErrors:
                log.error(f"Call failed with errors in {errorFileName}")
                return False
            return True


class FECaller(ResultLogFileChecker, ClusterCaller):
    """This class represents a general interface to call several FE-solvers.
    It can also distinguish between local and remote(fa institute cluster) calculations.

    The remote jobs are performed by copying the files of the local input directory to the
    cluster on "\\\\cluster.fa.bs.dlr.de\\<username>\\delis\\<runDirName>".
    Then the program creates an ssh connection to the cluster. More information about
    the ssh connection can be found in service.utilities.callSSH.
    After the completion of the job the result is copied back to the local runDir.
    This feature is inherited from ClusterCaller.

    :param feFilename: name of fe input file optionally with relative or absolute path
    :param runDir: absolute or relative path to the folder where the fe run should be executed
    """

    def __init__(self, **kwargs):
        ResultLogFileChecker.__init__(self)
        runDir = kwargs.pop("runDir", None)
        ClusterCaller.__init__(self, runDir, **kwargs)
        self.feFilename = kwargs.pop("feFilename", "")
        if not self.runDir:
            self.runDir = os.path.dirname(self.feFilename)

        self.feFilename = os.path.join(self.runDir, os.path.basename(self.feFilename))
        if not os.path.exists(self.feFilename):
            raise InternalError(f"Given fem input file does not exist: {self.feFilename}")

        self.localCmds = None
        self.localSubProcessSettings = {"shell": False}

        self.remoteCallFailed = False
        """This is set to true if a remote call failed. Calling methods can use this flag as information"""
        self.activateLicenseCheck = True

        self._useNumberOfCores = 2
        self._jobName = os.path.basename(os.path.splitext(self.feFilename)[0])

    @staticmethod
    def isLicenseAvailable():
        """Returns True if the required number of license tokens is available, otherwise False"""
        return True

    @duration.timeit
    def run(self, doRemoteCall=False, copyFilesLocalToHost=True, jobName=None, **kwargs):
        """
        This methods serves to execute a FE-input model within a fe solver (e.g. for linear static analysis)
        :param doRemoteCall: flag if the calculation should be done on a remote computer
        :param copyFilesLocalToHost: flag if all files in the directory runDir should be copied to the
                      remote machine
        :param jobName: Name of job
        :returns: True if there were no errors occured when calling the fe solver with the given input file
        """
        if not jobName:
            jobName = self.jobName

        if doRemoteCall:
            try:
                if self.activateLicenseCheck:
                    self.returnWhenLicenseAvailable()
                self.runRemote(copyFilesLocalToHost, jobName, **kwargs)
                # check error file after remote files were copied to local machine
                if not self.checkResultLogFile(jobName):
                    self.remoteCallFailed = True
                else:
                    retVal = 8

            except DelisSshError as exception:
                msg = "Remote call failed. Maybe the remote dir was not found, "
                msg += "the remote server did not answer or the ssh authentication failed. "
                msg += "Calculating locally."
                log.error(msg)

                log.info(f"Error message to the above warning: {exception}")
                doRemoteCall = False
                self.remoteCallFailed = True

        if not doRemoteCall:
            if self.activateLicenseCheck:
                self.returnWhenLicenseAvailable()
            retVal = self.runLocal(jobName, **kwargs)

        if self.checkResultLogFile(jobName) is False:
            log.info("Change return value to 1 due to erros in the above file.")
            retVal = 1

        retVal = self.checkReturnValueOfCall(retVal)
        log.info(f"{self.solverName} run finished")
        return retVal

    def runLocal(self, jobName, **kwargs):
        """doc"""
        self.localCmds = [jobName if elem == "<jobName>" else elem for elem in self.localCmds]
        log.info(f"call {self.solverName} locally ")
        infoStr = f"call {self.solverName} with the following command: "
        log.debug(infoStr + " ".join(self.localCmds))

        toolexe = self.localCmds[0]
        if (not os.path.exists(toolexe) and "win" in sys.platform) and (shutil.which(toolexe) is None):
            msg = "The given executable does not exist. "
            msg += "Please enter the correct path to settings.py. "
            msg += f"Acutal path: {toolexe}"
            raise InternalError(msg)

        toStderr = os.path.join(self.runDir, f"{jobName}_err.log")
        toStdout = os.path.join(self.runDir, f"{jobName}_out.log")

        retVal = subprocess.call(
            self.localCmds,
            cwd=self.runDir,
            stderr=open(toStderr, "w+"),
            stdout=open(toStdout, "w+"),
            shell=self.localSubProcessSettings.get("shell", False),
        )

        log.info(f'return value of {self.solverName} call is "{retVal}"')
        return retVal

    def returnWhenLicenseAvailable(self, sleeptime=5):
        """doc"""
        # wait one minute
        numberOfTries = 12
        while numberOfTries > 0:

            if self.isLicenseAvailable():
                return 0

            msgs = [
                f"No license for {self.solverName} available! ",
                "Wait until a license is available.",
                "check every 5s.",
            ]
            log.info(" ".join(msgs))
            log.debug(msgs[0])
            time.sleep(sleeptime)
            numberOfTries -= 1

    def checkReturnValueOfCall(self, retVal):
        """Methods check normal subprocess call result. 1 means failure, 0 means success
        If the fe solver returns special codes, please overwrite this method in derived subclass for the used fe solver
        """
        if retVal == 1:
            log.error(f'The {retVal} return code "{self.solverName}" indicates errors. Please check the logfile.')
            return False
        return True

    def _getNumberOfCores(self):
        return self._useNumberOfCores

    def _setNumberOfCores(self, numCores):
        self._useNumberOfCores = numCores

    def _getJobName(self):
        if self._jobName is None:
            self._jobName = os.path.basename(os.path.splitext(self.feFilename)[0])

        return self._jobName

    def _setJobName(self, jobName):
        self._jobName = jobName

    useNumberOfCores = property(fget=_getNumberOfCores, fset=_setNumberOfCores)
    jobName = property(fget=_getJobName, fset=_setJobName)


class AnsysCaller(FECaller):

    solverName = "Ansys"

    def __init__(self, **kwargs):

        FECaller.__init__(self, **kwargs)

        # running ansys
        os.environ["ANS_CONSEC"] = "YES"

        ansPath = os.path.normpath(ansysPath)
        if not os.path.exists(ansPath):
            ansPath = self.findAnsysExecutable()

        self.localCmds = [
            ansPath,
            "-o",
            "ansys.log",
            "-i",
            os.path.join(self.runDir, os.path.basename(self.feFilename)),
            "-b",
            "-np",
            str(self.useNumberOfCores),
            "-j",
            "<jobName>",
            "-m",
            "1200",
            "-db",
            "64",
            "-p",
            ansysLicense,
        ]

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        basePath = os.path.dirname(self.feFilename)
        baseName = jobName if jobName else os.path.splitext(os.path.basename(self.feFilename))[0]
        allerrs = glob.glob(os.path.join(basePath, baseName + "[0-9].err"))
        if not allerrs:
            errorFile = os.path.join(basePath, baseName + ".err")
        else:
            errorFile = allerrs[0]

        return errorFile, re.compile(r"\*{3} ERROR \*{3}", RE_MULTILINE)

    def findAnsysExecutable(self):
        """doc"""
        if "win" in sys.platform:

            os_env_key, ansysPath = next(
                ((key, value) for key, value in os.environ.items() if re.match(r"ANSYS\d+_DIR", key)), (None, None)
            )
            if ansysPath is None:
                return None
            versNum = re.findall(r"\d+", os_env_key)[0]
            return os.path.join(ansysPath, "bin", "winx64", "ANSYS%s.exe" % versNum)

        elif "linux" in sys.platform:
            anysdis = shutil.which("ansysdis")
            ansysVersion = re.search(r"/v(\d+)/ansys/bin", anysdis).group(1)
            return os.path.join(os.path.dirname(anysdis), "ansys%s" % ansysVersion)
        else:
            return None

    def checkReturnValueOfCall(self, retVal):
        """doc"""
        if retVal == 7:
            msg = 'Ansys return code is "7".This indicates license problems. '
            msg += "Please see ansys error file for more information."
            log.error(msg)

        if retVal in [0, 1]:
            msg = f'The ansys return code "{retVal}" indicates errors within ansys. '
            msg += "Please check the logfile."
            log.error(msg)

        return retVal

    @staticmethod
    def isLicenseAvailable():
        """
        This method returns if there is at least 1 ansys token available
        """
        licenseServerString = "1055@ansyssz1.intra.dlr.de"
        log.info("Check Ansys license availability.")
        return 1 <= availableFlexlmLicenseTokens(licenseServerString, ansysLicense)

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        baseFileInDir = os.path.basename(self.feFilename)
        base, _ = os.path.splitext(baseFileInDir)
        ansysCall = [
            "ansys241",
            "-o",
            "ansys.log",
            "-i",
            baseFileInDir,
            "-b",
            "-np",
            str(self.useNumberOfCores),
            "-j",
            base,
            "-m",
            "1200",
            "-db",
            "64",
            "-p",
            ansysLicense,
        ]
        runScriptCmds = []
        if "cara" in self.clusterName:
            runScriptCmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module load ansys/2024r1",
            ]

        runScriptCmds.append(" ".join(ansysCall))

        return runScriptCmds


class ParallelAnsysCaller(AnsysCaller):
    def __init__(self, **kwargs):
        """Derived ansys caller for parallel use
        Used for parallel calculation on CASE within Victoria but unless the
        model complexity does not exceed the computational ressources it can be used
        on any local machine (no remote call to cluster tested at the moment"""
        AnsysCaller.__init__(self, **kwargs)

        # running ansys
        os.environ["ANS_CONSEC"] = "YES"

        # command to enable multiple ansys instances to run on the same input file
        self.preCommands = ["setenv ANSYS_LOCK OFF"]

        # remove option because it is only useful on small memory systems
        dbFlag = self.localCmds.index("-db")
        self.localCmds = self.localCmds[:dbFlag] + self.localCmds[dbFlag + 2 :]

        memoryFlag = self.localCmds.index("-m")
        self.localCmds[memoryFlag + 1] = "2048"

    def setAnsysLogFile(self):
        """doc"""
        logFileIndxLocal = self.localCmds.index("-o")

        if logFileIndxLocal != -1:
            runIndex = self.feFilename.rsplit("_", 1)[-1].split(".", 1)[0]
            self.localCmds[logFileIndxLocal + 1] = f"ansys_{runIndex}.log"

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        basePath = os.path.dirname(self.feFilename)
        baseName = jobName if jobName else os.path.splitext(os.path.basename(self.feFilename))[0]
        errorFile = os.path.join(basePath, baseName + ".err")
        if not os.path.exists(errorFile):
            errorFile = ""

        return errorFile, re.compile("ERROR", RE_MULTILINE)

    def checkReturnValueOfCall(self, retVal):
        """doc"""
        jobName = os.path.splitext(os.path.basename(self.feFilename))[0]
        numberOfTries = 240

        while retVal == 7 and numberOfTries > 0:
            msg = 'Ansys return code is "7".This indicates license problems. '
            msg += "Please see ansys error file for more information."
            log.warning(msg)

            time.sleep(15)
            numberOfTries -= 1
            log.info("Start Ansys again!")

            retVal = self.runLocal(jobName)

        if retVal in [0, 1]:
            msg = f'The ansys return code "{retVal}" indicates errors within ansys. '
            msg += "Please check the logfile."
            log.error(msg)

        return retVal


class NastranCaller(FECaller):

    solverName = "Nastran"

    def __init__(self, **kwargs):
        """doc"""
        FECaller.__init__(self, **kwargs)

        nastran_exe = shutil.which("nastran")
        if not nastran_exe:
            nastran_exe = nastranPath

        self.localCmds = [
            nastran_exe,
            os.path.basename(self.feFilename),
            f"parallel={self.useNumberOfCores}",
            "scratch=yes",
            "old=no",
            "system(363)=1",
            f"sdirectory={self.runDir}",
        ]

        if platform.system() == "Linux":
            self.localCmds.insert(5, "batch=no")

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        baseFileInDir = os.path.basename(self.feFilename)
        if self.clusterName == "cara":
            # user defined environment variable
            cara_partion = os.environ.get("CARA_PARTITION", "ppp")
            useNumFECores = 1 if cara_partion == "ppp" else self.useNumberOfCores
        else:
            useNumFECores = self.useNumberOfCores

        runCmds = []
        if "cara" in self.clusterName:
            runCmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module load nastran/2023.2",
            ]
        runCmds.append(
            f"nast20232 {baseFileInDir} parallel={useNumFECores} scratch=yes old=no sdirectory=$(pwd)"
        )  # "system(363)=1")
        return runCmds

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        outFlag = re.search(r"out=(.*?)(\s|\Z)", " ".join(self.localCmds))
        dirname, base_file = os.path.split(self.feFilename)
        if outFlag:
            dirname = os.path.join(dirname, outFlag.group(1))

        basename = os.path.join(dirname, os.path.splitext(base_file)[0] + ".f06")

        return basename, re.compile(r"(?<!(IF THE FLAG IS ))FATAL", RE_MULTILINE)

    @staticmethod
    def isLicenseAvailable():
        """This method returns if there is at least 1 nastran token available"""
        licenseServer = "1700@nastransz2.intra.dlr.de"

        log.info("Check Nastran license availability.")
        return 13 <= availableFlexlmLicenseTokens(licenseServer, "MSCONE")


class AbaqusCaller(FECaller):
    """This class realizes an interface to Abaqus"""

    clusterAbaqusName = "abq2023"
    solverName = "Abaqus"

    def __init__(self, **kwargs):
        FECaller.__init__(self, **kwargs)
        # eclipse adds some env variabels that do not work with abaqus
        os.environ.pop("PYTHONIOENCODING", None)

        # scratch file dir set due to error with abaqus not able to create the temp dir in c:users ...
        tmpScratchFilesPath = os.path.join(self.runDir, "abaqusScratch")
        if os.path.exists(tmpScratchFilesPath):
            shutil.rmtree(tmpScratchFilesPath)

        os.makedirs(tmpScratchFilesPath, exist_ok=True)

        self.localCmds = [
            kwargs.pop("abaqusPath", abaqusPath),
            f"job={self.jobName}",
            "interactive",
            "-scratch",
            "abaqusScratch",
            "-cpus",
            str(self.useNumberOfCores),
        ]

    def checkReturnValueOfCall(self, retVal):
        """doc"""
        if retVal == 1:
            msg = f'The abaqus return code "{retVal}" indicates errors within abaqus. '
            msg += "Please check the logfile."
            log.error(msg)
            return False
        return True

    def runLocal(self, jobName, **kwargs):
        """doc"""
        if "-cpus" in self.localCmds:
            cpuNumsParam = self.localCmds.index("-cpus")
            self.localCmds[cpuNumsParam + 1] = str(self.useNumberOfCores)
        return super().runLocal(jobName, **kwargs)

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        basePath = os.path.dirname(self.feFilename)
        baseName = jobName if jobName else self.jobName
        useMsgFile = True
        if useMsgFile:
            filename = os.path.join(basePath, baseName + ".msg")
            errorPattern = re.compile(r"\*{3}ERROR|Errno\s\d+", RE_MULTILINE)
        else:
            filename = os.path.join(basePath, baseName + ".dat")
            errorPattern = re.compile(r"(error|Error|Errno\s\d+)", RE_MULTILINE)
        return filename, errorPattern

    @staticmethod
    def isLicenseAvailable(licenseType="abaqus", requiredTokens=5):
        """Abaqus uses it's own license queue. To utilize it, this method returns no license information"""
        return True

    #         licenseServerString = '27018@abaqussd1.intra.dlr.de'
    #         log.info('Check Abaqus license availability.')
    #         return requiredTokens <= availableFlexlmLicenseTokens(licenseServerString, licenseType)

    @staticmethod
    def getMaxNumberOfParallelExecutions(licenseType="abaqus", requiredTokens=5):
        """This method returns the actual number of parallel executions that are possible as int

        For a parameter description, please refer to "availableFlexlmLicenseTokens".
        """
        licenseServerString = "27018@dldeffmimp04lic"
        log.debug("Check Abaqus license availability - Max number.")
        numLic = availableFlexlmLicenseTokens(licenseServerString, licenseType) // requiredTokens
        log.debug(f"Number of possible abaqus runs: {numLic}")
        return numLic

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        baseFileInDir = os.path.basename(self.feFilename)
        cmds = []
        if "cara" in self.clusterName:
            cmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module load abaqus/2023",
                f"touch {jobName}.msg",
            ]
        cmds.append(
            f"{self.clusterAbaqusName} job={baseFileInDir} interactive -scratch abaqusScratch -cpus {self.useNumberOfCores}"
        )
        return cmds


class AbaqusPythonCaller(AbaqusCaller):
    """This class realizes an interface to Abaqus to call a Python script in an specified directory with the specified
    input filename.

    .. note::
        "from abaqus import *" is not possible with this call. Use AbaqusPythonCaeCaller instead!

    :param pythonSkriptPath: name of Abaqus Python input file optionally with relative or absolute path
    :param arguments: list of arguments passed on to the script
                      i.e. -odb odbFilename.odb -> ['-odb', 'odbFilename.odb']"""

    def __init__(self, **kwargs):
        AbaqusCaller.__init__(self, **kwargs)
        cae = kwargs.pop("cae", False)
        self.solverName = "AbaqusPython" if not cae else "AbaqusCaePython"
        # eclipse adds some env variabels that do not work with abaqus
        os.environ.pop("PYTHONIOENCODING", None)

        self.pythonScriptPath = kwargs.pop("pythonSkriptPath", None)
        if not self.pythonScriptPath:
            raise ImproperParameterError("python script was not given!")

        callParams = [kwargs.pop("abaqusPath", abaqusPath)]
        if not cae:
            callParams += ["python", self.pythonScriptPath]
        else:
            # instead of "noGUI" use "script" if cae should be opened in gui mode (it does not close automatically with "script")
            callParams += ["cae", "noGUI=" + self.pythonScriptPath]

        # cae requires "--" to separate cae args from python args.
        # Python args are not allowed to have "--" in the strings such as "--runDir"
        prependArgs = ["--"] if cae else []

        callParams += prependArgs + kwargs.pop("arguments", [])
        self.localCmds = callParams

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        baseFile, ext = os.path.splitext(os.path.basename(self.feFilename))

        pyScriptBaseDir = os.path.dirname(self.pythonScriptPath)
        pyScriptBaseFile = os.path.basename(self.pythonScriptPath)

        if pyScriptBaseDir != self.runDir:
            shutil.copy(self.pythonScriptPath, self.runDir)

        callParms = self.localCmds[1:]
        if "cae" in callParms[0]:
            callParms[1] = "noGUI=" + pyScriptBaseFile
        else:
            callParms[1] = pyScriptBaseFile

        runScriptCmds = []
        if "cara" in self.clusterName:
            runScriptCmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module load abaqus/2023",
                f"touch {jobName}.msg",
            ]

        runScriptCmds.append(f"basefile={baseFile}")

        if ext == ".odb":
            runScriptCmds += [
                "mv $basefile.odb $basefile_old.odb",
                "abaqus -upgrade -job $basefile -odb $basefile_old.odb > upgrade.log",
                'if grep -Fq "NO NEED TO UPGRADE" upgrade.log;',
                "  then",
                "    mv $basefile_old.odb $basefile.odb",
                "fi",
            ]

        runScriptCmds += ["abq2023 " + " ".join(callParms)]

        return runScriptCmds

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        basePath = os.path.dirname(self.feFilename)
        filename = os.path.join(basePath, "_err.log")
        errorPattern = re.compile(r"Error:", RE_MULTILINE)
        return filename, errorPattern


class AbaqusPythonCaeCaller(AbaqusPythonCaller):
    """This class realizes an interface to AbaqusCAE to call a Python script in an specified directory with the specified
    input filename.
    :param pythonSkriptPath: name of Abaqus Python input file optionally with relative or absolute path
    :param arguments: list of arguments passed on to the script
        i.e. -odb odbFilename.odb -> ['-odb', 'odbFilename.odb']

    """

    def __init__(self, **kwargs):
        kwargs["cae"] = True
        AbaqusPythonCaller.__init__(self, **kwargs)


class B2000ppCaller(FECaller):

    solverName = "B2000++"

    def __init__(self, **kwargs):
        """doc"""
        FECaller.__init__(self, **kwargs)

        b2000Run = shutil.which("b2000++")
        if not b2000Run:
            b2000Run = "b2000++"

        self.localCmds = [b2000Run, self.feFilename]

        self.subcaseNumber = kwargs.get("runSubcase", 1)
        self.workingDir = kwargs.get("feWorkDir", self.runDir)
        self.b2k_toolName_cara = kwargs.get("b2k_toolName_cara", "b2000++/4.6.3")

    def runLocal(self, jobName, **kwargs):
        """doc"""
        base, ext = os.path.splitext(self.feFilename)
        flag_modified = False
        if ".bdf" == ext:
            converter = B2000FromBDFConverter(self.feFilename)
            converter.runLocal(jobName)
            flag_modified = True
            self.feFilename = f"{base}.mdl"

        if self.workingDir != self.runDir:

            dbCreator = B2000ModelToDatabase(feWorkDir=self.workingDir)
            dbCreator.runLocal(jobName)
            basename = os.path.basename(self.feFilename)
            base2, _ = os.path.splitext(basename)
            self.feFilename = os.path.join(self.workingDir, f"{base2}.b2m")
            flag_modified = True

        if flag_modified:

            self.localCmds = [self.localCmds[0], self.feFilename]

        return FECaller.runLocal(self, jobName, **kwargs)

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""

        baseFileInDir = os.path.basename(self.feFilename)
        baseFile, ext = os.path.splitext(baseFileInDir)

        runScriptCmds = []
        if "cara" in self.clusterName:

            runScriptCmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module use /sw/DLR/FA/BS/STM/modulefiles",
                f"module load {self.b2k_toolName_cara}",
            ]

        if ext == ".bdf":
            runScriptCmds.append(f"b2convert_from_nas {baseFileInDir} {baseFile}.mdl")

        runScriptCmds += [
            f"b2ip++ {baseFile}.mdl",
            f"b2000++ {baseFile}.b2m",
            f"mv {baseFile}.b2m/log.txt {jobName}.log",
        ]

        if "b2mconv.py" in os.listdir(self.runDir):

            runScriptCmds.append(f"python b2mconv.py {baseFile}.b2m -o {baseFile}.pkl")

        return runScriptCmds

    def getErrorFileAndErrorPattern(self, jobName):
        """doc"""
        errorFile = os.path.join(self.runDir, f"{jobName}.log")
        if not os.path.exists(errorFile):
            errorFile = ""

        return errorFile, re.compile("CRITICAL|error|ERROR|Invalid", RE_MULTILINE)


class B2000ModelToDatabase(B2000ppCaller):

    solverName = "b2ip++"

    def __init__(self, **kwargs):

        B2000ppCaller.__init__(self, **kwargs)

        b2ipTool = shutil.which("b2ip++")
        if not b2ipTool:
            b2ipTool = "b2ip++"

        basename = os.path.basename(self.feFilename)
        base, _ = os.path.splitext(basename)

        workingDir = kwargs.pop("feWorkDir", os.path.dirname(self.feFilename))
        dbFile = os.path.join(workingDir, f"{base}.b2m")

        self.localCmds = [b2ipTool, self.feFilename, dbFile]

    def runLocal(self, jobName, **kwargs):
        """doc"""
        return FECaller.runLocal(self, jobName, **kwargs)


class B2000FromBDFConverter(B2000ppCaller):

    solverName = "b2convert_from_nas"

    def __init__(self, **kwargs):

        B2000ppCaller.__init__(self, **kwargs)

        b2convTool = shutil.which("b2convert_from_nas")
        if not b2convTool:
            b2convTool = "b2convert_from_nas"

        toMdlFile = kwargs.pop("toMdlFile", None)
        if toMdlFile is None:
            base, _ = os.path.splitext(self.feFilename)
            toMdlFile = f"{base}.mdl"

        self.localCmds = [b2convTool, self.feFilename, toMdlFile]

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        baseFileInDir = os.path.basename(self.feFilename)
        baseFile, _ = os.path.splitext(baseFileInDir)

        runScriptCmds = [
            "module load env/spack",
            "module load rev/23.05_r8",
            "module use /sw/DLR/FA/BS/STM/modulefiles",
            "module load b2000++/4.6.3",
            f"b2convert_from_nas {baseFileInDir} {baseFile}.mdl",
        ]
        return runScriptCmds


class OpenRadiossCaller(FECaller):

    solverName = "OpenRadioss"

    def __init__(self, **kwargs):
        """doc"""
        FECaller.__init__(self, **kwargs)
        self.__engineFile = self.feFilename.replace("0000.rad", "0001.rad")
        if not os.path.exists(self.__engineFile):
            raise FileNotFoundError(f"Engine file {self.__engineFile} does not exist")

        self.localCmds = []
        self.remoteCmds = []
        self.numThreadsOMP = kwargs.pop("numThreadsOMP", 2)

    def generateSolverSpecificRemoteCmds(self, jobName):
        """doc"""
        runScriptCmds = []
        if "cara" in self.clusterName:

            runScriptCmds += [
                "module load env/spack",
                "module load rev/23.05_r8",
                "module use /sw/DLR/FA/BS/STM/modulefiles",
                f"module load OpenRadioss",
                f"export OMP_NUM_THREADS={self.numThreadsOMP}",
                "export OMP_STACKSIZE=400m",
                f"starter_linux64_gf -i {self.feFilename} -np 1 -nt {self.numThreadsOMP}",
                f"engine_linux64_gf_ompi -i {self.__engineFile} -nt {self.numThreadsOMP}",
                'find . -name "*A[0-9]*" -print0 | xargs -i -0 bash -c "anim_to_vtk_linux64_gf {} > {}.vtk"',
            ]

        else:
            raise Exception("Unknown cluster name")

        return runScriptCmds


class AsterCaller(FECaller):

    solverName = "Code-Aster"

    def __init__(self, **kwargs):

        FECaller.__init__(self, **kwargs)

        asterBat = kwargs.pop("as_run_script", shutil.which("as_run"))
        if not asterBat:
            raise Exception("Cannot find as_run script to run a code aster study")

        self.localCmds = [asterBat, "--run", self.feFilename]
        self.remoteCmds = []

    def runLocal(self, jobName, **kwargs):
        """doc"""
        self.localCmds = [jobName if elem == "<jobName>" else elem for elem in self.localCmds]

        cmd = " ".join(self.localCmds)
        log.info(f"call {self.solverName} locally ")
        log.debug(f"call {self.solverName} with the following command: {cmd}")

        if "win" in sys.platform:
            as_run_file = self.localCmds[0]
            if not os.path.exists(as_run_file):
                msg = "The given executable does not exist. "
                msg += "Please enter the correct path to settings.py. "
                msg += f"Acutal path: {as_run_file}"
                raise InternalError(msg)

        p = subprocess.Popen(
            self.localCmds, cwd=self.runDir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, output_err = p.communicate()
        p.wait()

        retVal = p.returncode
        if retVal != 0:

            prefix = os.path.splitext(self.feFilename)[0]
            logFileAster = os.path.join(self.runDir, f"{prefix}_aster_out.log")
            logFileAsterErr = os.path.join(self.runDir, f"{prefix}_aster_err.log")

            with open(logFileAster, "w") as f:
                f.write(output.decode("utf-8", "ignore").strip())

            if any("SLURM" in key for key in os.environ.keys()):
                """Write all outputs to one file to reduce File I/O on HPC"""
                write_mode = "a"
                logFileAsterErr = logFileAster
            else:
                write_mode = "w"

            with open(logFileAsterErr, write_mode) as f:
                f.write(output_err.decode("utf-8", "ignore").strip())

        log.info(f'return value of {self.solverName} call is "{retVal}"')
        return retVal

    def checkResultLogFile(self, jobName):
        return True


class VegaCaller(FECaller):

    solverName = "Vega"

    def __init__(self, **kwargs):
        FECaller.__init__(self, **kwargs)

        vega_executable = kwargs.pop("vega_executable", shutil.which("vegapp"))
        if not vega_executable:
            raise Exception("Cannot find vegapp to convert fe files to code-aster")

        as_run_script = kwargs.pop("as_run_script", shutil.which("as_run"))
        availAsterVers = self.getAvailableAsterVersions(availAsterVers=True, as_run_script=as_run_script)

        asterVersion = next((vers for vers in availAsterVers if vers != "testing"), "testing")
        self.localCmds = [
            vega_executable,
            "-o",
            self.runDir,
            "--solver-version",
            asterVersion,
            self.feFilename,
            "nastran",
            "aster",
        ]
        self.remoteCmds = []

    def getAvailableAsterVersions(self, raiseOnError=False, as_run_script=None):
        """doc"""
        if as_run_script is None:
            as_run_script = shutil.which("as_run")

        if not as_run_script and raiseOnError:
            raise Exception("Code-Aster not found in system path")

        p = subprocess.run([as_run_script, "--info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        describe = p.stderr if p.stdout == b"" else p.stdout
        describe = describe.decode("utf-8").strip()
        pattern = re.compile("@VERSIONS@(.*?)@FINVERSIONS@", re.RegexFlag.DOTALL)
        res = pattern.search(describe).group(1)

        versions = re.findall(r"(?<=vers : )([\w\._-]+)", res, re.RegexFlag.MULTILINE)
        return versions

    @staticmethod
    def isLicenseAvailable():
        """
        Code Aster does not need any license! :-)
        """
        return True


def availableFlexlmLicenseTokens(licenseServerString, licenseType):
    """This method returns the number of available license tokens for a specific flexlm-based
    licensing system.

    :param licenseServerString: string to the flexlm server including port
    :param licenseType: type of license. It is the name after "Users of"
    """
    lmutilExe = _checkLmutils()
    lmutilStdout, lmutilStderr = _callLmUtils(licenseServerString, lmutilExe=lmutilExe)
    return _parseLmUtilsReturn(lmutilStdout, lmutilStderr, licenseType)


def _checkLmutils():
    """This method checks if lmutils can be found on the system path.

    :return: None
    :raise FileNotFoundError: if "lmutil" was not found on the system path or in the current dir
    """
    lmutilPath = shutil.which("lmutil")
    if lmutilPath is None:
        msg = '"lmutil" was not found on the system path to perform a license check. '
        msg += "Please provide the path to lmutil in the system path."
        raise FileNotFoundError(msg)

    return lmutilPath


def _callLmUtils(licenseServerString, lmutilExe="lmutil"):
    """doc"""

    lmTools = subprocess.Popen([lmutilExe, "lmstat", "-a", "-c", licenseServerString], stdout=subprocess.PIPE)
    lmutilStdout, lmutilStderr = lmTools.communicate()
    return lmutilStdout, lmutilStderr


def _parseLmUtilsReturn(lmutilStdout, lmutilStderr, licenseType):
    """doc"""
    if lmutilStderr is None:
        lmOutString = str(lmutilStdout.decode("utf-8"))
        licenseLine = f"Users of {licenseType}"
        for line in lmOutString.split("\n"):
            if licenseLine in line:
                # Count number of licenses available and used
                numbers = array(re.findall(r"\d+", line), dtype=int)
                if len(numbers) < 2:
                    log.warning(f'License state of type {licenseType} could not be obtained. Got this line : "{line}"')
                    return 0
                return numbers[0] - numbers[1]

        log.warning(f"could not find licenseType: {licenseType}")
        log.debug("Flexlm output: " + str(lmutilStdout))
        return 0
    else:
        # this is the stderr part - it should be empty
        raise BaseException("problems with return from license server")


def run_fe_cli():
    """doc"""
    parser = argparse.ArgumentParser(description="Run FE Model")
    parser.add_argument("feFile")
    parser.add_argument("-r", "--calc_remote", action="store_true", dest="calc_remote")
    parser.add_argument("-u", "--user_remote", type=str, dest="user_remote")

    options = parser.parse_args()
    feFile = os.path.abspath(options.feFile)
    _, ext = os.path.splitext(feFile)
    if ext == ".bdf":
        fecallClass = NastranCaller
    elif ext == ".mdl":
        fecallClass = B2000ppCaller
    elif ext == ".inp":
        fecallClass = AbaqusCaller
    elif ext in [".mac", ".ans"]:
        fecallClass = AnsysCaller
    else:
        msg = f"Unknown file extension: {ext}. The following extensions and tools are supported:\n"
        msg += "Abaqus: .inp\n"
        msg += "Nastran: .bdf\n"
        msg += "B2000++: .mdl\n"
        msg += "ANSYS: .mac|.ans\n"
        raise Exception(msg)

    if options.calc_remote and (options.user_remote is None):
        msg = "FE model should be executed remote on CARA but no username was given as parameter. "
        msg += "Please specify the username using the option '-u <USERNAME>' ."
        raise Exception(msg)

    fecall = fecallClass(feFilename=feFile)
    fecall.run(doRemoteCall=options.calc_remote)


if __name__ == "__main__":
    print(NastranCaller.isLicenseAvailable())
    #    AbaqusCaller.isLicenseAvailable()
    #    AnsysCaller.isLicenseAvailable()
    pass
