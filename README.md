# Incorta-DevOps-Task
1- It’s required to have a script to automatically record system resources utilization on a Linux machine. We expect to have 3 CSVs files under /opt/ directory. 
- CPU.csv
- MEM.csv [Free memory percencetage ]
- DISK.csv [ Root disk available space percentage ] 
... Each row should have two columns timestamp and utilization at that time. This should be triggered every 15 minutes. 

2- In the other part we need to use the configuration management tool like Ansible to do the following:
- Deploy and schedule the above script. 
- Install some Linux packages passed as parameters. 
- Install Java OpenJDK 11.
