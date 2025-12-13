import random
import sys,os

from os import listdir
from os.path import join, isfile, basename, isdir
from datetime import datetime
from skimage.io import imread,imsave
import numpy as np
from skimage.transform import resize

from morphodeep.paths import SCRATCH, STORE, WORK
from morphodeep.tools.utils import mkdir, execute, printe, get_path

#CREATE ENVIROENNMENT
#conda create --name cellpose python=3.8
#python -m pip install cellpose
#pip install scikit-image
#pip install h5py


#ACTIVATE ENVIRONNEMNT
# module purge
# conda activate cellpose4, cellpose3

def write_time(filename,times):
    f=open(filename, 'w')
    for label_name in times:
        f.write(label_name+":"+str(times[label_name])+"\n")
    f.close()

def read_time(filename):
    times={}
    if isfile(filename):
        for line in open(filename, "r"):
            label_name = line.strip().split(":")[0]
            t=line.strip().split(":")[1]
            times[label_name]=t
    return  times

def get_env():      
    sp = sys.path[1].split("/")
    if "envs" in sp:
        sp=sp[sp.index("envs") + 1]
        if sp.startswith("cellpose"):
            if sp=="cellpose": return 2
            return int( sp[8:])
    return 0

def get_diameter(seg):
    #Calculate average diameter
    cells, nb = np.unique(seg, return_counts=True)
    radius = []
    for i in range(len(cells)):
        if cells[i] != 0:
            radius.append(((np.pi * nb[i]) * 3.0 / 4.0) ** (1 / 3))
    diameter = np.int16(2 * np.mean(radius))
    print( f" --> Average diameter {diameter}")
    return diameter

def import_cellpose():
    cp_version = 0
    model=None
    try:
        cp_version = get_env()
        if cp_version == 0:
            print("First activate Conda CellPose environment ")
            quit()
        print(f"---> Found CellPose {cp_version}")
        from cellpose import models
        model = None
        if cp_version == 2:
            model = models.CellposeModel(gpu=True, model_type="cyto2")
        elif cp_version == 3:
            model = models.CellposeModel(gpu=True, model_type="cyto3")
        elif cp_version == 4:
            model = models.CellposeModel(gpu=True)
        if model is None:
            print("Unrocognized cellpose version")
            quit()
    except:
        printe("CellPose is required for prediction")
    return cp_version,model


