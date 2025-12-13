#Juste resize data which are in 512 to 256

import sys
from os import listdir
from os.path import join, isfile
from skimage.io import imread,imsave
sys.path.append("../..")


from morphodeep.tools.utils import mkdir




path="/lustre/fsn1/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/CONF-Ovules"
new_path="/lustre/fsn1/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/GT_512_3D/CONF-Ovules-256"
mkdir(new_path)


for method in listdir(path):
    for dataset in listdir(join(path,method)):
        for timepoint in listdir(join(path,method,dataset)):
            for filename in listdir(join(path,method,dataset,timepoint)):
                ofilename=join(new_path,method,dataset,timepoint,filename)
                if not isfile(ofilename) and filename.endswith("tiff"):
                    print(" -> open "+join(path,method,dataset,timepoint,filename))
                    im=imread(join(path,method,dataset,timepoint,filename))
                    if im.shape[0]==512:
                        im=im[::2,::2,::2]
                    mkdir(join(new_path,method,dataset,timepoint))
                    imsave(ofilename,im)
