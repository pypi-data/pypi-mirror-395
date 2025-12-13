import os,sys
from os import listdir
from os.path import isfile, isdir, join, islink
import time
import numpy as np
import random
import pickle
sys.path.append("../../")
from morphodeep.paths import JOBS


############## MODELS
def get_weights_filename(weight_files,epochs):
    filename=weight_files.format(epoch=epochs)
    if isfile(filename): return filename
    #CHECK POINT MODEL
    chekfilename=join(get_path(weight_files),get_basename(weight_files)+"-"+str(epochs)+".index")
    if isfile(chekfilename):
        return chekfilename
    return None

def get_last_epochs(weight_files):
    epochs = 1
    if weight_files!="" and isdir(get_path(weight_files)):
        for f in listdir(get_path(weight_files)):
            if isfile(join(get_path(weight_files),f)) and f.startswith(get_basename(weight_files)):
                endname=f.replace(get_basename(weight_files),'')
                if endname[0]=="-": #CHECKPOINT
                    if f.endswith("index"):
                        epochs = max(epochs,int(f.replace(".index","").split("-")[1]))
                else:
                    epochs = max(epochs, int(f.split(".")[1]))
    return epochs

def write_paths(paths,output_file):
    f=open(output_file, 'w')
    for p in paths:
        f.write(p+"\n")
    f.close()

def read_paths(output_file,shuffle=False,reverse=False):
    paths=[]
    printi("read "+output_file)
    for p in open(output_file, 'r'):
        f=get_basename(p.strip())
        paths.append(p.strip())
    if shuffle: random.shuffle(paths)
    if reverse: paths.reverse()
    printi("found "+str(len(paths))+" files")
    return paths

def read_txt_file(filename):
    img_files = []
    printi(f"Read {filename} ")
    for p in open(filename, 'r'):
        f = p.strip()
        if f not in img_files:
            img_files.append(f)
            if len(img_files)>1000: return img_files
    printi(f"found {len(img_files)} files")
    return img_files

def read_eval_file(filename):
    evals = {}
    if not isfile(filename): return evals
    #printi(f"Read Evaluation {filename} ")
    for p in open(filename, 'r'):
        f = p.strip().split(";")
        evals[f[0]]=f[1]
    #printi(f"found {len(evals)} files")
    return evals

def write_eval_file(filename,evals):
    f=open(f'{filename}','w')
    for e in evals:
        f.write(str(e)+";"+str(evals[e])+"\n")
    f.close()


def file_write(filname, stri):
    '''
    Write in a file
    '''
    mkdir(get_path(filname))
    f = open(filname, 'w')
    f.write(str(stri))
    f.close()

def file_read(filname,type=None):
    '''
    Read in a file
    '''
    line=""
    for f in open(filname, 'r'):
        line +=f
    if type=="int":
        return int(line)
    return line

def read_number(filename):
    import tensorflow as tf
    a=None
    if not isfile(filename):
        printe(" Miss "+filename)
    else:
        try:
            #print("Read "+filename)
            a=tf.io.read_file(filename)
            a=int(a)
        except ValueError as e:
            printe(" reading  " + filename)
    return a

def printp(v,prev=""):
    '''
    Write a percentage in one line
    '''
    sys.stdout.write('\r')
    v=int(np.round(v))
    sys.stdout.write(prev+"[%-100s] %d%%" % ('=' * v, v))
    sys.stdout.flush()

def printi(v):
    '''
       print with a specific indent
    '''
    print(" --> "+v)

def strc(v,p=1000):
    return str( round(v*p)/p)

def not_none(variables):
    if type(variables)==list:
        for v in variables:
            if v is None:
                return False
    else:
        if variables is None: return False
    return True

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printb(strs): printblue(strs)
def printg(strs): printgreen(strs)
def printr(strs): printred(strs)
def printy(strs): printyellow(strs)

def printblue(strs):
    print(bcolors.BLUE+strs+bcolors.ENDC)
def printred(strs):
    print(bcolors.RED+strs+bcolors.ENDC)
def printgreen(strs):
    print(bcolors.GREEN+strs+bcolors.ENDC)
def printyellow(strs):
    print(bcolors.YELLOW+strs+bcolors.ENDC)

