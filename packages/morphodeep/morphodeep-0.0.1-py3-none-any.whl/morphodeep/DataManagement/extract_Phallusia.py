import os
from os.path import isdir, join, isfile

from morphodeep.tools.image import imread, imsave
from morphodeep.tools.utils import mkdir, execute


def download_Phallusia_data(phallusia_path): #TODO
    if not isdir(phallusia_path):
        print(" --> you have first to download Phallusia  data to "+phallusia_path)
        return False
    return True




def extract_Phallusia_data(phallusia_path,gt_path):

    print(f" --> Extract Phalusia data  from {phallusia_path} to {gt_path}")
    if not download_Phallusia_data(phallusia_path): return False
    for zipfilename in os.listdir(phallusia_path):
        if zipfilename.endswith(".tar.gz"):
            embname = zipfilename.replace(".tar.gz", "")
            if not isdir(join(phallusia_path,embname)):
                execute(f"cd {phallusia_path}; tar -xf {zipfilename}")

            if not isdir(join(phallusia_path, embname)) or not isdir(join(phallusia_path, embname,"fuse"))  or not isdir(join(phallusia_path, embname,"seg")) :
                print(f" --> ERROR Extract Phalusia data for {join(phallusia_path,embname)}")
                quit()

            mkdir(join(gt_path, "membrane", embname))
            mkdir(join(gt_path, "segmented", embname))

            for membrane_filename in os.listdir(join(phallusia_path,embname,"fuse")):
                output_mem_filename = join(gt_path, "membrane",embname,membrane_filename.replace(".gz","").replace(".nii","_M.tiff"))
                output_seg_filename = join(gt_path, "segmented", embname, membrane_filename.replace(".gz", "").replace(".nii", "_S.tiff"))

                if not isfile(output_mem_filename) and not isfile(output_seg_filename):
                    #Clean Previous GZIP
                    if membrane_filename.endswith(".gz") and isfile(membrane_filename.replace(".gz","")):
                        execute("rm -f "+membrane_filename.replace(".gz",""))
                    if not membrane_filename.endswith(".gz") and isfile(membrane_filename+".gz"):
                        execute("rm -f " + membrane_filename)
                        membrane_filename=membrane_filename+".gz"

                    if membrane_filename.endswith(".gz"):
                        execute(f"cd "+join(phallusia_path,embname,"fuse")+f"; gunzip {membrane_filename}")
                        membrane_filename=membrane_filename.replace(".gz","")

                    seg_filename=join(phallusia_path,embname,"seg",membrane_filename.replace("_fuse_","_seg_"))
                    if not isfile(seg_filename):
                        if isfile(seg_filename+".gz"):
                            execute(f"cd "+join(phallusia_path, embname, "seg")+f"; gunzip {seg_filename}.gz")
                    if not isfile(seg_filename):
                        print(f" --> ERROR Extract Phalusia Missing Segfilenae at  {join(phallusia_path, embname,seg_filename)}")
                    else:
                        membrane = imread(join(phallusia_path,embname,"fuse",membrane_filename))
                        seg=imread(seg_filename)
                        seg[seg==1]=0 #Backround to 0

                        if membrane.shape!=seg.shape:
                            print(f" --> ERROR Shape different {membrane.shape} and {seg.shape} ")
                        else:
                            print(f"--> Save {output_mem_filename}")
                            imsave(output_seg_filename,seg)
                            imsave(output_mem_filename,membrane)

            execute(f"rm -rf {join(phallusia_path,embname)}")
            print(f" -> Done for {embname}")