from os.path import join, isfile, isdir
from os import listdir
from os.path import join
from morphodeep.tools.image import imsave,imread
from morphodeep.tools.utils import mkdir, execute
import numpy as np


def download_Arabidopsis_data(at_path):
    if not isdir(at_path):
        print(" --> you have first to download platseg data to "+at_path)
        print(" From :Willis L, Refahi Y, Wightman R, Landrein B, Teles J, Huang KC, Meyerowitz EM, Jönsson H. Cell size and growth regulation in the Arabidopsis thaliana apical stem cell niche. Proc Natl Acad Sci U S A. 2016 Dec 20;113(51):E8238-E8246. doi: 10.1073/pnas.1616768113. Epub 2016 Dec 5. PMID: 27930326; PMCID: PMC5187701..")
        print("https://doi.org/10.1073/pnas.1616768113")
        print(" Data location : https://www.repository.cam.ac.uk/items/f7cdcf20-e8ca-4cf5-b7ab-90350a8d00b2 ")
        print("wget https://www.repository.cam.ac.uk/bitstreams/95babfae-ae16-4dae-82f5-8656ceace4d6/download")
        print("mkdir Arabidopsis")
        print("mv download Arabidopsis/PNAS.zip")
        print("cd Arabidopsis")
        print("unzip PNAS.zip")
        return False
    return True

def get_seg_name(filename,path):
    for f in listdir(path):
        if f.startswith(filename.replace(".tif","")):
            return join(path,f)
    return None

def extract_Arabidopsis(at_path, gt_path):
    print(f" --> Extract Arabidopsis data  from {at_path} to {gt_path}")
    if not download_Arabidopsis_data(at_path): return False
    at_path=join(at_path,"PNAS")
    for embname in listdir(at_path):
        if isdir(join(at_path,embname)):
            if not isdir(join(at_path, embname)) or not isdir(join(at_path, embname,"processed_tiffs"))  or not isdir(join(at_path, embname,"segmentation_tiffs")) :
                print(f" --> ERROR Extract  Arabidopsis data for {join(at_path,embname)}")
                quit()

            mkdir(join(gt_path, "membrane", embname))
            mkdir(join(gt_path, "segmented", embname))

            for membrane_filename in listdir(join(at_path, embname, "processed_tiffs")):
                if membrane_filename.endswith("acylYFP.tif"):
                    output_mem_filename = join(gt_path, "membrane", embname, membrane_filename.replace(".tif", "_M.tiff"))
                    output_seg_filename = join(gt_path, "segmented", embname, membrane_filename.replace(".tif", "_S.tiff"))

                    if not isfile(output_mem_filename) and not isfile(output_seg_filename):
                        print(f"-->  processing "+join(at_path,embname,"processed_tiffs",membrane_filename))
                        seg_filename = get_seg_name(membrane_filename, join(at_path, embname, "segmentation_tiffs"))
                        if seg_filename is None or not isfile(seg_filename):
                            print(f" --> ERROR Extract Arabidopssis Seg for {seg_filename}")
                        else:

                            membrane = imread(join(at_path,embname,"processed_tiffs",membrane_filename))
                            seg = imread(seg_filename)


                            if membrane.shape != seg.shape:
                                print(f" --> ERROR Shape different {membrane.shape} and {seg.shape} ")
                                quit()
                            seg[seg==1]=0 #BACKGROUND
                            print(f"--> Save {output_mem_filename}")
                            imsave(output_seg_filename,seg)
                            imsave(output_mem_filename,membrane)

            execute(f"rm -rf {join(at_path, embname)}")