def printe(msg):
    printred(" ---> ERROR  " + str(msg))

def printw(msg):
    printy(" ---> WARNING  " +  str(msg))

def mkdir(path):
    '''
        Create path
    '''
    if not isdir(path):
        os.system("mkdir -p '" + path+"'")


def get_path(filename):
    '''
       return the absolute path from a filename
    '''
    if filename is None: return None
    return os.path.dirname(os.path.abspath(filename))


def get_filename(filename):
    '''
    return the trunck filename
    '''
    if filename is None: return None
    return os.path.basename(filename)

def get_basename(filename):
    '''
    return the trunck filename (without the extension)
    '''
    if filename is None: return None
    return get_filename(filename).split(".")[0]


def get_extension(filename):
    '''
    return the extension filename
    '''
    f = get_filename(filename)
    return f.replace(get_basename(f), '')


def get_time(filename):
    '''
    return the time step (in integer)
    '''
    if filename is None: return None
    filename = get_basename(filename)
    pos = filename.find("_t")
    if pos == -1:
        return "-1"
    filename = filename[pos + 2:]
    times = ""
    i = 0
    while i < len(filename) and filename[i].isdigit():
        times += filename[i]
        i += 1
    return int(times)

def get_time_format(filename,t,digits=3):
    if filename is None: return None
    base = get_basename(filename)
    pos = base.find("_t")
    if pos == -1: return "-1"
    oldt = base[pos:pos+2+digits]
    new_t="_t"+str(t).zfill(digits)
    return filename.replace(oldt,new_t)

def get_main_name(filename,key="_fuse"):
    if filename is None: return None
    base = get_basename(filename)
    pos = base.find(key)
    if pos == -1: return filename
    return base[0:pos]

def get_name_withtime(filename):
    if filename is None: return None
    base = get_basename(filename)
    pos = base.find("_t")
    if pos == -1: return filename
    next=base[pos+2:].find("_")
    if next==-1: next=base[pos+2:].find(".")
    if next==-1 : return base[:pos+5]
    return base[:pos+2+next]

def get_slice(im3D,z):
    if im3D is not None and  type(im3D) is np.ndarray and len( im3D.shape) >= 3 and z>0 and z<im3D.shape[2]:  return im3D[:, :, z]
    return None


def get_z(filename):
    '''
    return the z(in integer)
    '''
    filename = get_basename(filename)
    pos = filename.find("_z")
    if pos == -1:
        return "-1"
    filename = filename[pos + 2:]
    zz = ""
    i = 0
    while i < len(filename) and filename[i].isdigit():
        zz += filename[i]
        i += 1
    return int(zz)


def get_name(filename):
    '''
    return the embryo name
    '''
    filename = get_basename(filename)
    return filename.split("_")[0]



def get_cmd(vargs):
    '''
    Return the command line with all args with out job
    '''
    cmd = ""
    for k in vargs:
        if type(vargs[k]) == bool:
            if vargs[k] and k != "job":  # TRUE
                cmd += " --" + str(k)
        elif vargs[k] != "":
            cmd += " --" + str(k) + " " + str(vargs[k])
    return cmd



def get_gt_name(method):
    if method == "membrane":
        return "M"
    if method == "segmented":
        return "S"
    if method == "cell_counter":
        return "CC"
    if method == "semantic":
        return "JN"
    if method.startswith("cellpose"):
        return "CP"
    if method == "plantseg":
        return "PS"

    print(" --> this method is not yet implemente (in utils/get_gt_name).... "+str(method))
    quit()
    return None




def get_specie(name):
    if name == "PM": return "Phallusia-Mammillata"
    if name == "DR": return "Danio-Rerio"
    if name == "LP": return "LateralRootPrimordia"
    if name == "OV": return "Ovules"
    if name == "SS": return "SeaStar"
    if name == "AT": return "Arabidopsis-Thaliana"
    if name == "DM": return "Drosophila-Melanogaster"
    if name == "AA": return "Ascidiella-Aspersa"
    if name == "MM": return "Mus-Musculus"
    if name == "CP": return "CellPose"
    if name == "TN": return "tissuenet"
    if name == "all": return "all"
    if name == "CE": return "Caenorhabditis-Elegans"
    printe("unknown specie :" + str(name))
    quit()

