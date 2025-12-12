#!/usr/bin/env python3
# Jobs management for Chappyner package
# Authors: Fabio Pitari, Lucia Rodriguez Muñoz, Antonio Memmolo

import logging, subprocess, time
from .prompts import *
from .utils import IgnoreCtrlC

def list_queued_jobs(engine, scheduler):
    """List all the user's job ids currently in the scheduler queue

    Parameters
    ----------
    engine : object
        Object from one of the classes in the 'engines' module of
        Chappyner
    scheduler : str
        Scheduler to be used for job submission. Supported values:
        slurm, pbs

    Returns
    -------
    dict
        dict containing the (queued) job id as keys and their states as vlues
    """
    logging.info("Entering list_queued_jobs() function")

    jobs = {}

    if scheduler == "slurm":
        out = engine.command("squeue --me --noheader -o '%A %T'")["out"].strip()
        for line in out.splitlines():
            if not line:
                continue
            job_id, state = line.split()
            jobs[int(job_id)] = state

    elif scheduler == "pbs":
        out = engine.command("qstat -u $USER")["out"].strip()
        for line in out.splitlines():
            if not line or not line[0].isdigit():
                continue
            parts = line.split()
            job_id = int(parts[0].split('.')[0])
            state = parts[4]
            jobs[job_id] = state

    return jobs


def check_job_state(engine, scheduler, job_id):
    """Check the state of a job queued on the HPC cluster

    Parameters
    ----------
    engine : object
        Object from one of the classes in the 'engines' module of
        Chappyner
    scheduler : str
        Scheduler to be used for job submission. Supported values:
        slurm, pbs
    job_id : int
        The target job id to check the state

    Returns
    -------
    str
        State of the job, as displayed in the specific scheduler; it
        just returns the raw value, which is tipically different among
        schedulers (e.g. "RUNNING" from Slurm corresponds to "R" from
        PBS), thus portability has to be granted elsewhere in the code
    """
    logging.info("Entering check_job_state() function")
    if scheduler == "slurm":
        state = engine.command(f"squeue -j {job_id} -h -o %T")['out'].strip() # %T = state
    elif self.scheduler == "pbs":
        state = engine.command(f"qstat -f {job_id} | awk '/job_state/{{print $3}}'")['out'].strip() # double braces are meant to escape in f-strings
    logging.debug(f"Job state returned: {state}")
    return state


def cleanup(cluster_name, job, quit_intentionally):
    """Handle the exit strategy when quitting.

    Parameters
    ----------
    cluster_name : str
        Cluster name
    job : object
        Object from the ToolJob class
    quit_intentionally : bool
        Flag which is set to True if the user asked to quit the
        execution
    """
    with IgnoreCtrlC():
        rprint(f"[red]![/red] Please wait while checking the state of job {job.id}\n", text_style="grey50")

        # If the job is alive
        if job.state():

            # Cancel jobs if the program crashed
            if not quit_intentionally:
                job.cancel() # it might fail with unfortunate timings with Ctrl-C
                rprint(f"Unexpected exit; please check if you have unwanted jobs queued on {cluster_name}", text_style="red", prepend="╰─── ")
                sys.exit(1)

            # If the user wants to leave, ask what to do
            else:
                # N.B. IgnoreCtlrC doesn't work in ask_if_cancel() since
                # inquirer.select().execute() overrides sigint
                # internally too (just like IgnoreCtrlC), so it
                # overrides the IgnoreCtrlC override
                ask_if_cancel(job, cluster_name)


class ToolJob():
    "Manage jobs on a remote cluster, either via Slurm or PBS"
    def __init__(self, scheduler, tool_dir, engine):
        """Define how to connect to cluster, where to find job scripts
        there, and which scheduler use to to submit them.

        Parameters
        ----------
        scheduler : str
            Scheduler to be used for job submission. Supported values:
            slurm, pbs
        tool_dir : str
            Path on a directory on the remote cluster containing either
            a Slurm script named 'slurm.sh' or a PBS script named
            'pbs.sh', according to the scheduler parameter
        engine : object
            Object from one of the classes in the 'engines' module of
            Chappyner
        """
        self.scheduler = scheduler
        self.engine = engine
        self.tool_dir = tool_dir

    def submit(self, batch_options=''):
        """Submit a job contained in tool_dir on the cluster, and set
        the 'id' attribute after submission. The job is run from the
        user's remote home.

        Parameters
        ----------
        batch_options : str, optional
            A string containing options to be passed to the scheduler
            command who submit jobs (i.e. to 'sbatch' command for Slurm
            and to 'qsub' command for PBS)

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code of the
            submission command'
        """
        if self.scheduler == "slurm":
            run_batch = self.engine.command(f"sbatch --chdir $HOME {batch_options} {self.tool_dir}/slurm.sh")
            self.id = run_batch['out'].lstrip("Submitted batch job").strip()
            return run_batch
        elif self.scheduler == "pbs":
            # PBS cannot manipulate submission dir via options, so the
            # following assumes that user lands in ssh in its remote
            # home dir (which is nearly 100% sure unless very original
            # setups)
            run_batch = self.engine.command(f"qsub {batch_options} {self.tool_dir}/pbs.sh")
            self.id = run_batch['out'].strip()
            return run_batch

    def state(self):
        """Check the state of the job in the scheduler

        Returns
        -------
        str
            State of the job, as displayed in the specific scheduler; it
            just returns the raw value, which is tipically different among
            schedulers (e.g. "RUNNING" from Slurm corresponds to "R" from
            PBS), thus portability has to be granted elsewhere in the code
        """
        return check_job_state(self.engine, self.scheduler, self.id)

    def wait(self, poll_interval=5):
        """Wait polling job via ssh until the job enters in running
        state or finishes.

        Parameters
        ----------
        poll_interval : int, optional
            Seconds between polls. Default is 5.

        Returns
        -------
        str
            Either 'RUNNING' (for Slurm) or 'R' (for PBS) when the job
            is running; 'COMPLETED_OR_GONE' when the job is not in the
            queue anymore.
        """
        while True:
            state = self.state()

            if not state:
                # job no longer in the queue
                return "COMPLETED_OR_GONE"

            if state == "RUNNING" or state == "R":
                return "RUNNING"

            time.sleep(poll_interval)

    def cancel(self):
        """Cancel job (via 'scancel' for Slurm or 'qdel' for PBS)

        Returns
        -------
        dict
            Dictionary containing 3 keys: 'out' containing stdout, 'err'
            containing 'stderr', 'rc' containing return code of the
            cancel command'
        """
        if self.scheduler == "slurm":
            return self.engine.command(f"scancel {self.id}")
        elif self.scheduler == "pbs":
            return self.engine.command(f"qdel {self.id}")
