import sys

from skimage.io import imread,imsave

input_filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Fileset_1048713_Membrane.tiff"
output_filename="/lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Fileset_1048713_CP4.tiff"


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

cp_version, model = import_cellpose()

membrane=imread(input_filename)
masks = model.eval(membrane, do_3D=True, z_axis=0)[0]

imsave(output_filename,masks)