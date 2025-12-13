import os,sys
from os import listdir
from os.path import join, isdir, isfile, basename
import argparse
morphodeep_path="/lustre/fshomisc/home/rech/genlir01/uhb36wd/semantic/"
sys.path.append(morphodeep_path)

from morphodeep.paths import STORE,SCRATCH
from morphodeep.tools.utils import launch_job_array, get_job_id, execute, mkdir, get_specie
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--compress', help='Compress in STORE ', action='store_true')
parser.add_argument('--uncompress', help='Uncompress in STORE ', action='store_true')
parser.add_argument('--job', help='Launch the corresponding job ', action='store_true')
parser.add_argument('-ja',"--number", default="", help="number of path to restore")
parser.add_argument('-jaf',"--csv", default="", help="csv file")
parser.add_argument('-w',"--what", default="", help="a specific method ? (Optional : membrane, etc... ) ")
parser.add_argument('-m',"--mode", default="3D", help="a specific mode ? (Optional : 2D or 3D ) ")
parser.add_argument('-s',"--specie", default="", help="a specific specie ? (Optional : PM,OV,..) ")
parser.add_argument("-mo", "--microscope", default="",help="which microscope ? (SPIM (for lightsheet), CONF (for confocal),ALL (for both))")

args = parser.parse_args()


STORE_DB=join(STORE,"Semantic")
SCRATCH_DB=join(SCRATCH,"Semantic")

ms="" if args.microscope=="" or args.specie=="" else args.microscope+"-"+get_specie(args.specie)

print("Start Pression ")
def get_paths(path):
    paths=[]
    for GT in listdir(path): #GT_3D PD_3D
        if args.mode=="" or "GT_"+args.mode==GT :#or "PD_"+args.mode==GT:
            for pm in listdir(join(path,GT)): #SPIM-Phallusia-Mammillata or ..
                if ms == "" or ms == pm:
                    for method in listdir(join(path, GT, pm)): #Membrane, etc...
                        if args.what == "" or args.what == method:
                            print(" --> addd " + join(path, GT, pm, method))
                            paths.append(join(path, GT, pm, method))

    return paths


if args.job: #LMaunch Jobs
    #List All availables methods
    jobslist=[]
    if args.compress :  jobslist = get_paths(SCRATCH_DB)
    if args.uncompress: jobslist = get_paths(STORE_DB)

    if len(jobslist)==0:
        print(" Nothing to do..")
    else:
        cmd = join(os.getcwd(), "store_data.py ")
        if args.compress: cmd += " --compress"
        if args.uncompress: cmd += " --uncompress"
        jobname="RESTORE" if args.what=="" else "RESTORE_"+args.what
        if args.mode!="":jobname+="_"+args.mode
        if args.microscope != "": jobname += "_" + args.microscope
        if args.specie != "": jobname += "_" + args.specie
        launch_job_array(jobname,jobslist, cmd=cmd, cpus_per_task=1,max_job=10,prepost=True)
    quit()

paths=[]
if args.number!="" and args.csv!="":
    path=get_job_id(args.csv,args.number)
    paths.append(path)
else :#DIRECT
    paths=[]
    if args.compress :  paths = get_paths(SCRATCH_DB)
    if args.uncompress: paths = get_paths(STORE_DB)

print(f"Paths={paths}")
if len(paths)==0:
    print(" --> nothing more to proceed ")
    quit()


TEMP=join(SCRATCH,"TEMP",str(datetime.datetime.now()).replace(" ","-"))
#TEMP=join(SCRATCH,"TEMP","2025-02-11-22:33:44.755348")
def clear(create=True):
    os.system("rm -rf "+TEMP)
    if create: os.system('mkdir -p '+TEMP)

if args.compress :
    print(" --> COMPRESSS " + str(len(paths)) + " paths ")
    for path in paths:
        print("-> Compress "+path)
        method=os.path.basename(path); path=os.path.dirname(path)
        pm=os.path.basename(path); path=os.path.dirname(path)
        GT=os.path.basename(path); path=os.path.dirname(path)

        if not isdir(join("/" + STORE_DB, GT , pm, method)):   mkdir(join("/" + STORE_DB, GT, pm, method))

        for dataset in listdir(join(SCRATCH_DB,GT,pm,method)):
            prev_file=join(SCRATCH_DB,GT,pm,method,dataset+".tar.gz")
            if isfile(prev_file): execute(f"rm -f {prev_file}")#CLEAR TEMP GZ
            execute(f"cd {join(SCRATCH_DB,GT,pm,method)}; tar -cf {dataset}.tar.gz {dataset}")
            #MOVE TO STORE
            store_file=join("/" + STORE_DB, GT, pm, method, dataset +"tar.gz")
            if isfile(store_file): execute(f"rm -f {store_file}")  # CLEAR PREVIOUS GZ
            execute(f"mv "+join(SCRATCH_DB, GT, pm, method,dataset+".tar.gz")+f" {join(STORE_DB,GT, pm, method)}")



elif args.uncompress :
    print(" --> UNCOMPRESSS " + str(len(paths)) + " paths ")
    for path in paths:
        print("-> UNCompress " + path)
        method = os.path.basename(path);  path = os.path.dirname(path)
        pm = os.path.basename(path);  path = os.path.dirname(path)
        GT = os.path.basename(path);  path = os.path.dirname(path)


        if not isdir(join("/" + SCRATCH_DB, GT, pm, method)):   mkdir(join("/" + SCRATCH_DB, GT, pm, method))

        for datasetgz in listdir(join(STORE_DB, GT, pm, method)):
            clear()
            execute("cp -f "+join(STORE_DB, GT, pm, method, datasetgz) +" "+TEMP)
            execute("tar -xf '" + join(TEMP, datasetgz) + "' --directory " + join(SCRATCH_DB, GT, pm, method))
    clear(create=False)


else: print("Nothing to do..")
