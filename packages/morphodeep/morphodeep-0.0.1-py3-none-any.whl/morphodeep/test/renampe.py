import os
emb_name="250625-Virginie_02"
path="/media/SSD2/DATA/CElegans/250625-Virginie_02/JUNC"
for f in os.listdir(path):
    if f.endswith(".tiff"):
        os.system(f"mv {path}/{f} {path}/{f.replace('embryon2_CGT',emb_name+'_junctions').replace('_SEM','')}")