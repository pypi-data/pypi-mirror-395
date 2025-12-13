import os,sys
sys.path.append("../..")
from os.path import join, isfile, basename, dirname

from morphodeep.paths import WORK, RESULT, SCRATCH
#Retrieve all networks from server
from morphodeep.tools.utils import get_dataname, mkdir, execute, ssh_connect, ssh_ls, ssh_cp, ssh_isfile, ssh_push, \
    host_name

local_main_path="../../"

morphonet_name="morphonet"

class method:
    def __init__(self,specie,img_size=256,mode="3D",network="JUNNET",epochs=None,patches=False):
        self.img_size=img_size
        self.mode=mode
        self.specie=specie
        self.network=network
        self.epochs=epochs
        self.patches=patches

def get_networks(networks):
    from scp import SCPClient
    jz=ssh_connect(host_name)
    scpc = SCPClient(jz.get_transport())

    dist_path=join(WORK,"Semantic")
    local_path=join(local_main_path,"DATA")

    for method in networks:
        cm_path=join(f"NETWORKS_{method.img_size}_{method.mode}", method.specie,f"{method.network}_{method.img_size}")
        hfiles = ssh_ls(jz, join(dist_path,cm_path))
        last_epochs=0
        last_hfile=None
        for hfile in hfiles:
            if hfile.endswith(".h5"):
                epochs = int(hfile.split(".")[-2])
                if epochs>last_epochs:
                    last_epochs=epochs
                    last_epochs_file=hfile
                    last_hfile=hfile
        print(" --> FOUND "+str(last_hfile))
        if last_epochs>0:
            if not isfile(join(local_path,cm_path,last_epochs_file)):
                os.system('rm -rf '+join(local_path,cm_path)) #Delete Previous Files
                mkdir(join(local_path,cm_path))
                ssh_cp(scpc,join(dist_path, cm_path,last_epochs_file),join(local_path,cm_path))
    jz.close()
    print(" --> DONE ")

def get_test_data(networks,train=False,valid=False,sync_files=False):

    dist_path=join(WORK,"Semantic")
    local_path=join(local_main_path,"DATA")
    mkdir(local_path)
    for method in networks:
        mkdir(join(local_path,f"NETWORKS_{method.img_size}_{method.mode}", method.specie))
        if train:
            train_file = join(f"NETWORKS_{method.img_size}_{method.mode}", method.specie, "tf_train.txt")
            ltrain_file = join(local_path, train_file)
            if not isfile(ltrain_file) or sync_files:
                execute(  "rsync -avz --delete-before  " + host_name + ":" + join(dist_path, train_file) + " " + ltrain_file)
        if valid:
            valid_file = join(f"NETWORKS_{method.img_size}_{method.mode}", method.specie, "tf_valid.txt")
            lvalid_file = join(local_path, valid_file)
            if not isfile(lvalid_file) or sync_files:
                execute(  "rsync -avz --delete-before  " + host_name + ":" + join(dist_path, valid_file) + " " + lvalid_file)

        # Synchronize test files
        test_file = join(f"NETWORKS_{method.img_size}_{method.mode}", method.specie, "tf_test.txt")
        ltest_file = join(local_path, test_file)
        if not isfile(ltest_file) or sync_files:
            execute("rsync -avz --delete-before  " + host_name + ":" + join(dist_path,
                                                                            test_file) + " " + ltest_file)

        for f in open(ltest_file,"r"):
            #MEMBRANE
            fname=f.strip()
            #print(f"Retrieve {fname}")
            lfname=fname.replace(join(SCRATCH,"Semantic"),local_path)
            if  not isfile(lfname) and not isfile(lfname+".gz"):
                mkdir(os.path.dirname(lfname))
                execute("scp " + host_name + ":" +fname+ " " + lfname)
                execute(f"cd {dirname(lfname)} ; gzip {basename(lfname)} &")

            #SEGMENTED
            sfname=fname.replace("membrane","segmented").replace("_M.tiff","_S.tiff")
            lsfname=sfname.replace(join(SCRATCH,"Semantic"),local_path)
            if not isfile(lsfname) and not isfile(lsfname+".gz"):
                mkdir(os.path.dirname(lsfname))
                execute("scp " + host_name + ":" + sfname + " " + lsfname)
                execute(f"cd {dirname(lsfname)} ; gzip {basename(lsfname)} &")

            #SEMANTIC
            sfname = fname.replace("membrane", "semantic").replace("_M.tiff", "_JN.tiff")
            lsfname = sfname.replace(join(SCRATCH, "Semantic"), local_path)
            if not isfile(lsfname) and not isfile(lsfname+".gz"):
                mkdir(os.path.dirname(lsfname))
                execute("scp " + host_name + ":" + sfname + " " + lsfname)
                execute(f"cd {dirname(lsfname)} ; gzip {basename(lsfname)} &")

    print(" --> ALL DONE ")

