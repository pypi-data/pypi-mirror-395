from os.path import join, isfile, dirname, basename

from morphodeep.paths import WORK, SCRATCH
from morphodeep.tools.image import imread
from morphodeep.tools.utils import mkdir, execute, get_correspond_filename, host_name, ssh_connect, ssh_ls

local_data_path="/Users/efaure/Codes/PythonProjects/semantic/DATA"

jz=None

class method:
    def __init__(self,specie,img_size=256,mode="3D"):
        self.specie=specie
        self.img_size=img_size
        self.mode=mode
        self.specie=specie

def get_data_txt_file(dataset,reading=True):
    dist_path = join(WORK,"Semantic")
    test_file="tf_test.txt"
    network_dist_path = join(dist_path, f"NETWORKS_{dataset.img_size}_{dataset.mode}", dataset.specie,test_file)
    network_local_path = join(local_data_path,f"NETWORKS_{dataset.img_size}_{dataset.mode}", dataset.specie)
    if not isfile(join(network_local_path,test_file)):
        mkdir(network_local_path)
        execute("rsync -avz --delete-before  " + host_name + ":" + network_dist_path + " " + network_local_path)
        print(f" --> DONE for {dataset.specie}")

def test_reader(local_filename):
    if  isfile(local_filename):
        try:
            #print(f" --> Reading {local_filename}")
            im=imread(local_filename)
        except Exception as e:
            print(f"Error reading {local_filename} -> {e}")
            execute(f"rm -f {local_filename}")

def get_file(filename,reading=True):
    local_filename = filename.replace(join(SCRATCH, "Semantic"), local_data_path)
    if reading : test_reader(local_filename)
    if not isfile(local_filename):
        print(f"Sync {filename}")
        mkdir(dirname(local_filename))
        execute("scp  " + host_name + ":" + filename + " " + dirname(local_filename))

def get_data_test(dataset,add_methods=["segmented","semantic"]):
    test_file = join(local_data_path,f"NETWORKS_{dataset.img_size}_{dataset.mode}", dataset.specie,"tf_test.txt")
    if not isfile(test_file):
        print(f"Miss {test_file} file")
        return False
    print(f"get {test_file}")
    nb_datasets={}
    for f in open(test_file,"r"):
        filename=f.strip()
        dataset_name=basename(dirname(filename))
        if dataset_name not in nb_datasets: nb_datasets[dataset_name]=0
        nb_datasets[dataset_name]+=1
        if nb_datasets[dataset_name]<nb_per_dataset:
            get_file(filename) #Membrane
            for m in add_methods:
                get_file(get_correspond_filename(filename,m))
        else:
            print(f"skip dataset {filename} for {dataset_name}")



    print(f" --> DONE for {dataset.specie} found {nb_datasets} files")

def get_prediction_test(jz,dataset,methods=["semantic","cellpose3","cellpose4","plantseg"]):
    test_file = join(local_data_path, f"NETWORKS_{dataset.img_size}_{dataset.mode}", dataset.specie, "tf_test.txt")
    if not isfile(test_file):
        print(f"Miss {test_file} file")
        return False

    #Get Last Epochs Prediction
    if jz is None:
        from scp import SCPClient
        jz = ssh_connect(host_name)
        scpc = SCPClient(jz.get_transport())
    dist_path=ssh_ls(jz,join(SCRATCH, "Semantic",f"PD_{dataset.mode}",dataset.specie))
    print(dist_path)
    last_epochs=None
    for p in dist_path:
        if p.startswith("predict_semantic_EPOCHS_"):
            e=int(p[24:])
            if last_epochs is None or e>last_epochs:
                last_epochs=e
    print(f" Last Epochhs {last_epochs}")

    nb_datasets = {}
    for f in open(test_file, "r"):
        filename = f.strip()
        dataset_name = basename(dirname(filename))
        if dataset_name not in nb_datasets: nb_datasets[dataset_name] = 0
        nb_datasets[dataset_name] += 1
        if nb_datasets[dataset_name] < nb_per_dataset:
            for m in methods:
                pred_filename=get_correspond_filename(filename, m)
                if m=="semantic":
                    pred_filename=pred_filename.replace("GT_","PD_").replace("semantic",f"predict_semantic_EPOCHS_{last_epochs}").replace("_JN","_PS")
                get_file(pred_filename)

    print(f" --> DONE for {dataset.specie}")
    return jz


datasets=["CONF-Caenorhabditis-Elegans","CONF-Arabidopsis-Thaliana","CONF-LateralRootPrimordia","CONF-Ovules","CONF-SeaStar","SPIM-Phallusia-Mammillata","ALL-all"]

#RETRIEVE TEST FILE
'''for dataset in datasets:
    get_data_txt_file(method(dataset))
get_data_txt_file(method("ALL-all",mode="2D"))
'''

nb_per_dataset=10
#RETRIEVE GT FOR TEST FILE
for dataset in datasets:
    get_data_test(method(dataset))
    jz=get_prediction_test(jz,method(dataset))


