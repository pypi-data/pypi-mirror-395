import os
from os.path import dirname

import matplotlib.pyplot as plt
import numpy as np

from morphodeep.tools.utils import mkdir


def get_network_planseg(specie):
    if specie=="LP": return "generic_light_sheet_3D_unet"
    if specie == "OV": return "generic_confocal_3D_unet"
    if specie == "AT":  return  "confocal_3D_unet_sa_meristem_cells"


def get_binary_map():
    # Binary Color Map
    cols = np.zeros([5,3])
    cols[0,:]=[1,1,1] #OFF
    cols[4,:]=[1,0,0] #ON
    return plt.cm.colors.ListedColormap(cols)

def get_seg_map():
    #Semgnetaion color map (GLASBEY)
    import colorcet as cc
    seg_cmap=cc.glasbey
    seg_cmap[0]="#FFFFFF"
    return plt.cm.colors.ListedColormap(seg_cmap)

def get_semantic_map(only_colors=False):
    #Define Colors for Semantic
    #    0 : Background
    #    1 : Inside the Cell (Cytoplasm)
    #    2 : Junction Level 1 (Nice Membrane )
    #    3 : Junction Level 2
    #    4 : Junction Level 3
    cols = np.zeros([5,3])
    cols[0,:]=[0.5,0.5,0.5] #Background
    cols[1,:]=[1,1,0] #Inside the Cell (yellow)
    cols[2,:]=[0,0,1] #Junction Level 1 (Nice Membrane ) (red)
    cols[3,:]=[1,0,0] #Junction Level 2
    cols[4,:]=[0.5,0,0.5] #Junction Level 3
    if only_colors: return cols
    return plt.cm.colors.ListedColormap(cols)

def one_fig(data,cmap,filename):
    if type(cmap)==np.ndarray:
        cols = np.ones([2,3])
        cols[1,:]=cmap #Background
        cmap=plt.cm.colors.ListedColormap(cols)
    sizes = np.shape(data)
    fig = plt.figure()
    fig.set_size_inches(1. * sizes[1] / sizes[0], 1, forward = False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, cmap=cmap,aspect="equal",interpolation="nearest")
    mkdir(dirname(filename+".png"))
    plt.savefig(filename+".png", dpi = sizes[0])
    plt.close()

def get_metrics(eval):
    if eval is None or eval == "None": return None, None, None, None, None
    tab = eval.split(",")
    if len(tab) < 4: return None, None, None, None, None
    return float(tab[0].split(":")[1]), float(tab[1].split(":")[1]), float(tab[2].split(":")[1]), float(
        tab[3].split(":")[1]), float(tab[4].split(":")[1])

def im_set(ax, title, X, label1, Y, label2):
    ax.set_title(title)
    ax.set(xlabel=label1, ylabel=label2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.plot([0, 1], [0, 1], '-r')
    if len(X) > 0:
        # ax.plot([min(X), max(X)], [min(Y), max(Y)], '-r')
        ax.scatter(X, Y, s=10)

############ VIOLON PLOT

def remove_nan(m):
    return list(np.array(m)[np.isnan(m)==0])

def get_data(data):
    ErrorRate = []
    AveragePrecision = []
    Precision = []
    Recall = []
    IoU = []
    for e in data:
        er, ap, p, r, iou = get_metrics(data[e])
        if er is not None:  ErrorRate.append(er)
        if ap is not None:  AveragePrecision.append(ap)
        if p is not None:  Precision.append(p)
        if iou is not None:  IoU.append(iou)

    return remove_nan(ErrorRate), remove_nan(AveragePrecision), remove_nan(Precision), remove_nan(Recall), remove_nan(IoU)

def set_limit(data,max=1) :
    data=np.array(data)
    data[data>max]=max
    return list(data)

colors_methods={0:"red",1:"blue",2:"green",3:"yellow",4:"gray"} #JUNNET, Cellpose3,Cellpose4,PlantSeg,DUNNET

def plot_metric_violon(ax, data, label, xlabels):
    pos = []
    new_data = []
    for what in data:
        p=None
        if what.lower().startswith("cellpose3"):p=2
        elif what.lower().startswith("cellpose4"):p=3
        elif what.lower().startswith("junnet"):p=1
        elif what.lower().startswith("plantseg"):p=4
        elif what.lower().startswith("dunnet"):p=5
        pos.append(p)
        if len(data[what]) > 0: # Remove Empty list
            new_data.append(data[what])
        else:
            new_data.append([0])

    ax.set_title(label)

    violin_parts = ax.violinplot(new_data, pos, points=20, widths=0.3, showmeans=True, showextrema=True)
    # ax.set_ylim(0, 1)
    ax.set_xticks(pos)
    ax.set_xticklabels(xlabels, rotation=45, ha='right')
    ipc = 0
    for pc in violin_parts['bodies']:
        pc.set_facecolor(colors_methods[ipc])
        pc.set_edgecolor('black')
        ipc += 1


def plot_metrics_violon(name, datas):
    fig, axs = plt.subplots(1, 5, figsize=(25, 7))
    fig.suptitle(name)
    ErrorRate={}
    AveragePrecision={}
    Precision={}
    Recall={}
    IoU={}
    xlabels=[]
    for what in datas:
     ErrorRate[what], AveragePrecision[what], Precision[what], Recall[what], IoU[what] = get_data(datas[what])
     xlabels.append(what)
     #ErrorRate[what]=set_limit(ErrorRate[what])

    plot_metric_violon(axs[0], ErrorRate, "Error Rate", xlabels)
    plot_metric_violon(axs[1], AveragePrecision,  "Average Precision", xlabels)
    plot_metric_violon(axs[2], Precision, "Precision", xlabels)
    plot_metric_violon(axs[3], Recall, "Recall", xlabels)
    plot_metric_violon(axs[4],IoU, "IOU", xlabels)
    return fig
