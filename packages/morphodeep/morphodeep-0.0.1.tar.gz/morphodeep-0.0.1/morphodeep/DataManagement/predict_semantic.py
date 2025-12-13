import sys,os


sys.path.append('../../')

from skimage.measure import label
import argparse



#CELLPOSE LOAD
#from cellpose import models
#model = models.CellposeModel(gpu=True) #We have to first load the model with aconnection  online (so not in job...)

from morphodeep.DataManagement.extract_SeaUrchin_data import similar
from os.path import join, isfile, basename, isdir
from morphodeep.tools.utils import printp, mkdir, execute
from morphodeep import MorphoModel
from morphodeep.DataManagement.crop_and_resize import make8bit
from os import listdir
from datetime import datetime
from skimage.transform import resize
from morphodeep.tools.image import imread, imsave, semantic_to_segmentation, get_gaussian, get_border
import numpy as np
net_size=256
class data:
    def __init__(self,path,data_type,raw_name,seg_name,voxel_size,specie,microscope,patches=False,isotrope=True,background=None):
        self.data_type=data_type
        self.path = path
        self.raw_name=raw_name
        self.seg_name=seg_name
        self.voxel_size=voxel_size
        self.specie=specie
        self.microscope=microscope
        self.patches = patches
        self.isotrope=isotrope
        self.background=background

    def get_segi_name(self):
        if self.data_type=="Ascidian" or self.data_type=="Arabidopsis" or self.data_type=="SeaUrchin":
            return join(self.path,self.seg_name) #ALREADY SEGMENTED
        return join(self.path,f"Instance_" + basename(self.seg_name).split(".")[0] + ".tiff")


    def get_cp_name(self,v):
        return join(self.path,f"CellPose{v}_"+basename(self.raw_name).split(".")[0]+".tiff")

    def get_semseg_name(self,patches=False):
        if not patches: return join(self.path,f"NP_Segmentation_"+basename(self.raw_name).split(".")[0]+".tiff")
        return join(self.path,f"Segmentation_"+basename(self.raw_name).split(".")[0]+".tiff")

    def get_sem_name(self):
        return join(self.path,f"Semantic_"+basename(self.raw_name).split(".")[0]+".tiff")

    def get_acc_name(self):
        return join(data_path,"Accuracy", f"Accuracy_" + basename(self.raw_name).split(".")[0] + ".png")


parser = argparse.ArgumentParser()
parser.add_argument('-s',"--specie", default="", help="PM,AT,OT ")
args = parser.parse_args()


'''
for p in os.listdir("/lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION"):
    for pp in os.listdir("/lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/"+p):
        for f in os.listdir("/lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/"+p+"/"+pp):
            if f.endswith(".tif.tiff"):
                execute(
                    "mv /lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/" + p + "/" + pp + "/" + f + " /lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/" + p + "/" + pp + "/" + f.replace(
                        ".tif.tiff", ".tiff"))
            if f.endswith(".tif"):
                execute("mv /lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/"+p+"/"+pp+"/"+f+" /lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/"+p+"/"+pp+"/"+f.replace(".tif",".tiff"))
quit()
'''

data_path="/lustre/fsstor/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/Drosophila" #CANNOT ACCES TO STORE COPY IN WORK FIRST
data_path="/lustre/fswork/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/"
mkdir(join(data_path,"Accuracy"))
files=[]

