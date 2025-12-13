import os
import matplotlib.pyplot as plt
import numpy as np


def get_network_planseg(specie):
    if specie=="LP": return "generic_light_sheet_3D_unet"
    if specie == "OV": return "generic_confocal_3D_unet"
    if specie == "AT":  return  "confocal_3D_unet_sa_meristem_cells"


def get_main_path():
    main_path = "/Users/efaure/Codes/PythonProjects/morphodeep/figures"  # Local
    if not os.path.isdir(main_path): main_path = "/linkhome/rech/genlir01/uhb36wd/morphodeep/figures"  # Jean Zay
    return main_path

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
    plt.savefig(filename+".png", dpi = sizes[0])
    plt.close()