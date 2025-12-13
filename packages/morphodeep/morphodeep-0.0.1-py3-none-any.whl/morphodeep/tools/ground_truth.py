# -*- coding: latin-1 -*-

from tifffile import TiffFileError
from tqdm import tqdm
import os
from .image import imread, imsave
from .utils import mkdir, get_gt_filename, printi, get_path, launch_job_array, printw, printe, \
    file_write, get_correspond_filename, get_2D_filename, get_specie_from_name
from os.path import isdir, join, isfile, dirname, basename
from os import listdir
from skimage.morphology import binary_dilation,binary_erosion
from skimage.measure import regionprops
import numpy as np
from skimage.draw import line_nd
from itertools import combinations


######### TOOOLS


def get_distance_points(c,coords):
    c_all=np.array(c*len(coords)).reshape((len(coords),len(c)))
    d=np.power(np.array(coords)-c_all,2).sum(axis=-1)
    return d.sum()

def get_closest_points(c,coords):
    c_all=np.array(c*len(coords)).reshape((len(coords),len(c)))
    d=np.power(np.array(coords)-c_all,2).sum(axis=-1)
    ids=np.where(d==d.min())[0][0]
    return tuple(coords[ids])

def permut(points):
    return [tuple(sorted(combo)) for combo in combinations(points, 3)]

def get_closet_at(c,coords,distance):
    c_all=np.array(list(c)*len(coords)).reshape((len(coords),len(c)))
    d=np.power(np.array(coords)-c_all,2).sum(axis=-1)
    return np.array(coords)[d<distance]


######### SEMANTIC
def semantic(seg,distance = 30, background_value=0):
    '''
    Compute the semantic format ground truth from a segmentation file
    # Multi Classes :
    #    0 : Background
    #    1 : Inside the Cell (cytoplasm)
    #    2 : Junction Level 1 (Surface of Contact between 2 cells)
    #    3 : Junction Level 2 (Line of Contact between 3 cells)
    #    4 : Junction Level 3 (point of Contact between 4 or more cells)
    '''
    if seg is None: return None
    if len(seg.shape)==1:
        return None

    dim = len(seg.shape)
    print(f"Segmentation shape: {seg.shape}")
    # List all coords for all types of connections
    regions = regionprops(seg)
    pixel_neigbhors = {}
    for r in tqdm(regions):
        mask_box = seg == r.label
        border_box = np.uint8(binary_dilation(mask_box)) - np.uint8(binary_erosion(mask_box))
        coords = np.where(border_box == 1)
        # print(f"label {r.label} found {len(coords[0])} coords")
        for i in range(len(coords[0])):  # tqdm(range(len(coords[0]))):
            c = [coords[0][i], coords[1][i], coords[2][i]]   if dim==3 else [coords[0][i], coords[1][i]]
            pixel_box = seg[c[0] - 1:c[0] + 1, c[1] - 1:c[1] + 1,  c[2] - 1:c[2] + 1]  if dim==3 else  seg[c[0] - 1:c[0] + 1, c[1] - 1:c[1] + 1]  # Look for the neiggbhors of each pixel
            neis = tuple(np.unique(pixel_box))
            if len(neis) >= 2:
                if neis not in pixel_neigbhors: pixel_neigbhors[neis] = []
                if c not in pixel_neigbhors[neis]:
                    pixel_neigbhors[neis].append(c)

    print(f" found {len(pixel_neigbhors.keys())} with different connections ")

    sem = np.zeros_like(seg).astype(np.uint8)  # BACKGROUND
    #Each class of connections will overlap the previous one
    # 1 : Cytoplasm no contact with the other cells
    sem[seg>background_value]=1

    # 2 : Surface of Contact of 2 cells
    for ty in pixel_neigbhors:
        if len(ty) >= 2:
            # print(f"{ty} -> {len(pixel_neigbhors[ty])}")
            for c in pixel_neigbhors[ty]:
                if dim == 3 :sem[c[0], c[1], c[2]] = 2
                else : sem[c[0], c[1]] = 2

    # 3 : Line of Contact of 3 cells
    for ty in pixel_neigbhors:
        if len(ty) >= 3:
            # print(f"{ty} -> {len(pixel_neigbhors[ty])}")
            coords = pixel_neigbhors[ty].copy()
            # First we have to get the points which is the farest from all the other
            distances = {}
            for c in coords:    distances[tuple(c)] = get_distance_points(c, coords)
            sorted_dict = dict(sorted(distances.items(), key=lambda item: item[1], reverse=True))
            c1 = next(iter(sorted_dict.keys()))
            if dim == 3 : sem[c1[0], c1[1], c1[2]] = 3
            else:  sem[c1[0], c1[1]] = 3
            coords.remove(list(c1))  # Remove this point
            while len(coords) > 1:  # Ellongate the lines junctions
                c2 = get_closest_points(c1, coords)
                coords.remove(list(c2))  # REmove this point
                d = np.power((np.array(c1) - c2), 2).sum()
                if d > 1:
                    # print(f"Distance between {c1} and {c2} is: {d}")
                    if dim == 3 :
                        xx, yy, zz = line_nd(c1, c2)  # Inverser (x,y,z) -> (z,y,x)
                        sem[xx, yy, zz] = 3
                    else:
                        xx, yy = line_nd(c1, c2)  # Inverser (x,y,z) -> (z,y,x)
                        sem[xx, yy] = 3

                    # We also add this points to the final list
                    for i in range(len(xx)):
                        if dim == 3:  pixel_neigbhors[ty].append([xx[0], yy[0], zz[0]])
                        else: pixel_neigbhors[ty].append([xx[0], yy[0]])
                c1 = c2
                if dim == 3:   sem[c1[0], c1[1], c1[2]] = 3
                else: sem[c1[0], c1[1]] = 3


    #4  : point of contacts between 4 or more cells
    pb = 1 #Size of the points
    for ty in pixel_neigbhors:
        if len(ty) >= 4:
            # print(f"{ty} -> {len(pixel_neigbhors[ty])}")
            if len(pixel_neigbhors[ty]) == 1:
                ca = np.uint16(pixel_neigbhors[ty][0])
            else:  # Average points
                ca = np.zeros((dim,))
                for c in pixel_neigbhors[ty]: ca += c
                ca /= len(pixel_neigbhors[ty])
                ca = np.uint16(ca)
            # Now we look for each combination  of neigbhors
            for tyy in permut(ty):
                if tyy in pixel_neigbhors:
                    # print(f" look for points {tyy} -> {len(pixel_neigbhors[tyy])}")
                    closests = get_closet_at(ca, pixel_neigbhors[tyy], distance)
                    for cc in closests:
                        if dim == 3: sem[cc[0], cc[1], cc[2]] = 4  # Add the lines
                        else : sem[cc[0], cc[1]] = 4
            if dim == 3:  sem[ca[0] - pb:ca[0] + pb:, ca[1] - pb:ca[1] + pb,  ca[2] - pb:ca[2] + pb] = 4  # Create a box arrouond the central point
            else: sem[ca[0] - pb:ca[0] + pb:, ca[1] - pb:ca[1] + pb] = 4
    return sem



