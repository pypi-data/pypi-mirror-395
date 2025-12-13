from os import listdir
from os.path import isdir, join, isfile, basename, dirname
import os
from tqdm import tqdm
import sys
sys.path.append('../..')

from morphodeep.tools.image import imread
from morphodeep.tools.utils import mkdir


def execute(cmd):
    print(cmd)
    os.system(cmd)
import pandas as pd
from random import shuffle

def get_specie_from_name(filename):
    species=["CONF-Arabidopsis-Thaliana","CONF-Caenorhabditis-Elegans","CONF-LateralRootPrimordia","CONF-Ovules","CONF-Phallusia-Mammillata","CONF-SeaStar","SPIM-Phallusia-Mammillata"]
    for s in species:
        if filename.find(s)>0:
            return s
    return None

mode="2D"
mode="3D"


########## EVAL MISSING FILES
if False:
    for what in ["train","valid","test"]:
        predict_file=f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
        nb_files={}
        miss_files={}
        print(f"\nOpen {predict_file}")
        for f in tqdm(open(predict_file,"r")):
            fname = f.strip()
            membrane_ok=isfile(fname)
            segmentation_ok=isfile(fname.replace("membrane","segmented").replace("_M.tiff","_S.tiff"))
            semantic_ok = isfile(fname.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff"))
            count_ok = isfile(fname.replace("membrane", "cell_counter").replace("_M.tiff", "_CC.txt"))
            s=get_specie_from_name(fname)
            if membrane_ok and segmentation_ok and semantic_ok and count_ok:
                if s not in nb_files: nb_files[s]=0
                nb_files[s]+=1
            else:
                if s not in miss_files: miss_files[s]={}
                if "membrane" not in miss_files[s]:miss_files[s]["membrane"]=0
                if "segmented" not in miss_files[s]: miss_files[s]["segmented"] = 0
                if "semantic" not in miss_files[s]: miss_files[s]["semantic"] = 0
                if "counter" not in miss_files[s]: miss_files[s]["counter"] = 0
                if not membrane_ok:miss_files[s]["membrane"]+=1
                if not segmentation_ok: miss_files[s]["segmented"] += 1
                if not semantic_ok: miss_files[s]["semantic"] += 1
                if not count_ok: miss_files[s]["counter"] += 1
        print(f"\n\nFOR {what}")
        for s in nb_files:
            print(f" --> {nb_files[s]} for {s} files  in {what}")
        for s in miss_files:
            for type in miss_files[s]:
                if miss_files[s][type]>0: print(f" --> miss {miss_files[s][type]} for {type} , {s} files in {what}")
    quit()

def try_read(filename):
    im=None
    if isfile(filename):
        try:
            im = imread(filename)
        except:
            print(f"Error reading {filename}")
    else:
        print(f"Missing file  {filename}")
    return im

########## TEST READING FILE
if True:
    for what in ["train","valid","test"]:
        predict_file=f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
        nb_files={}
        miss_files={}
        print(f"\nREAD {predict_file}")
        for f in tqdm(open(predict_file,"r")):
            fname = f.strip()
            try_read(fname)
            try_read(fname.replace("membrane", "segmented").replace("_M.tiff", "_S.tiff"))
            try_read(fname.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff"))
    quit()

####### REDUCE FILES NUMBER
if False:
    what="test"
    predict_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
    nbFilesMax = 1000
    nb_files = {}
    for f in open(predict_file, "r"):
        fname = f.strip()
        if isfile(fname):
            s = get_specie_from_name(fname)
            if s not in nb_files: nb_files[s] = []
            nb_files[s].append(fname)

    for s in nb_files:   print(f" --> {nb_files[s]} for {s} files  in {what}")

    fw = open(predict_file, "w")
    nbkeep = {}
    for s in nb_files:
        nbkeep[s] = 0
        files = nb_files[s]
        shuffle(files)
        i = 0
        for fname in files:
            if i < nbFilesMax:
                fw.write(fname + "\n")
                nbkeep[s] += 1
            i += 1
    fw.close()

    print("\n\nKEEP")
    for s in nbkeep:
        print(f" --> {nbkeep[s]} for {s} files keeped")
    quit()


def open_results(filename):
    #print(f"Opening {basename(filename)}")
    if os.path.getsize(filename)==0: return None
    #print(f"Adding {filename}")
    df = pd.read_csv(filename,sep=';',encoding='utf-8',index_col='Unnamed: 0',low_memory=False)
    return df

def save_results(filename,time_process):
    time_process.to_csv(filename, sep=';', encoding='utf-8',  header=True)

def purge(filename,filelist):
    print(f" --> purge {filename}")
    if True:#not isfile(filename.replace(".csv", ".oldmax")):
        os.system(f"cp {filename} " + filename.replace(".csv", ".oldmax2"))
        df=open_results(filename)
        ndf=None
        for f in df.Filename:
            #print(f" --> {f}")
            if f in filelist:
                v=df[df.Filename==f]
                #print(f"keep {f}")
                if ndf is None:
                    ndf=v
                else:
                    ndf=pd.concat([v,ndf])
            #else: print(f"excluded {f}")
        save_results(filename,ndf)
##### PURGE CSV files

if False:
    what = "test"
    predict_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"

    path=f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic_RESULT/NETWORKS_256_{mode}/ALL-all"

    filelist=[]
    for f in open(predict_file,"r"):
        filelist.append(f.strip())

    for f in listdir(path):

        if isfile(join(path,f)): #CELLPOSE FILES
            if f.endswith(".csv") and not f.startswith("EVAL_EXTERNAL"):
                purge(join(path,f),filelist)
        else:
            for ff in listdir(join(path,f)):
                if ff.endswith(".csv") and not ff.startswith("EVAL_EXTERNAL"):
                    purge(join(path, f,ff), filelist)


    quit()

###### FILL TXT FILES ACCORDING CELLPOSE4 EVALUATION
if False:
    path = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic_RESULT/NETWORKS_256_{mode}/ALL-all"
    results=open_results(join(path,"EVAL_cellpose4.csv"))
    what="test"
    predict_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
    fw=open(predict_file,"w")
    nb_files=0
    for f in results.Filename:
        fw.write(f.strip()+"\n")
        nb_files+=1
    fw.close()
    print(f" Write {nb_files} in {predict_file}")

###### PURGE GT FILES WHICH ARE NOT IN TXT FILES

if False:
    path_gt = f"/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_{mode}/"
    TEMP_GT=path_gt.replace(f"GT_{mode}",f"GT_{mode}_TEMP")
    mkdir(TEMP_GT)
    nb_files =0
    for what in ["train", "valid", "test"]:
        predict_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
        print(f"\nOpen {predict_file}")
        for ff in tqdm(open(predict_file, "r")):
            f=ff.strip()
            nb_files+=1
            #print(f"-> copy {f}")
            if not isfile(f):
                print(f"ERROR: {f} is not a file")
                quit()
            else:
                dest_path=dirname(f).replace(f"GT_{mode}",f"GT_{mode}_TEMP")
                mkdir(dest_path)
                os.system(f"cp {f} {dest_path}/{basename(f)}")

            seg_file = f.replace("membrane", "segmented").replace("_M.tiff", "_S.tiff")
            if not isfile(seg_file):
                print(f"ERROR: {seg_file} is not a seg  file")
                quit()
            else:
                dest_path = dirname(seg_file).replace(f"GT_{mode}", f"GT_{mode}_TEMP")
                mkdir(dest_path)
                os.system(f"cp {seg_file} {dest_path}/{basename(seg_file)}")

            sem_file = f.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff")
            if not isfile(sem_file):
                print(f"ERROR: {sem_file} is not a sem  file")
                quit()
            else:
                dest_path = dirname(sem_file).replace(f"GT_{mode}", f"GT_{mode}_TEMP")
                mkdir(dest_path)
                os.system(f"cp {sem_file} {dest_path}/{basename(sem_file)}")

            count_file = f.replace("membrane", "cell_counter").replace("_M.tiff", "_CC.txt")
            if not isfile(count_file):
                print(f"ERROR: {count_file} is not a count  file")
                quit()
            else:
                dest_path = dirname(count_file).replace(f"GT_{mode}", f"GT_{mode}_TEMP")
                mkdir(dest_path)
                os.system(f"cp {count_file} {dest_path}/{basename(count_file)}")

    print(f"COPY {nb_files} files ")

    '''file_list=[]
    for what in ["train", "valid", "test"]:
        predict_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic/NETWORKS_256_{mode}/ALL-all/tf_{what}.txt"
        print(f"\nOpen {predict_file}")
        for f in tqdm(open(predict_file, "r")):
            file_list.append(f.strip())
    print(f"Found {len(file_list)} files ")

    
    nb_remove=0
    nb_keep=0
    for specie in listdir(path_gt):
        if isdir(join(path_gt,specie,"membrane")):
            for what in listdir(join(path_gt,specie,"membrane")):
                if isdir(join(path_gt,specie,"membrane",what)):
                    for ff in listdir(join(path_gt,specie,"membrane",what)):
                        f=join(path_gt,specie,"membrane",what,ff)
                        if f not in file_list:
                            print(f"{nb_remove}/{nb_keep} -> remove {f}")
                            nb_remove+=1
                            os.system(f"rm -f {f}")
                            seg_file=f.replace("membrane", "segmented").replace("_M.tiff", "_S.tiff")
                            if isfile(seg_file):os.system(f"rm -f {seg_file}")
                            sem_file=f.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff")
                            if isfile(sem_file):os.system(f"rm -f {sem_file}")
                            count_file=f.replace("membrane", "cell_counter").replace("_M.tiff", "_CC.txt")
                            if isfile(count_file): os.system(f"rm -f {count_file}")
                        else:
                            nb_keep+=1
    print(f"Removed {nb_remove} files and kept {nb_keep} files")
    '''