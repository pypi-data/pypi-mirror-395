from os import listdir
import sys
from os.path import join, isfile

sys.path.append('../../')
from morphodeep.tools.image import imread, imsave
from morphodeep.tools.utils import mkdir


def get_env():
    sp = sys.path[1].split("/")
    if "envs" in sp:
        sp=sp[sp.index("envs") + 1]
        if sp.startswith("cellpose"):
            if sp=="cellpose": return 2
            return int( sp[8:])
    return 0

def import_cellpose():
    cp_version = 0
    model=None
    try:
        cp_version = get_env()
        if cp_version == 0:
            print("First activate Conda CellPose environment ")
            quit()
        print(f"---> Found CellPose {cp_version}")
        from cellpose import models
        model = None
        if cp_version == 2:
            model = models.CellposeModel(gpu=True, model_type="cyto2")
        elif cp_version == 3:
            model = models.CellposeModel(gpu=True, model_type="cyto3")
        elif cp_version == 4:
            model = models.CellposeModel(gpu=True)
        if model is None:
            print("Unrocognized cellpose version")
            quit()
    except:
        print("CellPose is required for prediction")
        quit()
    return cp_version,model

embryon=2

path_membrane=f"/lustre/fsn1/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/CElegans/embryon{embryon}_CGT/FUSE_01"

cp_version, model = import_cellpose()
if cp_version!=4:
    print("CellPose 4 is required for prediction")
    quit()

path_seg=f"/lustre/fsn1/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/CElegans/embryon{embryon}_CGT/CellPose{cp_version}"
mkdir(path_seg)

for f in sorted(listdir(path_membrane)):
    segname=f.replace(".tiff",f"_CP{cp_version}.tiff")
    print(f"Predict {segname}")
    if not isfile(join(path_seg,segname)):
        membrane=imread(join(path_membrane,f))
        masks = model.eval(membrane, do_3D=True, z_axis=0)[0]
        imsave(join(path_seg,segname), masks)