####### CELL COUNTER
def cell_counter(seg,background=0):
    '''
    Calcul the number of cell (background exlude)
    '''
    cells=np.unique(seg)
    cells=cells[cells>background]
    nbCell=len(cells)
    return nbCell



#List of Ground Truth to be computed
methods=[]
methods.append("cell_counter")
methods.append("semantic")


def job_ground_truths(common_cmd,mode,input_path,microscope,specie,launch):
    jobslist=[] #Keep Trace For a Job Array Submission

    for method in methods:
        print(" Calcul Ground Truth "+method)
        mkdir(join(input_path, method))
        for emb in listdir(join(input_path,"membrane")):  # EMBRYOS PATH
            todo = 0
            nb_total = 0
            if mode=="2D"  and not launch: #IN JOB
                jobslist.append(join(input_path, "membrane", emb) + ";" + method)
            else: #3D or EXECTURE 2D
                if isdir(join(input_path,"membrane",emb)):
                    #print(f" OK for "+join(input_path,"membrane",emb))
                    for f in listdir(join(input_path,"membrane",emb)):
                        #print(f" FILE for " + join(input_path, "membrane", emb,f))
                        output_filename = get_gt_filename(join(input_path,"membrane",emb,f), method)
                        nb_total += 1
                        if not isfile(output_filename):
                            todo += 1
                            if not launch:
                                jobslist.append(join(input_path, "membrane",emb,f)+";"+method)
                                #print(" --> job for  "+method + " filename "+join(input_path, "membrane",emb,times,f))
                            else:
                                ground_truth(method,join(input_path,"membrane",emb,f))

            if nb_total>0:
                print(str(round(10000 * (nb_total-todo) / nb_total) / 100) + "% (" + str(nb_total-todo) + "/" + str(nb_total) + ")" + " ------> " + method + " for " + emb)

    if not launch and len(jobslist)>0:
        launch_job_array("GROUND_TRUTH_"+mode+"_"+microscope+"_"+specie,jobslist, cmd=common_cmd, cpus_per_task=10,prepost=False,max_job=5000)

def ground_truth(method,membrane_filename):
    if isfile(membrane_filename):ground_truth_file(method,membrane_filename)
    elif isdir(membrane_filename):ground_truth_path(method,membrane_filename)
    else:
        print(f"--> unknown membrane file {membrane_filename} ")

def ground_truth_path(method,membrane_path): #From a path
    for f in listdir(membrane_path):
        if isfile(join(membrane_path,f)):
            ground_truth(method,join(membrane_path,f))
