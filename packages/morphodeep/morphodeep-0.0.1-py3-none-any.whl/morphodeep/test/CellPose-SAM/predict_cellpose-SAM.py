from skimage.io import imread,imsave
from cellpose import models
import numpy as np

img=imread("Movie2_T00010_crop.tiff")

model = models.CellposeModel(gpu=True)

masks, flows, styles = model.eval(np.stack((img, 0*img, 0*img), axis=-1),
                                        channel_axis=-1, z_axis=1, niter=1000,
                                        flow3D_smooth=2, diameter=30,
                                        bsize=256, batch_size=64,
                                        channels=None, do_3D=True, min_size=1000)
print(f"masks shape={masks.shape}")
imsave("Movie2_T00010_crop_CP4.tiff",masks)