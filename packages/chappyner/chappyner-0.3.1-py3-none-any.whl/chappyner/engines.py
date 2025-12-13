#!/usr/bin/env python3
# Utils for ssh connection in Chappyner package
# based on subprocess + openssh commands in the local system
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo

import logging, time
import subprocess, signal
from .utils import IgnoreCtrlC

import paramiko
from fabric import Connection
from sshtunnel import SSHTunnelForwarder
from invoke import UnexpectedExit


class BaseEngine():
    """Base class for all the engines, so that shared methods or class
    attributes can be added just once here and inherited in every
    engine, avoiding boilerplate code. It's not meant to be used
    directly.
    """
    def wait_file(self, file_path, poll_interval=5, timeout=10):
        """Poll a remote host via SSH until a file exists.

        Parameters
        ----------
        file_path : str
            Full path of the file to check on remote host
        poll_interval : int, optional
            Seconds between polls, default is five
        timeout : int, optional
            Max seconds to wait, default is ten

        Returns
        -------
        bool
            True when the file is found

        Raises
        ------
        TimeoutError
            If the file is not found before timeout expires
        """
        start = time.time()
        while True:
            # check file existence with a shell test
            stream = self.command(f"test -e {file_path} && echo OK || echo WAITING")

            if "OK" in stream['out']:
                return True  # file found

            if time.time() - start > timeout:
                raise TimeoutError(f"File {file_path} not found within {timeout}s")

            time.sleep(poll_interval)


