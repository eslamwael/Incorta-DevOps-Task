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


