from os import listdir
from os.path import isdir, join, isfile

import numpy as np
from tqdm import tqdm

from morphodeep.tools.image import get_junctions

#from ..config import RESULT

try :
    import matplotlib.pyplot as plt
except :
    a=1#print(" Matplotlib is not installed ...")

try :
    from tensorflow.python.summary.summary_iterator import summary_iterator
except :
    a=1#print(" Tensorflow is not installed ...")


colors={}
colors['train']=(0, 1, 0)
colors['validation']=(1, 0, 0)
def remove_axis(axs,h,w):
    if len(axs.shape) == 1:
        ax = axs[w]
    else:
        ax = axs[h, w]
    ax.axis('off')

def merge_mask_Z(image,nb_cut=6,border=15):
    z_step = int(round((image.shape[2]-2*border) / (nb_cut-1)))
    image_cut=np.zeros([image.shape[0],image.shape[1],3,nb_cut]).astype(np.uint8) #X, Y , RGB, CHANNELS
    im=np.zeros([image.shape[0],image.shape[1],3]).astype(np.uint8)  #Temporary
    for i in range(nb_cut):
        z=border+i*z_step
        if z>image.shape[2]:z=image.shape[2]
        #FOR IMAGE BETWEEN -1 and 1
        #memrane= (image[..., z, 1]+1)*128
        # FOR IMAGE BETWEEN 0 AND 1
        memrane = image[..., z, 1] * 255
        memrane[memrane>255]=255
        memrane[memrane<0]=0
        memrane=np.uint8(memrane)

        #red = np.uint16(image[..., z, 0] * 255) + np.uint16(memrane)
        #red[red > 255] = 255
        #im[..., 0] = np.uint8(red)
        red=np.copy(memrane)
        red[image[..., z, 0]>0.5]=255
        im[...,0]  = red
        im[...,1]  = memrane
        im[..., 2] = memrane
        image_cut[...,i] = im
    return image_cut


def add_image_to_dualmask(image,mask,nb_cut=6,border=15):
    print(" add_image_to_dualmask")
    print(image.shape)# (64, 64, 3)
    print(mask.shape) # (64, 64, 64, 2)
    z_step = int(round((image.shape[2]-2*border) / (nb_cut-1)))
    image_cut = np.zeros([image.shape[0], image.shape[1], 3, nb_cut]).astype(np.uint8)  #X, Y , RGB, CHANNELS
    im = np.zeros([image.shape[0], image.shape[1], 3]).astype(np.uint8)  # Temporary
    for i in range(nb_cut):
        z = border + i * z_step
        if z > image.shape[2]: z = image.shape[2]
        memrane = (image[..., z] + 1) * 128
        memrane[memrane > 255] = 255
        memrane = np.uint8(memrane)
        red = np.uint16(mask[..., z, 0] * 255) + np.uint16(memrane)
        red[red > 255] = 255
        green = np.uint16(mask[..., z, 1] * 255) + np.uint16(memrane)
        green[green > 255] = 255

        im[..., 0] = np.uint8(red)
        im[..., 1] = np.uint8(green)
        im[..., 2] = memrane
        image_cut[..., i] = im
    return image_cut


