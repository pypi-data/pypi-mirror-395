#Launch  the prediction with different environnemnt (cellpose3,cellpose4, plant-seg, morphodeep ...)
#The Evaluation has to be launch with the conda morphodeep
import argparse
import os.path
from datetime import datetime
import sys
from skimage.transform import resize
from math import isnan

sys.path.append("../")

from os import listdir
import pandas as pd
from os.path import isfile, join, isdir, basename, dirname

import h5py
import numpy as np

from morphodeep.paths import SCRATCH, WORK, RESULT
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation
from morphodeep.tools.utils import execute, mkdir, get_specie_from_name, get_specie

parser = argparse.ArgumentParser()
parser.add_argument("--eval",action="store_true")
parser.add_argument("--predict",action="store_true")
parser.add_argument('-f',"--filename", default=None, help="external filename to be evaluated")
parser.add_argument('-m',"--method", default="semantic", help="cellpose3,cellpose4,semantic,plantseg")
parser.add_argument('-t',"--mode", default="3D", help="2D,3D")
parser.add_argument('-sp',"--specie", default="all", help="PM,CE,AT,OT,all...")
parser.add_argument('-mo',"--microscope", default="ALL", help="ALL,CONF,SPIM")
parser.add_argument('-n',"--network", default="JUNNET", help="DUNNET,etc..")
parser.add_argument('-i',"--img_size", default=256, help="128,256")
parser.add_argument('-p',"--patches", default="True", help="True or False")
parser.add_argument('-e',"--epochs", default=0, help="number of epochs")
args = parser.parse_args()
method=args.method
patches=args.patches=="True"
specie=args.specie
microscope=args.microscope
img_size=args.img_size
mode=args.mode
network=args.network
epochs=None if args.epochs==0 else int(args.epochs)
external_filename=args.filename

sys.argv=[sys.argv[0]] #Reset args for MorphoModel

#RESULT, PANDAS FRAMEWORK
thresholds_IOU=[0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.98, 1]
columns = ["Filename", "Number of Cells", "Size X", "Size Y", "Size Z", "Prediction Time", "Error Rate",
           "Average Precision", "Precision", "Recall", "IOU", "IOU Quality"]
for threshold in thresholds_IOU:  columns.append(f"AP IOU Threshold {threshold}")
columns.append("Vi Split")
columns.append("Vi Merge")
columns.append("Vi Total")


def get_env():
    sp = sys.path[1].split("/")
    if "envs" in sp:
        sp=sp[sp.index("envs") + 1]
        if sp.startswith("cellpose"):
            if sp=="cellpose": return 2
            return int( sp[8:])
    return 0

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
        print("CellPose is required for prediction")
        quit()
    return cp_version,model

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

def get_free_index(df):
    indexs = df.index
    i = len(indexs)
    while i in indexs:
        i += 1
    return i

def open_results(filename):
    if isfile(filename):
        df = pd.read_csv(filename,sep=';',encoding='utf-8',index_col='Unnamed: 0',low_memory=False)
    else:
        df = pd.DataFrame()

    #Add Missing Columns
    for c in columns:
        if c not in df:
            df[c] = None

    return df

def save_results(filename,time_process):
    time_process.to_csv(filename, sep=';', encoding='utf-8',  header=True)

def get_index(df,name):
    indexs=df.loc[df.Filename==name]
    if len(indexs.index)>0:
        return indexs.index[0]
    return None

def insert(df,fname,what,value):
    index=get_index(df,fname)
    #print(f" --> Inserting {what} at index {index}")
    if index is None:#Create a new entry
        empty_col=[fname]
        for c in range(len(columns)-1):empty_col.append(None)
        df.loc[ get_free_index(df)] = empty_col
    index = get_index(df, fname)
    #print(f" --> Inserting {what} at index {index}")
    if index is None:
        print(f"Error finding the index for {fname}")
        quit()
    df.at[index,what] = value
    return df

def isfilling(df,fname):
    idx = get_index(df, fname)
    #print(f"Missing {fname} at index {idx}")
    if idx is None: return False #Not the predicted data
    '''for w in df.loc[idx]:
        try:
            if isnan(float(w)):
                #print(f"Missing value for {w}")
                return True
        except:
            a = 1
    return False
    '''
    a=df.loc[df.Filename == fname]["Size X"]>0
    return a.any()

