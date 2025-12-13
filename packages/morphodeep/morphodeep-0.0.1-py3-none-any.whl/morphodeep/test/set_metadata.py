import os
from os.path import join
import numpy as np
from astec.io.image import imread, imsave
from astec.components.spatial_image import SpatialImage

path="/media/SSD2/DATA/CElegans/250625-Virginie2/FUSE/FUSE_01"
#path="/media/SSD2/DATA/CElegans/250625-Virginie2/SEG/SEG_JUNC_01"
#path="/media/SSD2/DATA/CElegans/250625-Virginie2/SEG/SEG_JUNC_01"

voxelsize=[ 0.144992 , 0.144992 , 0.144992 ]
for f in sorted(os.listdir(path)):
    if f.endswith(".nii"):
        print(f"Processing {f}")
        im=np.uint16(imread(join(path,f)))
        imsave(join(path,f), SpatialImage(im, voxelsize=voxelsize))
