from os.path import join, isfile, isdir
from os import listdir
from os.path import join

from morphodeep.tools.image import imsave
from morphodeep.tools.utils import mkdir
import numpy as np

def download_PlantSeg_data(plantseg_path):
    if not isdir(plantseg_path):
        print(" --> you have first to download platseg data to "+plantseg_path)
        print(" From : Adrian Wolny Lorenzo Cerrone Athul Vijayan Rachele Tofanelli Amaya Vilches Barro Marion Louveaux Christian Wenzl Sören Strauss David Wilson-Sánchez Rena Lymbouridou Susanne S Steigleder Constantin Pape Alberto Bailoni Salva Duran-Nebreda George W Bassel Jan U Lohmann Miltos Tsiantis Fred A Hamprecht Kay Schneitz Alexis Maizel Anna Kreshuk (2020) Accurate and versatile 3D segmentation of plant tissues at cellular resolution eLife 9:e57613.")
        print("https://doi.org/10.7554/eLife.57613")
        print(" Data location : https://osf.io/uzq3w/ ")
        print(" --> Rename PATH in CONF-Ovules and CONF-LateralRootPrimordia")
        return False
    return True


def extract_PlantSeg_data(data_type,plantseg_path,gt_path):
    import h5py
    print(" --> Extract PlantSeg data for "+data_type+ " from "+plantseg_path+ " to "+gt_path)
    if not download_PlantSeg_data(plantseg_path): return False
    mkdir(gt_path)
    for what in ["train","test","val"]:
        mkdir(join(gt_path,"membrane",what))
        mkdir(join(gt_path,"segmented",what))
        for filename in listdir(join(plantseg_path, data_type,what)):
            if filename.endswith("h5") and  filename:
                print("--> Extract from "+join(plantseg_path, data_type,what,filename))
                emb_time = filename.replace(".h5", "")
                if not isfile(join(gt_path, "segmented", what, emb_time + '_S.tiff')):
                    hf = h5py.File(join(plantseg_path, data_type,what,filename), 'r')

                    raw=hf.get('raw')
                    label = np.array(hf.get('label'))
                    if data_type=="CONF-LateralRootPrimordia":
                        label[label==1]=0 #CHANGE BACKGROUND VALUE

                    if not isfile(join(gt_path, "segmented", what,emb_time+'_S.tiff')):
                        imsave(join(gt_path,"membrane",what,emb_time+'_M.tiff'),raw)
                        imsave(join(gt_path, "segmented", what,emb_time+'_S.tiff'),label)

