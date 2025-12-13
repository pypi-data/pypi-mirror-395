# -*- coding: latin-1 -*-
from os import listdir

import numpy as np
from skimage.morphology import binary_dilation
from skimage.transform import resize
from skimage.util import random_noise

from .image import imread, imsave, normalize, poisson_noise, gaussian_bluring, downsampling
from .utils import get_correspond_filename, read_paths, mkdir, get_time, get_basename, get_z, read_number
from os.path import isfile, basename, dirname, join
import random

from ..paths import TEMP, SCRATCH

try:
    import tensorflow as tf
except:
    pass

augmentations = [None, 'rotate-1', 'rotate-2', 'rotate-3', 'flip-1', 'flip-2', 'flip-3', 'flipate-1-1', 'flipate-1-2',
                 'flipate-1-3', 'flipate-2-1', 'flipate-2-2', 'flipate-2-3', 'flipate-3-1', 'flipate-3-2',
                 'flipate-3-3']


############### #DATA AUGMENTATION
def flip_3D(x,f=None):
    if f is None:
        f=random.randint(0,2) #0 nothing, 1, flip up and down; 1, flip left and right, 2 flip z
    if f==0:
        return x
    f=f%3 #To avoid errors ...
    #print(f"flip_3D {f}\n")
    x=x.swapaxes(f, 0)
    return x

def rotate_3D(x,f=None):
    if f is None:
        f = random.randint(0, 3)  # 0, x-axis; 1, y-axis, 2 z-axis , 3 : nothing
    axes=None
    if f == 0:
        return x
    elif f==1:
        axes=(0, 2)
    elif f==2:
        axes=(0, 1)
    elif f==3:
        axes=(1, 2)
    if axes is None:
        return x
    return np.rot90(x,axes=axes)

def flip_2D(x,f=None):
    """Flip augmentation

    Args:
        x: Image to flip

    Returns:
        Augmented image
    """
    if len(x.shape) == 2: x = np.reshape(x, [x.shape[0], x.shape[1], 1])
    if f is None:
        f = random.randint(0, 2)
    if f == 0: #NOTHING
        return x
    elif f == 1:
        x = tf.image.flip_left_right(x)
    elif f==2:
        x = tf.image.flip_up_down(x)
    elif f==3:
        x = tf.image.flip_left_right(x)
        x = tf.image.flip_up_down(x)
    if len(x.shape) >2: x=x[...,0]
    return x.numpy()

def rotate_2D(x,f=None):
    """Rotation augmentation

    Args:
        x: Image

    Returns:
        Augmented image
    """
    if f is None:
        f = random.randint(0, 3)
    if len(x.shape) == 2: x = np.reshape(x, [x.shape[0], x.shape[1], 1])
    x=tf.image.rot90(x,k=f) # rotating `a` counter clockwise by 90 degrees
    if len(x.shape) > 2: x = x[..., 0]
    return x.numpy()

def augmented(image,action):

    if action == None:
        return image
    method=action.split("-")[0]
    f=int(action.split("-")[1])
    #print(f"AUGMENTED IMAGE WITH method={method} and f={f}  for shape={image.shape}\n")
    if len(image.shape)==3:  # 3D
        if method=="flip":
            image=flip_3D(image,f=f)
        elif method=="rotate":
            image=rotate_3D(image,f=f)
        elif method== "flipate":
            image = flip_3D(image, f=f)
            image = rotate_3D(image, f=int(action.split("-")[2]))
    else: #2D
        if method == "flip":
            image = flip_2D(image, f=f)
        elif method == "rotate":
            image = rotate_2D(image, f=f)
        if method == "flipate":
            image = flip_2D(image, f=f)
            image = rotate_2D(image, f=int(action.split("-")[2]))
    return image



