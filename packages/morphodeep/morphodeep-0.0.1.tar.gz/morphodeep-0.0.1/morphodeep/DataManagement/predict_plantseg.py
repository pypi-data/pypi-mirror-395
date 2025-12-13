from skimage.transform import resize

from morphodeep.paths import SCRATCH
from morphodeep.tools.utils import get_filename, execute, mkdir, get_path, get_basename
from os.path import join, isdir, isfile, basename
from skimage.io import imread, imsave
import h5py
import os

#conda activate plant-seg

network_plantseg={}
network_plantseg["LP"]="generic_light_sheet_3D_unet"
network_plantseg["OV"]="generic_confocal_3D_unet"
network_plantseg["AT"]="confocal_3D_unet_sa_meristem_cells"
network_plantseg["PM"]="generic_light_sheet_3D_unet"
network_plantseg["SS"]="generic_confocal_3D_unet"
network_plantseg["CE"]="generic_confocal_3D_unet"

species={}
species["CONF-Arabidopsis-Thaliana"]="AT"
species["CONF-Caenorhabditis-Elegans"]="CE"
species["CONF-LateralRootPrimordia"]="LP"
species["CONF-Ovules"]="OV"
species["CONF-SeaStar"]="SS"
species["SPIM-Phallusia-Mammillata"]="PM"

def find_specie(filename):
    for s in species:
        if filename.find(s) >= 0:
            return species[s]
    return None
def predict_plantseg(specie,txt_path,what=None):
    # Predict TRAIN, TEST, and VALID DATA PATH
    whats = ["train", "test", "valid"] if what is None or what == "" else [what]
    print(f" --> Compute data for {whats}")

    ratio = 1
    if  specie == "PM": ratio = 2

    nb_done=1
    nb_max = 10
    Exceptions=["N_435_final_crop_ds2_M.tiff","N_522_final_crop_ds2_M.tiff","N_441_final_crop_ds2_M.tiff"] #OV There is error from plantseg to predict this files
    while nb_done>0:
        nb_done=0
        for what in whats:

            TEMP_PATH = join(SCRATCH,"TEMP",specie,"plantseg",what ) #TEMPORARY , WILL BE DELETED AFTER
            execute("rm -rf "+TEMP_PATH)
            mkdir(TEMP_PATH)

            #COPY ALL FILES IN THE SAME PATH
            files_list=[]
            files_shape={}
            which_specie=None
            for line in open(join(txt_path+"_" + what + ".txt"), "r"):
                filename = line.strip()
                if basename(filename) not in Exceptions:
                    new_plantseg_name = filename.replace("/GT", "/PD").replace("/membrane/", "/plantseg/").replace("_M.tiff","_PS.tiff")
                    if  isfile(new_plantseg_name): print(" --> already computed "+new_plantseg_name)
                    if not isfile(new_plantseg_name) and len(files_list)<nb_max:
                        print(f"okok {specie}")
                        is_ok=True
                        if specie == "all":
                            actual_specie = find_specie(filename)
                            if which_specie is None: which_specie = actual_specie
                            elif which_specie != actual_specie: #Changement of specie
                                is_ok=False
                        if is_ok:
                            if ratio==1:
                                execute("cp -f "+filename+" "+TEMP_PATH)
                            else:
                                print(f"ratio={ratio} for {basename(filename)}")
                                im = imread(filename)
                                files_shape[filename] = im.shape
                                imsave(join(TEMP_PATH, basename(filename)), im[::ratio, ::ratio, ::ratio])
                            files_list.append(filename)
            nb_files=len(files_list)
            nb_done+=nb_files
            current_network=network_plantseg[which_specie] if specie=="all" else network_plantseg[specie]
            if nb_files==0:
                print(f" --> everything is computed for {what}!")
            else:
                #CREATE CONFIG FILE FOR PLANTSEG
                config_file=join(txt_path+ "_config_" + what + "_plantseg.yaml")
                print(" --> prepare config file "+config_file)
                fw = open(config_file, "w")
                fw.write('path: ' +TEMP_PATH + "\n")
                for line in open("semantic/DataManagement/config_plantseg.template", "r"):
                    if line.find("model_name") >= 0:
                        fw.write('  model_name: "' + current_network + '"')
                    else:
                        fw.write(line)
                fw.close()

                #LAUNCH PLANT SEG
                execute("plantseg --config "+config_file)

                #CONVERT DATA
                if not isdir(join(TEMP_PATH, "PreProcessing")):
                    print(" --> MISS Preprocessing path "+join(TEMP_PATH, "PreProcessing"))

                for line in files_list:
                    filename=get_filename(line.strip())
                    plantseg_name = join(TEMP_PATH,"PreProcessing", current_network, "MultiCut",filename.replace(".tiff", "_predictions_multicut.h5"))
                    if not isfile(plantseg_name):
                        print(" --> MISS filename "+plantseg_name)
                    else:
                        new_plantseg_name = line.replace("/GT","/PD").replace("/membrane/","/plantseg/").replace("_M.tiff", "_PS.tiff")

                        f = h5py.File(plantseg_name, 'r')
                        data = f['segmentation']
                        mkdir(get_path(new_plantseg_name))
                        if ratio >1:
                            data=resize(data,files_shape[line],preserve_range=True,order=0).astype(data.dtype)
                        imsave(new_plantseg_name, data)

                #REMOVE TEMP DATA...
                execute("rm -rf "+TEMP_PATH)




