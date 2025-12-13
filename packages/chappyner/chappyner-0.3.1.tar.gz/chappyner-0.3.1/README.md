# Chappyner
<div align="center">
   <img src="https://gitlab.hpc.cineca.it/interactive_computing/chappyner/-/raw/81169c6a84fc996d561bbdae01f17c217c93f5bb/pip_package/chappyner/chappyner_logo.png" width="300" height="300">
</div>

Chappyner allows to schedule and run web services on compute nodes of a remote HPC clusters and access them from your local browser. The backend services are mainly (but not necessarily) run via Apptainer/Singularity containers.

The main inspiration for Chappyner is [Open Ondemand](https://openondemand.org/), from which it inherits the main logics as well as part of the codes that it uses on the remote side; Chappyner replaces the Apache + nginx role in Open Ondemand with Python scripts + ssh tunnels, in order to be daemonless. In this way, any user can run backend services (*tools*) from containers in a remote directory (*warehouse*) with no needs of servers running on the HPC cluster (other than sshd).

***

## Install
You can install Chappyner in a Python virtual environment[^venv] of your current path using for instance:
```bash
python3 -m venv chappyner_venv # or choose the name you like
source chappyner_venv/bin/activate
pip install --upgrade pip
pip install <pip_package directory path>
```

## Quick start
A typical general syntax for Chappyner might the following:
```bash
chappyner --user <my username on cluster> --host <url or host in ~/.ssh/config for login nodes> --warehouse <remote path with tools containers> --tool <name of the tool to start> [plus any option for the scheduler submit command]
```
but for default clusters like e.g. Cineca clusters you can exploit some package-embedded settings and ready-to-use warehouses on the clusters to make this syntax shorter. For instance, to use Chappyner on [Leonardo](https://www.hpc.cineca.it/systems/hardware/leonardo/) you can run something like this:
```bash
chappyner --user <my username on cluster> --cluster leonardo --tool <name of the tool to start> [any sbatch option you like]
```

You can list all the default HPC clusters using the `--list-clusters` option and the avaliable tools remotely with the `--list-tools` option. Please note that using the default clusters might imply to automatically run some script on your local computer to allow the access to the specific cluster[^startup_script]. For instance, in the Leonardo case, a script will run to retrieve Smallstep certificates and to set ssh known hosts properly for login nodes, in order to ease the access to the cluster via ssh; if you don't like this behaviour you can disable it via the `--no-startup-script` option and perform those steps manually before using Chappyner.

Here it follows a list of examples to make it clearer:
```bash
# Run Jupyter on Leonardo with default configs (1 task, 1 hour on lrd_all_serial partition, no gpus, using your default account)
chappyner --user <my user name on leonardo> --cluster leonardo --tool jupyter
```
```bash
# Run Jupyter on Leonardo for 3 hours using 4 tasks and one gpu on boost_usr_prod partition with your account <my account>
chappyner --user <my user name on leonardo> --cluster leonardo --tool jupyter --ntasks 4 --gres gpu:1 --partition boost_usr_prod --account <my account> --time 03:00:00
```
```bash
# Run a VNC desktop via noVNC + TurboVNC  on Leonardo with default parameters (1 task, 1 hour on boost_usr_prod partition, 1 gpu, using your default account)
chappyner --user <my user name on leonardo> --cluster leonardo --tool vnc
```
```bash
# Run a VNC desktop via noVNC + TurboVNC  on Leonardo using the boost_qos_dbg for 30 minutes
chappyner --user <my user name on leonardo> --cluster leonardo --tool vnc -q boost_qos_dbg --time 30:00
```
Please check the `--help` option for the full list of options, as well as the documentation of your scheduler[^scheduler] and your cluster[^cineca_user_guide] for the full set of job submit options.

## Official repository
Chappyner source code is hosted at [this link](https://gitlab.hpc.cineca.it/interactive_computing/chappyner), where you can also find documentation and examples related to the *warehouse* to be hosted remotely.

## Custom warehouse
If you want to build your warehouse with your own tools you can exploit the `--warehouse` option; if coupled with `--cluster` it overwrites the default system value, whereas if you are deploying Chappyner on a different HPC cluster you need to couple it with the `--host` option.

Warehouses has to be built with a specific structure in order to be compliant with the client package here. Please refer to the original repo for details (see warehouses/README.md).

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [here](http://www.gnu.org/licenses/).

## Mantainers
This code is mantained by [HPC department](https://www.hpc.cineca.it/) at [Cineca](https://www.cineca.it/en).

## Authors
[Fabio Pitari](mailto:f.pitari@cineca.it?&subject=Chappyner), [Lucia Rodriguez Muñoz](mailto:l.rodriguezmunoz@cineca.it?&subject=Chappyner), [Antonio Memmolo](mailto:a.memmolo@cineca.it?&subject=Chappyner)

[^venv]: If you are not confident with Python virtual environments you can find a beginner's guide [here](https://realpython.com/python-virtual-environments-a-primer/)
[^startup_script]: You can inspect the scripts content using the `--list-clusters` option
[^scheduler]: For Slurm you can refer to the ["sbatch" command options](https://slurm.schedmd.com/sbatch.html); for PBS you can refer to the ["qsub" command options](https://www.jlab.org/hpc/PBS/qsub.html)
[^cineca_user_guide]: For Cineca clusters you can find all the User's guides [here](https://docs.hpc.cineca.it/index.html)