def get_specie_short(name):
    if name == "Phallusia-Mammillata": return "PM"
    if name == "Danio-Rerio" : return "DR"
    if name == "Arabidopsis-Thaliana" : return "AT"
    if name == "Ovules": return "OV"
    if name == "SeaStar": return "SS"
    if name == "LateralRootPrimordia": return "LP"
    if name == "Drosophila-Melanogaster" : return "DM"
    if name == "Ascidiella-Aspersa": return  "AA"
    if name == "Mus-Musculus": return  "MM"
    if name == "CellPose": return "CP"
    if name == "all": return "all"
    if name == "Caenorhabditis-Elegans": return "CE"
    printe("unknown specie :" + str(name))
    quit()


def get_specie_from_name(filename):
    species=["CONF-Arabidopsis-Thaliana","CONF-Caenorhabditis-Elegans","CONF-LateralRootPrimordia","CONF-Ovules","CONF-Phallusia-Mammillata","CONF-SeaStar","SPIM-Phallusia-Mammillata","ALL-CellPose"]
    for s in species:
        if filename.find(s)>0:
            return s
    return None

def get_filename_from(filename, old_method, new_method):
    path=get_path(filename).replace("/"+old_method,"/"+new_method)
    base=get_basename(filename)
    ext=get_extension(filename)
    st="_" + get_gt_name(old_method)
    pos=base.rfind(st)
    if pos==-1:
        printe("did not find it "+str(pos))
        print(path)
        print(old_method)
        print(new_method)
        print(base)
        print(ext)
        print(st)
        quit()
    f=join(path,base[:pos] +"_" + get_gt_name(new_method) + base[pos + len(st):] + ext)
    if new_method=="cell_counter": f=f.replace(".tiff",".txt")
    if new_method.startswith("cellpose") or new_method == "plantseg": f = f.replace("GT", "PD")
    #print(" ---> " + f)
    return f

def get_resize_filename(filename,img_size):
    if img_size!=512: #original file size
        return filename.replace("GT_512_","GT_"+str(img_size)+"_")
    return None
def get_gt_filename(filename,  new_method):
    return get_filename_from(filename,"membrane",new_method)

def get_correspond_filename(filename,new_method):
    #print(" --> get_correspond_filename for "+filename+ " for method "+str(new_method))
    if new_method=="membrane": return filename
    old_method =  "membrane"
    filename=filename.replace("/"+old_method+"/", "/" + new_method + "/")
    return get_gt_filename(filename,  new_method)

def get_2D_filename(filename,z_axis,z):
    filename=filename.replace("3D/", "2D/")
    p=filename.rfind("_")
    return filename[0:p] +f"_o{z_axis}_z{z}" + filename[p:]

def get_borders(data,coords,border=10):
    xmin=max(0,coords[0].min()-border)
    xmax=min(data.shape[0],coords[0].max()+border)
    ymin=max(0,coords[1].min()-border)
    ymax=min(data.shape[1],coords[1].max()+border)
    if len(coords)==3:
        zmin=max(0,coords[2].min()-border)
        zmax=min(data.shape[2],coords[2].max()+border)
        return xmin,xmax,ymin,ymax,zmin,zmax
    return xmin, xmax, ymin, ymax

def get_boxes_border(box,shape,border):
    box=np.array(box)
    steps=np.zeros(3)
    for i in range(3): steps[i]=round((box[3+i]-box[i])*border)

    for i in range(3):
        box[i] -= steps[i]
        box[i+3] += steps[i]

    for i in range(3):
        box[i] = max(0,box[i])
        box[i + 3] = min(shape[i],box[i + 3])
    return box


def get_dataname(database):
    if database == "sm": return "SegmentedMembrane"
    return database


image_formats=["mha","nii","tiff","tif","inr"]
def get_image_file(filename): #Return the existing image file (with various format)
    trunck=filename
    if filename.find(".")>0: trunck=filename[:filename.find(".")]
    trunck+="."
    for f in image_formats:
        for ext in ["",".zip",".gzip", ".gz"]:
            if isfile(trunck+f+ext):
                return trunck+f+ext
    return None