#OTHERS
if args.specie=="OT" or  args.specie=="":
    #DROSOPHILIA
    files.append(data(data_path+"Drosophila/CONF/","Drosophila","Dme_Confocal_E3_SpiderGFP-His2AvRFP_01.tiff","Drosophila_Confocal.tiff",(0.4,0.4,2),"all","ALL",patches=True))
    files.append(data(data_path+"Drosophila/SPIM/","Drosophila","Drosophila_c00_Full.tiff","Drosophila_SiMView.tiff",(0.41,0.41,2.03),"all","ALL",patches=True,background=0))
    #MOUSE
    files.append(data(data_path+"Mouse/CONF/","Mouse","Mmu_E1_CAGTAG1_01_Membranes.tiff","Mouse_Confocal.tiff",(0.62,0.62,1),"all","ALL",patches=True))
    files.append(data(data_path+"Mouse/SPIM/","Mouse","Mmu_SiMView_00_t0000_Cropped.tiff","Mouse_SiMView.tiff",(0.41,0.41,2.03),"all","ALL",patches=True))
    #ZEBRA
    files.append(data(data_path+"Zebra/CONF/","Zebra","ZC2-Dre_E3_timelapse_t0001_z1-91.tiff","Zebrafish_Confocal.tiff",(0.62,0.62,0.9),"all","ALL",patches=True))
    files.append(data(data_path+"Zebra/SPIM/","Zebra","ZDre_SiMView_SPM00_TM000000_CM00_CM01_CHN02_CHN03.fusedStack_Cropped.tiff","Zebrafish_SiMView.tiff",(0.41,0.41,2.03),"all","ALL",patches=True))


### ASCIDIAN
if args.specie=="PM" or  args.specie=="":
    ranget=[1,50,100,150,190]
    mkdir(join(data_path,"Ascidian","SPIM"))
    #TRANSFERT DATA TO DATA_INTEGRATION
    input_path="/lustre/fswork/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/Embryos/SPIM-Phallusia-Mammillata/140317-Patrick-St8"
    for t in ranget:
        if not isfile(join(data_path,"Ascidian","SPIM","140317-Patrick-St8_fuse_t"+str(t).zfill(3)+".nii.gz")):
            execute("cp -r "+join(input_path,"fuse/140317-Patrick-St8_fuse_t"+str(t).zfill(3)+".nii.gz")+" "+join(data_path,"Ascidian","SPIM"))
        if not isfile(join(data_path,"Ascidian","SPIM","140317-Patrick-St8_seg_t"+str(t).zfill(3)+".nii.gz")):
            execute("cp -r "+join(input_path,"seg/140317-Patrick-St8_seg_t"+str(t).zfill(3)+".nii.gz")+" "+join(data_path,"Ascidian","SPIM"))
    for t in ranget:
        files.append(data(data_path+"Ascidian/SPIM/","Ascidian","140317-Patrick-St8_fuse_t"+str(t).zfill(3)+".nii.gz","140317-Patrick-St8_seg_t"+str(t).zfill(3)+".nii.gz",(1,1,1),"PM","SPIM",patches=True))

### ARABIDOPSIS
if args.specie=="AT" or  args.specie=="":
    ranget=[0,20,40,60,76]
    mkdir(join(data_path,"Arabidopsis","CONF"))
    #TRANSFERT DATA TO DATA_INTEGRATION
    input_path="/lustre/fswork/projects/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/Embryos/CONF-Arabidopsis-Thaliana/plant4/"
    for t in ranget:
        if not isfile(join(data_path,"Arabidopsis","CONF","plant4_fuse_t"+str(t)+".tiff")):
            execute("cp -r "+join(input_path,"fuse/plant4_fuse_t"+str(t)+".tiff")+" "+join(data_path,"Arabidopsis","CONF"))
        if not isfile(join(data_path,"Arabidopsis","CONF","plant4_seg_t"+str(t)+".tiff")):
            execute("cp -r "+join(input_path,"seg/plant4_seg_t"+str(t)+".tiff")+" "+join(data_path,"Arabidopsis","CONF"))

    for t in ranget:
        files.append(data(data_path+"Arabidopsis/CONF/","Arabidopsis","plant4_fuse_t"+str(t)+".tiff","plant4_seg_t"+str(t)+".tiff",(1,1,1),"AT","CONF",patches=True))

