from os.path import join, isfile, isdir
from os import listdir
from os.path import join


from skimage.io import imsave
from skimage.segmentation import watershed
from skimage.morphology import binary_dilation, binary_erosion
import numpy as np

from morphodeep.tools.utils import mkdir


def download_CElegans_data(celegans_path):
    if not isdir(celegans_path):
        print(" --> you have first to download C elegans data to "+celegans_path)
        #TODO
        print(" --> Rename PATH in CONF-CElegans")
        return False
    return True


def dilate_Cell(seg,footprint = 6):
    footprint = np.ones((footprint, footprint, footprint))
    background = binary_erosion(binary_dilation(seg > 0, footprint=footprint), footprint=footprint)  # BACKGROUND
    return watershed(1 - background, markers=seg, mask=background)


def extract_CElegans_data(celegans_path,gt_path):
    print(" --> Extract CElegans data from "+celegans_path+ " to "+gt_path)
    if not download_CElegans_data(celegans_path): return False


    #TRAINING DATA
    what="CMapTrainingGroundTruth"
    if isdir(join(celegans_path,what)):
        for emb in listdir(join(celegans_path,what)):
            if isdir(join(celegans_path,what,emb)):
                for memb_filename in listdir(join(celegans_path,what,emb,"RawMemb")): #170614plc1p1_030_rawMemb.nii.gz
                    if memb_filename.endswith("nii.gz"):
                        seg_filename = join(join(celegans_path,what,emb,"SegCell",memb_filename.replace("rawMemb","segCell"))) #170614plc1p1_030_segCell.nii.gz
                        if not isfile(seg_filename):
                            print(f"--> miss {seg_filename}")
                        else:
                            print(f"--> Process {memb_filename}")
                            gt_mem_filename=join(gt_path, "membrane", what, memb_filename.replace("_rawMemb.nii.gz","_M.tiff"))
                            gt_seg_filename=join(gt_path, "segmented", what, memb_filename.replace("_rawMemb.nii.gz","_S.tiff"))
                            if not isfile(gt_seg_filename):
                                from morphonet.tools import imread
                                #SEGMENTATION
                                seg=imread(seg_filename) #RETURN 5D
                                if len(seg.shape)==5:   seg=seg[...,0,0]
                                seg=dilate_Cell(seg)

                                #MEMBRANE
                                memb = imread(join(celegans_path,what,emb,"RawMemb",memb_filename))
                                if len(memb.shape) == 5:   memb = memb[..., 0, 0]

                                mkdir(join(gt_path,"membrane", what))
                                mkdir(join(gt_path, "segmented", what))

                                print(" ------> shape is "+str(seg.shape))

                                imsave(gt_mem_filename,memb)
                                imsave(gt_seg_filename,seg)

    quit()
    # VALIDATION DATA
    what = "ValidationGroundTruth"
    if isdir(join(celegans_path,what)):
        for memb_filename in listdir(join(celegans_path, what)):  # WT_Sample1_090_rawMemb.nii.gz
            if memb_filename.endswith("rawMemb.nii.gz"):
                seg_filename = join(join(celegans_path, what,  memb_filename.replace("rawMemb", "segCell_G")))  # 170614plc1p1_030_segCell.nii.gz
                if not isfile(seg_filename):
                    print(f"--> miss {seg_filename}")
                else:
                    emb=memb_filename[3:10]
                    gt_mem_filename = join(gt_path, "membrane", what, memb_filename.replace("_rawMemb.nii.gz", "_M.tiff"))
                    gt_seg_filename = join(gt_path, "segmented", what, memb_filename.replace("_rawMemb.nii.gz", "_S.tiff"))
                    if not isfile(gt_seg_filename):
                        from morphonet.tools import imread
                        # SEGMENTATION
                        seg = imread(seg_filename)  # RETURN 5D
                        if len(seg.shape)==5:   seg=seg[...,0,0]
                        seg = dilate_Cell(seg)

                        # MEMBRANE
                        memb = imread(join(celegans_path, what, memb_filename))
                        if len(memb.shape) == 5:   memb = memb[..., 0, 0]

                        mkdir(join(gt_path, "membrane", what))
                        mkdir(join(gt_path, "segmented", what))

                        print(f" ------> shape is {seg.shape} an {memb.shape}")

                        imsave(gt_mem_filename, memb)
                        imsave(gt_seg_filename, seg)




