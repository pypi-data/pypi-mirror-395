from os import listdir
from os.path import join, isfile, isdir
import os

from skimage.io import imread

'''path="/lustre/fsn1/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/CONF-Ovules/cell_mask"

def rename(path):
    print(" --> rename "+str(path))
    for f in listdir(path):
        if isfile(join(path, f)):
            if f.endswith("tiff") and not f.endswith("CM.tiff")  and not f.endswith("_MASK.tiff"):
                os.system("mv '"+join(path,f)+"' '"+join(path,f.replace(".tiff","_MASK.tiff"))+"'")
        else:
            rename(join(path,f))

rename(path)
'''

'''
path="/lustre/fsstor/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/CONF-SeaUrchin/"
for method in listdir(path):
    if isdir(join(path, method)):
        for emb in listdir(join(path, method)):
            if emb.find(" stage")>=0:
                print("Rename "+join(path, method,emb.replace(" ","_")))
                os.rename(join(path, method,emb),join(path, method,emb.replace(" ","_")))
'''
'''#Rename in filename
path="/lustre/fswork/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/NETWORKS_512_3D/ALL-all"
for filename in listdir(path):
    if isfile(join(path, filename)) and filename.endswith(".txt") and filename.startswith("tf"):
        newfile=""
        for line in open(join(path,filename),'r'):
            newfile+=line.replace(" ","_")
        f=open(join(path,filename),'w')
        f.write(newfile)
        f.close()
'''

path="/lustre/fsn1/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/SPIM-Phallusia-Mammillata/segmented"
for emb in listdir(path):
    if isdir(join(path, emb)):
        for embdir in listdir(join(path, emb)):
            for f in listdir(join(path, emb,embdir)):
                if f.find("_z")>=0:
                    #print(f"read "+join(path, emb,embdir,f))
                    im=imread(join(path, emb,embdir,f))
                    if len(im.shape)==2:
                        os.system("rm -f "+join(path, emb,embdir,f))
                        print(" Remove "+join(path, emb,embdir,f))
