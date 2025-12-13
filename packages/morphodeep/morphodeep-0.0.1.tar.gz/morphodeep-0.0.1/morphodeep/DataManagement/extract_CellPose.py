from os.path import join, isfile, isdir
from os import listdir
from os.path import join

from morphodeep.tools.image import imsave, imread
from morphodeep.tools.utils import mkdir
import numpy as np
##### Junctions Extraction First #interface_cellpose_gtk_2.0.py
##### Green Channel Only #channel_eval.py

def extract_Cellpose_data(data_type,cellpose_path,gt_path,img_size=128, step=64):
    import h5py
    print(" --> Extract Cellpose data for "+data_type+ " from "+cellpose_path+ " to "+gt_path)
    for what in ["train_cyto2_junction_gray","test_cyto2_junction_gray"]:
        mkdir(join(gt_path,"membrane",what))
        mkdir(join(gt_path,"segmented",what))
        for filename in listdir(join(cellpose_path,what)):
            segfilename = filename.replace("_img.png", "_masks.png")
            if filename.endswith("_img.png") and isfile(join(cellpose_path,what,segfilename)):
                print("--> Extract from "+join(cellpose_path,what,filename))
                emb_time=filename.replace("_img.png", "")
                mkdir(join(gt_path,"membrane",what, emb_time))
                mkdir(join(gt_path, "segmented", what, emb_time))

                raw=imread(join(cellpose_path, what, filename))
                label = imread(join(cellpose_path, what, segfilename))

                shape=raw.shape
                print(" ------> shape is "+str(shape))

                for x in range(0,shape[0]+img_size,step):
                    maxX = x + img_size
                    minX = x
                    if maxX >= shape[0]:
                        maxX = shape[0] - 1
                        minX = maxX - img_size
                    if minX < 0: minX = 0
                    for y in range(0,shape[1]+img_size,step):
                        maxY = y + img_size
                        minY = y
                        if maxY >= shape[1]:
                            maxY = shape[1] - 1
                            minY = maxY - img_size
                        if minY < 0: minY = 0
                        stop=False
                        if maxX - minX != img_size: stop = True
                        if maxY - minY != img_size: stop = True
                        if stop:
                            print(minX,maxX,minY,maxY)
                            quit()

                        if not stop:
                            codename="_X"+str(minX)+"_Y"+str(minY)
                            if not isfile(join(gt_path, "segmented", what, emb_time,emb_time+codename+'_S.tiff')):
                                print(" --> extracting segmented "+join(gt_path, "segmented", what, emb_time,emb_time+codename+'_S.tiff'))
                                imsave(join(gt_path,"membrane",what, emb_time,emb_time+codename+'_M.tiff'),raw[minX:maxX,minY:maxY])
                                imsave(join(gt_path, "segmented", what, emb_time,emb_time+codename+'_S.tiff'),label[minX:maxX,minY:maxY])