class MorphoExamples():
    def __init__(self, path_name,mode,img_size,input_shape,output_shape,augmentation,reverse=False,shuffle=False):
        self.paths= read_paths(path_name,shuffle=shuffle,reverse=reverse)
        if shuffle: random.shuffle(self.paths)
        self.mode = mode
        self.dim = 2 if mode == "2D" else 3
        self.img_size = img_size
        self.input_shape = input_shape  # NETWORK INPUT SHAPE
        self.output_shape = output_shape  # NETWORK INPUT SHAPE
        self.augmentation = augmentation
        self.idx=0
        # In case of muyltiple data per batch
        self.batch_input,self.batch_output =[],[]


    def get_batch(self):
        #print(f" --> extract one batch on {len(self.batch_input)} size")
        batch = []
        if len(self.batch_input)>0  and len(self.batch_output) >0:
            data_input=np.expand_dims(self.batch_input[0], -1)
            data_output=np.expand_dims(self.batch_output[0], -1)
            # SPLIT OUTPUT IN MULTIPLES CLASSES
            if self.dim == 2:
                data_output = np.concatenate((data_output == 0, data_output == 1, data_output == 2, data_output >= 3), axis=-1)  # 512x512x4
            else:
                data_output = np.concatenate(
                    (data_output == 0, data_output == 1, data_output == 2, data_output == 3, data_output == 4),
                    axis=-1)  # 512x512x5

            batch = [np.float32(data_input),np.float32(data_output) ]
            self.batch_input.pop()
            self.batch_output.pop()

        return batch


    def get_next(self,what_else=None,batch_size=8,only_this=None):
        if len(self.paths)==0: #NO AVAIABLE DATA
            return None,None
        if only_this is not None:
            while self.paths[self.idx].find(only_this)==-1: self.idx +=1 #To focus only on a psecific dataset
        batch=self.get_batch()
        if len(batch)>0: return batch

        #print(f" Construct a new images batch {batch_size} for {self.paths[self.idx]}")

        me = MorphoExample(self.paths[self.idx], self.mode,  self.img_size,self.input_shape, self.output_shape, self.augmentation)
        self.idx = 0 if self.idx >= len(self.paths) - 1 else self.idx + 1
        example=me.prepare_data(what_else=what_else, batch_size=batch_size,verbose=False)
        if example is None:
            return self.get_next(what_else=what_else,batch_size=batch_size,only_this=only_this) #New Retrieve
        if what_else is not None:
            self.batch_input=example['input']
            self.batch_output = example['output']
            batch=self.get_batch()
            example['input']=batch[0]
            example['output'] = batch[1]
            self.batch_input=[]
            self.batch_output=[]
            return example  # For export and testing
        self.batch_input, self.batch_output=example
        return self.get_batch()



