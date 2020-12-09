# Incorta-DevOps-Task

- Track resource utilization over time. It’s required to have a script to automatically record system resources utilization on a Linux
machine. The scipt creates 3 CSV files  for (CPU - Memory Usage - Disk space usage) under /opt/ directory.

- Using Ansible to do the following (Deploy and schedule the above script - Install some Linux packages passed as parameters - Install Java OpenJDK 11)

## Table of contents
<!--ts-->
   * [Getting Started](#getting-started)
      * [Prerequisites](#prerequisites)
   * [Requirement 1: "Record system resources utilization"](#requirement-1-record-system-resources-utilization)
   * [Requirement 2: "Using Ansible configuration tool"](#requirement-2-using-ansible-configuration-tool)
      * [Deploy and Schedule Script](#deploy-and-schedule-script)
      * [Install Linux packages passed as parameters](#install-linux-packages-passed-as-parameters)
      * [Install Java OpenJDK 11 on Linux environment](#install-java-openJDK-11-on-linux-environment)
   * [Summary](#summary) 
   * [Future work: Visualize system utilization](#future-work-visualize-system-utilization)
<!--te-->

Getting Started
=================

These tasks are done on a local host for development and testing using Linux distribution (Ubuntu 18.04 or CentOS 7)

Prerequisites
-------------
As we will see in the second requirement, all the prerequisites will be installed for hosts via Ansible playbooks.

Packages on linux distribution:

- *python3*
- *python3-venv*
- *ansible*

Python packages on your python virtual environment:
- *psutil : To retrieve information on system utilization*

Requirement 1: "Record system resources utilization"
==============
**Python script *util.py* to automatically record system resources utilization on a Linux machine using [psutil python package](https://pypi.org/project/psutil/ "psutil python package")**

**Exact steps of the script are the following:**
1. Import necessary libraries ( psutil - datetime - csv )
2. Get CPU utilization as percentage in the current time.
3. Save and append results from "Step 2" as a csv file in /opt/ directory every time the script is run.
4. Repeat "Steps 2 & 3" to get free memory & free disk spaces as percentages.

**Example: Getting percentages of used virtual memory in *MEM.csv* with the corresponding timestamp**
```python
# psutil.virtual_memory().percent: returns the percentage of used memory
mem_free_per = round((100 - psutil.virtual_memory().percent),2)

mem_csvRow = [dt.datetime.now(),mem_free_per]
mem_csv = "/opt/MEM.csv"

# Appending results in the csv file
with open(mem_csv, "a", newline='') as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerow(mem_csvRow)
```
Output sample for MEM.csv:
``` 
2020-12-08 00:35:02.228761,29.0
2020-12-08 00:36:02.368104,29.7
```
Requirement 2: "Using Ansible configuration tool"
================

Deploy and Schedule Script
-------------------------

**Deploy and schedule "util.py" python script to run every 15 minutes using Ansible configuration management tool**

### Approach: Create a project specific [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html "Python Virtual Environment") with only the required python packages. The script is run on the virtual environment, scheduled and deployed using Ansible playbooks.

**Exact steps:**

- Install and create a python 3 virtual environment named "py_venv" on etc/ansible directory via "setup_venv.yml" playbook ( apt is replaced with yum in case of using CentOs 7 )
```yaml
## setup_venv.yml
  - name: Install the venv library
    command: apt install python3-venv

  - name: Create python virtual environment on Ansible directory
    command: python3 -m venv /etc/ansible/py_venv
```
- Activate the virtual the created environment "py_venv" using the command:
```shell
source py_venv/bin/activate
```
- Install any needed python libraries such as psutil on the installed virtual environment via "venv_packages.yml" playbook

```yaml
## venv_packages.yml
  - name: Install psutil on virtual environment
    pip:
      name: psutil
      virtualenv: /etc/ansible/py_venv
```
*Note: Although Virtual environment benefit is not clear here. However, in real projects it is used instead of local environments to help keep dependencies required by different projects separate by creating isolated python virtual environments for them (specially for site-packages)*

- Clone the script from a public GitHub repo that acts as a server/master to a local directory with [Git Ansible module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html "Git Ansible module")  via “clone_script” playbook. 
```yaml
## clone_script.yml
  vars:
    username: eslamwael
    repo_name: Linux-untilization-Python-script

  tasks:
  - name: Download python script from Git
    git:
      repo: https://github.com/{{ username }}/{{ repo_name }}.git
      dest: /etc/ansible/playbooks/Python_script/
```
*Note: the benefit of using Git module that it gets the latest commit every time the task runs.*

- Start cron scheduler then run the script on the virtual environment every 15 minutes via “schedule_script_venv” playbook, cron logs are saved in the /opt directory in case of scheduling errors
```yaml
## schedule_script_venv.yml
  - name: Start cron scheduler service
    service:
      name: cron
      state: started

  - name: Run script every 15 minutes
    cron:
      name: "schedule script"
      minute: "*/15"
      job: Python_virtual_env_path script.py >> /opt/cron.log 2>&1
```
Note that [Cron Ansible module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html "Cron Ansible Module")  allows you to create named crontab entries automatically via cron jobs in the playbooks as follows:

```cron
*/15 * * * * /etc/ansible/py_venv/bin/python3 /etc/ansible/playbooks/Python_script/util.py >> /opt/cron.log 2>&1
```

- Master may need to shut down the scheduler for some or all hosts, so additional playbook "stop_scheduler" is added to stop the cron scheduler from running
```yaml
## stop_scheduler.yml
  - name: Stop cron scheduler service
    service:
      name: cron
      state: stopped
```

Install Linux packages passed as parameters
-------------------------------------------

- Use Ansible playbook variables to take linux package name as an argument, then install it on "linux_package.yml" playbook using Ansible built-in packages manager such as [apt module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html "apt module") in case of Ubuntu or [yum module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_module.html "yum module") in case of CentOS 

```yaml
## linux_package.yml
  vars:
    package: "{{ pkg }}"

  tasks:

  - name: Install Linux Package
    apt:
      name: "{{ package }}"
```
- Running "linux_package" playbook and taking linux package name "apache2 in this example" as an extra argument
```shell
sudo ansible-playbook packages_playbook.yml --extra-vars "pkg=apache2"
```

Install Java OpenJDK 11 on Linux environment
--------------------------------------------

- Install Java OpenJDK using ansible playbook "openjdk11_install.yml" by using apt module (Ubuntu) or yum module (CentOs)
```
## openjdk11_install.yml
  tasks:

  - name: Install Java OpenJDK 11
    apt:
      name: openjdk-11-jdk
      update_cache: yes
```
Summary 
=======

File  | Functionality
-------------    | -------------
util.py          | Python script to get information on Cpu, memory and disk utilization and save them in a Csv files under /opt 
setup_venv.yml     | Ansible playbook to install venv library and setup python 3 virtual environment
venv_packages.yml     | Ansible playbook to install any needed python package for the project such as psutil
clone_script.yml     | Ansible playbook to download the python script "util.py" from a github repo, run again for new commits
schedule_script_ven.yml      | Ansible playbook to start cron scheduler and run the python script every 15 minutes 
stop_schedule.yml     | Ansible playbook to stop cron scheduler from running the script
linux_package.yml     | Ansible playbook to install a linux package by taking the package name as an argument
openjdk11_install.yml     | Ansible playbook to install Java Open Jdk 11 on linux environment     

Future work: Visualize system utilization
=========================================

- Creating a python script with a visualization library such as [matplotlib](https://matplotlib.org/) or [plotly](https://plotly.com/python/) to create a static interactive graphs for CPU, memory and disk usages over time.
- This can be done by importing the three generated CSV files in from /opt directory

###    Thank you
