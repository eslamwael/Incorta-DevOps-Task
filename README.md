# Incorta-DevOps-Task

- Track resource utilization over time. It’s required to have a script to automatically record system resources utilization on a Linux
machine. We expect to have 3 CSVs  for ( CPU - Memory Usage - Disk space usage ) files under /opt/ directory.

- Using Ansible to do the following ( Deploy and schedule the above script - Install some Linux packages passed as parameters - Install Java OpenJDK 11)

## Getting Started

These tasks are done on a local machine for development and testing using Linux distribution ( Ubuntu 18.04 or CentOS 7 to match the company's environment )

### Prerequisites
As we will see in the second requirement, all the prerequisites will be installed for hosts via Ansible playbooks.

Packages on linux distribution:

- *python3*
- *python3-venv*
- *ansible*

Python packages on your python virtual environment:
- *psutil : To retrieve information on system utilization*

## Requirement 1:
**Python script *util.py* to automatically record system resources utilization on a Linux machine using [psutil python package](https://pypi.org/project/psutil/ "psutil python package")**

**Exact steps of the script are the following:**
1. Import necessary libraries ( psutil - datetime - csv )
2. Get CPU utilization as percentage in the current time.
3. Save and append results from "Step 2" as a csv file in /opt/ directory every time the script is run.
4. Repeat "Steps 2 & 3" to get free memory & free disk spaces as percentages.

Example: Getting percentages of used virtual memory in *MEM.csv* with the corresponding timestamp
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
## Requirement 2.1:
**Deploy and schedule the "util.py" python script to run every 15 minutes using Ansible configuration management tool**

### Approach: Create a project specific [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html "Python Virtual Environment") with only the required python packages. The script is run on the virtual environment, scheduled and deployed using five Ansible playbooks

**Exact steps:**

- Install and create a python 3 virtual environment named "py_venv" on etc/ansible directory via "setup_venv.yml" playbook, apt is replaced with yum in case using CentOs 7
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
*Note: the benifit of using Git module that it gets the latest pull request every time the task is run.*

- Start cron scheduler then run the script on the virtual environment every 15 minutes via “schdule_script_venv.yml” playbook, cron logs are saved in the /opt directory in case of scheduling errors
```yaml
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

- Master may need to shut down the scheduler for some or all hosts, so additional playbook "stop_scheduler.yml" is added to stop the cron scheduler from running
```yaml
  - name: Stop cron scheduler service
    service:
      name: cron
      state: stopped
```

## Requirement 2.2:
**Install some Linux packages passed as parameters using Ansible**
- Use Ansible playbook variables to take linux package name as an argument, then install it on "linux_package.yml" playbook using Ansible built-in packages manager such as [apt module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html "apt module") in case of Ubuntu or [yum module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_module.html "yum module") in case of CentOS 

```yaml
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
## Requirement 2.3:
**Install Java OpenJDK 11 using Ansible**

- Create an [Ansible Role](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html "Ansible Role") named java using anisble-galaxy command in ansible directory:
```shell
ansible-galaxy init java
```
- In tasks directory under roles, edit the java role to install openjdk-11-jdk. yum is used instead of apt in case of using CentOS
```yaml
- name: Install Java OpenJDK 11
  apt:
    name: openjdk-11-jdk
    update_cache: yes
```
- Deploy the installed java using ansible playbook "java_playbook.yml" by calling the java role
```yaml
  roles:
    - ../roles/java
```
## Summary 

File  | Functionality
-------------    | -------------
util.py                | Python script to get information on Cpu, memory and disk utilization and save them in a Csv files under /opt 
Content Cell     | Content Cell
Content Cell     | Content Cell
