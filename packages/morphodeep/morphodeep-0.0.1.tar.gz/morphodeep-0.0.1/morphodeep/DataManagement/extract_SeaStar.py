from os import listdir
from os.path import join, isdir, isfile
from difflib import SequenceMatcher

from skimage.io import imsave
from skimage.transform import resize

from morphodeep.tools.image import imread
import numpy as np

from morphodeep.tools.utils import mkdir, execute


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_corresponding(name,path,done):
    best=None
    bestv=0
    trunk=name[0:name.find("_",9)]
    rtrunk=name[name.rfind("_"):]
    rtrunk=rtrunk.replace("stk010.tif","stk10.tif")
    for file in listdir(path):
        if file not in done and file.startswith(trunk) and file.endswith(rtrunk):
            bv=similar(name,file)
            if bv>bestv:
                bestv=bv
                best=file
    return best


def extract_SeaStar_data(seastar_path,gt_path):
    raw_path="high-resolution_raw_images_resized"
    seg_path="high-resolution_label_images"
    print(" --> Extract SeaStar data from " + seastar_path + " to " + gt_path)

    for what in listdir(join(seastar_path,raw_path)) : #128-cell-stage, etc.. 
        if isdir(join(seastar_path,raw_path,what)):
            for emb_type in listdir(join(seastar_path,raw_path,what)): #WT, WT-Comp
                done=[]
                for f in listdir(join(seastar_path, raw_path, what,emb_type)):

                    filename = join(gt_path, "segmented", what, emb_type + "_" + f.replace(".tif", '_S.tiff'))
                    if isfile(filename):
                        print(f"--> done {filename}")
                    else:
                        mem_name = join(seastar_path, raw_path, what, emb_type, f)
                        print(" -> process "+mem_name)
                        #Look for the corresponding segmneted name
                        seg_name=get_corresponding(f,join(seastar_path,seg_path,what,emb_type),done)
                        if seg_name is None:
                            print(" --> didn't find any correspondance ")
                            quit()
                        done.append(seg_name)
                        seg_name=join(seastar_path,seg_path,what,emb_type,seg_name)
                        #print( " ------------> "+seg_name)
                        raw=imread(mem_name)
                        seg=imread(seg_name)
                        a,c=np.unique(seg,return_counts=True)
                        ratio = c.max() / c[c < c.max()].max()
                        if ratio<10:
                            idx = a[np.where(c == c[c < c.max()].max())[0][0]]
                            seg[seg == idx] = 0  # Inside the embryo
                            print(" --> remove "+str(idx)+ " which is in the middle of the embryo")

                        if raw.shape!=seg.shape:
                            print(" --> shape error")
                            print(raw.shape)
                            print(seg.shape)
                            quit()

                        mkdir(join(gt_path, "segmented", what))
                        mkdir(join(gt_path, "membrane", what))
                        seg[seg == 1] = 0  # CHANGE BACKGROUND VALUE
                        print(" --> save segmented "+str(filename))
                        imsave(join(gt_path,"membrane",what, emb_type + "_" + f.replace(".tif",'_M.tiff')),raw)
                        imsave(filename,seg,check_contrast=False)
    print(" --> everythig is extracted")
#