### SEAURCHIN
if args.specie=="SU" or  args.specie=="":
    def get_corresponding(name, path):
        best = None
        bestv = 0
        trunk = name[0:name.find("_", 9)]
        rtrunk = name[name.rfind("_"):]
        rtrunk = rtrunk.replace("stk010.tif", "stk10.tif")
        for file in listdir(path):
            if  file.startswith(trunk) and file.endswith(rtrunk):
                bv = similar(name, file)
                if bv > bestv:
                    bestv = bv
                    best = file
        return best

    ranget=[0,20,40,60,76]
    mkdir(join(data_path,"SeaUrching","CONF"))
    #TRANSFERT DATA TO DATA_INTEGRATION
    raw="high-resolution_raw_images_resized"
    seg = "high-resolution_label_images"
    input_path="/lustre/fsstor/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/SeaUrchin/high-resolution_raw_label_images/"
    if isdir(input_path):
        for stage in listdir(join(input_path,raw)):
            for embtype in listdir(join(input_path,raw,stage)):
                isdone=False
                for f in listdir(join(input_path,raw,stage,embtype)):
                    if not isdone and f.startswith("embryo1"):
                        seg_file = get_corresponding(f, join(input_path, seg, stage,embtype))
                        if seg_file is not None:
                            dest_raw=join(data_path,"SeaUrching","CONF",stage.replace(" ","_")+"_"+embtype+"_"+f)
                            if not isfile(dest_raw):
                                execute("cp -r '"+join(input_path,raw,stage,embtype,f)+"' '"+dest_raw+"'")
                            dest_seg = join(data_path, "SeaUrching", "CONF", "SEG_"+stage.replace(" ","_")+"_"+embtype+"_"+f)
                            if not isfile(dest_seg):
                                execute("cp -r '" + join(input_path, seg, stage,embtype,seg_file) + "' '" + dest_seg+ "'")
                            #print(f"keep stage={stage} embtype={embtype} -> {dest_raw} with {dest_seg}")
                            print('sea_list.append("'+stage.replace(" ","_")+"_"+embtype+"_"+f+'")')
                            isdone=True
    sea_list=[]
    sea_list.append("256-cell_stage_wt_embryo1_20190806_pos3_stk05.tif")
    sea_list.append("256-cell_stage_wt-comp_embryo1_20200812_pos6_stk08.tif")
    sea_list.append("128-cell_stage_wt_embryo1_20190806_miniata_rasGFP_H2BRFP_pos3_stk03.tif")
    sea_list.append("128-cell_stage_wt-comp_embryo1_20200812_pos6_stk02.tif")
    sea_list.append("512-cell_stage_wt_embryo1_20190806_pos3_stk05.tif")
    sea_list.append("512-cell_stage_wt-comp_embryo1_20200812_pos6_stk08.tif")
    for s in sea_list:
        files.append(data(data_path+"SeaUrching/CONF/","SeaUrchin",s,"SEG_"+s,(1,1,1),"SU","CONF",patches=True))

### C ELEGANS

#FIRST CREATE THE INSTANCE SEGMENTATION
def seg_to_instance(seg):
    cells=np.unique(seg)
    segl=np.zeros_like(seg,dtype=np.uint16)
    l=1 #Labels number
    for c in cells:
        if c>0:
            segc=np.uint16(label(np.uint16(seg==c)))
            segc[segc > 0] += l
            segl+=segc
            l+=len(np.unique(segc))
    return segl

for f in files:
    if not isfile(f.get_segi_name()):
        print(f"Process Instance for {f.get_segi_name()}")
        seg=imread(join(f.path,f.seg_name))
        segi=seg_to_instance(seg)
        imsave(f.get_segi_name(),segi)


###### PREDICT SEMANTIC
model_loaded=None
model=None
tf_activated=False
try:
    import tensorflow as tf
    tf_activated=True
except:
    print(" -> required tensorfload for semantic")

