# Incorta-DevOps-Task

- Track resource utilization over time. It’s required to have a script to automatically record system resources utilization on a Linux
machine. We expect to have 3 CSVs  for ( CPU - Memory Usage - Disk space usage ) files under /opt/ directory.

- Using Ansible to do the following ( Deploy and schedule the above script - Install some Linux packages passed as parameters - Install Java OpenJDK 11)

## Getting Started

These tasks are done on a local machine for development and testing using Linux distribution ( Ubuntu or CentOS 7 to match the company's environment )

### Prerequisites

You need to install the following on your linux distribution ( apt in Ubuntu, yum in CentOS )

```
python3
ansible
```
You need to install the following on your Python environment 
```
psutil : To retrieve information on system utilization
datetime: To access current timestamp
```
## Requirement 1:
- Python script "util.py" to automatically record system resources utilization on a Linux machine using psutil library <https://pypi.org/project/psutil/>  

Exact steps of the script are the following:
```
1- Import necessary libraries ( psutil - datetime - csv )
2- Get CPU utilization as percentage in the current time.
3- Append results from "Step 2" in a csv file every time the script is run.
4- Repeat "Steps 2 & 3" to get free memory & free disk spaces as percentages.
```
Example: Getting percentages of used virtual memory in MEM.csv with the corresponding timestamp
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
Deploy and schedule the "util.py" python script to run every 15 minutes using Ansible configuration management tool.