def bbox_overlap(bbox1,bbox2):
    dim=int(len(bbox1)/2)
    bbox=np.zeros([dim*2,])
    for i in range(dim):
        bbox[i]=min(bbox1[i],bbox2[i])
    for i in range(dim):
        bbox[i+dim]=max(bbox1[i+dim],bbox2[i+dim])
    return np.uint16(bbox)

def shift_bbox(bbox,border=2,shape=None):
    newbox=np.array([bbox[0]-border,bbox[3]+border,bbox[1]-border,bbox[4]+border,bbox[2]-border,bbox[5]+border])
    if shape is not None:
        for i in [0,2,4]: newbox[i]=max(0,newbox[i])
        newbox[1] = min(shape[0], newbox[1])
        newbox[3] = min(shape[1], newbox[3])
        newbox[5] = min(shape[2], newbox[5])
    return newbox[0],newbox[1],newbox[2],newbox[3],newbox[4],newbox[5]


def execute(cmd,p=True):
    if p: print(cmd)
    os.system(cmd)


def save_dict(filename_,di_):
    with open(filename_, 'wb') as f:
        pickle.dump(di_, f)

def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pickle.load(f)
    return ret_di

######################## JOBS
def is_job(jobname):
    jobtem = "job-" + str(jobname) + "_" + jobname + ".txt"
    os.system("/usr/bin/squeue -n " + jobname + " > " + jobtem)
    nbline = 0
    for f in open(jobtem, "r"):
        nbline += 1
    os.system('rm -f ' + jobtem)
    return nbline > 1

def count_nb_job():
    return int(os.popen('/usr/bin/squeue | grep uhb36wd | grep -c prepost').read().strip())


def launch_job_cpu(jobname, cmd="", launch=None, delete_job=False,duration=20, cpus_per_task=1, prepost=True,tensorflow_load=False,job_limit=100,astec=False,relaunch=True):
    '''
    Run a prepost JOB in Jean Zay
    '''
    long=True
    if prepost:    long=False
    if launch is None:
        launch=False
    if delete_job:
        if is_job(jobname):
            print(" Cancel Job " + jobname)
            os.system("/usr/bin/scancel -n " + jobname)
        else:
            print(" dont exist " + jobname)
    else:
        if launch:
            print('python -u ' + cmd + "\n")
            os.system('python -u ' + cmd + "\n")
            return True
        if is_job(jobname):
            print(" ->> "+jobname+" already running")
            return False

        if prepost: #Check number of running job in preprost
            while count_nb_job()>job_limit:
                print(" Wait 1 mn next avialable job")
                time.sleep(60)

        os.system('rm -f ' + join(JOBS, jobname + '.*'))
        f = open(join(JOBS, jobname + ".sh"), 'w')
        f.write('#!/bin/sh\n')  # TESTER BASH ?
        f.write('#SBATCH --job-name=' + jobname + '\n')
        f.write('#SBATCH --output=' + join(JOBS, jobname + '.out') + '\n')
        f.write('#SBATCH --error=' + join(JOBS, jobname + '.err') + '\n')
        f.write('#SBATCH --ntasks=1\n')
        f.write('#SBATCH --cpus-per-task=' + str(cpus_per_task) + '\n')
        f.write('#SBATCH --hint=nomultithread\n')
        if duration is None:
            duration = 20 if not long else 100
        f.write("#SBATCH --time=" + str(duration) + ":00:00\n")
        if prepost:
            f.write('#SBATCH --partition=prepost\n')
            f.write("#SBATCH -A dhp@v100 \n")
        else:
            f.write("#SBATCH -A dhp@cpu \n")


        f.write('cd ${SLURM_SUBMIT_DIR}\n')
        f.write('module purge\n')
        f.write('module load anaconda-py3/2021.05\n')
        f.write('conda activate py38\n') #This env contains tensorflow-cpu
        if astec:
            f.write('conda activate astec\n')
            f.write(cmd + "\n")
        else:
            # f.write('set -x\n')
            f.write('python -u ' + cmd + "\n")
        #if relaunch: f.write(relaunch_job(JOBS,jobname))
        f.close()
        print(" --> SUBMIT " + jobname)
        os.system('/usr/bin/sbatch ' + join(JOBS, jobname + '.sh'))


