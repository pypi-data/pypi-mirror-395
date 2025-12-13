#!/usr/bin/env python3
# Utils for Chappyner package
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo

import logging, os, subprocess, signal
from importlib import metadata
import tempfile
from jinja2 import Template

from notifypy import Notify
import sys
if sys.version_info < (3, 10):
    import importlib_resources as resources
else:
    import importlib.resources as resources

from rich.panel import Panel
from rich.console import Console

def print_logo(logo_style, version_style):
    """ Print Chappyner logo. It accepts all the styles rules for the
    Rich package (https://rich.readthedocs.io/en/latest/style.html).
    The Chappyner version is also printed.

    Parameters
    ----------
    logo_style : str
        Style rules for logo
    version_style: str
        Style rules for version
    """
    # Retrieve version from pyproject.toml and apply Rich style
    ver = f"[{version_style}]version {metadata.version('chappyner')}[/{version_style}]"

    # Print logo with version embedded
    rprint(f"""
╭──────╮╭─╮
│      ││ │─╮╭───╮╭────╮╭────╮╭─╮ ╭─╮╭───╮╭───╮╭───╮
│   ───┤│   ││ . ││  . ││  . ││ ╰─╯ ││ │ ││ -_╯│ ╭─╯
╰──────╯╰─┴─╯╰─┴─╯│  ╭─╯│  ╭─╯╰─╮ ╭─╯╰─┴─╯╰───╯╰─╯
                  ╰──╯  ╰──╯    ╰─╯
{ver}
    """, text_style=logo_style)


def render_j2(template, **dictionary):
    """ Take a string containing Jinja2 placeholders and return a new
    rendered string (see examples below).

    Parameters
    ----------
    template : str
        It can (should) contains Jinja2 placeholders
    **dictionary : dict, optional
        Values to be rendered can be passed here

    Returns
    -------
    str
        Rendered Jinja2 string

    Examples
    --------
    ## All the followings will print 'Hello foo and bar'

    # Render j2 string passing optional arguments
    render_j2("Hello {{ var1 }} and {{ var2 }}", var1='foo', var2='bar')

    # Render j2 string unpacking a dictionary
    somedictionary = {'var1' : 'foo', 'var2' : 'bar'}
    render_j2("Hello {{ var1 }} and {{ var2 }}", **somedictionary)

    # Render j2 string using Python local variables
    var1 = 'foo'
    var2 = 'bar'
    render_j2("Hello {{ var1 }} and {{ var2 }}", **locals())
    """
    return Template(template).render(**dictionary)


def rprint(text, text_style='', title=None, subtitle=None, border_style=None, prepend=''):
    """ Print text using Rich style format. Text can be also wrapped in
    a panel if title, subtitle and/or border_style are provided. Check
    https://rich.readthedocs.io/en/latest/style.html for Rich style
    format, and
    https://rich.readthedocs.io/en/stable/appendix/colors.html for
    colors. Any combination of styles and colors can be set as default
    in the text_style and border_style parameter, but also used inline
    with Rich syntax (e.g. [bold green]Your text[/bold green]).

    Parameters
    ----------
    text : str
        The text content to print
    text_style : str, optional
        Style of the text content
    title : str, optional
        Optional title of the panel
    subtitle: str, optional
        Optional subtitle of the Panel
    border_style : str, optional
        Style of the Panel border (e.g., 'red', 'bold green')
    prepend : str, optional
        Prepend a string to the text with no style rules applied
        (ignored if text is in a panel)
    """
    # Create a console (from Rich) which is self-contained inside this
    # function. This is not efficient since it initialize Console() once
    # again at every print, but is light enough to be better than
    # initializing useless global variable around in the main function
    console = Console()

    # Decide whether to use a Panel or simple text
    if title or subtitle or border_style:
        console.print(
            Panel(
                text,
                title=title,
                subtitle=subtitle,
                border_style=border_style or "yellow",
                style=text_style,
                expand=False,
                width=72
            )
        )
    else:
        console.print(f"[default]{prepend}[/default]" + text, style=text_style)


def notify(title, text, icon=None):
    """ Send notifications to user desktop and terminal, if supported

    Parameters
    ----------
    title : str
        Title to be shown in the notification
    text : str
        Text to be shown in the notification
    icon : str, optional
        Path of an image file to be shown as icon in the notification.
        The path is relative to the package directory. If not provided,
        the Python logo is shown.
    """
    # Send ASCII bell to notify terminal (if supported)
    print("\a", end="", flush=True)

    # Send notification to desktop (if supprted)
    notification = Notify()
    notification.title = title
    notification.message = text
    if icon:
        notification.icon = resources.files(__package__).joinpath(f"{icon}")

    logging.info(f"Sending desktop notification with\n - title: {title}\n - message: {text}\n - icon: {icon}")
    notification.send()


