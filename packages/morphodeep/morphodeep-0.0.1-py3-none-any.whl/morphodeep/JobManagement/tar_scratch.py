import os
import sys
sys.path.append("../..")
from os.path import join, isfile
from os import listdir
from morphodeep.tools.utils import mkdir, execute
from morphodeep.paths import SCRATCH,STORE

db="SegmentedMembrane"
db_path=join(SCRATCH,"DATABASE",db)
db_out=join(STORE,"DATABASE",db)
for gt in listdir(db_path):
    mkdir(join(db_out,gt))
    for specie in listdir(join(db_path,gt)):
        mkdir(join(db_out, gt,specie))
        for method in  listdir(join(db_path,gt,specie)):
            mkdir(join(db_out, gt, specie,method))
            for emb in listdir(join(db_path,gt,specie,method)):
                store_file=join(db_out,gt,specie,method,emb+".tar.gz")
                if not isfile(store_file):
                    cmd = "tar -cf '" + store_file + "' '" + join(db_path,gt,specie,method, emb) + "'"
                    print(cmd)
                    execute(cmd)
                else: print( " --> ok "+store_file)





