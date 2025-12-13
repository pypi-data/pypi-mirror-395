#!/usr/bin/env python3
# Manage command line options for Chappyner package
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo

import argparse, logging, sys, socket
from datetime import datetime
if sys.version_info < (3, 10):
    import importlib_resources as resources
else:
    import importlib.resources as resources

import yaml
from rich.logging import RichHandler
from .utils import render_j2, rprint
from .jobs import list_queued_jobs
from .prompts import ask_if_resume, ask_resume_id
#from importlib import metadata # if retrieving version is needed

def get_arguments():
    """Retrieve variable from option passed at execution time. All the
    unrecognized options are stored to be passed to the scheduler submit
    command.

    Returns
    -------
    args : object
        ArgParse object containing native Chappyner options
    batch_options : list
        List containing all the unrecognized options (and values), to be
        passed to submit command
    """
    # N.B. do not start using logging from this function since this would
    # force default logging settings, hiding all the other loggings. You can
    # use it starting from check_local() function

    parser = argparse.ArgumentParser(add_help=False, description="Chappyner provides access to HTTP services ('tools') on HPC clusters via queued jobs and SSH tunnels. The user supplies cluster connection details (see the --user, --host, and/or --cluster options) and selects a tool available in a cluster directory ('warehouse') using the --tool option. A job is submitted to run the chosen tool and returns the information needed to connect. Default resource values are set for these job submissions, but users will likely want to change them; sbatch/qsub options can therefore be appended to the chappyner command to tune the job. The tool implementation can either be in a default path when --cluster is used, or provided from a custom warehouse by specifying the --warehouse option (required when using --host). Chappyner is developed and mantained by Cineca HPC department, please check https://gitlab.hpc.cineca.it/interactive_computing/chappyner for more detailed documentation.")

    parser.add_argument('--help', action='help', # not automated to avoid -h which conflicts with qsub -h
                        help='Print this help and exit')

    #parser.add_argument('--version', action='version', version=f'%(prog)s {metadata.version("chappyner")}', # retrieve version from package
    parser.add_argument('--version', action='version', version='', # relies on version printed in the logo
                        help='Print Chappyner version')

    parser.add_argument('--user', metavar='USERNAME',
                        dest='user', required=False,
                        help='Username to use on the HPC cluster')

    parser.add_argument('--host', metavar='HOST',
                        dest='host', required=False, default=None,
                        help='Remote ssh host to connect with. You can either use any host configured in your local SSH config file or the login node url coupling it with --user. Mutually exclusive with --cluster')

    parser.add_argument('--warehouse', metavar='REMOTE_PATH',
                        dest='warehouse', required=False, default=None,
                        help='Remote path on the cluster to which chappyner client will interact. A default value is automatically set when using --cluster option. If you want to deploy your own warehouse on an HPC cluster please read the Chappyner repo documentation')

    parser.add_argument('--tool', metavar='TOOL',
                        dest='tool', required=False, default=None,
                        help='Tool to start (use --list-tools to list the available values in the warehouse)')

    parser.add_argument('--list-tools', action='store_true',
                        dest='list_tools', required=False, default=False,
                        help='List avaliable tools in the warehouse of the given cluster/host for the --tool option')

    parser.add_argument('--engine', metavar="SSH_ENGINE",
                        dest='engine', required=False, default=None, # real default set in check_local()
                        help='Choose ssh implementation. Supported profiles are: socket (ssh commands from your system shell, using ssh sockets), nosocket (ssh commands, without sockets), paramiko (experimental, using paramiko and derivative packages). Default is "socket" (but if you are using the --cluster option default might differ for different clusters)')

    parser.add_argument('--cluster', metavar='DEFAULT_CLUSTER',
                        dest='cluster', required=False, default=None,
                        help='Alias for predefined set of options for specific clusters. It requires --user. Mutually exlusive with --host. You can use --list-clusters for the possible values. Specific HPC clusters might require some preliminary operation from your side to connect via ssh (e.g. retrieving certificates, setting known hosts) which might be executed by default by Chappyner; you can disable this behaviour via --no-startup-script option')

    parser.add_argument('--list-clusters', action='store_true',
                        dest='list_clusters', required=False, default=False,
                        help='List avaliable default clusters for the --cluster option')

    parser.add_argument('--no-startup-script', action='store_false',
                        dest='exec_startup_script', required=False, default=True,
                        help='If coupled with --cluster, avoids to run the startup script associated with it (you can inspect the scripts using the --list-clusters option)')

    parser.add_argument('--port', metavar='LOCAL_PORT',
                        dest='port', required=False, default=None, type=int, # real default set in check_local()
                        help='Local port to be used to expose and access the tool from your browser. Default is a random free port')

    parser.add_argument('--keyfile', metavar="SSH_KEYFILE",
                        dest='keyfile', required=False, default=None,
                        help='Path for ssh private key to be used in the ssh connections')

    parser.add_argument('--debug', action='store_true',
                        dest='debug', required=False, default=False,
                        help='Run in debug mode')

    parser.add_argument("-/--<any batch option>", metavar="VALUE", nargs="*", default=[],
                        help="You can add any option of sbatch/qsub command to overwrite/complement default values of the tool's job. Check 'man sbatch'/'man qsub' on your cluster for details.")

    # All the values from known options are stored as attributes into
    # args; all the unknown options, values and arguments are stored as
    # strings into the batch_options list. N.B. this means that, in case
    # of namesake options, chappyner ones prevails, thus keep them as
    # unambiguous as possible
    args, batch_options = parser.parse_known_args()

    return args, batch_options


