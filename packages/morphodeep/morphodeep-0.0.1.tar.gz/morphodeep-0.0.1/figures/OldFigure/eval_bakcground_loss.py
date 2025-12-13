#LOAD SEMANTIC NETWORKS
import os,sys

from skimage.measure import label

morphodeep_path="/lustre/fshomisc/home/rech/genlir01/uhb36wd/morphodeep/"
sys.path.append(morphodeep_path)
from morphodeep.paths import SCRATCH,OLD_SCRATCH,TEMP

from os.path import isfile, join
import numpy as np
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation

'''nfj = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D", img_size=256,specie="PM",microscope="SPIM")
nfj.load_model()
nfj.load_weights(epochs=1000)

file_test="/lustre/fswork/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/NETWORKS_512_3D/SPIM-Phallusia-Mammillata/tf_test.txt"
for line in open(file_test,"r"):
    filename=line.strip().replace(OLD_SCRATCH,SCRATCH)
    if not isfile(filename):
        print("MISS"+filename)
    else:
        print(f" --> Process {filename}")
        im=imread(filename)
        out=nfj.predict_3D_semantic_full(im,crop=False)
        background=label(out==0)
        print(np.unique(background))

        #seg=semantic_to_segmentation(out)
        #print(np.unique(seg))
        imsave(join(TEMP,"BACKGROUND",os.path.basename(filename)),background)

'''
filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/SPIM-Phallusia-Mammillata/membrane/190926-Gedeon/190926-Gedeon_fuse_t188/190926-Gedeon_fuse_t188_M.tiff"
im = imread(filename)

nfj = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D", img_size=256,specie="PM",microscope="SPIM")
nfj.load_model()

preds={}
def write_result(preds,filename):
    f=open(filename,"w")
    for e in preds:
        f.write(str(e)+":")
        for v in preds[e]:  f.write(str(v)+";")
        f.write("\n")
    f.close()

for epoch in range(1,3898,50):
    print(f" -> Load epoch {epoch}")
    nfj.load_weights(epochs=epoch)
    out = nfj.predict_3D_semantic_full(im, crop=False)
    background = label(out == 0)
    v,c=np.unique(background, return_counts=True)
    preds[epoch]=c
    write_result(preds,"background_result.txt")