def imshow(axs,h,w,image,name,cmap="viridis",interpolation='antialiased',vmin=None,vmax=None):
    '''ma=image.max()
    mi=image.min()
    if mi>=0 and ma<=10: # 0 and 1
        cmap="viridis"
    elif ma>100:
        cmap="gray"
    print(" --> "+name+ "->"+cmap+ " "+str(ma)+ " "+str(mi))'''
    if interpolation is None:
        interpolation="None"
    '''if shape==1: #Just one image for each
        axs[w].imshow(image[:, :, 0], cmap=cmap,interpolation=interpolation)
        axs[w].set_title(name)
        axs[w].axis('off')
    else: #Multiples Inputs and/or Outputs
        for h in range(image.shape[2]):
            axs[h,w].imshow(image[:,:,h],cmap=cmap,interpolation=interpolation)
        axs[0,w].set_title(name)
        for h in range(shape):
            axs[h, w].axis('off')
    '''
    if len(axs.shape)==1:
        ax=axs[w]
    else:
        ax = axs[h,w]
    if image is not None:
        if type(image) is np.ndarray :

            if len(image.shape)==3: # (X,Y,MULTIPLE CHANNEL)
                if image.shape[2] ==   2:  image=np.concatenate((image[:, :, 0], image[:, :, 1]))
                elif image.shape[2] == 3:  image = np.concatenate((np.concatenate((image[:, :, 0], image[:, :, 1])), np.concatenate((image[:, :, 2], np.zeros_like(image[:, :, 2])))),axis=1)
                elif image.shape[2] == 4:  image = np.concatenate((np.concatenate((image[:, :, 0], image[:, :, 1])), np.concatenate((image[:, :, 2], image[:, :, 3]))),axis=1)
                elif image.shape[2] == 5:
                    image = np.concatenate((np.concatenate((image[:, :, 0], image[:, :, 1])),
                                           np.concatenate((image[:, :, 2], image[:, :, 3])),
                                            np.concatenate((image[:, :, 4], np.zeros_like(image[:, :, 2])))),axis=1)
                elif image.shape[2] == 6:
                    image = np.concatenate((np.concatenate((image[:, :, 0], image[:, :, 1])),
                                           np.concatenate((image[:, :, 2], image[:, :, 3])),
                                            np.concatenate((image[:, :, 4],  image[:, :, 5]))),axis=1)
            if len(image.shape)==4: # (X,Y,RGB, CHANNEL)
                if image.shape[3] ==   2:  image=np.concatenate((image[..., 0], image[..., 1]))
                elif image.shape[3] == 3:
                    image = np.concatenate((np.concatenate((image[..., 0], image[..., 1])),
                                            np.concatenate((image[..., 2], np.zeros_like(image[..., 2])))), axis=1)
                elif image.shape[3] == 4:
                    image = np.concatenate((np.concatenate((image[..., 0], image[..., 1])),
                                            np.concatenate((image[..., 2], image[..., 3]))), axis=1)
                elif image.shape[3] == 5:
                    image = np.concatenate((np.concatenate((image[..., 0], image[..., 1])),
                                            np.concatenate((image[..., 2], image[..., 3])),
                                            np.concatenate((image[..., 4], np.zeros_like(image[..., 2])))), axis=1)
                elif image.shape[3] == 6:
                    image = np.concatenate((np.concatenate((image[..., 0], image[..., 1])),
                                        np.concatenate((image[..., 2], image[..., 3])),
                                        np.concatenate((image[..., 4], image[..., 5]))), axis=1)
            if cmap=="junctions":
                ax.imshow(image, cmap=get_junctions(), interpolation=None,vmin=0,vmax=4)
            else:
                if vmin is not None and vmax is not None:
                    ax.imshow(image, cmap=cmap, interpolation=interpolation,vmin=0,vmax=4)
                else:
                    ax.imshow(image, cmap=cmap, interpolation=interpolation)
        else: #TXT
            ax.text(0.5, 0.5, str(image),  fontsize=40, horizontalalignment='center',  verticalalignment='center',   transform=ax.transAxes)
    ax.set_title(name)
    ax.axis('off')


def histo_iou(ax,name,ious,nb_bins=30,with_bar=True,line=False):
    if line:
        bins = np.histogram(ious, nb_bins, range=(0, 2 + 2.0 / nb_bins))
        y_bins = np.zeros(bins[0].shape)
        for y in range(y_bins.shape[0]): y_bins[y] = (bins[1][y] + bins[1][y + 1]) / 2.0
        ax.plot(y_bins, bins[0], '-b')
    else:
        bins = ax.hist(ious, bins=nb_bins, range=(0, 2 + 2.0 / nb_bins))
    if with_bar:
        ax.plot([1, 1], [0, bins[0].max()], "-r")  # Vertical Bar to separare element
        ax.text(1.5, bins[0].max() / 2, 'under')
        ax.text(0.3 , bins[0].max() / 2, 'over')
    ax.set_title(name)
    return bins