class MorphoExample():
    def __init__(self,img_path,mode,img_size,input_shape,output_shape,augmentation):
        self.img_path=img_path.replace("/gpfsscratch/rech/","/lustre/fsn1/projects/rech/") #CHGNT DE NOM DE SCRATCH
        #print("-->"+self.img_path)
        self.mode=mode
        self.dim=2 if mode=="2D" else 3
        self.img_size=img_size
        self.input_shape=input_shape #NETWORK INPUT SHAPE
        self.output_shape = output_shape #NETWORK INPUT SHAPE
        self.augmentation=augmentation
        #else:  print("No augmentation\n")

    def get_patches(self,data_input,data_output):
        # Patches Mode
        x = random.randint(0, data_input.shape[0] - self.input_shape[0])
        y = random.randint(0, data_input.shape[1] - self.input_shape[1])
        if self.dim == 2:
            coords = [x, y]
            data_input = data_input[x:x + self.input_shape[0], y:y + self.input_shape[1]]
            data_output = data_output[x:x + self.input_shape[0], y:y + self.input_shape[1]]
        else:
            z = random.randint(0, data_input.shape[2] - self.input_shape[2])
            coords = [x, y, z]
            data_input = data_input[x:x + self.input_shape[0], y:y + self.input_shape[1], z:z + self.input_shape[2]]
            data_output = data_output[x:x + self.input_shape[0], y:y + self.input_shape[1],  z:z + self.input_shape[2]]
        return data_input,data_output,coords

    def dilate_semantic(self,data,new_shape):#dilate (before reduce size) only junctions of face,line etc..
        axis_ratio = np.array(data.shape) / np.array(new_shape)
        footprint = np.ones(np.uint8(np.floor(axis_ratio) + 1))
        junctions = np.copy(data)
        for j in range(2, 5):
            junctions[binary_dilation(data == j, footprint=footprint)] = j
        return junctions


    def resize(self,data,filename,new_shape,order=None,dilate_junctions=False):
        temp_path = dirname(filename).replace("/Semantic/","/TEMP_Resize_Semantic/") #IN SCRARTCH
        mkdir(temp_path)
        exf = str(new_shape[0]) + "_" + str(new_shape[1])
        if self.mode == "3D": exf += "_" + str(new_shape[2])

        temp_file =join(temp_path , exf + "_" + basename(filename))
        if isfile(temp_file):
            data = imread(temp_file)
            #print(f" RESIZE DATA SHAPE {data.shape}")
        else:
            if dilate_junctions: data=self.dilate_semantic(data,new_shape)
            data = resize(data, new_shape[0:self.dim] , preserve_range=True,order=order).astype(data.dtype)
            #print(f" save reshape data {temp_file}")
            imsave(temp_file, data)
        return data


    def get(self,gt,new_shape=None,coords=None): #GT is Ground Truth
        #print(" --> look for "+str(gt) + " for "+self.img_path)
        if gt=="cell_counter" or  gt == "age" : #File Test
            filename2D = get_correspond_filename(self.img_path, "cell_counter")
            #print(" --> "+filename2D)
            if not isfile(filename2D):
                print(" --> Miss filename "+filename2D)
                return None

        if gt == "t": return get_time(self.img_path)
        if gt == "name" : return get_basename(self.img_path)
        if self.mode == "2D":
            if gt == "z" : return  get_z(self.img_path)
            if gt == "age" :
                filename2D = get_correspond_filename(self.img_path, "cell_counter")
                filename3D = filename2D.replace("2D", "3D")
                filename3D = filename3D[:filename3D.find("_z")] + ".txt"  # /gpfsscratch/rech/dhp/uhb36wd/DATABASE/SegmentedMembrane/crop_512_3D/SPIM-Phallusia-Mammillata/200825-Louise/200825-Louise_fuse_t030/cell_counter/200825-Louise_fuse_t030_CC.txt
                if not isfile(filename3D):
                    #print(" --> Use the 2D Age, Miss filename 3D "+filename3D)
                    return read_number(filename2D)
                return read_number(filename3D)
            if gt == "cell_counter": return read_number(get_correspond_filename(self.img_path, gt))

        elif self.mode == "3D":
            if gt == "age" or gt== "cell_counter":
                return read_number(get_correspond_filename(self.img_path, "cell_counter"))

        return self.get_image(gt=gt,new_shape=new_shape,coords=coords)

    def get_image(self,gt="membrane",filename=None,new_shape=None,coords=None):
        #print(f"Get_image for {gt}")
        if filename is None:
            filename=get_correspond_filename(self.img_path,gt)
        #print(f"Read filename {filename}")
        if not isfile(filename):
            print(f" --> MISS image filename for {gt} -> {filename} ")
            return None

        image = imread(filename)
        if image is None :
            print(f" --> ERROR Readning image filename for {gt} -> {filename}")
            return None

        if image.shape==(0,):
            print(f" --> this file is corruped for {gt} -> {filename} ")
            return None

        if new_shape is not None:
            image = self.resize(image,filename,new_shape, order=0)

        if coords is not None:
            if self.dim==3:
                [x, y, z]=coords
                image = image[x:x + self.input_shape[0], y:y + self.input_shape[1], z:z + self.input_shape[2]]
            else :
                [x, y]=coords
                image = image[x:x + self.input_shape[0], y:y + self.input_shape[1]]


        #print(f"Image size is {image.shape}")
        #print(f" ACTION IS {self.action}")
        '''if self.action is not None:
            print(f" AUGEMENT {gt}")
            image = augmented(image,self.action)
        '''
        #print(f"Augmented Image size is {image.shape}")
        return image

    def prepare_data(self,what_else=None,batch_size=1, verbose=False    ):
        if verbose: print(f" --> prepare {batch_size} data ")
        batch_input=[]
        batch_output =[]

        coords = None
        new_shape=None
        filename=self.img_path

        membrane_filename= get_correspond_filename(self.img_path, "membrane")
        semantic_filename = get_correspond_filename(self.img_path, "semantic")
        if verbose: print(f"Look for membrane_filename={membrane_filename} and semantic_filename={semantic_filename} ")
        if isfile(membrane_filename) and isfile(semantic_filename):
            #READ IMAGES
            try:
                data_input=imread(membrane_filename)
                data_output=imread(semantic_filename)
                if data_input is not None and data_output is not None:
                    new_shape=None
                    #PREPARE PATCHES MODE
                    if (np.array(data_input.shape) < np.array(self.input_shape[0:self.dim])).any():  # SMALL IMAGES (of One of the axes
                        ratio = np.uint8(np.floor(np.max(np.array(self.input_shape[0:self.dim]) / np.array(data_input.shape))) + 1)
                        if verbose: print(f" Small Images with ratio {ratio}\n")
                        new_shape =list(np.array(data_input.shape[0:self.dim])*ratio)
                        patches_input = self.resize(data_input, membrane_filename, new_shape)
                        patches_output = self.resize(data_output, semantic_filename, new_shape,  order=0)
                    else:
                        patches_input=data_input
                        patches_output=data_output


                    #PREPARE NORMAL MODE
                    full_input = self.resize(data_input, membrane_filename,  self.input_shape[0:self.dim])
                    full_output = self.resize(data_output, semantic_filename, (self.output_shape[0:self.dim]), order=0,  dilate_junctions=data_input.shape > self.input_shape)

                    nb_attempt=0
                    while len(batch_input)<batch_size and nb_attempt<10*batch_size:
                        if random.random() > 0.2:  # 80% PATCHES MODE
                            if verbose: print(f" Batch {nb_attempt} Patches Mode")
                            data_input, data_output, coords = self.get_patches(patches_input, patches_output)
                        else: #FULL SIZE MODE
                            if verbose: print(f" Batch {nb_attempt} Normale Mode")
                            data_input=full_input
                            data_output=full_output
                            new_shape=full_input.shape

                        if what_else is None and self.augmentation: #No data augmentation for test prediction
                            action = augmentations[random.randint(0, len(augmentations) - 1)]
                            if action is not None and self.mode=="3D":
                                if verbose: print(f" Batch {nb_attempt} Auigmentation with {action} ")
                                data_input = augmented(data_input, action)
                                data_output = augmented(data_output, action)

                            if random.random() > 0.2:  #80% ADD NOISE TO INPUT DATA
                                noise_type = ['poisson', 'downsampling', 'gaussian']
                                try:
                                    noise=noise_type[random.randint(0,len(noise_type)-1)]
                                    if verbose: print(f" Batch {nb_attempt} Raw Auigmentation with {noise} ")
                                    if noise=='poisson': data_input=poisson_noise(data_input)
                                    elif noise=='gaussian': data_input=gaussian_bluring(data_input)
                                    elif noise == 'downsampling': data_input = downsampling(data_input)
                                except:
                                    a=1 #We do not perform the data augmentation

                        # Normalisation
                        data_input = normalize(data_input)

                        #print(f"{i} example input {np.unique(normalize(data_input))}")
                        #print(f"{i} example output {np.unique(data_output)}")
                        if verbose:
                            print(f"{nb_attempt} example input {np.unique(data_input)}")
                            #imsave(join(SCRATCH,"PATCHES",f"data_input{nb_attempt}.tiff"),data_input)
                            print(f"{nb_attempt} example output {np.unique(data_output)}")
                            #imsave(join(SCRATCH, "PATCHES", f"data_output{nb_attempt}.tiff"), data_output)
                            #if len(np.unique(data_input))<10:  quit()
                            print(f" new shape={new_shape}")

                        if data_input.max()<3: #To Avoid Error in Normalisation process
                            batch_input.append(data_input)
                            batch_output.append(data_output)

                        nb_attempt+=1

            except Exception as e:
                print(" Error reading data")
                print(e)
                #quit()


        if what_else is not None: #For export and testing
            if len(batch_input)==0 or len(batch_output)==0: return None
            example= {}
            example["input"] = batch_input
            example["output"] =  batch_output
            for f in what_else:
                if f=="filename": example[f]=filename
                else: example[f]=self.get(f,new_shape=new_shape,coords=coords)
            return example
        if len(batch_input)==0: return None
        return batch_input, batch_output