def ground_truth_file(method,membrane_filename):
    printi("compute ground truth for " + membrane_filename)
    seg_filename = get_gt_filename(membrane_filename, "segmented")
    output_filename = get_gt_filename(membrane_filename, method)
    if  not isfile(seg_filename):
        printw("miss " + seg_filename)
        printw("with membrane " + membrane_filename)
        #quit()
    else:
        if isfile(output_filename) :
           print(" --> already computed " + method + " at " + output_filename)
        else:
            print(" --> compute " + method + " at " + output_filename)
            mkdir(get_path(output_filename))
            out=None
            try:
                seg=imread(seg_filename)
                if seg is None: os.system(f"rm -f {seg_filename}") #REMOVE WRONG FILES...
                if method == "cell_counter":
                    out =cell_counter(seg)
                elif method == "semantic":
                    out = semantic(seg)
            except (ValueError,TiffFileError) as err:
                print(" \nFAILED :",err)
                printe("\nmembrane_filename= " + str(membrane_filename))
                printe("\nbackground_filename= " + str(get_gt_filename(membrane_filename,  "background_embryo")))
                printe("\nseg_filename= " + str(seg_filename))
                #quit()

            if out is not None:
                if type(out)==int:  file_write(output_filename, out) #Cell Counter
                else: imsave(output_filename, out)
            else:
                printe(" FAILED to compute ground truth ")
                #quit()


def exist_a_file_starting(filename):
    path=dirname(filename).replace("3D/","2D/")
    filename=basename(filename)
    p = filename.rfind("_")
    filename=filename[0:p]+"_o2_z"
    for f in listdir(path):
        if f.startswith(filename):
            return True
    return False

def extract_2D(txt_path,what=None): #CONVERT membrane and segmented 3D TO 2D IMAGES
    whats = ["train","test","valid"] if what is None or what == "" else [what]
    print(" -->  for " + str(whats) + ".txt")
    for what in whats:
        what_path_3D=join(txt_path + "_" + what + ".txt")
        what_path_2D = what_path_3D.replace("_3D", "_2D")

        print(f" -> convert 2D images from {what_path_3D} to {what_path_2D}")
        total = 0
        for line in open(what_path_3D, "r"): total += 1
        i = 0
        files=[]
        for line in open(what_path_3D, "r"):
            filename = line.strip()
            specie=get_specie_from_name(filename)
            #print(f" -> extract {specie} from {filename}")
            print(f"{i}/{total} -> convert {filename} ")
            if specie in ["CONF-Ovules"] and filename.find("N_449_ds2x")>=0:#not exist_a_file_starting(filename):
                seg_filename=get_correspond_filename(filename, "segmented")
                seg = imread(seg_filename)
                mem = imread(filename)
                nb_files=0
                if mem is not None and seg is not None:
                    for z_axis in range(3):
                        for z in range(0,seg.shape[z_axis]):
                            segz=None
                            if z_axis==0:
                                segz=seg[z,...]
                                memz=mem[z,...]
                            elif z_axis==1:
                                segz=seg[:,z,...]
                                memz=mem[:,z,...]
                            elif z_axis==2:
                                segz=seg[...,z]
                                memz=mem[...,z]

                            if segz is not None and len(np.unique(segz))>1: #ONLY WITH AT LEAST ONE SEGMENTED CELL
                                memb_name=get_2D_filename(filename,z_axis,z)
                                seg_name=get_2D_filename(seg_filename,z_axis,z)

                                mkdir(dirname(memb_name))
                                mkdir(dirname(seg_name))

                                #if not isfile(memb_name): imsave(memb_name,memz)
                                ff=['N_449_ds2x_o1_z430_M','N_449_ds2x_o1_z405_M','N_449_ds2x_o2_z419_M','N_449_ds2x_o2_z90_M','N_449_ds2x_o2_z234_M','N_449_ds2x_o1_z382_M','N_449_ds2x_o2_z40_M','N_449_ds2x_o2_z532_M','N_449_ds2x_o1_z518_M']
                                for f in ff:
                                    if memb_name.find(f)>=0:
                                        imsave(memb_name, memz)

                                if not isfile(seg_name):
                                    nb_files += 1
                                    #imsave(seg_name,segz)
                                files.append(memb_name)
                print(f" -->{nb_files} files created")
            else:
                memb_starting_name= filename.replace("3D/", "2D/")
                memb_starting_name=memb_starting_name[0:memb_starting_name.rfind("_")]
                #print(f"PATH {dirname(memb_starting_name)} start with {basename(memb_starting_name)}")
                for f in listdir(dirname(memb_starting_name)):
                    if f.startswith(basename(memb_starting_name)):
                        files.append(join(dirname(memb_starting_name),f))
            i+=1


        if isfile(what_path_2D):
            print(f" -> File already exist  {what_path_2D}")
        else:
            print(f" --> write {len(files)} files")
            mkdir(dirname(what_path_2D))
            fw=open(what_path_2D,"w")
            for f in files:
                fw.write(f+"\n")
            fw.close()