def create_config_plantseg(filename):
    execute("rm -rf " + PLANTSEG_PATH)
    mkdir(PLANTSEG_PATH)
    config_file = join(PLANTSEG_PATH, "config_plantseg.yaml")
    print(" --> prepare config file " + config_file)
    network_plantseg = {}
    network_ps = None
    network_plantseg["CONF-LateralRootPrimordia"] = "generic_light_sheet_3D_unet"
    network_plantseg["CONF-Ovules"] = "generic_confocal_3D_unet"
    network_plantseg["CONF-Arabidopsis-Thaliana"] = "confocal_3D_unet_sa_meristem_cells"
    network_plantseg["SPIM-Phallusia-Mammillata"] = "generic_light_sheet_3D_unet"
    network_plantseg["CONF-SeaStar"] = "generic_confocal_3D_unet"
    network_plantseg["CONF-Caenorhabditis-Elegans"] = "generic_confocal_3D_unet"
    for n in network_plantseg.keys():
        if filename.find(n)>0:
            network_ps=network_plantseg[n]
    if network_ps is None:
        print(f"Didnt find network for {filename}")
        quit()
    fw = open(config_file, "w")
    fw.write('path: ' + PLANTSEG_PATH + "\n")
    for line in open("../../semantic/DataManagement/config_plantseg.template", "r"):
        if line.find("model_name") >= 0:
            fw.write('  model_name: "' + network_ps + '"')
        else:
            fw.write(line)
    fw.close()
    return config_file,network_ps

def get_names(f):
    input_filename=None
    output_filename=None
    gt_filename=None
    semantic_filename = None
    voxelsize=None
    if external_filename is not None:
        tab = f.split(";")
        if len(tab) < 3:
            print(f"Not well define {f} ")
            print("Should be, input_file,ground_truth_file,spacing")
            quit()
        input_filename = tab[0]
        extension = os.path.splitext(input_filename)[1]
        if extension == ".gz":  extension = os.path.splitext(os.path.splitext(input_filename)[0])[1] + extension
        gt_filename = tab[1]
        output_filename = input_filename.replace(extension, f"_{name}_{ext}" + extension)
        if method == "semantic":
            semantic_filename = output_filename.replace(f"_{ext}", "_SEM")
        voxelsize=tab[2].split("x")
        voxelsize = [float(voxelsize[0]), float(voxelsize[1]), float(voxelsize[2])] if len(voxelsize) == 3 else [float(voxelsize[0]), float(voxelsize[1])]
    else:
        input_filename = f.strip()
        # specie=get_specie_from_name(f)
        gt_filename = input_filename.replace("membrane", "segmented").replace("_M.tiff", "_S.tiff")
        output_filename = input_filename.replace(f"GT_{mode}", f"PD_{mode}").replace("membrane", name).replace("_M.tiff",
                                                                                                  f"_{ext}.tiff")
        if method == "semantic":
            if ms == "ALL-all":
                output_filename = input_filename.replace(f"GT_{mode}", f"PD_{mode}/{ms}/{name}").replace("membrane/", f"").replace(
                    "_M.tiff", f"_{ext}.tiff")

            semantic_filename = output_filename.replace(f"_{ext}.tiff", f"_SEM.tiff")
    return input_filename,output_filename,gt_filename,semantic_filename,voxelsize

TEMP_PATH = join(SCRATCH,"TEMP","TEMPORAL" ) #TEMPORARY , WILL BE DELETED AFTER
mkdir(TEMP_PATH)
PLANTSEG_PATH = join(TEMP_PATH, "PlantSeg")

#List of files to predict
ms=f"{microscope}-{get_specie(specie)}"
if external_filename is not None:
    predict_file=external_filename
    baseevalname="EVAL_EXTERNAL"
else:
    predict_file=join(WORK,"Semantic",f"NETWORKS_{img_size}_{mode}",f"{ms}/tf_test.txt") #DEFAULT TEST
    baseevalname="EVAL"

#Output Path
path_file = f"{RESULT}/NETWORKS_{img_size}_{mode}/" #Depend of the specie in the file
mkdir(path_file)
#COMMON TO PREDICTION AND EVALUATION
name=method
ext=None
if method.startswith("cellpose"):
    time_file = join(path_file, ms,f"{baseevalname}_{method}.csv")
    ext="CP"
elif method == "plantseg":
    time_file = join(path_file, ms,f"{baseevalname}_{method}.csv")
    ext="PS"
elif method == "semantic":
    from morphodeep import MorphoModel
    if epochs is not None and epochs > 0:
        model = MorphoModel(network=network, mode=mode, img_size=img_size, specie=specie, microscope=microscope,epochs=epochs)
        model.load_model()
        model.load_weights(epochs=epochs)
    else:
        model = MorphoModel(network=network, mode=mode, img_size=img_size, specie=specie, microscope=microscope)
        model.load_model()
        model.load_weights()
        epochs = model.epochs_loaded
        if epochs==0:
            print(f"Didnt find epochs for {method}")
            quit()
    ext="SEG"
    path_file = f"{RESULT}/NETWORKS_{img_size}_{mode}/{ms}"  # Depend of the specie in the model
    time_file = join(path_file, f"{network}_{img_size}", f"{baseevalname}_{network}_{img_size}_EPOCHS_{epochs}.csv")
    name = f"{network}_{img_size}_EPOCHS_{epochs}"
    if patches:
        time_file =time_file.replace(".csv","_patches.csv")
        name=name+"_patches"

