import os
import sys
sys.path.append("../..")
from os.path import join, isfile,isdir
from os import listdir
from morphodeep.tools.utils import mkdir, execute
from morphodeep.paths import WORK,STORE


db_path=join(WORK,"Semantic")
db_out=join(STORE,"Semantic")
for gt in listdir(db_path): #NETWORKS_512_3D
    print(f"gt={gt}")
    if gt.startswith("NETWORKS"):
        mkdir(join(db_out,gt))
        for specie in listdir(join(db_path,gt)): #CONF-Arabidopsis-Thaliana
            print(f"specie={specie}")
            mkdir(join(db_out, gt,specie))
            for network in listdir(join(db_path,gt,specie)): #JUNNET_256
                print(f"network={network}")
                if isdir(join(db_path, gt, specie,network)) and network=="JUNNET_256" :
                    #Get the last Epochs for this network
                    last_epochs = 0
                    last_hfile = None
                    for hfile in listdir(join(db_path,gt,specie,network)):
                        if hfile.endswith(".h5"):
                            epochs = int(hfile.split(".")[-2])
                            if epochs > last_epochs:
                                last_epochs = epochs
                                last_epochs_file = hfile
                                last_hfile = hfile

                    if last_hfile is not None and last_epochs > 0:
                        print(" --> FOUND " + str(last_hfile))
                        store_file=join(db_out,gt,specie,network+"-"+str(last_epochs)+".tar.gz")
                        if not isfile(store_file):

                            #We erase previous store file
                            for e in range(last_epochs):
                                prev_store_file = join(db_out, gt, specie,  network + "-" + str(e) + ".tar.gz")
                                if isfile(prev_store_file):execute("rm -rf "+prev_store_file)

                            cmd = "tar -cf '" + store_file + "' '" + join(db_path,gt,specie, network) + "'"
                            print(cmd)
                            #quit()
                            execute(cmd)
                            print(" --> DONE ")
                        else: print( " --> ok "+store_file)


                        #Now we can remove all previous epochs from work files
                        for hfile in listdir(join(db_path,gt,specie,network)):
                            if hfile!=last_hfile:
                                cmd="rm -f "+join(db_path,gt,specie,network,hfile)
                                print(cmd)
                                execute(cmd)





