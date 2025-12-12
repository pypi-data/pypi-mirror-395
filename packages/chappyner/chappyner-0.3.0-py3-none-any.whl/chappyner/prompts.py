#!/usr/bin/env python3
# User prompts for Chappyner package
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo

from InquirerPy import inquirer
from .utils import rprint
import sys

def ask_if_resume():
    """Ask the user if she/he wants to resume a job already queued or
    to start a new one

    Returns
    -------
    bool
        Whether to resume the tool (True) or not (False)
    """
    options = [
        "Resume a queued tool",
        "Start a new one",
    ]
    options.append("Exit")
    choice = inquirer.select(
        message = f"│ ╰─ Are you sure you want to start a new tool?",
        choices = options,
        qmark = "",
        amark = "",
        default = options[0]
    ).execute()

    if choice == options[0]:
        return True
    elif choice == options[1]:
        return False
    else: # Last option (2) is Exit
        rprint("Bye!", text_style = "bold blue", prepend="╰─── ")
        sys.exit(0)


def ask_resume_id(tools_history, active_tools):
    """Ask which (currently queued) tool has to be resumed

    Parameters
    ----------
    tools_history : dict
        Keys are job ids of tools already started; values are
        dictionaries which contains tool name, batch options and submit
        timestamp
    active_tools : dict
        It contains data about Chappyner tools currently in the
        scheduler queue; keys are their job ids, while values are their
        status Returns

    Returns
    -------
    int
        Job id of the tool to resume
    """
    if len(active_tools.keys()) == 1:
        return list(active_tools.keys())[0]

    else:
        options = [f"{tools_history[job_id]['tool']} in job {job_id}" for job_id in active_tools.keys()]
        options.append("Exit")
        choice = inquirer.select(
            message = f"├─── Which tool do you want to resume?",
            choices = options,
            qmark = "",
            amark = "",
            default = options[0]
        ).execute()

        if choice == options[-1]: # Last option is Exit
            rprint("Bye!", text_style = "bold blue", prepend="╰─── ")
            sys.exit(0)
        else:
            return list(active_tools.keys())[options.index(choice)]


def ask_if_cancel(job, cluster_name):
    """Ask if the current job has to be canceled or kept queued. In the
    former case, it directly cancel it.

    Parameters
    ----------
    job : int
        Current job
    cluster_name : string
        Cluster name from warehouse_inventory.yml
    """
    rprint(f"Job {job.id} is still ongoing on {cluster_name}", text_style="medium_purple", prepend = "╭─ ")
    options = [
        "Cancel it, I'm done!",
        "Keep it, I'll be back soon enough!",
    ]
    choice = inquirer.select(
        message = f"├─┬─ What do you prefer?",
        choices = options,
        qmark = "",
        amark = "",
        default = options[0]
    ).execute()

    if choice == options[0]:
        rprint(f"Canceling job {job.id}", text_style="grey50", prepend="│ ╰─ ")
        job.cancel()
    elif choice == options[1]:
        rprint(f"You can resume the tool just re-running Chappyner", prepend="│ ╰─ ")
