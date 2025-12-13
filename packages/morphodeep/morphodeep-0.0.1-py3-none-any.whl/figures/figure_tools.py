from os import listdir
from os.path import isfile, join, isdir, basename
import pandas as pd
import os
from matplotlib import pyplot as plt
import random

def get_color_methods(method):
    colors_methods={"cellpose3":"orange","cellpose4":"red","plantseg":"green"}
    for cm in colors_methods:
        if method.find(cm)>0:
            return colors_methods[cm]
    #Variation of Semantic
    cmap=plt.cm.get_cmap("hsv", 30)
    is_in=0
    while is_in<50:
        i=random.randint(1,30)
        if cmap(i) not in colors_methods.values():
            colors_methods[method]=cmap(i)
            return colors_methods[method]
    return "blue" #default for all semantic

def open_results(filename):
    #print(f"Opening {basename(filename)}")
    if os.path.getsize(filename)==0: return None
    print(f"Adding {filename}")
    df = pd.read_csv(filename,sep=';',encoding='utf-8',index_col='Unnamed: 0',low_memory=False)
    return df

def add_results(results,img_size,ms,filename):
    if filename.endswith(".csv"):
        if img_size not in results: results[img_size] = {}
        if ms not in results[img_size]: results[img_size][ms] = {}
        #filename
        # EVAL_cellpose4.txt
        # EVAL_DUNNET_256_EPOCHS_143.csv
        #print(f"filename {filename}")
        '''if filename.lower().find("cellpose")>0 or filename.lower().find("plantseg")>0:
            method=basename(filename.replace(".csv","")).replace("EVAL_","")
        else: #Semantic
            tab=basename(filename.replace(".csv","")).replace("EVAL_","").split("_")
            method=tab[0]+"_"+tab[3] #Network ,  Epocjs
        '''
        method=ms+"_"+basename(filename.replace(".csv","")).replace("EVAL_","")
        if method not in results[img_size][ms]: results[img_size][ms][method] = {}
        df=open_results(filename)
        if df is not None:   results[img_size][ms][method]=df
    return results


def get_colums():
    # RESULT, PANDAS FRAMEWORK
    thresholds_IOU = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.98, 1]
    columns = ["Filename", "Number of Cells", "Size X", "Size Y", "Size Z", "Prediction Time", "Error Rate",
               "Average Precision", "Precision", "Recall", "IOU", "IOU Quality"]
    for threshold in thresholds_IOU:  columns.append(f"AP IOU Threshold {threshold}")
    columns.append("Vi Split")
    columns.append("Vi Merge")
    columns.append("Vi Total")
    return columns,thresholds_IOU