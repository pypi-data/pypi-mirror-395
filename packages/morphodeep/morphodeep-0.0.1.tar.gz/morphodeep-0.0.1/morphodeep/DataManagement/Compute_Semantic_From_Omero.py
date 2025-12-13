#!/usr/bin/env python
import os,sys,time
from os.path import join,isfile,isdir
sys.path.append("../../")




path_data="/data/semantic/DATA/" #LOKI


import argparse
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation
from morphodeep.tools.utils import mkdir
parser = argparse.ArgumentParser()
parser.add_argument('-d',"--datasetid", default=20150, help="omero id number")
parser.add_argument('-s',"--segmentation", default=True, help="compute and upload the semantic segmentation")
parser.add_argument('-r',"--remove_zeros", default=False, help="when you have a new empty background at 0 after registration")

args = parser.parse_args()

if args.datasetid=="":
    print(" --> specify a dataset id")
    quit()
datasetid=int(args.datasetid)

patches=True #Patches Mode (True=with patches , slower but better)

method="semantic"

from morphodeep import MorphoModel
ntf = MorphoModel(mode="3D", img_size=256,microscope="SPIM",specie="PM")
ntf.load_model()
ntf.load_weights()


#BAVCKGROUN TO LOAD
#method = "FusedToBackground"
#method="SplitChannels"

sys.path.append("../../../morphoomero")
import morphoomero
mom = morphoomero.connect()

#FIND THE PROJECT (mehtod get_project by id does not seems to work...)
embryolist = mom.list_projects()
dataset=None
input_set_name=""
project=None
path_name=""
if embryolist is not None:
    for o_emb in embryolist:
        for path in mom.get_datasets(o_emb.getid()):
            if path.getid()==datasetid:
                dataset=path
                input_set_name = dataset.getName()
                path_name=path.getName()
                project=o_emb
                print(f"\n\n--> Find embryo {project.getName()} with path {path_name}\n\n")
if dataset is None:
    print(" --> didn't find this path with project id "+str(datasetid))
    quit()

#DOWNLOAD DATA
mkdir(path_data)
path_project=join(path_data,"DATASET-"+str(datasetid))
mkdir(path_project)
path_download=join(path_project,path_name)
mkdir(path_download)

#OUTPUT SEMANTIC DATA
image_suffix="junctions"
output_name="JUNC_"+str(input_set_name).replace("FUSE_","")
path_upload=join(path_project,output_name)
mkdir(path_upload)

#OUTPUT SEGMENTATION DATA
image_seg_suffix="junctions_segmentation"
output_seg_name="SEG_JUNC_"+str(input_set_name).replace("FUSE_","")
path_seg_upload=join(path_project,output_seg_name)
mkdir(path_seg_upload)

#CREATE OUTPUT PATH
dataset_idout=None
dataset_out=None
out_images_ids = {}
for path in mom.get_datasets(project.getid()):
    if path.getName()==output_name:
        dataset_idout=path.getid()
        dataset_out=path
if dataset_idout is None: #Test if the proejct already exist
    dataset_idout=mom.create_dataset(output_name,project_id=project.getid())
    dataset_out=mom.get_dataset_by_id(dataset_idout,project.getid())
    mom.add_kvp(dataset_out,"epochs",str(ntf.epochs_loaded))
    mom.add_kvp(dataset_out, "networks", "JUNNET")
else:
    out_images_ids = mom.get_images_filename(dataset_idout)


list_images_ids = mom.get_images_filename(dataset.getid())
'''#TEMP
list_images_ids_S={}
for k in list_images_ids:
    if len(list_images_ids_S)<20:
        list_images_ids_S[k]=list_images_ids[k]
list_images_ids=list_images_ids_S
print(list_images_ids)
#TEMP'''

for f in sorted(list_images_ids):
    #DOWNLOAD
    print(" --> Download " + f)
    if not isfile(join(path_download,f)):
        mom.export_image(list_images_ids[f], join(path_download, f))
    if not isfile(join(path_download, f)): raise TypeError(" --> error downloading "+f)
    #PREDICT
    fout = f.replace("_fuse", "_" + image_suffix.lower()).replace(".gz","")
    print(" --> Compute semantic " + fout)
    if not isfile(join(path_upload, fout)):
        input = imread(join(path_download, f))
        semantic=ntf.predict(input,patches=patches,remove_zeros=args.remove_zeros)
        imsave(join(path_upload, fout), semantic)
    if not isfile(join(path_upload, fout)): raise TypeError(" --> error computing semantic " + fout)

    #UPLOAD
    print(" --> Upload semantic " + fout)
    if fout not in out_images_ids:
        mom.add_image_to_dataset_java(join(path_upload,fout),dataset_idout)

print(" --> Semantic DONE for "+method+" applied to "+path_name)

if args.segmentation:
    # CREATE  OUTPUT DATA
    mom = morphoomero.connect()

    dataset_idout = None
    dataset_out = None
    out_images_ids = {}
    for path in mom.get_datasets(project.getid()):
        if path.getName() == output_seg_name:
            dataset_idout = path.getid()
            dataset_out = path
    if dataset_idout is None:  # Test if the proejct already exist
        dataset_idout = mom.create_dataset(output_seg_name, project_id=project.getid())
        dataset_out = mom.get_dataset_by_id(dataset_idout, project.getid())
        mom.add_kvp(dataset_out, "epochs", str(ntf.epochs_loaded))
        mom.add_kvp(dataset_out, "networks", "JUNNET")
    else:
        out_images_ids = mom.get_images_filename(dataset_idout)

    list_images_ids = mom.get_images_filename(dataset.getid())
    '''# TEMP
    list_images_ids_S = {}
    for k in list_images_ids:
        if len(list_images_ids_S) < 20:
            list_images_ids_S[k] = list_images_ids[k]
    list_images_ids = list_images_ids_S
    print(list_images_ids)
    # TEMP'''

    for f in sorted(list_images_ids):
        fout = f.replace("_fuse", "_" + image_seg_suffix.lower()).replace(".gz", "")
        print(" --> Compute segmentation " + fout)
        if not isfile(join(path_seg_upload, fout)):

            fin = f.replace("_fuse", "_" + image_suffix.lower()).replace(".gz", "")
            if not isfile(join(path_upload, fin)): raise TypeError(" --> error reading " + fin)
            else:
                semantic = imread(join(path_upload, fin)) # READ SEMANTIC PREDICTION
                segmentation=semantic_to_segmentation(semantic)
                imsave(join(path_seg_upload, fout), segmentation)
            if not isfile(join(path_seg_upload, fout)): raise TypeError(" --> error computing segmentation " + fout)

            # UPLOAD
            print(" --> Upload segmentation " + fout)
            if fout not in out_images_ids:
                mom.add_image_to_dataset_java(join(path_seg_upload, fout), dataset_idout)

print(" --> Semantic Segmentation DONE for "+method+" applied to "+path_name)

os.system("rm -rf "+ path_project)