import sys,os
sys.path.append('../../')
from os.path import basename, join, isfile
from morphodeep.tools.utils import get_last_epochs, get_weights_filename, mkdir
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation
import numpy as np
output_path="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic_Figure/figure_2"
mkdir(output_path)
filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_3D/SPIM-Phallusia-Mammillata/membrane/140317-Patrick-St8/140317-Patrick-St8_fuse_t100_M.tiff" #Bakcground effect
#filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_3D/CONF-Arabidopsis-Thaliana/membrane/plant4/20hrs_plant4_trim-acylYFP_M.tiff" #Closure Effect
im=imread(filename)
im=np.swapaxes(im,0,2)
print(im.shape)
step_shape=10
step_epochs=10

model = MorphoModel(method="FusedToSemantic", network="DUNNET", mode="2D")
model.load_model()
print(f"model.weight_files is {model.weight_files}")
last_epochs=get_last_epochs(model.weight_files)
print(f"Last epoch is {last_epochs}")
nbTI=0
for e in range(0, last_epochs, step_epochs):
    wfilename = get_weights_filename(model.weight_files, e)
    if wfilename is not None and isfile(wfilename):
        nbTI+=1

nbTZ=0
for z in range(0,im.shape[2],step_shape):
    nbTZ+=1

imt = np.zeros(im[...,0].shape + (nbTI,nbTZ), dtype=np.uint8)
print(f"new shape{imt.shape}")
nbI=0
for e in range(0,last_epochs,step_epochs):
    if model.load_weights(epochs=e) != -1:
        nbZ = 0
        for z in range(0,im.shape[2],step_shape):
            print(f"Processing epoch: {e} for z:{z}")
            imt[...,nbI,nbZ] = model.predict(im[...,z], patches=False)
            nbZ+=1
        nbI+=1

nbZ=0
for z in range(0,im.shape[2],step_shape):
    sem_file = join(output_path, basename(filename).replace("M.tiff", f"E{e}_Z{z}_S.tiff"))
    print(f"Export to {sem_file}")
    sem=imt[...,nbZ]
    imsave(sem_file, np.swapaxes(sem, 0, 2))
    #Generate segmentation
    imz = np.zeros(im[..., 0].shape + (nbTI,), dtype=np.uint16)
    for nbI in range(sem.shape[2]):
        imz[...,nbI]=semantic_to_segmentation(sem[...,nbI])

    imsave(sem_file.replace("S.tiff", "SEG.tiff"),np.swapaxes(imz, 0, 2))
    nbZ+=1