# Incorta-DevOps-Task

- Track resource utilization over time. It’s required to have a script to automatically record system resources utilization on a Linux
machine. We expect to have 3 CSVs  for ( CPU - Memory Usage - Disk space usage ) files under /opt/ directory.

- Using Ansible to do the following ( Deploy and schedule the above script - Install some Linux packages passed as parameters - Install Java OpenJDK 11)

## Getting Started

These tasks are done on a local machine for development and testing using Linux distribution ( Ubuntu 18.04 or CentOS 7 to match the company's environment )

### Prerequisites
As we will see in the second requirement, all the prerequisites will be installed for hosts via Ansible playbooks.

You need to install the following on your linux distribution ( apt in Ubuntu, yum in CentOS )
```
python3
python3-venv
ansible
```
You need to install the following on your python virtual environment
```
psutil : To retrieve information on system utilization
```
## Requirement 1:
**Python script *util.py* to automatically record system resources utilization on a Linux machine using [psutil python package](https://pypi.org/project/psutil/ "psutil python package")

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
  - name: Install psutil on virtual environment
    pip:
      name: psutil
      virtualenv: /etc/ansible/py_venv
```
- Clone the script from a GitHub repoy that acts as a server/master to a local directory via “clone_playbook.yml” playbook
```yaml
  - name: Clone python script from Git Repo
    command: sudo git clone https://github.com/*.git /etc/ansible/playbooks/Python_script/
```
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
Note that [Cron Ansible module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html "Cron Ansible Module")  allows you to create named crontab entries automatically via cron jobs in the playbooks

- Master may need to shut down the scheduler for some or all hosts, so additional playbook is added to stop the cron scheduler from running
```yaml
  - name: Stop cron scheduler service
    service:
      name: cron
      state: stopped
```