else:
    print("Unknown method")
    quit()

mkdir(os.path.dirname(time_file))

excluded=["190417-Evan-U0126_fuse_t028_M.tiff","Movie1_t00006_crop_gt_M.tiff","N_435_final_crop_ds2_M.tiff","N_441_final_crop_ds2_M.tiff","170226-Alexandre-St8_fuse_t037_M.tiff","170226-Alexandre-St8_fuse_t069_M.tiff","170226-Alexandre-St8_fuse_t048_M.tiff"]

#COunt nimber of lines ..
nb_lines=0
for f in open(predict_file,"r"):nb_lines+=1

#os.system(f"rm -rf {time_file}")
print(f"\n\n RESULT {time_file}\n\n")
df = open_results(time_file)
#os.system(f"cp {time_file} "+time_file.replace(".csv",".keep"))
if args.predict:
    if method.startswith("cellpose"):
        cp_version, model = import_cellpose()
        print(f" --> Found CellPose {cp_version}")
        if method!=f"cellpose{cp_version}":
            print("Error version do not correspond to conda environnement")
            quit()
    elif method == "plantseg":
        execute("rm -rf " + PLANTSEG_PATH)
        mkdir(PLANTSEG_PATH)

    i=0
    for f in open(predict_file,"r"):
        if not f.startswith("#"):
            input_filename, output_filename, gt_filename, semantic_filename,vs=get_names(f)
            #print(f"{i}/{nb_lines} -->Process {input_filename} ")
            if basename(input_filename)  in excluded : print(f"{i}/{nb_lines} --> {input_filename} excluded")
            elif get_index(df, input_filename) is not None:  print(f"{i}/{nb_lines} --> {output_filename} already exists")
            elif isfile(input_filename):
                print(f"{i}/{nb_lines}  --> Processing  {output_filename}")
                membrane=imread(input_filename)
                if membrane is None :
                    print(f"Error Missing {input_filename} ")
                else:
                    z_axis = np.where(membrane.shape == np.min(membrane.shape))[0][0] if mode=="3D" else None

                    masks=None
                    end=None
                    mkdir(dirname(output_filename))
                    if method.startswith("cellpose"):
                        start = datetime.now()
                        do_3D=True if  mode=="3D" else False
                        if cp_version == 2 or cp_version == 3:
                            segmentation = imread(gt_filename)
                            if segmentation is None:
                                print(f"Error Missing Segmentation File {gt_filename}")
                                quit()
                            masks = model.eval(membrane, diameter=get_diameter(segmentation), do_3D=do_3D)[0]
                        elif cp_version == 4:
                            #masks = model.eval(membrane, do_3D=do_3D, z_axis=z_axis)[0]
                            masks, flows, styles = model.eval(np.stack((membrane, 0 * membrane, 0 * membrane), axis=-1),
                                                              channel_axis=-1, z_axis=z_axis, niter=1000,
                                                              flow3D_smooth=2, diameter=30,
                                                              bsize=256, batch_size=64,
                                                              channels=None, do_3D=do_3D, min_size=1000)

                        if mode=="3D":
                            #print(f"BEFORE mask={masks.shape}, membrane={membrane.shape} with z_axis={z_axis}")
                            if z_axis == 1: masks = np.swapaxes(masks, 0, 1)
                            if z_axis == 2: masks = np.swapaxes(np.swapaxes(masks, 0, 2),0,1)
                        if masks.shape!=membrane.shape:
                            print("ERROR SHAPES")
                            print(f"mask={masks.shape}, membrane={membrane.shape} with z_axis={z_axis}")
                            quit()
                        end = datetime.now()
                    elif method == "semantic":
                        start = datetime.now()
                        original_shape = None
                        if mode=="3D" and vs is not None and vs[0] != vs[2]:
                            original_shape = membrane.shape
                            ratio = vs[2] / vs[0]
                            if z_axis == 0:   new_shape = np.uint16([membrane.shape[0] * ratio, membrane.shape[1], membrane.shape[2]])
                            elif z_axis == 1:   new_shape = np.uint16([membrane.shape[0], membrane.shape[1] * ratio, membrane.shape[2]])
                            else:   new_shape = new_shape = np.uint16([membrane.shape[0], membrane.shape[1], membrane.shape[2] * ratio])
                            membrane = resize(membrane, new_shape, preserve_range=True).astype(membrane.dtype)
                            print(f" --> Resized using voxel size to {membrane.shape}")
                        sem=model.predict(membrane,patches=patches)
                        masks=semantic_to_segmentation(sem)
                        if original_shape is not None:
                            masks=resize(masks,original_shape, preserve_range=True,order=0).astype(masks.dtype)
                        end=datetime.now()

                        imsave(semantic_filename,sem)
                    elif method == "plantseg":
                        config_file,network_ps=create_config_plantseg(input_filename)
                        imsave(join(PLANTSEG_PATH,"membrane.tiff"), membrane)
                        start = datetime.now()

                        execute("plantseg --config " + config_file)
                        if not isdir(join(PLANTSEG_PATH, "PreProcessing")):
                            print(" --> MISS Preprocessing path " + join(PLANTSEG_PATH, "PreProcessing"))
                            quit()
                        plantseg_name = join(PLANTSEG_PATH, "PreProcessing", network_ps,"membrane_predictions.h5")
                        if not isfile(plantseg_name):
                            print(" --> MISS filename " + plantseg_name)
                        else:
                            end = datetime.now()
                            fw = h5py.File(plantseg_name, 'r')
                            imsave(output_filename.replace("PS.tiff","PRED.tiff"), fw['predictions'])

                        plantseg_multicut_name = join(PLANTSEG_PATH, "PreProcessing", network_ps,"MultiCut","membrane_predictions_multicut.h5")
                        if isfile(plantseg_multicut_name):
                            fw = h5py.File(plantseg_multicut_name, 'r')
                            masks = fw['segmentation']

                    if end is None:
                        print(f"error during prediction of {f}")
                    else:
                        c_time=(end - start).total_seconds()
                        print(f"-->  {input_filename} in {c_time}s")
                        df=insert(df,input_filename,"Prediction Time",c_time)
                        save_results(time_file, df)
                        imsave(output_filename, masks)

        i+=1