def get_predicted_test_data(networks,sync_files=False):
    dist_path = join(WORK, "Semantic")
    local_path = join(local_main_path, "DATA")

    for method in networks:
         test_file =join(local_path, f"NETWORKS_{method.img_size}_{method.mode}", method.specie, "tf_test.txt")
         for f in open(test_file, "r"):
            # MEMBRANE# /lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/GT_3D/SPIM-Phallusia-Mammillata/membrane/140317-Patrick-St8/140317-Patrick-St8_fuse_t139_M.tiff
            fname = f.strip() #

            if method.network.startswith("cellpose") or method.network.startswith("plantseg"):
                #CELLPOSE OR PLANTSEG
                segname=fname.replace(f"GT_{method.mode}",f"PD_{method.mode}").replace("membrane",method.network)
                if method.network.startswith("cellpose"): segname=segname.replace("_M.tiff","_CP.tiff")
                if method.network.startswith("plantseg"): segname = segname.replace("_M.tiff", "_PS.tiff")
                lsegname=segname.replace(join(SCRATCH, "Semantic"), local_path)
                if not isfile(lsegname) or sync_files:
                    mkdir(os.path.dirname(lsegname))
                    execute("rsync -avz --delete-before  " + host_name + ":" + segname + " " + os.path.dirname(lsegname))

            else:
                #SEMANTIC #/lustre/fsn1/projects/rech/dhp/uhb36wd/Semantic/PD_3D/ALL-all/DUNNET_256_EPOCHS_143/SPIM-Phallusia-Mammillata/140317-Patrick-St8/140317-Patrick-St8_fuse_t139_SEG.tiff (AND SEM)
                network_name=f"{method.network}_{method.img_size}_EPOCHS_{method.epochs}"
                if method.patches:network_name+="_patches"
                segname=fname.replace(f"GT_{method.mode}",f"PD_{method.mode}/{method.specie}/{network_name}").replace("/membrane","").replace("_M.tiff","_SEG.tiff")

                lsegname=segname.replace(join(SCRATCH, "Semantic"), local_path)
                if not isfile(lsegname) or sync_files:
                    mkdir(os.path.dirname(lsegname))
                    execute("rsync -avz --delete-before  " + host_name + ":" + segname + " " + os.path.dirname(lsegname))

                semname = segname.replace("_SEG.tiff","_SEM.tiff")
                lsemname = semname.replace(join(SCRATCH, "Semantic"), local_path)
                if not isfile(lsemname) or sync_files:
                    mkdir(os.path.dirname(lsemname))
                    execute("rsync -avz --delete-before  " + host_name + ":" + semname + " " + os.path.dirname(lsemname))

#
def get_results(networks):
    #os.system("rsync -avz --delete-before  " + host_name + ":/gpfswork/rech/dhp/uhb36wd/RESULT/* " + RESULT)

    dist_path = RESULT
    local_path = join(local_main_path, "RESULT")

    for method in networks:
        network_dist_path = join(dist_path, f"NETWORKS_{method.img_size}_{method.mode}", method.specie)
        network_local_path = join(local_path,f"NETWORKS_{method.img_size}_{method.mode}")
        mkdir(network_local_path)
        execute("rsync -avz --delete-before  " + host_name + ":" + network_dist_path + " " + network_local_path)
    print(" --> DONE ")


def get_external_data(mode="3D",species=["Drosophila", "Mouse", "Zebra","Ascidian"]):
    if mode=="3D":
        for specie in species:
            execute(  f"rsync -avz --delete-before  {host_name}:/lustre/fsn1/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/{specie}  /Users/efaure/SeaFile/MorphoDeep/semantic/figures/figure_5/EXTERNAL_DATA_{mode}/")
    else:
        execute(
            f"rsync -avz --delete-before  {host_name}:/lustre/fsn1/projects/rech/dhp/uhb36wd/DATA_INTEGRATION/EXTERNAL_DATA_{mode}  /Users/efaure/SeaFile/MorphoDeep/semantic/figures/figure_5/")


