import psutil # Retrieving information on system utilization
import csv # Write data to csv file
import datetime as dt # Retreive current time


## == CPU Utilization == ##
# psutil.cpu_percent: return CPU utilization as percentage
cpu_csvRow = [dt.datetime.now(),psutil.cpu_percent(interval=1, percpu=False)]
cpu_csv = "/opt/CPU.csv"

# Appending results in the csv file
with open(cpu_csv, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerow(cpu_csvRow)

## == Memory Utilization == ##

# psutil.virtual_memory().percent: returns the percentage of used memory
mem_free_per = round((100 - psutil.virtual_memory().percent),2)

mem_csvRow = [dt.datetime.now(),mem_free_per]
mem_csv = "/opt/MEM.csv"

# Appending results in the csv file
with open(mem_csv, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerow(mem_csvRow)

## == Disk Utilization == ##

# psutil.disk_usage('/').percent: returns root disk used space percentage
disk_free_per = round((100 - psutil.disk_usage('/').percent),2)

disk_csvRow = [dt.datetime.now(),disk_free_per]
disk_csv = "/opt/DISK.csv"

# Appending results in the csv file
with open(disk_csv, "a") as fp:
    wr = csv.writer(fp, dialect='excel')
    wr.writerow(disk_csvRow)