if args.eval or method == "semantic":
    from morphodeep.networks.metrics import eval_metrics, voi_metrics
    i=0
    for f in open(predict_file, "r"):
        if not f.startswith("#"):
            input_filename, output_filename, gt_filename, semantic_filename,vs = get_names(f)
            #print(f"{i}/{nb_lines} -->Process {input_filename} ")
            if basename(input_filename) in excluded: print(f"{i}/{nb_lines} --> {input_filename} excluded")
            elif not isfile(output_filename):
                print(f"{i}/{nb_lines} -->  {output_filename} missing output file ")
            elif isfilling(df,input_filename) :
                print(f"{i}/{nb_lines} -->  {output_filename} already eval")
            else:
                print(f"{i}/{nb_lines} --> eval {output_filename}")
                segmentation = imread(gt_filename)
                masks = imread(output_filename)
                z_axis = np.where(segmentation.shape == np.min(segmentation.shape))[0][0] if mode=="3D" else 0
                if masks.shape!=segmentation.shape:
                    if z_axis==1: masks=np.swapaxes(masks,0,1)
                    if z_axis == 2: masks = np.swapaxes(masks, 0, 2)
                if masks.shape!=segmentation.shape:
                    print(f"mask={masks.shape} seg={segmentation.shape} z_axis={z_axis}")
                    print("ERROR")
                    quit()

                nb_cells = len(np.unique(segmentation)) - 1  # Remove Background
                #print(f"segmenation shape {segmentation.shape} and masks {masks.shape}")

                error_rate, average_precision, precision, recall, iou, iou_over = eval_metrics(segmentation, masks)
                #print(error_rate, average_precision, precision, recall, iou, iou_over)
                stats={}
                for threshold in thresholds_IOU:
                    error_rate2, average_precision2, precision2, recall2, iou2, iou_over2= eval_metrics(segmentation, masks,threshold=threshold)
                    stats[threshold]=average_precision2

                vi_split, vi_merge, vi_total=voi_metrics(segmentation, masks)


                df = open_results(time_file)
                insert(df,input_filename, "Error Rate", error_rate)
                insert(df,input_filename,"Average Precision",average_precision)
                insert(df,input_filename, "Precision", precision)
                insert(df,input_filename, "Recall", recall)
                insert(df,input_filename, "IOU", iou)
                insert(df,input_filename, "IOU Quality", str(iou_over))
                insert(df,input_filename, "Number of Cells", nb_cells)
                insert(df,input_filename, "Size X", masks.shape[0])
                insert(df,input_filename, "Size Y", masks.shape[1])
                if len(masks.shape)==3: insert(df,input_filename, "Size Z", masks.shape[2])
                insert(df, input_filename, "Vi Split", vi_split)
                insert(df, input_filename, "Vi Merge",vi_merge)
                insert(df, input_filename, "Vi Total", vi_total)
                for threshold in thresholds_IOU:
                    insert(df,input_filename, f"AP IOU Threshold {threshold}",stats[threshold])
                save_results(time_file, df)
                #print(df.loc[get_index(df,input_filename)])


        i+=1

print(" --> ALL DONE ")
print(" --> ALL DONE ")