def plot3D(axs,h,w,coords,name):
    if len(axs.shape)==1:
        ax=axs[w]
    else:
        ax = axs[h,w]
    if coords is not None:
        ax.plot3D(coords[0], coords[1], coords[2])
    ax.set_title(name)

def get_tb(event_dir):
    #print(" Proicess "+event_dir)
    to_plots = {}
    for event in summary_iterator(event_dir):
        for value in event.summary.value:
            if value.tag.find("loss")>=0 or value.tag.find("acc")>=0:
                value.tag=value.tag.replace("_nonuclei","") #Just name changemnt
                if value.tag not in to_plots:
                    to_plots[value.tag]={}
                try:
                    v=np.frombuffer(value.tensor.tensor_content, dtype=np.float32) #When I write it with tf.summary.scalar
                    v=v[0]
                except:
                    v = value.simple_value #Write with  callback tensrofboard
                #print(" " + str(value.tag) + " at " + str.(event.step) + " -> " + str(v))
                to_plots[value.tag][event.step]=v
    return to_plots

def get_smooth(all_plots,smoothing):
    # Smoothing ....
    if smoothing is None or smoothing<=0:
        return None
    smooth_plots = {}
    for step in tqdm(all_plots):
        smooth_plots[step] = {}
        for measure in all_plots[step]:
            smooth_plots[step][measure] = {}
            l = len(all_plots[step][measure]) * smoothing
            for x in sorted(all_plots[step][measure]):
                Y = []
                for xx in sorted(all_plots[step][measure]):
                    if xx >= x - l and xx <= x + l:
                        Y.append(all_plots[step][measure][xx])
                smooth_plots[step][measure][x] = np.array(Y).mean()
    return smooth_plots


def plot_compare(models,name,limit=None,smoothing=0.1): #Limit =[ [x_left,x_right],[y_bottom,y_top] , [x_left,x_right],[y_bottom,y_top] ]
    global compare
    print(" --> plot compare "+name)
    nb_fig=0 #Correspond to the numberf of loss / accuracry measuremnt to compare
    for model in models:
        all_plots=get_smooth(model.all_plots,smoothing)
        for step in all_plots:
            fig_Y = 0
            for measure in all_plots[step]:
                fig_Y += 1
            nb_fig=max(nb_fig,fig_Y)
    print(" --> found "+str(nb_fig)+ " figures to plot")
    fig, axs = plt.subplots(1, nb_fig, figsize=(5 * nb_fig, 7))
    fig.suptitle(name)
    for model in models:
        all_plots=get_smooth(model.all_plots,smoothing)
        for step in all_plots:
            fig_Y = 0
            for measure in all_plots[step]:
                X = []
                Y = []
                for x in sorted(all_plots[step][measure]):
                    X.append(x)
                    Y.append(all_plots[step][measure][x])
                axs[fig_Y].plot(X, Y, label=step + " " + model.jobname)
                axs[fig_Y].legend()
                axs[fig_Y].set_title(measure.replace('epoch_', ''))
                if limit is not None and  limit[fig_Y] is not None:
                    if limit[fig_Y][0] is not None:
                        axs[fig_Y].set_xlim(left=limit[fig_Y][0][0],right=limit[fig_Y][0][1])
                    if limit[fig_Y][1] is not None:
                        axs[fig_Y].set_ylim(bottom=limit[fig_Y][1][0],top=limit[fig_Y][1][1])
                fig_Y += 1
    plt.savefig(join(RESULT,"compare_"+name+".png"))
    plt.close(fig)