if tf_activated:
    for f in files:
        for patches in [True, False]:
            if not isfile(f.get_semseg_name(patches=patches)):
                print(f"Process Semantic for {f.get_semseg_name(patches=patches)}")
                if model is None or model_loaded!=f.specie+"_"+f.microscope:
                    model = MorphoModel(method="FusedToSemantic", network="JUNNET", mode="3D",img_size=net_size, specie=f.specie,microscope=f.microscope)
                    model.load_model()
                    model.load_weights()#epochs=1536)
                    model_loaded =f.specie+"_"+f.microscope

                rawdata=imread(join(f.path,f.raw_name))
                if rawdata.shape[0]<rawdata.shape[2]: rawdata=np.swapaxes(rawdata,0,2)

                init_shape = rawdata.shape
                print(f"convert raw image with shape {rawdata.shape}")
                start_time=datetime.now()
                voxel_size = f.voxel_size
                if f.isotrope:
                    anisotropy = f.voxel_size[2] / f.voxel_size[1]  # 1/0.2=5 -> 100,100,20 ->  100,100,20*5
                    if anisotropy != 1:
                        rawdata = resize(rawdata, [rawdata.shape[0], rawdata.shape[1], int(anisotropy * rawdata.shape[2])],preserve_range=True).astype(rawdata.dtype)
                        print(f"found anisotropy of {anisotropy}, image shape is now {rawdata.shape}")

                rawdata, maxi, background = make8bit(rawdata, return_values=True,background=f.background)
                rawdata = (np.float32(rawdata) * 2.0 / 255.0) - 1.0
                #imsave(join(f.path, "Pre_" + f.raw_name), np.swapaxes(rawdata, 0, 2))
                if patches:  # PREDICT TILES
                    predict_shape = rawdata.shape[0:3] + (5,)
                    image_predict = np.zeros(predict_shape, dtype=np.float32)
                    print(f"predict semantic with shape {rawdata.shape} using tiles of {net_size} voxels")
                    nb_image_predict = np.ones(predict_shape, dtype=np.float32)
                    borders = get_gaussian(net_size)
                    slidingWindow = int(round(net_size / 2))

                    i = 0
                    nbTotal = float(len(range(0, rawdata.shape[0], slidingWindow)) * len( range(0, rawdata.shape[1], slidingWindow)) * len( range(0, rawdata.shape[2], slidingWindow)))
                    for x in range(0, rawdata.shape[0], slidingWindow):
                        for y in range(0, rawdata.shape[1], slidingWindow):
                            for z in range(0, rawdata.shape[2], slidingWindow):
                                bx, ex = get_border(x, x + net_size, rawdata.shape[0])
                                by, ey = get_border(y, y + net_size, rawdata.shape[1])
                                bz, ez = get_border(z, z + net_size, rawdata.shape[2])
                                input = rawdata[bx:ex, by:ey, bz:ez]
                                original_shape = input.shape
                                if original_shape[0] < net_size or original_shape[1] < net_size or   original_shape[2] < net_size:  # Need To Resize Image
                                    input = resize(input, [net_size, net_size, net_size], preserve_range=True).astype(input.dtype)
                                    if ex - bx > original_shape[0]: ex = original_shape[0]
                                    if ey - by > original_shape[1]: ey = original_shape[1]
                                    if ez - bz > original_shape[2]: ez = original_shape[2]
                                patch_predict = model.model.predict(np.reshape(input, (1, net_size, net_size, net_size)), verbose=0)
                                patch_predict = patch_predict[0, ...] * borders
                                borders_reshape = borders
                                if original_shape[0] < net_size or original_shape[1] < net_size or \
                                        original_shape[2] < net_size:  # Need To Resize Image
                                    patch_predict = resize(patch_predict, original_shape + (5,), preserve_range=True).astype(
                                        input.dtype)
                                    borders_reshape = resize(borders, original_shape, preserve_range=True).astype(
                                        input.dtype)

                                image_predict[bx:ex, by:ey, bz:ez] += patch_predict
                                nb_image_predict[bx:ex, by:ey, bz:ez] += borders_reshape
                                printp(100.0 * float(i) / nbTotal, prev="Predict tiles ")
                                i += 1
                    print("")
                    image_predict /= nb_image_predict
                    del nb_image_predict
                else:
                    rawdata = resize(rawdata, [net_size, net_size, net_size], preserve_range=True).astype(rawdata.dtype)
                    print(f"predict semantic with shape {rawdata.shape}")
                    image_predict = model.model.predict(np.reshape(rawdata, (1,) + rawdata.shape), verbose=0)
                    image_predict = image_predict[0, ...]
                image_predict = np.uint8(np.argmax(image_predict, axis=-1))  # Convert probabilities in 5 class
                print("convert semantic to instance segmentation")
                data = semantic_to_segmentation(image_predict)
                data = resize(data, init_shape, preserve_range=True, order=0)
                print(f"-> execution time {datetime.now()-start_time}")
                imsave(f.get_sem_name(),np.swapaxes(image_predict,0,2))
                print(f"Save to "+f.get_semseg_name(patches=patches))
                imsave(f.get_semseg_name(patches=patches), np.swapaxes(data,0,2))
                print(f"found {len(np.unique(data)-1)} cells ")


