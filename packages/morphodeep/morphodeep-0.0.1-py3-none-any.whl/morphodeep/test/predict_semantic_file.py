import sys, os
sys.path.append('../../')
import argparse
from os.path import isfile
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation

#python predict_semantic_file.py  -i /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225.nii -o /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225_ALL-256-SEM.tiff
#python predict_semantic_file.py  -n 128 -i /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225.nii -o /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225_ALL-128-SEM.tiff
#python predict_semantic_file.py  -s PM -m SPIM -i /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225.nii -o /lustre/fsn1/projects/rech/dhp/uhb36wd/TEMP/Julia_Evaluation/250527-Julia_fuse_t225_PM-256-SEM.tiff

#python predict_semantic_file.py -s PM -m CONF -i /lustre/fsn1/projects/rech/dhp/uhb36wd/Luisa-DATA/RAW/Fileset_1048713_M.tiff -o /lustre/fsn1/projects/rech/dhp/uhb36wd/Luisa-DATA/SEM/Fileset_1048713_SEM.tiff
parser = argparse.ArgumentParser()
parser.add_argument('-i',"--input", default=None, help="input file")
parser.add_argument('-o',"--output", default=None, help="output file")
parser.add_argument('-s',"--specie", default="all", help="specie (or all)")
parser.add_argument('-m',"--microscope", default="ALL", help="microscope (or ALL)")
parser.add_argument('-p',"--patches", default=True, help="patches mode")
parser.add_argument('-n',"--net_size", default=256, help="128,256")


args = parser.parse_args()

if args.input is None: raise ImportError("Please provide an input file")
if not isfile(args.input): raise ImportError(f"unknown input file {args.input}")
if args.input is None: raise ImportError("Please provide an ouput file")

net_size=args.net_size

model = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D",img_size=net_size, specie=args.specie,microscope=args.microscope)
model.load_model()
model.load_weights()

rawdata=imread(args.input)
semantic=model.predict(rawdata,patches=args.patches)

imsave(args.output,semantic)

segmentation=semantic_to_segmentation(semantic)

imsave(args.output.replace("_SEM.tiff","_SEG.tiff"),segmentation)