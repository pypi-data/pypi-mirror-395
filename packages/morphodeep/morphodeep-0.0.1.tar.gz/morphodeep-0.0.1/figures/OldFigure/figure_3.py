import sys,os
sys.path.append("..")
from morphodeep.tools.utils import mkdir
from os.path import join,isdir
from morphodeep.tools.image import semantic_to_segmentation
from morphodeep.tools.image import imread,imsave
from morphodeep.tools.image import re_label
from morphodeep.model_core import MorphoModel
import numpy as np

#notebook --no-browser

def get_main_path():
    main_path = "/Users/efaure/Codes/PythonProjects/morphodeep/figures"  # Local
    if not os.path.isdir(main_path): main_path = "/linkhome/rech/genlir01/uhb36wd/morphodeep/figures"  # Jean Zay
    return main_path

main_path=get_main_path()
data_path=join(main_path,"DATA")
figure_path=join(main_path,"fig2")
mkdir(figure_path)


path_data="/gpfsstore/rech/dhp/uhb36wd/DATA_INTEGRATION"
if not isdir(path_data): path_data="/Users/efaure/Projects/180216-DeepLearningon4DEmbryo/DATABASE/DATA-Integration/KellerLab"
filename="Drosophila_c=00_Full.tif"
membrane=imread(join(path_data,"Drosophila",filename))
membrane=np.swapaxes(membrane,0,2)

#LOAD SEMANTIC NETWORKS
nfj = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D", img_size=256,specie="all",microscope="ALL")
nfj.load_model()
nfj.load_weights()

semantic = nfj.predict_3D_semantic(membrane,patches=True,crop=False)
imsave(join(path_data,"Drosophila",filename.replace(".tif","_JN")),semantic)
segmentation=semantic_to_segmentation(semantic)
imsave(join(path_data,"Drosophila",filename.replace(".tif","_S")),segmentation)