#CELLPOSE PREDICTION
import sys

def get_env():
    sp = sys.path[1].split("/")
    if "envs" in sp:
        sp=sp[sp.index("envs") + 1]
        if sp.startswith("cellpose"):
            if sp=="cellpose": return 2
            return int( sp[8:])
    return 0

cp_version=get_env()
print(f"---> Found CellPose {cp_version}")
if cp_version>0:
    model=None
    for f in files:
        if not isfile(f.get_cp_name(cp_version)):
            print(f"Process CellPose {cp_version} for {f.get_cp_name(cp_version)}")
            rawdata = imread(join(f.path, f.raw_name))
            seg=imread(f.get_segi_name())
            if rawdata.shape[0] < rawdata.shape[2]:
                rawdata = np.swapaxes(rawdata, 0, 2)
                seg = np.swapaxes(seg, 0, 2)

            print(f" shape={rawdata.shape} and {seg.shape}")
            #Calculate average diameter
            cells, nb = np.unique(seg, return_counts=True)
            radius = []
            for i in range(len(cells)):
                if cells[i] != 0:
                    radius.append(((np.pi * nb[i]) * 3.0 / 4.0) ** (1 / 3))
            diameter = np.int16(2 * np.mean(radius))
            print( f" --> Average diameter {diameter}")
            start_time = datetime.now()
            anisotropy = f.voxel_size[2] / f.voxel_size[1]
            if model is None:
                try:
                    from cellpose import models
                    print(f" Load CellPose Model ")
                    if cp_version==2:model = models.CellposeModel(gpu=True,model_type="cyto2")
                    elif cp_version == 3:  model = models.CellposeModel(gpu=True, model_type="cyto3")
                    elif cp_version==4:model = models.CellposeModel(gpu=True)
                except:
                    print("CellPose is required for prediction")
                    quit()
            if cp_version == 2 or cp_version == 3:
                masks = model.eval(rawdata, diameter=diameter,anisotropy=anisotropy, do_3D=True)
            elif cp_version == 4:
                masks = model.eval(rawdata, diameter=diameter, anisotropy=anisotropy, do_3D=True, z_axis=2)

            print(f" --> execution time {datetime.now() - start_time}")
            print(f" --> Found {len(np.unique(masks[0]))} / {len(cells)}")
            imsave(f.get_cp_name(cp_version), masks[0])
            print(f"Save to {f.get_cp_name(cp_version)}" )