def predict_plantseg_files(filename):
    TEMP_PATH = join(SCRATCH, "TEMP", "plantseg")  # TEMPORARY , WILL BE DELETED AFTER
    execute("rm -rf " + TEMP_PATH)
    networks = {"CONF": "generic_confocal_3D_unet", "SPIM": "generic_light_sheet_3D_unet"}

    for n in networks:
        mkdir(TEMP_PATH)
        network = networks[n]
        files_list = []
        for f in open(filename, "r"):
            if not f.startswith("#"):
                tab = f.split(";")
                if len(tab) < 3:
                    print(f"Not well define {f}")
                    quit()
                input_filename = tab[0]
                if input_filename.find("/"+n+"/") >= 0:
                    output_filename = input_filename.replace(".tif", f"_PS.tif")
                    if not isfile(output_filename):
                        execute("cp -f " + input_filename + " " + TEMP_PATH)
                        files_list.append(input_filename)
        if len(files_list)>0:
            print(f"Predict {len(files_list)} files ")

            config_file = join(TEMP_PATH, f"plantseg_config_{network}_plantseg.yaml")
            if not isfile(config_file):  # CREATE CONFIG FILE FOR PLANTSEG
                print(" --> prepare config file " + config_file)
                fw = open(config_file, "w")
                fw.write('path: ' + TEMP_PATH + "\n")
                for line in open("semantic/DataManagement/config_plantseg.template", "r"):
                    if line.find("model_name") >= 0:
                        fw.write('  model_name: "' + network + '"')
                    else:
                        fw.write(line)
                fw.close()

            # LAUNCH PLANT SEG
            execute(f"plantseg --config {config_file}")

            # CONVERT DATA
            if not isdir(join(TEMP_PATH, "PreProcessing")):
                print(" --> MISS Preprocessing path " + join(TEMP_PATH, "PreProcessing"))
                quit()
            for input_filename in files_list:
                plantseg_name = join(TEMP_PATH, "PreProcessing", network, "MultiCut",
                                     get_filename(input_filename).replace(".tif", "_predictions_multicut.h5"))
                if not isfile(plantseg_name):
                    print(" --> MISS filename " + plantseg_name)
                else:
                    f = h5py.File(plantseg_name, 'r')
                    data = f['segmentation']
                    output_filename = input_filename.replace(".tif", f"_PS.tif")
                    print(f"Save {output_filename}")
                    imsave(output_filename, data)

            # REMOVE TEMP DATA...
            execute("rm -rf " + TEMP_PATH)