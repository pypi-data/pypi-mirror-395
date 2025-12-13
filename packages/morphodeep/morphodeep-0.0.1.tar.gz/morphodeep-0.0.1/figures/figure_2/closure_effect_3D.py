import sys,os
sys.path.append('../../')
from os.path import basename, join, isfile
from morphodeep.tools.utils import get_last_epochs, get_weights_filename
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation
import numpy as np
output_path="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic_Figure/figure_2"
filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_3D/SPIM-Phallusia-Mammillata/membrane/140317-Patrick-St8/140317-Patrick-St8_fuse_t100_M.tiff"
#filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_3D/CONF-Arabidopsis-Thaliana/membrane/plant4/20hrs_plant4_trim-acylYFP_M.tiff"
im=imread(filename)
im=np.swapaxes(im,0,2)
print(im.shape)
step_shape=30
step_epochs=100

model = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D")
model.load_model()
print(f"model.weight_files is {model.weight_files}")
last_epochs=get_last_epochs(model.weight_files)
print(f"Last epoch is {last_epochs}")
nbTI=0
for e in range(0, last_epochs, step_epochs):
    wfilename = get_weights_filename(model.weight_files, e)
    if wfilename is not None and isfile(wfilename):
        nbTI+=1
if nbTI==0:
    print("No weights file found")
    quit()
else:
    print(f"Found {nbTI} weights files")
imt = np.zeros(im.shape + (nbTI,), dtype=np.uint8)
seg= np.zeros(im.shape + (nbTI,), dtype=np.uint16)

print(f"new shape{imt.shape}")
nbI=0
for e in range(0,last_epochs,step_epochs):
    if model.load_weights(epochs=e) != -1:
        print(f"Processing epoch: {e} ")
        imt[...,nbI] = model.predict(im, patches=False)
        seg[...,nbI] = semantic_to_segmentation(imt[...,nbI])
        nbI += 1



for z in range(0, im.shape[2], step_shape):
    sem_file = join(output_path, basename(filename).replace("M.tiff", f"E{e}_Z{z}_S.tiff"))
    print(f"Export to {sem_file}")
    imsave(sem_file, np.swapaxes( imt[..., z,:], 0, 2))
    imsave(sem_file.replace("S.tiff", "SEG.tiff"), np.swapaxes(seg[..., z,:], 0, 2))