#PLOT RESULT
if tf_activated:
    from morphodeep.tools.image import get_glasbey
    from matplotlib import pyplot as plt
    from morphodeep.networks.IOU_loss import IOU

    def plot_seg(ax, title, im, cmapp=None):
        ax.set_title(title, fontsize=25)
        if cmapp is None: cmapp = cmap
        ax.imshow(im, cmap=cmapp, interpolation="None")
        ax.axis('off')

    for f in files:
        if True:#f.raw_name=="Mmu_E1_CAGTAG1_01_Membranes.tiff":#True:#not isfile(join(f.path, f.get_acc_name())): #Always recompute ...
            print(f"Process Accuracy for {f.get_acc_name()}")
            rawdata = imread(join(f.path, f.raw_name))
            gt_segmented = imread(f.get_segi_name())
            cps={}
            for cp_v in[2,3,4]:
                if isfile(f.get_cp_name(cp_v)):
                    cps[cp_v]=imread(f.get_cp_name(cp_v))
                    if cp_v==4: cps[cp_v] = cps[cp_v]=np.swapaxes(cps[cp_v], 1, 2)
            sems={}
            for patches in [True, False]:
                sems[patches]=imread(f.get_semseg_name(patches))

            print(f"11 raw {rawdata.shape}  gt {gt_segmented.shape}")
            for cp_v in cps: print(f" cp {cp_v} {cps[cp_v].shape}")
            for patches in sems: print(f" Patches  {patches} sem {sems[patches].shape}")


            if rawdata.shape[0] < rawdata.shape[2]: rawdata = np.swapaxes(rawdata, 0, 2)
            if gt_segmented.shape[0] < gt_segmented.shape[2]: gt_segmented = np.swapaxes(gt_segmented, 0, 2)
            for cp_v in cps:
                if cps[cp_v].shape[0] < cps[cp_v].shape[2]: cps[cp_v] = np.swapaxes(cps[cp_v], 0, 2)
            for patches in sems:
                if sems[patches].shape[0] < sems[patches].shape[2]: sems[patches] = np.swapaxes(sems[patches], 0, 2)

            print(f"22 raw {rawdata.shape}  gt {gt_segmented.shape}")
            for cp_v in cps: print(f" cp {cp_v} {cps[cp_v].shape}")
            for patches in sems: print(f" Patches  {patches} sem {sems[patches].shape}")


            if gt_segmented.shape[0]!=rawdata.shape[0]: gt_segmented = np.swapaxes(gt_segmented, 0, 1)
            for patches in sems:
                if  sems[patches].shape[0] != rawdata.shape[0]:  sems[patches] = np.swapaxes( sems[patches], 0, 1)
            for cp_v in cps:
                if cps[cp_v].shape[0] != rawdata.shape[0]: cps[cp_v] = np.swapaxes(cps[cp_v], 0, 1)

            print(f"raw {rawdata.shape}  gt {gt_segmented.shape}")
            for cp_v in cps: print(f" cp {cp_v} {cps[cp_v].shape}")
            for patches in sems: print(f" Patches  {patches} sem {sems[patches].shape}")


            print("Compute IOU")
            #COMPUTE IOU
            result = {}
            error = {}
            for patches in sems:
                if f.data_type=="Ascidian": error_sem, result["error_gt_seg"] = IOU(gt_segmented[::2,::2,::2], sems[patches][::2,::2,::2], return_statistics=True)
                else: error_sem, result["error_gt_seg"] = IOU(gt_segmented, sems[patches], return_statistics=True)
                error[f'sem_{patches}']= int(error_sem * 100) / 100
            for cp_v in cps:
                if f.data_type=="Ascidian": ecp, result["error_gt_cp"] = IOU(gt_segmented[::2,::2,::2], cps[cp_v][::2,::2,::2], return_statistics=True)
                else: ecp, result["error_gt_cp"] = IOU(gt_segmented, cps[cp_v], return_statistics=True)
                error[f'cp_{cp_v}'] =  int(ecp * 100) / 100


            fig, axs = plt.subplots(3, 7, figsize=(70, 40))
            cmap = get_glasbey(100000)

            zs = int(gt_segmented.shape[2] / 2)
            iz = 0
            for z in [zs - int(zs / 2), zs, zs + int(zs / 2)]:
                plot_seg(axs[iz, 0], f"Images", np.swapaxes(rawdata[..., z], 0, 1), cmapp="gray")
                plot_seg(axs[iz, 1], f"gt z={z}/{gt_segmented.shape[2]}", np.swapaxes(gt_segmented[..., z], 0, 1))
                for patches in sems:
                    title=f"Sem IOU={error[f'sem_{patches}']}"
                    if patches: title="Patches "+title
                    plot_seg(axs[iz, 2+patches], title, np.swapaxes(sems[patches][..., z], 0, 1))
                for patches in [True,False]:
                    if patches not in sems: axs[iz, 2+patches].axis('off')
                for cp_v in cps:
                    plot_seg(axs[iz, 2+cp_v], f"CellPose {cp_v} IOU={error[f'cp_{cp_v}']}", np.swapaxes(cps[cp_v][..., z], 0, 1))
                for cp_v in [2,3,4]:
                    if cp_v not in cps: axs[iz, 2+cp_v].axis('off')
                iz += 1

            plt.savefig(f.get_acc_name())
            plt.close(fig)