class LocalEngine():
    "Run single commands or scripts on local host."
    def command(self, cmd):
        """Run a local command and return stdout, stderr, and the exit
        code.

        Parameters
        ----------
        cmd : str
            Command to run

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        logging.info(f"=> Running command: {cmd}")
        result = subprocess.run(
            cmd,
            shell=True,           # True if passing a single string; False if passing a list
            capture_output=True,  # capture both stdout and stderr
            text=True             # return strings instead of bytes
        )
        logging.debug(f"rc of command execution: {result.returncode}")
        logging.debug(f"stdout of command execution: {result.stdout.strip()}")
        logging.debug(f"stderr of command execution: {result.stderr.strip()}")
        return {"out": result.stdout.strip(), "err": result.stderr.strip(), "rc": result.returncode}

    def tmpscript(self, script_content):
        """Save script_content to a temporary file, execute it
        respecting its shebang, and return stdout, stderr, returncode
        (and then delete the file).

        Parameters
        ----------
        script_content : str
            Content of the script to be run. The script is stored in the
            temporary directory of the system, with 700 permissions

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code'
        """
        # create temp file in /tmp (default on Linux) or %TEMP% (default on Windows)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(script_content.encode())
            tmp_path = tmp.name
        logging.info(f"Temporary file for startup script: {tmp_path}")

        # make it executable
        os.chmod(tmp_path, 0o700)

        try:
            # run it with self.command (the kernel handles the shebang)
            stream = self.command(tmp_path)
            logging.debug(f"rc of startup script execution: {stream['rc']}")
            logging.debug(f"stout of startup script execution: {stream['out']}")
            logging.debug(f"stderr of startup script execution: {stream['err']}")
            return stream
        finally:
            # remove the temp file
            os.unlink(tmp_path)
            logging.debug(f"Temporary file {tmp_path} removed")


class IgnoreCtrlC():
    """Disable Ctrl-C (SIGINT) in its context manager for Python
    process, subprocess.run and subprocess.Popen. Use it with
    caution for very restricted safe contexts, as it might forbid the
    user to kill the script (N.B. in Unix/Linux systems, if you really
    need to - not gracefully - terminate the execution you can still use
    Ctrl-\ for SIGQUIT).
    N.B. Overrides for subprocess use preexec_fn which is not portable
    on Windows.
    """
    def __init__(self, subprocesses=True):
        """Define if SIGINT, besides the main Python execution, has to
        be inhibited for the child processes from subprocess.run and
        subprocess.Popen too
        """
        self.subprocesses = subprocesses

    def __enter__(self):
        """Override SIGINT with SIG_IGN for Python; when requested, it
        does it also for subproces.run and subprocess.Popen
        """
        # Override SIGINT for Python process
        self._original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        # If requested, override SIGINT behaviour in child processes
        # spawned via subprocess library
        if self.subprocesses:

            # Override subprocess.run
            self._orig_run = subprocess.run
            def run_with_ignore(*args, **kwargs):
                kwargs.setdefault("preexec_fn", self._ignore_sigint)
                return self._orig_run(*args, **kwargs)
            subprocess.run = run_with_ignore

            # Override subprocess.Popen
            self._orig_popen_init = subprocess.Popen.__init__
            def popen_init_with_ignore(popen_self, *args, **kwargs):
                kwargs.setdefault("preexec_fn", self._ignore_sigint)
                self._orig_popen_init(popen_self, *args, **kwargs)
            subprocess.Popen.__init__ = popen_init_with_ignore

        logging.info("Ctrl-C inhibited")

    def __exit__(self, exc_type, exc_val, exc_tb):
        "Undo any override from __enter__() for SIGINT"

        # Restore original handler for Python process
        signal.signal(signal.SIGINT, self._original_handler)

        if self.subprocesses:
            # Remove override for subprocess.run
            subprocess.run = self._orig_run

            # Remove override for subprocess.Popen
            subprocess.Popen.__init__ = self._orig_popen_init

        logging.info("Ctrl-C restored")
        # Do not suppress exceptions
        return False

    @staticmethod
    def _ignore_sigint():
        """Helper used as preexec_fn to ignore SIGINT in subprocesses."""
        signal.signal(signal.SIGINT, signal.SIG_IGN)
