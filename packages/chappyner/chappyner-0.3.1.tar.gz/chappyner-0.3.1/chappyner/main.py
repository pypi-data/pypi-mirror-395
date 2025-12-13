#!/usr/bin/env python3
#  ______ __
# |      |  |--.---.-.-----.-----.--.--.-----.-----.----.
# |   ---|     |  _  |  _  |  _  |  |  |     |  -__|   _|
# |______|__|__|___._|   __|   __|___  |__|__|_____|__|
#                    |__|  |__|  |_____|
#
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo
"""
Chappyner is a Python code which allows to schedule and run web services
on compute node of a remote HPC clusters and expose them on your local
browser via SSH tunnels. The backend services are mainly (but not
necessarily) tought to be run via Apptainer/Singularity containers.
The main inspiration for Chappyner comes from Open Ondemand
(https://openondemand.org/), from which it inherits the main logics as
well as part of the codes that it uses on the remote side; Chappyner
replaces the Apache + nginx role in Open Ondemand with Python scripts +
tunnels, so that it can be easily run by any user on any HPC cluster
with no needs of root privileges. Please check the --help option and the
README for more details about Chappyner client and for the backend side
details.
"""

import sys, logging
from .utils import *
from .args import *
from .jobs import ToolJob, check_job_state, cleanup