def check_local(args, batch_args=[]):
    """Elaborate all the options from get_arguments() to translate into
    variables. It might also quit the code if the options are not enough
    or inconsistent, or if they're simple enough not to require any
    action from the main code (e.g. --list-clusters)

    Parameters
    ----------
    args : object
        ArgParse object containing parsed options
    batch_args : list, optional
        List of options and arguments to be passed to job scheduler at submit
        time

    Returns
    -------
    host
        SSH cluster host (either just the url or an host in ~/.ssh/config.
        String.
    keyfile
        Identity file to be used in ssh commands. Either string containing
        path or None.
    local_port
        Local port on which expose tools. Integer.
    batch_options
        User-defined for sbatch/qsub command in Slurm/PBS schedulers. String.
    SshEngine
        One of the classes from the 'engines' module in Chappyner
    startup_script_content
        Script to be run before SSH initialization for default clusters (if
        defined). Programming language is set via shebang. Either string or
        None
    tool
        Tool to run in the batch job. Either string or None
    list_tools
        Defines if the user asked to list the warehouse tools or not. Boolean
    user
        SSH user. Either string or None (in case it is defined in
        ~/.ssh/config)
    warehouse
        Remote path containing the warehouse files. String.
    """
    # Enable debugging infos when requested
    if args.debug == True:
        logging.basicConfig(
            format="{asctime} {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            level=logging.DEBUG,
            handlers=[RichHandler()]
        )

    # N.B. you can use logging from now on
    logging.info("Entering in check_local() function")

    # Initialize variables
    cluster, engine, host, keyfile, list_tools, local_port, exec_startup_script, tool, user, warehouse = args.cluster, args.engine, args.host, args.keyfile, args.list_tools, args.port, args.exec_startup_script, args.tool, args.user, args.warehouse
    batch_options = " ".join(batch_args)
    startup_script_content = None

    # Debug
    logging.info(f"Chappyner options/arguments parsed from options: {args}")
    logging.info(f"Scheduler options/arguments parsed from options: {batch_options}")

    # In case --list-clusters option was used, print default clusters
    # list and exit
    if args.list_clusters:
        with resources.files(__package__).joinpath("default_clusters.yml.j2").open("r") as d:
            clusters = yaml.safe_load(d) # yaml to dictionary, not rendered
        rprint("Available clusters for the --cluster option:", text_style="cyan", prepend="╰─┬─ ")
        for cluster in clusters.keys():
            if cluster != list(clusters.keys())[-1]:
                rprint(cluster, prepend="  ├─── ")
            else:
                rprint(cluster, prepend="  ╰─── ")
        for cluster in clusters.keys():
            rprint(f"{clusters[cluster]['description'].strip()}", title=cluster, border_style="cyan")
            if "startup_script" in clusters[cluster].keys():
                rprint(f"Using --cluster={cluster} the following script will be automatically run on your computer before connecting to {cluster} via ssh (unless you add the --no-startup-script option):\n\n{clusters[cluster]['startup_script'].strip()}", title=f"Startup script for {cluster}", border_style="yellow")
        sys.exit(0)

    ### In any other case you need one between --host and --cluster
    ### If neither --cluster and --host are specified
    if cluster == None and host ==None:
        raise InvalidOptions("Missing minimal options (--list-clusters, --cluster or --host), please check --help")

    # If both --cluster and --host are specified
    elif cluster != None and host !=None:
        raise InvalidOptions("You need to specify either --cluster or --host, not both")

    # In any other case you specified one of the two.
    # If just --cluster is specified
    elif cluster != None:
        # Exit if user is not specified
        if user == None:
            raise InvalidOptions("The --cluster option requires the --user option too.")

        # load yaml file containing default clusters
        with resources.files(__package__).joinpath("default_clusters.yml.j2").open("r") as d:
            default_clusters = yaml.safe_load(render_j2(d.read(), **locals())) # yaml to dictionary

        # If cluster is known, set variables accordingly
        if cluster in default_clusters:
            # Set default host
            host = default_clusters[cluster]["url"]
            # Use default warehouse if not differently specified via
            # --warehouse option
            if not warehouse:
                warehouse = default_clusters[cluster]["warehouse"]
                logging.info("Default warehouse {warehouse} for {cluster} will be used")
            # Use default engine if specified as cluster defaults and
            # not differently specified via --engine option
            if not engine and "engine" in default_clusters[cluster].keys():
                engine = default_clusters[cluster]["engine"].strip()
                logging.info("Default engine {engine} for {cluster} will be used")
            # Dump startup script content if present in cluster defaults
            # and --no-startup-script is not specified
            if exec_startup_script and "startup_script" in default_clusters[cluster].keys():
                startup_script_content = default_clusters[cluster]["startup_script"].strip()
                logging.info("Startup script for {cluster} will be run")
        # If the cluster is unknown, exit
        else:
            raise InvalidOptions(f"Cluster {cluster} is unknown, check --list-clusters for availiable default clusters or specify both --host and --warehouse for custom clusters.")

    # If just --host is specified
    elif host != None:
        # You can't go on if the warehouse of a custom cluster is
        # not specified (all the variables remain unchanged; --user
        # is not enforced since user might be already specified in a
        # ~/.ssh/config host)
        if warehouse is None:
            raise InvalidOptions(f"You need to specify --warehouse too for the specific warehouse path on {host} host")

    # Set random (free) local port if not specified by user
    if not local_port:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0)) # 0 is a random free port
            local_port = s.getsockname()[1]
            logging.info(f"Local port {local_port} is free, chosen.")

    # Set default value for engine if not previously set via --cluster
    # defaults or via --engine option
    if not engine:
        logging.info("Engine not set so far, thus the default value 'socket' will be used")
        engine = "socket"

    # Import engine
    if engine == "nosocket":
        from .engines import NoSocketEngine as SshEngine
    elif engine == "socket":
        from .engines import SocketEngine as SshEngine
    elif engine == "paramiko":
        from .engines import ParamikoEngine as SshEngine
    else:
        raise InvalidOptions(f"Engine {engine} unknown, please check --help for supported values")

    return batch_options, host, keyfile, list_tools, local_port, SshEngine, startup_script_content, tool, user, warehouse


