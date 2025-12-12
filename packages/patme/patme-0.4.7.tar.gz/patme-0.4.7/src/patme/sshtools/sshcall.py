# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Connect via python to a host using ssh and submit commands or copy files via sftp.

The following methods utilize a method to perform ssh calls by a public/private key(recommended) or by username/password.
Please refer to the method descriptions for further details. An example is also given in patme.sshtools.cara
"""
import getpass
import os
import shutil
import subprocess
from subprocess import PIPE, run

from patme.service.exceptions import ImproperParameterError
from patme.service.logger import log

_numberOfProtocolBannerExceptions = 0
userDir = os.path.expanduser("~")
privateKeyFileConfig = os.path.join(userDir, "id_rsa")  # might be overwritten by config reader


def callSSH(
    hostname,
    remoteCommand,
    privateKeyFile=privateKeyFileConfig,
    username=None,
    hostKeyString=None,
    keytype="ssh-rsa",
    port=None,
    printOutput=True,
):
    """This method creates an ssh connection to a host and executes a command remotely.

    :param hostname: Name of the host computer. Can be ip address or dns name.
    :param remoteCommand: This is a string containing the command to be executed on a
        linux machine. Be aware that the initial current directory is the home directory
        and one should first change to the directory that is actually used.
    :param username: name of the user on the host
    :param privateKeyFile: Path and name of the private rsa key. This key is used as
        private key for authentication. A copy of the corresponding public key
        must be present on the host in "~/.ssh/authorized_keys".
        A correct line in authorized_keys consists of the encryption type and the key: "ssh-rsa AAA....."
    :param hostKeyString: Key string of the host computer.
        Not required if the key is already in "~/.ssh/known_hosts".

        This is the key from the file "~/.ssh/known_hosts" used by openssh on a linux machine and usually starts with "AAA..."
    :param keytype: type of the ssh key for the hostKeyString ['ssh-rsa','ssh-dss']
    :param port: port number of the host computer to connect to.
    :param printOutput: Flag if the ssh output should be output. Defaults to True
    :return: string, output from host
    """
    if hostKeyString:
        _expandKnownHostsFile(hostname, hostKeyString, port, keytype)

    callArgs = [shutil.which("ssh")]

    ssh_alias = os.environ.get("PATME_SSH_ALIAS", None)
    if ssh_alias is None:
        if (privateKeyFile is not None) and os.path.exists(privateKeyFile):
            callArgs += ["-i", privateKeyFile]

        callArgs += ["-o", "BatchMode=true"]
        if port:
            callArgs += ["-p", str(port)]
        if not username:
            username = getpass.getuser()
        callArgs += [f"{username}@{hostname}", remoteCommand]

    else:
        callArgs += [ssh_alias, remoteCommand]

    log.info("Call ssh: " + " ".join(callArgs))
    result = run(callArgs, stdout=PIPE, stderr=PIPE, universal_newlines=True, encoding="latin-1", errors="ignore")
    rc, out, err = result.returncode, result.stdout, result.stderr

    if printOutput or rc != 0:
        log.info("SSH return string: \n" + out)
        if err:
            log.error("SSH error string:\n" + err)

    return out


def copyFilesSCP(
    files,
    hostname,
    privateKeyFile,
    username=None,
    srcBaseDir=".",
    destBaseDir=".",
    hostKeyString=None,
    mode="put",
    keytype="ssh-rsa",
    port=None,
):
    """Method copies files from a local machine into a remote directory via a SSH tunnel

    :param files: List of local files which are copied to the remote machine.
    :param hostname: Name of the host computer. Can be ip address or dns name.
    :param privateKeyFile: Path and name of the private rsa key. This key is used as
        private key for authentication.
    :param srcBaseDir: Source base directory of relative files to copy
    :param destBaseDir: Destination directory
    :param hostKeyString: Key string of the host computer.
        Not required if the key is already in "~/.ssh/known_hosts".
        This is the key from the file "~/.ssh/known_hosts" used by openssh on a linux machine and usually starts with "AAA..."
    :param mode: mode to copy to or from a remote machine (put,get)
    :param keytype: type of the ssh key for the hostKeyString ['ssh-rsa','ssh-dss']
    :param port: port number of the host computer to connect to.
    """
    if hostKeyString:
        _expandKnownHostsFile(hostname, hostKeyString, port, keytype)

    if mode not in ["put", "get"]:
        raise ImproperParameterError("wrong mode")

    sendList = [f if os.path.isabs(f) else os.path.join(srcBaseDir, f) for f in files]

    callArgs = [shutil.which("scp"), "-T"]
    ssh_alias = os.environ.get("PATME_SSH_ALIAS", None)
    if ssh_alias is None:

        if (privateKeyFile is not None) and os.path.exists(privateKeyFile):
            callArgs += ["-i", privateKeyFile]

        callArgs += ["-o", "BatchMode=true"]
        if port:
            callArgs += ["-p", str(port)]
        if not username:
            username = getpass.getuser()
        userAndHost = f"{username}@{hostname}:"
    else:
        userAndHost = f"{ssh_alias}:"

    if mode == "put":
        source = sendList
        dest = userAndHost + destBaseDir
    else:
        source = [f'{userAndHost}{" ".join(sendList)}']
        dest = destBaseDir

    callArgs += source + [dest]
    log.info("Call scp: \n" + " ".join(callArgs))

    out = subprocess.check_output(callArgs).decode()
    log.info("SCP result: " + out)

    return out


def _expandKnownHostsFile(hostname, hostKeyString, port="", keytype="ssh-rsa"):
    """Expands the known hosts file if neccessary"""
    sshFolder = os.path.join(os.path.expanduser("~"), ".ssh")
    if not os.path.exists(sshFolder):
        os.makedirs(sshFolder)
    knownHostsFile = os.path.join(sshFolder, "known_hosts")
    fileMode = "a" if os.path.exists(knownHostsFile) else "w"

    knownHostLine = f"[{hostname}]:{port}" if port else f"{hostname}"
    knownHostLine += f" {keytype} {hostKeyString}"

    knownHosts = []
    if os.path.exists(knownHostsFile):
        with open(knownHostsFile) as f:
            knownHosts = f.readlines()
    if any([knownHostLine in line for line in knownHosts]):
        # host already in knownHosts file
        return
    else:
        with open(knownHostsFile, fileMode) as f:
            if knownHosts and not (knownHosts[-1] == "" or knownHosts[-1][-1] == "\n"):
                f.write("\n")
            f.write(f"{knownHostLine}\n")


if __name__ == "__main__":
    pass
