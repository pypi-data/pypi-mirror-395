from skimage.morphology import binary_erosion, binary_dilation
from skimage.segmentation import watershed

from morphodeep.tools.image import imread,imsave
import numpy as np
path="/Users/efaure/Desktop/SEM/"
nuclei=imread(path+'1048713_t000.tiff')
nuclei=nuclei[1,...]

#create nuclei markers
markers=np.zeros_like(nuclei)
ms=3
for n in np.unique(nuclei):
    if n>0:
        coords=np.where(nuclei==n)
        bary=[np.int16(coords[0].mean()),np.int16(coords[1].mean()),np.int16(coords[2].mean()),]
        markers[bary[0]-ms:bary[0]+ms,bary[1]-ms:bary[1]+ms,bary[2]-ms:bary[2]+ms]=n
imsave(path+"markers.tif",markers)

semantic=imread(path+"Fileset_1048713_SEM.tiff")

background=np.zeros_like(semantic)
background[semantic>0]=1
imsave(path+"background.tif",background)

membrane=np.zeros_like(semantic)
membrane[semantic>1]=1
imsave(path+"membrane.tif",membrane)


#WWATERSHED ON RAWIMAGE
rawimage=imread(path+"Fileset_1048713_M.tiff")
w=watershed(rawimage,markers=markers,mask=background)
imsave(path+"watershed_on_raw.tif",w)

#WWATERSHED ON MEMBRANE SEMANTIC
w=watershed(membrane,markers=markers,mask=background)
imsave(path+"watershed_on_semantic_membrane.tif",w)

#WWATERSHED ON SEMANTIC SEGMENTATION
sem_seg=imread(path+"Fileset_1048713_SEM_SEG.tiff")
seg_seg_mem=np.zeros_like(sem_seg)
cells=np.unique(sem_seg)
for c in cells:
    if c>0:
        mask=np.zeros_like(sem_seg)
        mask[sem_seg==c]=1
        seg_seg_mem+=mask-binary_erosion(mask)

seg_seg_mem=binary_dilation(seg_seg_mem)
imsave(path+"membrane_sem_seg.tif",seg_seg_mem)

w=watershed(seg_seg_mem,markers=markers,mask=background)
imsave(path+"watershed_on_semantic_segmentation.tif",w)