def launch_job_gpu(jobname, cmd="", nbGPUS=1, memory=0, long=False, launch=None):
    '''
    Run a prepost JOB in Jean Zay
    '''
    if memory == 2: jobname+="_A"
    if launch is None: launch=False
    if launch:
        os.system('python -u ' + cmd + "\n")
        return True
    if is_job(jobname):
        return False
    os.system('rm -f ' + join(JOBS, jobname + '.*'))

    f = open(join(JOBS, jobname + ".sh"), 'w')
    f.write('#!/bin/sh\n')  # TESTER BASH ?
    f.write('#SBATCH --job-name=' + jobname + '\n')
    f.write('#SBATCH --output=' + join(JOBS, jobname + '.out') + '\n')
    f.write('#SBATCH --error=' + join(JOBS, jobname + '.err') + '\n')
    f.write('#SBATCH --ntasks=1\n')
    f.write('#SBATCH --gres=gpu:' + str(nbGPUS) + '\n')
    if memory == 2:
        f.write("#SBATCH -A dhp@a100 \n")
    else:
        f.write("#SBATCH -A dhp@v100 \n")
    if nbGPUS > 1:
        f.write('#SBATCH --ntasks-per-node=' + str(nbGPUS) + '\n')
    if memory == 1:
        f.write("#SBATCH -C v100-32g\n")
        long = False  # Do not accept long job
    elif memory == 2:
        f.write("#SBATCH -C a100\n") #80GB MEMORY
        long=False #Do not accept long job
    elif memory==3:
        f.write("#SBATCH --partition=gpu_p2\n")
        long = False  # Do not accept long job
    if not long:
        f.write("#SBATCH --time=20:00:00\n")
    else:
        f.write("#SBATCH --time=100:00:00\n")

    f.write('#SBATCH --cpus-per-task=10\n')
    # f.write('#SBATCH --hint=nomultithread\n')
    f.write('cd ${SLURM_SUBMIT_DIR}\n')
    f.write('module purge\n')
    if jobname.startswith('CellPose'):
        f.write('module load anaconda-py3/2021.05\n')
        f.write('conda activate cellpose\n')
    else:
        f.write('module load singularity\n')
        f.write('module load python/3.7.3\n')
        f.write('module load tensorflow-gpu/py3/2.7.0\n') #module load tensorflow-gpu/py3/2.6.0
    f.write('python -u ' + cmd + "\n")
    f.close()
    print(" --> SUBMIT " + jobname)
    os.system('/usr/bin/sbatch ' + join(JOBS, jobname + '.sh'))



def launch_job_array(jobname,jobslist, cmd="", max_run=None, duration=20, cpus_per_task=1,prepost=False,tensorflow_load=False,max_job=500):
    
    '''
    Run a prepost JOB in Jean Zay
    '''
    #Prepare the files to do
    os.system("rm -f "+join(JOBS,jobname)+"*")
    f=open(join(JOBS,jobname+".csv"),"w")
    if len(jobslist)>max_job:  jobslist=jobslist[:max_job] #Max Job
    if len(jobslist) > 5000:  jobslist = jobslist[:5000]  # JEAN ZAY JOB LIMIT
    #f.write("#JOB "+jobname+"\n") #Just to skip index 0
    for i in range(len(jobslist)):
        f.write(jobslist[i]+"\n")
    f.close()

    f = open(join(JOBS, jobname + ".slurm"), 'w')
    f.write('#!/bin/bash\n')  # TESTER BASH ?
    f.write('#SBATCH --job-name=' + jobname + '\n')
    f.write('#SBATCH --output=' + join(JOBS, jobname + '=%x_%A_%a.out') + '\n')
    f.write('#SBATCH --error=' + join(JOBS, jobname + '=%x_%A_%a.err') + '\n')
    f.write('#SBATCH --ntasks=1\n')
    f.write('#SBATCH --cpus-per-task=' + str(cpus_per_task) + '\n')
    f.write('#SBATCH --hint=nomultithread\n')
    if prepost:
        f.write('#SBATCH --partition=prepost\n')
        f.write("#SBATCH -A dhp@v100 \n")
    else:
        f.write("#SBATCH -A dhp@cpu \n")
    if duration is not None:
        f.write("#SBATCH --time=" + str(duration) + ":00:00\n")
    f.write('#SBATCH --array=0-' + str(len(jobslist)-1))
    if max_run is not None: f.write('%' + str(max_run ) + '\n')
    else : f.write('\n')
    f.write('cd ${SLURM_SUBMIT_DIR}\n')
    f.write('module purge\n')
    f.write('module load singularity\n')
    if tensorflow_load:
        f.write('module load python/3.7.3\n')
        f.write('module load tensorflow-gpu/py3/2.7.0\n')
    else:
        f.write('module load anaconda-py3/2021.05\n')
        f.write('conda activate py38\n')

    f.write('python -u ' + cmd + " -ja ${SLURM_ARRAY_TASK_ID} -jaf "+join(JOBS,jobname+".csv") +"\n")
    f.close()
    print(" --> SUBMIT " + jobname + " with "+str(len(jobslist))+" sub jobs")
    os.system('/usr/bin/sbatch ' + join(JOBS, jobname + '.slurm'))