def main():
    "Entry point for chappyner package"

    # Print logo
    print_logo(logo_style="bold blue", version_style="magenta")

    # Extract main variables from user's arguments. The
    # check_local() function handles all the options requiring local
    # operations (and might quit the program when those operations are
    # enough, e.g. with the --list-clusters option), whereas any option
    # requiring  is handled during this main() execution after the
    #  engine init via the check_remote() function
    try:
        batch_options, host, keyfile, list_tools, local_port, SshEngine, startup_script_content, tool, user, warehouse = check_local(*get_arguments())
    except InvalidOptions as e:
        rprint(f"{e}", title="Error", border_style="red")
        sys.exit(1)

    # Debug variables
    logging.info(f"Variables to be used during execution:\n-> host: {host}\n-> warehouse: {warehouse}\n-> user: {user}\n-> tool: {tool}\n-> list_tools: {list_tools}\n-> local_port: {local_port}\n-> keyfile: {keyfile}\n-> batch_options: {batch_options}\n-> startup_script_content (follows below):\n--------\n{startup_script_content}\n--------")

    # Initialize local engine for local commands
    local = LocalEngine()

    # Run startup script if present (either from user's options or from
    # cluster defaults)
    if startup_script_content:
        rprint("Running startup script to ease access on the chosen cluster", text_style="grey50", prepend="├─ ")
        run_startup = local.tmpscript(render_j2(startup_script_content, **locals()))

        if run_startup['rc'] != 0:
            rprint(f"Startup script failed with return code {run_startup['rc']}", prepend="╰──── ", text_style="red")
            rprint(f"{startup_script_content}", border_style="yellow", title="Startup script content", text_style="cyan")
            rprint(f"{run_startup['out']}", border_style="green", title="Startup script stdout")
            rprint(f"{run_startup['err']}", border_style="red", title="Startup script stderr")
            sys.exit(1)

    # Initialize engine for ssh commands. This means to choose a
    # specific ssh implementations among the ones in the engines module,
    # and initialize its ssh preliminary operations when needed (e.g.
    # creating sockets, or initialize paramiko connections, etc.), which
    # will be undone at the end of this context manager
    with SshEngine(host, user, keyfile) as ssh:
        # Test ssh connection
        rprint("Testing connection to cluster", prepend="├─ ")
        run_test = ssh.test()
        if run_test['rc'] != 0:
                rprint(f"Connecting to {host} via  failed with return code {run_test['rc']} and with the following error(s)", text_style="red", prepend="╰──── ")
                rprint(f"{run_test['err']}", border_style="red", title="ssh stderr")
                sys.exit(1)

        # Validate the options w.r.t. the remote side, e.g. if the
        # warehouse and the tool are valid. Quit the program if user
        # asked just to list the tools
        warehouse_data, resume_id = check_remote(list_tools, ssh, tool, warehouse)
        cluster_name = warehouse_data['cluster_name'] # just for convenience

        # Create ~/.chappyner/sessions remotely (if not present already)
        ssh.command(f"mkdir -p {warehouse_data['user_dir']}/sessions")

        # Initialize job object containing tool's info and remote
        # connection details
        job = ToolJob(scheduler=warehouse_data['scheduler'].lower(), tool_dir=f"{warehouse}/tools/{tool}/", engine=ssh)

        # Init for flag to be set as True when the user decides to quit.
        # It helps to distinguish between straightforward sessions and
        # software crashes / keyboard interrupts
        quit_intentionally = False

        # From now on, when the code quits for any reason, it tries to
        # understand if the job has to be canceled or not
        try:
            # Case 1: start a new tool job
            if not resume_id:
                rprint(f"Submitting job for {tool}", prepend="╰─┬─ ")

                # Submit job. Here IgnoreCtrlC tries to prevent zombie
                # jobs if Ctrl-C is pressed before assigning job id
                # (but there is an unavoidable grey area in which, with
                # a very unfortunate timing, Ctrl-C leaves jobs queued).
                with IgnoreCtrlC():
                    run_batch = job.submit(batch_options)
                    job_id = job.id # just for convenience when e.g. rendering jinja2

                # Exit if the job fails
                if run_batch['rc'] != 0:
                    rprint(f"Job submission failed on {cluster_name} with return code {run_batch['rc']} and the following stderr", text_style='red', prepend="  ╰─── ")
                    rprint(f"{run_batch['err']}", border_style="red", title="Job submission stderr")
                    if batch_options:
                        rprint(f"The error might be due to:\n - incompatibilities among the options you used submitting the job, which where the followings:\n      [yellow]{batch_options}[/yellow]\n - unstable network connectivity;\n - issues with cluster scheduler;", border_style="yellow", title="Hint")
                    else:
                        rprint(f"The error might be due to:\n - unstable network connectivity;\n - issues with cluster scheduler\nIf the issue persists you might want to search further insights running with --debug", border_style="yellow", title="Hint")
                    sys.exit(1)

                # Update tools history
                with IgnoreCtrlC():
                    ssh.command(f'echo -e "{job.id}:\n  warehouse: \"{warehouse}\"\n  tool: \"{tool}\"\n  batch_options: \"{batch_options}\"\n  submit_timestamp: \"$(date +"%Y-%m-%dT%H:%M:%S%:z")\"" >> {warehouse_data["user_dir"]}/tools_history.yml')
                rprint(f"Job ID: {job.id}", prepend="  ├─── ")

            # Case 2: resume a tool already queued
            else:
                rprint(f"Restoring connection to tool in job {resume_id}", prepend="╰─┬─ ")

                # If some options will be ignored, tell the user
                if batch_options or tool or warehouse:
                    rprint(f"Additional options ignored while resuming jobs", text_style="yellow", prepend="  ├─── ")

                # If the job is not anymore in the queue, quit
                if not check_job_state(job.engine, job.scheduler, resume_id):
                    rprint(f"Sorry! Job {resume_id} may no longer be queued on {cluster_name}", text_style='red', prepend="╭─┴─── ")
                    sys.exit(0)
                # Re-connect otherwise
                else:
                    job.id = resume_id
                    rprint("Connection restored!", text_style="cyan", prepend="  ├─── ")

            # Wait for job running
            rprint(f"[orange3]Waiting[/orange3] for job {job.id} to be running (this might take a while)", prepend="  ├─── ")
            job.wait()
            rprint("Job running!", text_style="green3", prepend="  ╰─── ")

            # Retrieve session details from connection.yml
            connection_yaml = f"{warehouse_data['user_dir']}/sessions/job_{job.id}-files/connection.yml"
            ssh.wait_file(connection_yaml, timeout=30)

            session_data = yaml.safe_load(ssh.command(f"cat {connection_yaml}")['out'])
            logging.info(f"Data parsed from connection.yml: {session_data}")
            node, node_port, token = session_data["node"], session_data["port"], session_data["token"] # just for convenience

            # Notify the user when the job is running
            notify(title="Job running!", text=f"Job {job.id} on {warehouse_data['cluster_name']}\nis running {tool}", icon="chappyner_logo.png")

            # Print warehouse motd (if present)
            if "motd" in warehouse_data.keys() and warehouse_data['motd'] != None: # Print warehouse motd if present and not empty
                rprint(warehouse_data['motd'].strip(), border_style="grey63")

            # Print information about job
            rprint(text=render_j2(session_data["job_info"], **locals()),
                   title="Job details",
                   border_style="medium_purple")

            # Print connection details about the tool
            rprint(text=render_j2(session_data["tool_info"], **locals()),
                   title="Tool details",
                   subtitle="[yellow]When you want to leave, press Enter[/yellow]",
                   border_style="deep_sky_blue1")

            # Forward ports from HPC compute node to localhost via ssh
            # (N.B.: execution waits here the user exploiting the
            # session, until port forwarding is blocked by user pressing
            # Enter. Ctrl-C is ignored in that specific step since the
            # user might try to copy tokens, when required by the tool,
            # using Ctrl-C, which would actually kill the Python
            # execution).
            ssh.forward_port("localhost", local_port, node, node_port)

            # User pressed Enter here, so he/she wants to quit
            quit_intentionally = True

        except KeyboardInterrupt:
            # Hide errors when the user is understandably tired of
            # waiting the job and presses Ctrl-C
            logging.info(f"User stopped execution via keyboard")
            quit_intentionally = True

        finally:
            if hasattr(job, "id"):
                cleanup(cluster_name, job, quit_intentionally)
            rprint("Bye!", text_style = "bold blue", prepend="╰─── ")

if __name__ == "__main__":
    main()
