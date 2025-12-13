import sys, os
sys.path.append('../../')
import argparse
from os.path import isfile, isdir, join
from morphodeep import MorphoModel
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation

#python predict_semantic.py -s PM -m CONF -i /lustre/fsn1/projects/rech/dhp/uhb36wd/Luisa-DATA/RAW/Fileset_1048713_M.tiff -o /lustre/fsn1/projects/rech/dhp/uhb36wd/Luisa-DATA/SEM/Fileset_1048713_SEM.tiff
parser = argparse.ArgumentParser()
parser.add_argument('-pa',"--path", default=None, help="path files")
parser.add_argument('-s',"--specie", default="all", help="specie (or all)")
parser.add_argument('-m',"--microscope", default="ALL", help="microscope (or ALL)")
parser.add_argument('-p',"--patches", default=True, help="patches mode")
parser.add_argument('-i',"--img_size", default=256, help="128,256")


args = parser.parse_args()

if args.path is None: raise ImportError("Please provide an input path")
if not isdir(args.path): raise ImportError(f"unknown path file {args.path}")

net_size=int(args.img_size)

model = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D",img_size=net_size, specie=args.specie,microscope=args.microscope)
model.load_model()
model.load_weights()

for f in sorted(os.listdir(args.path)):
    if not f.startswith(".") and f.find("_SEG")==-1:
        print(f"Processing image {f}")
        extension = os.path.splitext(f)[1]
        if extension == ".gz":  extension = os.path.splitext(os.path.splitext(f)[0])[1] + extension
        outputfile = join(args.path,f.replace(extension, f"_SEG"+extension))
        if  isfile(outputfile):
            print(f"--> already predict {outputfile}")
        else:
            rawdata = None
            try:
                rawdata = imread(join(args.path, f))
            except Exception as e:
                print(f"Cannot read this image {f} -> {e}")
            if rawdata is not None:
                semantic=model.predict(rawdata,patches=args.patches)
                segmentation=semantic_to_segmentation(semantic)
                print(f"Save to {outputfile}")
                imsave(outputfile,segmentation)