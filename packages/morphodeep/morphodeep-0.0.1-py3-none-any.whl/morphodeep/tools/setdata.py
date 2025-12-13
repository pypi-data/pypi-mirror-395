
from os import listdir
from os.path import isdir, join, isfile
import random
import numpy as np
###############@ - WRITE TEXT FILE FOR TRAIN AND TESTS
from morphodeep.tools.utils import write_paths, mkdir, get_path


keep_for_prediction={}
keep_for_prediction["PM"]=["140317-Patrick-St8","200619-Romuald","220126-Sergio"]
keep_for_prediction["AT"]=["plant4"]
keep_for_prediction["SS"]=["wt_embryo1","wt-comp_embryo1"] #For Each STage


def load_imgpath(ms_path): # FROM MICROSCOPE-SPECIES  PATH
    list_imgs = []
    for emb in listdir(ms_path):  # EMBRYOS PATH
        if isdir(join(ms_path, emb)):  # EMBRYO NAME
            for f in listdir(join(ms_path, emb)):
                list_imgs.append(join(ms_path, emb, f))
    random.shuffle(list_imgs)
    return list_imgs


#GENEREATE PATHS
def generate_paths(specie,microscope,input_path,tfrecord_file,test_split,validation_split):
    print(f" --> write for {specie} -> {tfrecord_file}")
    print(" with "+str(test_split)+ " for test and "+str(validation_split)+ " for validation")
    if isfile(tfrecord_file + "_train.txt"):
        print(" FILES ALREADY EXIST PLEASE DELETE THEM FIRST IF YOU ARE SURE TO REGENERATE THE DATASET")
        quit()

    test_paths = []
    train_paths = []
    valid_paths = []
    if specie=="all":
        print(f"input_path={input_path}")
        print(f"tfrecord_file={tfrecord_file}")

        to_merge = ["CONF-Arabidopsis-Thaliana", "CONF-SeaStar", "SPIM-Phallusia-Mammillata",
                    "CONF-Caenorhabditis-Elegans","CONF-LateralRootPrimordia","CONF-Ovules","ALL-Cellpose"]

        # Statistics
        all_path = tfrecord_file.replace("/ALL-all/tf", "")
        for what in ["train", "test", "valid"]:
            for dataset in to_merge:
                datasets = []
                for line in open(join(all_path, dataset, "tf_" + what + ".txt"), 'r'):
                    datasets.append(line.strip())
                print(" --> in the " + what + " database found " + str(len(datasets)) + " for " + dataset)

        if input_path.find("3D")>0: #NB PER SPECIE
            nb_max = {'train': 200, 'test': 100, 'valid': 10}  # 3D
        else:
            nb_max = {'train': 60000, 'test': 1000, 'valid': 1000}  # 2D


        for what in ["train", "test", "valid"]:
            print(" --> create " + tfrecord_file +"_"+ what + ".txt")
            lines = []
            for dataset in to_merge:
                datasets = []
                for line in open(join(all_path, dataset, "tf_" + what + ".txt"), 'r'):
                    datasets.append(line.strip())
                if len(datasets) > nb_max[what]:
                    random.shuffle(datasets)
                    datasets = datasets[0:nb_max[what]]
                for line in datasets:
                    file=line.strip()
                    if not isfile(file):
                        print(f"-> MISS {file}")
                    lines.append(file)
                    if what=="train": train_paths.append(file)
                    if  what == "test": test_paths.append(file)
                    if  what == "valid": valid_paths.append(file)

            mkdir(tfrecord_file.replace("/tf",""))
            f = open(tfrecord_file +"_"+ what + ".txt", "w")
            random.shuffle(lines)
            for line in lines:
                f.write(line + "\n")
            f.close()

    else:
        #One Specie only
        mwhat = "membrane" #Look for file in membrane path
        if specie=="OV" or specie=="LP": #ALREADY SPLIT
            for what in ['test','train','val']:
                for f in listdir(join(input_path, mwhat, what)):
                    filename=join(input_path, mwhat, what,f)
                    if what=="test":test_paths.append(filename)
                    elif what == "train": train_paths.append(filename)
                    elif what == "val": valid_paths.append(filename)

        elif  specie=="CE": #ALREADY SPLIT
            train_paths = []
            test_paths = []
            for what in ['CMapTrainingGroundTruth', 'ValidationGroundTruth']:
                for f in listdir(join(input_path, mwhat, what)):
                    filename = join(input_path, mwhat, what, f)
                    if what=="CMapTrainingGroundTruth": train_paths.append(filename)
                    else : test_paths.append(filename)


            nb_valid=int(len(test_paths)*20/100)
            random.shuffle(test_paths)
            valid_paths = []
            for v in range(nb_valid):
                valid_paths.append(test_paths.pop(0))


        elif specie=="PM" and microscope=="CONF":
            for what in listdir(join(input_path, mwhat)):
                for f in listdir(join(input_path, mwhat, what)):
                    filename=join(input_path, mwhat, what,f)
                    test_paths.append(filename)
                    train_paths.append(filename)

        else: #GENERIC CASES
            paths=load_imgpath(join(input_path, mwhat))
            print(" --> found " + str(len(paths)) + " images for " + input_path)
            train_paths, valid_paths, test_paths = get_paths(paths, test_split, validation_split,keep_for_prediction=keep_for_prediction[specie])

    print(" --> train_paths contains " + str(len(train_paths)) + " samples ")
    print(" --> test_paths contains " + str(len(test_paths)) + " samples ")
    print(" --> valid_paths contains " + str(len(valid_paths)) + " samples ")
    mkdir(get_path(tfrecord_file))
    write_paths(train_paths,tfrecord_file + "_train.txt")
    write_paths(test_paths, tfrecord_file+ "_test.txt")
    write_paths(valid_paths,tfrecord_file + "_valid.txt")


def get_paths(paths,test_split,validation_split,keep_for_prediction=None):
    exludes=[]
    if keep_for_prediction is not None:
        new_paths=[]
        for p in paths:
            ex=False
            for e in keep_for_prediction:
                if p.find(e)>=0:  ex=True #and p.find("stk01_")>=0 #For Sea URchin
            if ex:
                exludes.append(p)
            else :
                new_paths.append(p)

        paths=new_paths
        print(" --> excludes "+str(len(exludes))+ " in "+str(keep_for_prediction)+ "and keep "+str(len(paths)))

    cut = 0
    # TEST  DATASET
    test_paths = []
    if test_split > 0:
        nb_test =np.uint64(np.round(len(paths) * test_split))
        test_paths = paths[0:nb_test]
        cut = nb_test

    # VALIDATION DATASET
    valid_paths = []
    if validation_split > 0:
        nb_valid = np.uint64(np.round(len(paths) * validation_split))
        valid_paths = paths[cut:cut + nb_valid]
        cut += nb_valid

    for p in exludes: test_paths.append(p)


    train_paths = paths[cut:]

    return train_paths,valid_paths,test_paths





