from os import listdir
from os.path import isdir, join, isfile

from tqdm import tqdm

from skimage.io import imread, imsave
'''
path="/Users/efaure/SeaFile/MorphoDeep/semantic/DATA/DATA_INTEGRATION/ALL-CellPose/membrane"
for what in listdir(path):
    if isdir(join(path,what)):
        for f in tqdm(listdir(join(path,what))):
            if f.endswith(".png"):
                nf=join(path,what,f.replace("_img.png","_M.tiff"))
                if not isfile(nf):
                    im=imread(join(path,what,f))
                    imsave(nf,im)
'''


path="/Users/efaure/SeaFile/MorphoDeep/semantic/DATA/DATA_INTEGRATION/ALL-CellPose/segmented"
for what in listdir(path):
    if isdir(join(path,what)):
        for f in tqdm(listdir(join(path,what))):
            if f.endswith(".png"):
                nf=join(path,what,f.replace("_masks.png","_S.tiff"))
                if not isfile(nf):
                    im=imread(join(path,what,f))
                    imsave(nf,im)