def push_morphonet(hostname,networks):
    from scp import SCPClient
    mn = ssh_connect(hostname)
    scpc = SCPClient(mn.get_transport())

    dist_path = "/DATA/MODELS"
    local_path = join(local_main_path, "DATA")
    temp_path=join(local_path,"TEMP")
    os.system(f"rm -rf {temp_path}")
    os.system(f"mkdir -p {temp_path}")
    for method in networks:
        network_name=method.specie+f"_FusedToSemantic_{method.network}_{method.mode}_{method.img_size}"
        print(f"Uploading {network_name} to morphonet {dist_path}")

        #List Current Downloaded Epochs
        last_epochs=0
        last_epochs_file=None
        cm_path = join(f"NETWORKS_{method.img_size}_{method.mode}", method.specie, f"{method.network}_{method.img_size}")
        local_net = join(local_path, cm_path)
        for hfile in os.listdir(local_net):
            if hfile.endswith(".h5"):
                epochs = int(hfile.split(".")[-2])
                if epochs > last_epochs:
                    last_epochs = epochs
                    last_epochs_file = hfile
        if last_epochs_file is None:
            print(f"--> ERROR {network_name} please firtst downlaod the  network locallly using 'get_networks'")
        else:
            print(f" -> last epochs is {last_epochs}")
            #Look at the distant epochs #distant_epochs = ssh_ls(mn, join(dist_path, network_name+".epochs"))
            epochs_name=network_name+".epochs"
            required=True
            if ssh_isfile(mn,join(join(dist_path, epochs_name))):
                ssh_cp(scpc, join(join(dist_path, epochs_name)), temp_path)
                if isfile(join(temp_path,epochs_name)):
                    current_epochs=None
                    with open(join(temp_path,epochs_name), "r") as f:
                        for line in f:
                            current_epochs=int(line.strip())
                    if    current_epochs is not None:
                        print(f"--> distance epochs is {current_epochs} ")
                        if last_epochs==current_epochs:
                            print(f"--> the network {network_name} is already update ")
                            required=False
            #We Push the new network
            if required:
                print(f"Uploading {network_name} at epochs {last_epochs} to morphonet {dist_path}")
                # Write a file with current epochs number
                with open(join(temp_path, epochs_name), "w") as f:
                    f.write(str(last_epochs))

                ssh_push(scpc, join(temp_path, epochs_name), dist_path)
                mn.exec_command(f"chown www-data:www-data {join(dist_path,epochs_name)}")
                #Copy Networks
                dist_networks=join(dist_path,network_name+".h5")
                ssh_push(scpc, join(local_net, last_epochs_file), dist_networks)
                mn.exec_command(f"chown www-data:www-data {dist_networks}")


    mn.close()
    #os.system(f"rm -rf {temp_path}")
    print(" --> DONE ")



#GET RESULT + CSV Benchmark
networks=[]

species=["SPIM-Phallusia-Mammillata","CONF-Arabidopsis-Thaliana","CONF-LateralRootPrimordia","CONF-Ovules","CONF-SeaStar","CONF-Caenorhabditis-Elegans","ALL-all","CONF-Phallusia-Mammillata"]
for specie in species:
    networks.append(method(specie))

#get_results(networks)
#get_results([method("ALL-all")]) ##3D
#get_results([method("ALL-all",img_size=128)]) ##3D 128
#get_results([method("ALL-all",mode="2D")]) #2D#


#SYNCHRONIZE LAST EPOCHS NETWORKS
#get_networks([method("ALL-all")]) ##3D
#get_networks([method("ALL-all",img_size=128)]) ##3D 128
get_networks([method("ALL-all",mode="2D")]) #2D#

#PUSH LAST NETWORKS ON MORPHONET
#push_morphonet(morphonet_name,[method("ALL-all")]) ##3D
#push_morphonet(morphonet_name,[method("ALL-all",img_size=128)]) ##3D 128
push_morphonet(morphonet_name,[method("ALL-all",mode="2D")])  ##3D



#SYNCHORINZE TEST FILES
#get_test_data([method("ALL-all")])
#get_test_data([method("ALL-all",img_size=128)])
#get_test_data([method("ALL-all",mode="2D")])

#SYNCHRONIZE PREDICTION TEST FILES
#get_predicted_test_data([method("ALL-all",128,"3D","JUNNET",2463,True)])
#get_predicted_test_data([method("ALL-all",256,"3D","JUNNET",1523,True)])
#get_predicted_test_data([method("ALL-all",network="cellpose4")])
#get_predicted_test_data([method("ALL-all",network="cellpose3")])
#get_predicted_test_data([method("ALL-all",network="plantseg")])

#SYNCHRONISZE PREDICTION EXTERNAL DATA
#get_external_data()
#get_external_data(species=["Ascidian"])
#get_external_data(mode="2D")
