from os.path import isdir, join

#### MAIN WORKING PATH
user="uhb36wd"
SCRATCH = join("/lustre/fsn1/projects/rech/dhp/",user)
STORE= join("/lustre/fsstor/projects/rech/dhp/",user)
WORK =  join("/lustre/fswork/projects/rech/dhp/",user)
EXE=join("/linkhome/rech/genlir01/",user,"semantic")
OLD_SCRATCH = join("/gpfsscratch/rech/dhp",user)
TEMP=join(SCRATCH,"TEMP")


#LOKI PATH
if not isdir(WORK):
    local_path="/data/MorphoDeep/semantic"
    if isdir(local_path):
        EXE = join(local_path,"semantic")
        SCRATCH = local_path
        WORK = local_path
        STORE = local_path


#LOCAL PATH
if not isdir(WORK):
    local_path="/Users/efaure/Codes/PythonProjects/morphodeep/"
    if isdir(local_path):
        EXE = join(local_path,"morphodeep")
        SCRATCH = local_path
        WORK = local_path
        STORE = local_path

#CIONA PATH
if not isdir(WORK):
    local_path="/media/SSD1/JZ/"
    if isdir(local_path):
        EXE = join(local_path,"semantic")
        SCRATCH = local_path
        WORK = local_path
        STORE = local_path

if not isdir(WORK):
    print(" --> didn't find any good repositeroies")


RESULT = join(WORK, "Semantic_RESULT")
JOBS=join(WORK,"JOBS")

#ORIGNIAL DATAPATH
species = ["SPIM-Phallusia-Mammillata", "CONF-Arabidopsis-Thaliana", "CONF-LateralRootPrimordia", "CONF-Ovules","CONF-SeaStar", "CONF-Caenorhabditis-Elegans"]

#### PLANTSEG
plantseg_path=join(STORE,"DATA_INTEGRATION","PlantSeg")

#### SEA Star
seastar_path=join(STORE,"DATA_INTEGRATION","SeaStar","high-resolution_raw_label_images")

#### ARABIDOPSIS
arabidopsis_path=join(STORE,"DATA_INTEGRATION","Arabidopsis")

#### CellPose (2D only)
cellpose_path=join(STORE,"DATA_INTEGRATION","CellPose")

#### PHALLUSIA
phallusia_path=join(STORE,"DATA_INTEGRATION","Phallusia")

#### CELEGANS
celegans_path=join(STORE,"DATA_INTEGRATION","CElegans")