def check_remote(list_tools, engine, tool, warehouse):
    """Elaborate all the options from get_arguments() and check_local
    with respect to the remote side on the cluster, i.e. the warehouse.
    It might also quit the code if the options are not enough or
    inconsistent, or if they're simple enough not to require any action
    from the main code (e.g. --list-tools)

    Parameters
    ----------
    engine : object
        An object from one of the classes in the 'engines' module
    warehouse : str
        The path of the warehouse on the cluster
    tool : str or None
        The tool requested (if requested, see 'list_tools')
    list_tools : bool
        Wether the user asked to just list the tools or not

    Returns
    -------
    dict
        Data retrieved remotely from warehouse_inventory.yml
    int or None
        When restoring, it's the job id to resume
    """
    logging.info("Entering in check_remote() function")

    # Validate warehouse
    run_warehouse = engine.command(f"cat {warehouse}/warehouse_inventory.yml")
    if run_warehouse['rc'] != 0:
        rprint(f"Path {warehouse} on {host} doesn't seem to be a valid warehouse", text_style="red", prepend="╰──── ")
        sys.exit(1)

    warehouse_data = yaml.safe_load(run_warehouse['out'])
    logging.debug(f"Data parsed from warehouse_inventory.yml: {warehouse_data}")

    # In case --list-tools option was used, print tools list and exit
    if list_tools:
        rprint("Available tools for the --tool option:", text_style="cyan", prepend="╰─┬─ ")
        for tool_name in warehouse_data['tools'].keys():
            if tool_name != list(warehouse_data['tools'].keys())[-1]:
                rprint(tool_name, prepend="  ├─── ")
            else:
                rprint(tool_name, prepend="  ╰─── ")
        for tool_name, tool_description in warehouse_data['tools'].items():
            rprint(tool_description, title=tool_name, border_style="cyan")
        sys.exit(0)

    # Retrieve the list of past jobs, and which one of them is active
    resume_id, active_tools = None, {} # init
    tools_history = yaml.safe_load(engine.command(f"cat {warehouse_data['user_dir']}/tools_history.yml")['out']) # N.B. returns None if file doesn't exist
    if tools_history:
        active_jobs = list_queued_jobs(engine, warehouse_data['scheduler'])
        skipped_states = ["COMPLETING"]
        active_tools = {job_id: state for job_id, state in active_jobs.items() if job_id in set(tools_history.keys()) and state not in skipped_states} # set() increase efficiency if the history is very long

    # If there are no active tools and neither --list-tools nor --tool
    # were specified, exit
    if (not active_tools) and (not tool):
        rprint(f"No tools currently queued on {warehouse_data['cluster_name']} and --tool option was not specified", text_style="red", prepend="╰─── ")
        sys.exit(0)

    # If the user survived until here, this means that either he/she is
    # starting a new tool or restoring a tool which is still active.
    # If user has tools already queued, check what to do
    if active_tools:

        # List active tools
        rprint(f"You have tools already queued on the cluster", text_style="yellow", prepend = "├─┬─ ")
        rprint("", text_style="cyan", prepend = "│ │ ")

        for old_job_id, old_job_state in active_tools.items():
            old_tool = tools_history[old_job_id]['tool']
            old_batch_options = tools_history[old_job_id]['batch_options']
            old_submit_timestamp = datetime.fromisoformat(str(tools_history[old_job_id]['submit_timestamp'])).astimezone().strftime("%A, %B %d, %Y, %H:%M:%S %Z")

            rprint(f"Job {old_job_id} with {old_tool} (state: {old_job_state})", text_style="medium_purple", prepend="│ ├─┬── ")
            if old_batch_options:
                rprint(f"Batch options: [cyan]{old_batch_options}[/cyan]", prepend="│ │ ├──── ")
            else:
                rprint(f"Batch options: [grey50]none[/grey50]", prepend="│ │ ├──── ")
            rprint(f"Submitted on: {old_submit_timestamp}", prepend="│ │ ╰──── ")
            rprint("", text_style="cyan", prepend = "│ │ ")

        # Resume automatically when --tool was not passed; ask what to
        # do if it was passed. If user decides not to resume tools,
        # resume_id keeps staying to None
        if not tool: # just for better graphic output
            rprint(f"Your tool is going to be resumed", prepend="│ ╰─ ")
        if (not tool) or (ask_if_resume() == True):
            resume_id = ask_resume_id(tools_history, active_tools)

    # If --tool was specified and there are no active jobs, user wants
    # unequivocally submit a new tool job; in this case it will be
    # checked if it's present in the warehouse
    if tool and not resume_id:
        if tool not in warehouse_data['tools'].keys():
            rprint(f'Tool {tool} is not available in the warehouse. Available tools: {", ".join(list(warehouse_data["tools"].keys()))}. Please use the --list-tools option if you need details of these tools', text_style="red", prepend="╰──── ")
            sys.exit(1)

    return warehouse_data, resume_id


class InvalidOptions(Exception):
    "Placeholder to define a specific exception for unusable options"
    pass