class NoSocketEngine(BaseEngine):
    """Define remote hosts, on which you can run commands, wait for
    files appearing, or forward ports. This implementation relies on
    local openssh installation and run its commands via subprocess. By
    default it doesn't specify any socket, thus handhakes are constantly
    repeated. It is probably compliant, but not tested, with other SSH
    implementations than OpenSSH.
    """
    def __init__(self, host, user=None, keyfile=None):
        """Define host details and build the common part of every future
        ssh command toward the host (ssh_base_cmd, on top of which other
        arguments or options will be appended). The only mandatory
        parameter is the ssh host, which might be defined in
        ~/.ssh/config and thus including every detail of the ssh
        connection.

        Parameters
        ----------
        host : str
            remote host (IP or hostname or ssh config host)
        user : str, optional
            ssh username
        keyfile : str, optional
            path to a private key file to use
        """
        self.host, self.user, self.keyfile = host, user, keyfile

        self.ssh_base_cmd = ["ssh"]
        if self.keyfile:
            self.ssh_base_cmd += ["-i", self.keyfile]
        if self.user != None:
            self.ssh_base_cmd.append(f"{self.user}@{self.host}")
        else: # don't prepend user if not specified, since it's supposed to be in ssh config host
            self.ssh_base_cmd.append(f"{self.host}")
        logging.info(f'Base for ssh commands: {" ".join(self.ssh_base_cmd)}')

    def __enter__(self):
        "Placeholder to make class compliant as context manager"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        "Placeholder to make class compliant as context manager"
        return False

    def command(self, cmd, verbose=False):
        """Run a command on a remote host via SSH using subprocess.

        Parameters
        ----------
        cmd : str
            Shell command to execute remotely
        verbose : bool, optional
            Enable maximum verbosity for ssh

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        if verbose:
            ssh_cmd = self.ssh_base_cmd + ["-vvv", cmd]
        else:
            ssh_cmd = self.ssh_base_cmd + [cmd]

        logging.info(f'=> Running command: {" ".join(ssh_cmd)}')
        result = subprocess.run(
            ssh_cmd,
            shell = False,         # True if passing a single string; False if passing a list
            capture_output = True, # capture both stdout and stderr
            text = True            # return strings instead of bytes
        )
        logging.debug(f"rc of command execution: {result.returncode}")
        logging.debug(f"stdout of command execution: {result.stdout.strip()}")
        logging.debug(f"stderr of command execution: {result.stderr.strip()}")
        return {"out": result.stdout.strip(), "err": result.stderr.strip(), "rc": result.returncode}

    def test(self):
        """Test SSH connection running a test command remotely

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        return self.command("echo Connected to $HOSTNAME", verbose=True)

    def forward_port(self, local_address, local_port, node_address, node_port):
        """Forward remote node port on a local port. During the
        forwarding, the execution waits the user to press Enter (Ctrl-C
        is inhibited to avoid pressing it by mistake to copy-and-paste
        from terminal, killing Python)

        Parameters
        ----------
        local_address : str
            Local host; this is enforced (even if not mandatory in ssh
            syntax) to enhance security
        local_port : int
            Local port
        node_address : str
            Hostname/local ip of the compute node
        node_port : int
            node name and port to be forwarded, separated by columns

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        ssh_cmd = self.ssh_base_cmd + ["-N", "-L", f"{local_address}:{local_port}:{node_address}:{node_port}"]
        logging.info(f'=> Running command: {" ".join(ssh_cmd)}')

        try: # kills port forwarding at the end
            process = subprocess.Popen(
                ssh_cmd,
                shell = False,              # True if passing a single string; False if passing a list
                stdin = subprocess.DEVNULL, # avoids unexpected stalls (e.g. sometime socket engine would wait for user pressing Enter once again)
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True
            )

            # Barrier before killing the process (waits for user pressing Enter..,)
            logging.info(f"Remote {node_address}:{node_port} forwarded to {local_address}:{local_port} (until user presses Enter)")
            with IgnoreCtrlC(subprocesses=False):
                input()

        finally:
            # Kill the port forwarding process after Enter is pressed
            process.send_signal(signal.SIGINT)
            logging.info("Sent SIGINT to ssh to stop port forwarding")

        out, err = process.communicate()
        rc = process.returncode
        logging.debug(f"rc of command execution: {rc}")
        logging.debug(f"stdout of command execution: {out.strip()}")
        logging.debug(f"stderr of command execution: {err.strip()}")
        return {"out": out.strip(), "err": err.strip(), "rc": rc}


class SocketEngine(NoSocketEngine):
    """Define remote hosts, on which you can run commands, wait for
    files appearing, or forward ports. This implementation relies on
    local openssh installation and run its commands via subprocess. By
    default it uses ControlMaster capability from OpenSSH to avoid
    multiple handshakes and authentication requests. Sockets are created
    in $HOME/.chappyner/sockets, and deleted when the context manager
    exits (the empty directories stays there).
    """
    def __enter__(self):
        """Start socket using ~/.chappyner/sockets/<timestamp> as socket
        file
        """
        logging.info(f"Adding control master settings")
        # Build sockets dir in ~/.chappyner/sockets (but cross platform)
        from pathlib import Path
        from datetime import datetime

        home = Path.home()
        socket_dir = home / ".chappyner" / "sockets" # pathlib syntax (N.B. .chappyner is not hidden on Windows)
        socket_dir.mkdir(parents=True, mode=0o700, exist_ok=True)

        # Define socket file path inside it
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.socket_file_path = str(socket_dir / timestamp)
        logging.info(f"Socket file path: {self.socket_file_path}")

        # Add ControlPath to every command
        self.ssh_base_cmd += ["-S", self.socket_file_path]
        logging.info(f'New base for ssh commands: {" ".join(self.ssh_base_cmd)}')

        # Start socket with "ControlPersist=yes". Here Ctrl-C is
        # prevented because any KeyboardInterrupt exeption in the
        # context manager would be passed to Popen too, and this would
        # kill the socket manager before SocketEngine.__exit__()
        ssh_cmd = self.ssh_base_cmd + ["-N", "-M"]
        logging.info(f'=> Running command: {" ".join(ssh_cmd)}')

        with IgnoreCtrlC(subprocesses=False):
            self.socket_process = subprocess.Popen(
                ssh_cmd,
                shell = False, # True if passing a single string; False if passing a list
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True
            )

        # Wait for socket to be available, to avoid race condition with
        # the following ssh commands; this also act as barrier when
        # password is requested, since the socket is not created until
        # the correct password is passed
        ssh_cmd = self.ssh_base_cmd + ["-O", "check"]
        logging.info(f'=> Running command: {" ".join(ssh_cmd)} until success')
        socket_works = False # init
        while socket_works == False:
            wait_socket = subprocess.run(
                ssh_cmd,
                shell = False,         # True if passing a single string; False if passing a list
                capture_output = True, # capture both stdout and stderr
                text = True            # return strings instead of bytes
            )
            if int(wait_socket.returncode) == 0:
                socket_works = True
            else:
                #logging.debug(f"stdout: {wait_socket.stdout.strip()}")
                #logging.debug(f"sterr: {wait_socket.stderr.strip()}")
                time.sleep(1)
        logging.info("Socket ready")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        "Kill the control master when the context manager is over"

        # Quit the control master
        ssh_cmd = self.ssh_base_cmd + ["-O", "exit"]
        logging.info(f'=> Running command {" ".join(ssh_cmd)} to quit control master')
        subprocess.run(
            ssh_cmd,
            shell = False,         # True if passing a single string; False if passing a list
            capture_output = True, # capture both stdout and stderr
            text = True            # return strings instead of bytes
        )

        # Logs control master process
        logging.info(f"=> Logs for socket process:")
        out, err = self.socket_process.communicate()
        rc = self.socket_process.returncode
        logging.debug(f"rc of command execution: {rc}")
        logging.debug(f"stdout of command execution: {out}")
        logging.debug(f"stderr of command execution: {err}")

        return False


class ParamikoEngine(BaseEngine):
    """Define remote hosts, on which you can run commands, wait for
    files appearing, or forward ports. This implementation relies on
    Paramiko and its derivatives Fabric and Sshtunnel. It is a fully
    Python-native implementation independent from any SSH implementation
    in local host, but still experimental due to several open issues in
    Paramiko 4.0.0 (see patches in the code to workaround them)
    """
    def __init__(self, host, user=None, keyfile=None):
        """Define a set of operations to run on a remote host via SSH
        using Fabric. The only mandatory parameter is the ssh host,
        which might be defined in ~/.ssh/config and thus including every
        detail of the ssh connection.

        Parameters
        ----------
        host : str
            remote host (IP or hostname or ssh config host)
        user : str, optional
            ssh username
        keyfile : str, optional
            path to a private key file to use
        """
        self.user = user
        self.host = host
        self.connect_kwargs = {}
        if keyfile:
            self.connect_kwargs["key_filename"] = keyfile

        # Apply monkeypatch for paramiko
        self._monkeypatch_paramiko()

        # Apply monkeypatch for sshtunnel
        self._monkeypatch_sshtunnel()

    def __enter__(self):
        "Start connection to host"
        self.conn = Connection(
            host=self.host,
            user=self.user,
            connect_kwargs=self.connect_kwargs
        )

        if self.user:
            logging.info(f"Connected to {self.user}@{self.host}")
        else:
            logging.info(f"Connected to {self.host}")

        return self

    def __exit__(self, exc_type, exc, tb):
        "Close connection to host"
        if self.conn:
            try:
                self.conn.close()
                logging.info(f"Closed connection to {self.host}")
            except Exception as e:
                logging.exception("Error closing connection")
                return False # Returning False propagates exceptions from the with-block
        else:
            logging.error("Connection to {self.host} was already closed")

    def command(self, cmd):
        """Run a command on a remote host via SSH using subprocess.

        Parameters
        ----------
        cmd : str
            Shell command to execute remotely
        verbose : bool, optional
            Enable maximum verbosity for ssh

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        logging.info(f"=> Running command: {cmd}")
        try:
            result = self.conn.run(cmd, hide=True)
            logging.debug(f"rc of command execution: {result.exited}")
            logging.debug(f"stdout of command execution: {result.stdout.strip()}")
            logging.debug(f"stderr of command execution: {result.stderr.strip()}")
            return {"out": result.stdout.strip(), "err": result.stderr.strip(), "rc": result.exited}
        except UnexpectedExit as e:
            return {"out": e.result.stdout.strip(), "err": e.result.stderr.strip(), "rc": e.result.exited}

    def test(self):
        """Test SSH connection running a test command remotely

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        return self.command("echo Connected to $HOSTNAME")

    def forward_port(self, local_address, local_port, node_address, node_port):
        """Forward remote node port on a local port using sshtunnel.
        During the forwarding, the execution waits the user to press
        Enter (Ctrl-C is inhibited to avoid pressing it by mistake to
        copy-and-paste from terminal, killing Python)

        Parameters
        ----------
        local_address : str
            Local host; this is enforced (even if not mandatory in ssh
            syntax) to enhance security
        local_port : int
            Local port
        node_address : str
            Hostname/local ip of the compute node
        node_port : int
            node name and port to be forwarded, separated by columns

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        logging.info(f"Setting up SSH tunnel: {local_address}:{local_port} -> {node_address}:{node_port}")

        tunnel = SSHTunnelForwarder(
            (self.conn.host, self.conn.port or 22),
            ssh_username=self.conn.user,
            ssh_pkey=self.conn.connect_kwargs.get("key_filename"),
            allow_agent=True,
            remote_bind_address=(node_address, node_port),
            local_bind_address=(local_address, int(local_port)),
        )

        try:
            tunnel.start()
            logging.info(f"Remote {node_address} forwarded to {local_address} (until user presses Enter)")
            # Barrier before killing the process (waits for user pressing Enter..,)
            with IgnoreCtrlC():
                input()

        finally:
            # Kill the port forwarding process after that Enter is pressed
            tunnel.stop()
            logging.info("Tunnel stopped")

        return {"out": "", "err": "", "rc": 0}

    def _monkeypatch_paramiko(self):
        """Temporary fix for paramiko bug:
        https://github.com/paramiko/paramiko/issues/2462
        """
        def _override(self, key):
            if hasattr(key, "public_blob") and key.public_blob:
                return key.public_blob.key_type, key.public_blob.key_blob
            else:
                return key.get_name(), key
        paramiko.auth_handler.AuthHandler._get_key_type_and_bits = _override

    def _monkeypatch_sshtunnel(self):
        """Temporary fix for sshtunnel bug:
        https://github.com/pahaz/sshtunnel/issues/299
        """
        # It might worth to deprecate sshtunnel since it doesn't seem to
        # be mantained anymore, in favor of a paramiko-native solution:
        # https://github.com/paramiko/paramiko/blob/4.0.0/demos/forward.py
        # (or newer), or to embed it in Chappyner to keep it mantained
        if not hasattr(paramiko, "DSSKey"):
            paramiko.DSSKey = None
