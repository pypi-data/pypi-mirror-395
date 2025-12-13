import os,sys
import time
from os.path import join
sys.path.append("../..")
from morphodeep.paths import JOBS


def read_csv(filename):
    list_job=[]
    for line in open(filename,"r"):
        jobname=line.strip()
        if jobname[0]!="#":
            list_job.append(line.strip())
    return list_job

def get_job_running():
    list_job = []
    jobtem = "job.txt"
    os.system("/usr/bin/squeue -u uhb36wd  -o '%.78j' > " + jobtem)
    nbline = 0
    for line in open(jobtem, "r"):
        nbline += 1
        if nbline>1:
            list_job.append(line.strip())

    os.system('rm -f ' + jobtem)
    return list_job

print("start")
while True:
    list_job=read_csv("job_list.csv")
    job_running=get_job_running()
    for job in list_job:
        if job in job_running:
            a=1
            #print(" --> "+job+" STILL RUNNING ")
        else:
            print(time.strftime("%Y/%m/%d at %H:%M:%S", time.localtime())+" --> LAUNCH "+job)
            os.system('/usr/bin/sbatch ' + join(JOBS, job + '.sh'))

    time.sleep(600)