def predict_cellpose(specie,txt_path,mode="3D",what=None):

    cp_version,model=import_cellpose()

    whats = ["train", "test", "valid"] if what is None or what == "" else [what]
    print(" -->  for " + str(whats) + ".txt")

    cellpose_dir = f"cellpose{cp_version}"

    ratio=1
    z_axis = 2
    if mode=="3D":
        if specie=="LP" or specie=="AT" or specie=="SS" or specie=="OV":z_axis=0
        if specie == "LP" or specie == "OV" or specie == "PM": ratio=2

    for what in whats:
        print(f" --> Predict CellPose {cp_version} on {txt_path}_{what}.txt")
        cellpose_time = join(WORK,"Semantic","PD_"+mode,f"CellPose{cp_version}","Prediction_Time_"+what+".txt")
        mkdir(get_path(cellpose_time))
        times=read_time(cellpose_time)
        total=0
        for line in open(join(txt_path + "_" + what + ".txt"), "r"): total+=1
        i=0
        for line in open(join(txt_path+"_" + what + ".txt"), "r"):
            line=line.strip()
            cellpose_filenaname = line.replace("/GT", "/PD").replace("/membrane/", "/"+cellpose_dir+"/").replace("_M.tiff",
                                                                                                             "_CP.tiff")
            i+=1
            if  isfile(cellpose_filenaname):
                print(f"{i}/{total} --> exist {cellpose_filenaname}")
            else:

                label_name = line.replace("/membrane/", "/segmented/").replace("_M", "_S")
                if not isfile(label_name) or not isfile(line):
                    print(f" --> predict {cellpose_filenaname} --> miss input data {line}")
                    print(" --> or "+label_name)
                else:

                    #READ CURRENT MASK TO GET AVERAGE DIAMETER
                    membrane = imread(line)  #READ RAW DATA
                    #print(f"{i}/{total} --> predict CellPose for {cellpose_filenaname} with shape {membrane.shape}")
                    if len(membrane.shape)==1: #ERROR in images
                        print(f"shape error {membrane.shape}")
                    else:
                        n=datetime.now()
                        original_shape = membrane.shape
                        seg = imread(label_name)
                        nb_cells = len(np.unique(seg))

                        if ratio>1:
                            membrane=membrane[::ratio,::ratio,::ratio]
                            seg=[seg[::ratio,::ratio,::ratio]]
                            print(f"reduce shape from {original_shape} to {membrane.shape}")

                        do_3D=len(membrane.shape) == 3
                        if cp_version == 2 or cp_version == 3:
                            masks = model.eval(membrane, diameter=get_diameter(seg),  do_3D=do_3D)[0]
                        elif cp_version == 4:
                            if do_3D:
                                masks = model.eval(membrane, do_3D=do_3D, z_axis=z_axis)[0]
                            else:
                                masks = model.eval(membrane)[0]
                            if masks.shape!=membrane.shape:
                                masks=np.swapaxes(masks,0,2).swapaxes(0,1) #CELLPOSE 4 INVERT SHAPE
                        #print(f"masks shape {masks.shape} and raw shape {membrane.shape}")

                        if ratio > 1:
                            masks=resize(masks,original_shape,preserve_range=True,order=0).astype(masks.dtype)

                        #print(f"after ratio masks shape {masks.shape} and raw shape {membrane.shape}")
                        times[cellpose_filenaname]=str(datetime.now() - n)
                        mkdir(get_path(cellpose_filenaname))
                        write_time(cellpose_time,times)


                        del seg
                        print(f" --> Predict {cellpose_filenaname} in {times[cellpose_filenaname]} -> found {len(np.unique(masks))} / {nb_cells} cells")
                        imsave(cellpose_filenaname, masks,check_contrast=False)



def predict_cellpose_files(filename):
    cp_version, model = import_cellpose()

    if not isfile(filename):
        print(f" --> this file {filename} does not exist ...")
        quit()
    print(f"--> Predict cellpose {cp_version} for {filename}")

    for f in open(filename, "r"):
        if not f.startswith("#"):
            tab = f.split(";")
            if len(tab) < 3:
                print(f"Not well define {f}")
                quit()
            input_filename = tab[0]
            gt_filename = tab[1]

            if not isfile(input_filename):
                print(f"--> Miss  image file {input_filename}")
            else:
                extension = os.path.splitext(input_filename)[1]
                output_filename = input_filename.replace(extension, f"_CP{cp_version}"+extension)
                print(f"Predict {output_filename}")
                if not isfile(output_filename):
                    image_input = imread(input_filename)
                    z_axis=np.where(image_input.shape==np.min(image_input.shape))[0][0]
                    do_3D = len(image_input.shape) == 3
                    if cp_version == 2 or cp_version == 3:
                        if not isfile(gt_filename):
                            print(f"--> Miss GT images file {gt_filename}")
                        else:
                            gt = imread(gt_filename)
                            masks = model.eval(image_input, diameter=get_diameter(gt), do_3D=do_3D)[0]
                    elif cp_version == 4:
                        if do_3D:
                            masks = model.eval(image_input, do_3D=do_3D, z_axis=z_axis)[0]
                        else:
                            masks = model.eval(image_input, do_3D=do_3D, z_axis=None)[0]
                        if do_3D and z_axis==2:
                            masks = np.swapaxes(masks, 0, 2).swapaxes(0, 1)  # CELLPOSE 4 INVERT SHAPE
                    print(f"masks shape {masks.shape} and raw shape {image_input.shape}")
                    imsave(output_filename, masks, check_contrast=False)








