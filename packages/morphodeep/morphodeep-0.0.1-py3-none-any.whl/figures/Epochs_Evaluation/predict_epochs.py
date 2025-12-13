import sys, os
from datetime import datetime
sys.path.append('../../')
from morphodeep.networks.metrics import eval_metrics
from morphodeep.tools.utils import mkdir
import pandas as pd
import numpy as np


import argparse
from os.path import isfile, join
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation

#python predict_epochs.py -i /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/EPOCHS_EVALUATION_3D/DATA -o /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/EPOCHS_EVALUATION_3D
#python predict_epochs.py -t 2D -i /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/EPOCHS_EVALUATION_2D/DATA -o /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/EPOCHS_EVALUATION_2D

parser = argparse.ArgumentParser()
parser.add_argument('-i',"--input_path", default=None, help="input file")
parser.add_argument('-o',"--output_path", default=None, help="output path")
parser.add_argument('-g',"--ground_truth", default=None, help="ground truth file")
parser.add_argument('-t',"--mode", default="3D", help="2D,3D")
parser.add_argument('-sp',"--specie", default="all", help="PM,CE,AT,OT,all...")
parser.add_argument('-mo',"--microscope", default="ALL", help="ALL,CONF,SPIM")
parser.add_argument('-n',"--network", default="JUNNET", help="DUNNET,etc..")
parser.add_argument('-im',"--img_size", default=256, help="128,256")
parser.add_argument('-p',"--patches", default="False", help="True or False")

args = parser.parse_args()
input_path=args.input_path
output_path=args.output_path
patches=args.patches=="True"
specie=args.specie
microscope=args.microscope
img_size=args.img_size
mode=args.mode
network=args.network
sys.argv=[sys.argv[0]] #Reset args for MorphoModel


mkdir(output_path)


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

def get_free_index(df):
    indexs = df.index
    i = len(indexs)
    while i in indexs:
        i += 1
    return i

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


#READ IMAGE AND SEGMENTATION
images={}
gt={}
nb_cells={}
for f in os.listdir(input_path):
    if f.find("_M.")>0:
        images[f.split("_M.")[0]]=imread(input_path+"/"+f)
    if f.find("_S.")>0:
        trunk=f.split("_S.")[0]
        gt[trunk]=imread(input_path+"/"+f)
        nb_cells[trunk]=len(np.unique( gt[trunk]))-1
print(f"Found {nb_cells}")

for f in images:
    if f not in gt:
        print(f"Error finding the index for {f}")
        quit()

model = MorphoModel(method="FusedToSemantic", network="JUNNET", mode=mode,img_size=img_size, specie=specie,microscope=microscope)
model.load_model()
model.load_weights()
epochs_loaded = model.epochs_loaded
print(f"epochs_loaded: {epochs_loaded}")

time_file = join(output_path,f"Compare_Epochs_{mode}_{img_size}_{specie}_{microscope}_{patches}.csv")
print(f"\n\n RESULT {time_file}\n\n")
df = open_results(time_file)
for epochs in range(0,epochs_loaded,20):
    epochs_name=f"EPOCHS_{epochs}"
    miss_it=False
    for f in images:
        fname = epochs_name+"_"+ f
        if get_index(df, fname) is  None:miss_it=True
    if miss_it:
        print(f"Predict {epochs}/{epochs_loaded} ")
        if model.load_weights(epochs=epochs)!=-1:
            for f in images:
                start = datetime.now()
                if f.startswith("10"):
                    semantic=model.predict(images[f],patches=False)
                else:
                    semantic = model.predict(images[f], patches=True)
                segmentation=semantic_to_segmentation(semantic)
                end = datetime.now()
                fname = epochs_name + "_" + f
                #imsave(join(output_path,f+"_"+epochs_name+"_SEM.tiff"),semantic)
                #imsave(join(output_path,f+"_"+epochs_name+"_SEG.tiff"),segmentation)

                error_rate, average_precision, precision, recall, iou, iou_over = eval_metrics(gt[f], segmentation)
                df = open_results(time_file)
                c_time = (end - start).total_seconds()

                df = insert(df, fname, "Prediction Time", c_time)
                insert(df, fname, "Error Rate", error_rate)
                insert(df, fname, "Average Precision", average_precision)
                insert(df, fname, "Precision", precision)
                insert(df, fname, "Recall", recall)
                insert(df, fname, "IOU", iou)
                insert(df, fname, "IOU Quality", str(iou_over))
                insert(df, fname, "Number of Cells", nb_cells[f])
                insert(df, fname, "Size X", gt[f].shape[0])
                insert(df, fname, "Size Y", gt[f].shape[1])
                if len(gt[f].shape) == 3: insert(df, fname, "Size Z", gt[f].shape[2])
                save_results(time_file, df)
                print(f"--> {f} -> {fname} in {c_time}s -> AP={average_precision}  IOU={iou}")

print(" DONE DONE !!")