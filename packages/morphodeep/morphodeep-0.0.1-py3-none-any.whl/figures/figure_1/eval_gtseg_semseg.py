#Launch  the prediction with different environnemnt (cellpose3,cellpose4, plant-seg, morphodeep ...)
#The Evaluation has to be launch with the conda morphodeep
import argparse
import os.path
from datetime import datetime
import sys
from math import isnan


sys.path.append("../../")
from morphodeep.tools.ground_truth import semantic
from morphodeep.networks.metrics import eval_metrics, voi_metrics

import pandas as pd
from os.path import isfile, join, basename
import numpy as np

from morphodeep.paths import SCRATCH, WORK
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation
from morphodeep.tools.utils import execute, mkdir, get_specie_from_name, get_specie

parser = argparse.ArgumentParser()
parser.add_argument('-t',"--mode", default="3D", help="2D,3D")
parser.add_argument('-sp',"--specie", default="all", help="PM,CE,AT,OT,all...")
parser.add_argument('-mo',"--microscope", default="ALL", help="ALL,CONF,SPIM")
parser.add_argument('-i',"--img_size", default=256, help="128,256")

args = parser.parse_args()
specie=args.specie
microscope=args.microscope
mode=args.mode
img_size=args.img_size
sys.argv=[sys.argv[0]] #Reset args for MorphoModel

#RESULT, PANDAS FRAMEWORK
thresholds_IOU=[0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.98, 1]
columns = ["Filename", "Number of Cells", "Size X", "Size Y", "Size Z", "Prediction Time", "Error Rate",
           "Average Precision", "Precision", "Recall", "IOU", "IOU Quality"]
for threshold in thresholds_IOU:  columns.append(f"AP IOU Threshold {threshold}")
columns.append("Vi Split")
columns.append("Vi Merge")
columns.append("Vi Total")


def open_results(filename):
    if isfile(filename):
        df = pd.read_csv(filename,sep=';',encoding='utf-8',index_col='Unnamed: 0')
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
        df.loc[len(df.index)] = empty_col
    index = get_index(df, fname)
    #print(f" --> Inserting {what} at index {index}")
    if index is None:
        print(f"Error finding the index for {fname}")
        quit()
    df.at[index,what] = value

def missing_eval(df,fname):
    idx = get_index(df, fname)
    #print(f"Missing {fname} at index {idx}")
    if idx is None: return False #Not the predicted data
    for w in df.loc[idx]:
        try:
            if isnan(float(w)):
                #print(f"Missing value for {w}")
                return True
        except:
            a = 1
    return False


#List of files to predict
ms=f"{microscope}-{get_specie(specie)}"
predict_file=join(WORK,"Semantic",f"NETWORKS_{img_size}_{mode}",f"{ms}/tf_test.txt")

#Output Path
path_file = f"/lustre/fswork/projects/rech/dhp/uhb36wd/Semantic_RESULT/NETWORKS_{img_size}_{mode}/" #Depend of the specie in the file
mkdir(path_file)
time_file = join(path_file, ms,f"EVAL_GTSEG_SEMSEG.csv")
mkdir(os.path.dirname(time_file))

print(f"\n\n RESULT {time_file}\n\n")

#COunt nimber of lines ..
nb_lines=0
for f in open(predict_file,"r"):nb_lines+=1

excluded=["Movie2_T00020_crop_gt_M.tiff","Movie1_t00006_crop_gt_M.tiff"]
df = open_results(time_file)
i=0
for f in open(predict_file,"r"):
    fname=f.strip()
    if get_index(df, fname) is not None:
        print(f"{i}/{nb_lines} -->  {fname} already computed")
    elif basename(fname) not in excluded:
        segmentation = fname.replace("membrane", "segmented").replace("_M.tiff", "_S.tiff")
        print(f"{i}/{nb_lines} --> {fname} ")
        if isfile(segmentation) and get_index(df, fname) is None:
            seg = imread(segmentation)
            semantic_name = fname.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff")
            if not isfile(semantic_name):
                #Generate the semantic
                print(f"-> Generate semantic segmentation for {semantic_name}")
                sem=semantic(seg)
                imsave(semantic_name,sem)
            else:
                sem=imread(semantic_name)

            start = datetime.now()
            semseg=semantic_to_segmentation(sem)
            end = datetime.now()
            c_time = (end - start).total_seconds()
            insert(df, fname, "Prediction Time", c_time)

            nb_cells = len(np.unique(segmentation)) - 1  # Remove Background
            # print(f"segmenation shape {segmentation.shape} and masks {masks.shape}")

            error_rate, average_precision, precision, recall, iou, iou_over = eval_metrics(seg, semseg)
            stats = {}
            for threshold in thresholds_IOU:
                error_rate2, average_precision2, precision2, recall2, iou2, iou_over2 = eval_metrics(seg, semseg,
                                                                                                     threshold=threshold)
                stats[threshold] = average_precision2

            vi_split, vi_merge, vi_total = voi_metrics(seg, semseg)

            df = open_results(time_file)
            insert(df, fname, "Error Rate", error_rate)
            insert(df, fname, "Average Precision", average_precision)
            insert(df, fname, "Precision", precision)
            insert(df, fname, "Recall", recall)
            insert(df, fname, "IOU", iou)
            insert(df, fname, "IOU Quality", str(iou_over))
            insert(df, fname, "Number of Cells", nb_cells)
            insert(df, fname, "Size X", semseg.shape[0])
            insert(df, fname, "Size Y", semseg.shape[1])
            if len(semseg.shape) == 3: insert(df, fname, "Size Z", semseg.shape[2])
            insert(df, fname, "Vi Split", vi_split)
            insert(df, fname, "Vi Merge", vi_merge)
            insert(df, fname, "Vi Total", vi_total)
            for threshold in thresholds_IOU:
                insert(df, fname, f"AP IOU Threshold {threshold}", stats[threshold])
            save_results(time_file, df)

    i+=1


print(" --> ALL DONE ")
print(" --> ALL DONE ")