def get_job_id(job_filename ,job_number):
    job_number=int(job_number)
    i=0
    for line in open(job_filename,"r"):
        if i==job_number:
            return line.strip()
        i+=1
    return None


def write_gzip(path,recursive=False,delete_before=True):
    st=""
    for f in listdir(path):
        if f.endswith(".h5") or f.endswith(".tif") or f.endswith(".tiff") or f.endswith(".mha"):
            if delete_before and isfile(join(path,f+".gz")): execute("rm -f "+join(path,f+".gz"))
            st+="cd "+path+"; gzip "+f+'\n'
        if recursive and isdir(join(path,f)): st+=write_gzip(join(path,f))
    return st


def gzip_job(path,recursive=False):
    '''
    Run a GZIP JOB in Jean Zay
    '''
    jobname=path.replace("/","_")
    if is_job(jobname):
        print(" ->> "+jobname+" already running")
        return False

    st = write_gzip(path, recursive=recursive)
    if st == "":
        print("-> nothing to zip in " + path)
        return False


    f = open(join(JOBS, jobname + ".sh"), 'w')
    f.write('#!/bin/sh\n')
    f.write('#SBATCH --job-name=' + jobname + '\n')
    f.write('#SBATCH --output=' + join(JOBS, jobname + '.out') + '\n')
    f.write('#SBATCH --error=' + join(JOBS, jobname + '.err') + '\n')
    f.write('#SBATCH --ntasks=1\n')
    f.write('#SBATCH --cpus-per-task=1\n')
    f.write('#SBATCH --hint=nomultithread\n')
    f.write("#SBATCH --time=20:00:00\n")
    f.write("#SBATCH -A dhp@cpu \n")
    f.write('cd ${SLURM_SUBMIT_DIR}\n')
    f.write(st)
    f.close()
    print(" --> SUBMIT " + path)
    os.system('/usr/bin/sbatch ' + join(JOBS, jobname + '.sh'))



#### SSH COMMANDS
host_name="jz"
is_proxy={"jz":True,"morphonet":False}


def ssh_connect(host_name):
    import paramiko
    conf = paramiko.SSHConfig()
    conf.parse(open(os.path.expanduser('~/.ssh/config')))
    host = conf.lookup(host_name)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if is_proxy[host_name]:
        client.connect(
            host['hostname'], username=host['user'],
            # if you have a key file
            # key_filename=host['identityfile'],
            password='yourpassword',
            sock=paramiko.ProxyCommand(host.get('proxycommand'))
        )
    else:
        client.connect(  host['hostname'], username=host['user'])
    return client






def ssh_ls(client,path):
    print("-->"+str(path))
    stdin, stdout, stderr = client.exec_command('ls '+path)
    res=stdout.read().decode("utf8")
    return res.strip().split("\n")

def ssh_isfile(client,filename):
    files = ssh_ls(client, filename)
    for f in files:
        if filename==f:
            return True
    return False

def ssh_cp(scpc,inputfile,outputpath):
    print(f"Download {inputfile} to {outputpath}")
    scpc.get(inputfile,outputpath)

def ssh_push(scpc,inputfile,outputpath):
    print(f"Upload {inputfile} to {outputpath}")
    scpc.put(inputfile,outputpath)

def ssh_exec(scpc,cmd):
    print(f"Exec {cmd} ")
    scpc.scp_command(cmd)

