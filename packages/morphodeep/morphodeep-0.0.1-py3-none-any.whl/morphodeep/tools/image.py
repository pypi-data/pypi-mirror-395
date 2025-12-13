# -*- coding: latin-1 -*-

import os, time
import random
from math import floor
from os.path import join, isfile
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.transform import resize
from skimage.util import random_noise

from morphodeep.tools.utils import printe, mkdir, get_path, bbox_overlap
from threading import Thread
from math import isnan



def normalize(x, pmin=3, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32,remove_zeros=False):
    """Percentile-based intensity normalization.

        Intensities are linearly rescaled such that the ``pmin`` and
        ``pmax`` percentiles map approximately to 0 and 1.

        Parameters
        ----------
        x : numpy.ndarray
            Input image.
        pmin, pmax : float
            Lower and upper percentiles used to estimate the intensity
            range.
        axis : int or tuple of int, optional
            Axis along which to compute the percentiles.
        clip : bool, optional
            Whether to clip the normalized values into [0, 1].
        eps : float, optional
            Small constant to avoid division by zero.
        dtype : type, optional
            Desired output dtype.

        Returns
        -------
        numpy.ndarray
            Normalized image.
    """
    if x is None: return None
    if remove_zeros:
        y=x[x!=0]
        mi = np.percentile(y,pmin,axis=axis,keepdims=True)
        ma = np.percentile(y,pmax,axis=axis,keepdims=True)
    else:
        mi = np.percentile(x,pmin,axis=axis,keepdims=True)
        ma = np.percentile(x,pmax,axis=axis,keepdims=True)

    return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)

def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
    """Normalize an image given explicit min and max values.

            Parameters
            ----------
            x : numpy.ndarray
                Input image.
            mi, ma : float or numpy.ndarray
                Minimum and maximum intensity values used for rescaling.
            clip : bool, optional
                Whether to clip the result into [0, 1].
            eps : float, optional
                Small constant to avoid division by zero.
            dtype : type, optional
                Desired output dtype.

            Returns
            -------
            numpy.ndarray
                Normalized image.
    """

    if dtype is not None:
        x   = x.astype(dtype,copy=False)
        mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
        ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
        eps = dtype(eps)

    try:
        import numexpr
        x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
    except ImportError:
        x =                   (x - mi) / ( ma - mi + eps )

    if clip:
        x = np.clip(x,0,1)

    return x

#DATA AUGMENTATION
def gaussian_bluring(data_input):
    return gaussian_filter(data_input,random.randint(1,2))

def downsampling(data_input):
    v=random.randint(2,4)
    if len(data_input.shape)==2:
        return resize(data_input[::v,::v],data_input.shape)
    return resize(data_input[::v, ::v, ::v], data_input.shape)

def poisson_noise(data_input):
    return random_noise(np.uint8(np.round(np.float32(data_input)*255/data_input.max())),mode="poisson",clip=True)

def imsave_nii(filename, data, header=None, voxelsize=[1, 1, 1]):
    import nibabel as nib
    if header is None:
        header = nib.Nifti1Header()
        header.set_xyzt_units(3 or 8)  # 3 correspond to micrometers | 8 for seconds
        dtype = data.dtype
        if dtype == np.float16:  # NOT SUPPORTED
            dtype = np.float32
        header.set_data_dtype(dtype)
        if len(data.shape)==2:
            header['dim'] = [4, np.shape(data)[0], np.shape(data)[1], 0, 1, 0, 0, 0]
            header['pixdim'] = [1, voxelsize[0], voxelsize[1], 1, 128, 0, 0, 0]
        elif len(data.shape)==3:
            header['dim'] = [4, np.shape(data)[0], np.shape(data)[1], np.shape(data)[2], 1, 0, 0, 0]
            header['pixdim'] = [1, voxelsize[0], voxelsize[1], voxelsize[2], 128, 0, 0, 0]
    img = nib.nifti1.Nifti1Image(data, None, header=header)
    nib.save(img, filename)


def imsave_h5(filename,data):
    import h5py
    hf = h5py.File(filename, 'w')
    hf.create_dataset('Data', data=data)
    hf.close()


def imsave(filename, data, header=None,thread=False):
    if data is None:
        return None
    filename = filename.strip()
    tozip=False
    if filename.endswith(".gz"):
        filename=filename.replace(".gz","")
        tozip=True
    if thread:
        it=imsave_thread(filename,data,header=header)
        it.run()
    else:
        # print(" Save "+filename)
        mkdir(get_path(filename))
        if filename.find("nii") > 0:
            return imsave_nii(filename, data, header=header)
        if filename.find("h5") > 0:
            return imsave_h5(filename, data)
        from skimage.io import imsave as imsave_sk
        try:
            imsave_sk(filename, data, check_contrast=False)
        except:
            imsave_sk(filename, data)
    if tozip:
        if isfile(filename+".gz"): os.system('rm -f '+filename+".gz")
        os.system('cd '+os.path.dirname(filename)+"; gzip "+os.path.basename(filename)+ " &")


class imsave_thread(Thread):
    # Just perform the saving in thread
    def __init__(self, filename, data, header=None):
        Thread.__init__(self)
        self.filename = filename
        self.data = data
        self.header = header

    def run(self):  # START FUNCTION
        imsave(self.filename, self.data, header=self.header,thread=False)


def imread_nii(filename):
    import nibabel as nib
    img = nib.load(filename)
    return np.array(img.dataobj, dtype=np.dtype(str(img.get_data_dtype())))

def imread(filename):
    from skimage.io import imread as imread_sk
    #print(" Read "+filename)
    filename=filename.strip()
    if not isfile(filename):
        printe("Miss "+filename)
        return None
    try:
        if filename.find("nii") > 0:
            return imread_nii(filename)
        if filename.find("inr") > 0:
            from morphonet.ImageHandling import imread as imreadINR
            data, vsize = imreadINR(filename)
            return data
        if filename.find("mha") > 0:
            import itk
            image=itk.imread(filename)
            nparray=itk.GetArrayFromImage(image)
            if len(nparray.shape)==3:
                return np.swapaxes(nparray,0,2) #REVERSE Z and X
            return nparray
        if filename.find("h5") > 0:
            import h5py
            with h5py.File(filename, "r") as f:
                return np.array(f["Data"])

        temp_path = None
        if filename.endswith("gz"):
            temp_path = "TEMP" + str(time.time())
            while os.path.isdir(temp_path):  # JUST IN CASE OF TWISE THE SAME
                temp_path = "TEMP" + str(time.time())
            os.system("mkdir -p " + temp_path)
            os.system("cp " + filename + " " + temp_path)
            filename = join(temp_path, os.path.basename(filename))
            os.system("gunzip " + filename)
            filename = filename.replace('.gz', '')

        im = imread_sk(filename)
        if temp_path is not None:
            os.system("rm -rf " + temp_path)
        return im
    except Exception as e:
        printe(" Reading "+filename)
        printe(e)
        #quit()
        return None



def is_low_contrast(img,low_contrast=None):
    if low_contrast is None:
        from skimage.exposure import is_low_contrast as ilc
        return ilc(img)
    return img.mean()<low_contrast

def get_number_of_cell(cell_counter_model, img):  # Warning this model work in 512 x 512
    '''
    Compute the number of cells using CellCounter
    img is a 2D 8bit raw data Images
    CellCounter works only with image size =512
    TODO : Update img to predict batch_size larger than 1...
    '''
    from skimage.transform import resize
    img_size = 512
    if img.shape[0] != img_size or img.shape[1] != img_size:
        img = resize(img, [img_size, img_size], preserve_range=True, order=0)
    input = np.zeros([1, img_size, img_size, 1])
    input[0, :, :, 0] = 2.0 * img / 255.0 - 1.0  # Normalize as it is in CellCounter
    nb = cell_counter_model.predict(input)
    return round(nb[0][0])

def get_barycenters(segmented,background_threshold=0, min_pixel=0):
    cells = np.unique(segmented)
    barys = {}
    for c in cells:
        if c > background_threshold:
            coords = np.where(segmented == c)
            if len(coords[0]) > min_pixel:
                if len(segmented.shape) == 3:
                    barys[c] = [coords[0].mean(), coords[1].mean(), coords[2].mean()]
                else:
                    barys[c] = [coords[0].mean(), coords[1].mean()]
    return barys


def segmentation_accuracy(gt, seg, background_threshold):
    if gt is None or seg is None or  len(np.unique(gt)) == 1:  return None
    PG, PB = compare_segmentation(gt, seg, background_threshold=background_threshold)
    return  PB / (PG + PB)


def compare_segmentation(gt,pd,background_threshold=0):
    from skimage.transform import resize
    if gt.shape[0]<pd.shape[0]:
        pd=resize(pd,gt.shape, preserve_range=True, anti_aliasing=False, order=0).astype(pd.dtype)
    elif gt.shape[0]>pd.shape[0]:
        gt=resize(gt,pd.shape, preserve_range=True, anti_aliasing=False, order=0).astype(gt.dtype)

    mask=gt!=background_threshold
    diff=gt-pd
    cells=diff[mask]
    if len(cells)==0:
        return 1,0
    Good=len(np.where(cells==0)[0])
    Bad=len(cells)-Good

    '''cells = np.unique(gt)
    TP=0 # True Positif
    TN=0 # True Negatif
    FP=0 # False Positif
    FN=0 # False Negatif
    Good=0
    Bad=0
    for c in cells:
        if c > background_threshold:
            gt_mask = np.uint8(gt==c)
            pd_mask = np.uint8(pd==c)
            segment_result = pd_mask + gt_mask * 2
            TP += len(np.where(segment_result == 3)[0]) #Cell well Segmented
            TN += len(np.where(segment_result == 0)[0])
            FP += len(np.where(segment_result == 1)[0]) #Extend Cell
            FN += len(np.where(segment_result == 2)[0]) #Missing Cell

            Good += len(np.where(segment_result == 3)[0])
            Bad +=len(np.where(segment_result == 1)[0])

    #return TP,TN,FP,FN
    '''
    return Good,Bad





def get_bbox(regions,label):
    for region in regions:
        if region['label']==label:
            return region["bbox"]
    return None







def mess(M,T,S):
    return M+":" + str(round(100.0 * T / S,2))+"%"

def stat(G,B):
    if G is None:
        return ""
    return " "+mess("Good",G,G+B)+", "+mess("Bad",B,G+B)

def percentage(v):
    return  str(round(100.0 * v)) + " %"


def get_markers(mode,segmented,background_threshold=0, min_pixel=0,ratio=1):
    #if segmented.shape[-1]==1:
    #    segmented=np.reshape(segmented,segmented.shape[0:-1])
    shape=segmented.shape
    cells = np.unique(segmented)
    if ratio!=1:
        nshape=[]
        for c in shape:
            v = c if c<=3 else int(round(c/ratio))
            nshape.append(v)
        shape=nshape
    markers=np.zeros(shape).astype(np.uint16)
    for c in cells:
        if c > background_threshold:
            coords = np.where(segmented == c)
            if len(coords[0]) > min_pixel:
                coord=[]
                for s in range(len(coords)): #Shape
                    coord.append(floor(coords[s].mean()/ratio))
                if mode=="2D":
                    markers[coord[0], coord[1]] = c
                else:
                    markers[coord[0],coord[1],coord[2]]=c
    return markers


def get_markers_from_local_minima(mode,img):
    from skimage.morphology import local_minima
    from skimage.measure import label
    lm = local_minima(img)
    labels = label(lm)
    return get_markers(mode, labels)

def find_two_seeds(mask,factor_reduce=1):
    from scipy.spatial.distance import cdist
    coords = np.where(mask) # Take the 2 farest points
    # print(len(coords[0]))
    vT = np.zeros([len(coords[0]), len(coords)])
    for s in range(len(coords)):
        vT[:, s] = coords[s]
    dist = cdist(vT, vT)
    maxi = dist.max()
    coords_maxi = np.where(dist == maxi)
    del dist
    if len(coords_maxi[0]) >= 2:
        ipt1 = coords_maxi[0][0]
        ipt2 = coords_maxi[0][1]
        if len(coords) == 3:
            pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])
            pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])
        elif len(coords) == 2:
            pt1 = np.array([coords[0][ipt1], coords[1][ipt1]])
            pt2 = np.array([coords[0][ipt2], coords[1][ipt2]])
        v = pt2 - pt1
        # print(v)
        seed1 = factor_reduce * np.int32(pt1 + v * 1.0 / 3.0)
        seed2 = factor_reduce * np.int32(pt1 + v * 2.0 / 3.0)
        return [seed1,seed2]
    return None


def get_glasbey(maxv):
    import matplotlib.pyplot as plt
    # Generate CMAP
    vals = np.linspace(0, 1, maxv + 1)
    np.random.shuffle(vals)
    cols = plt.cm.jet(vals)
    cols[0, :] = 0  # BACLGROUND
    cols[0, 3] = 1
    return  plt.cm.colors.ListedColormap(cols)

def get_junctions():
    import matplotlib as mpl
    return (mpl.colors.ListedColormap(['black','grey', 'blue', 'red', 'cyan']))


def get_gaussian(img_size,mode="3D",shape=None):
    """Create a simple "border weighting" array for patch blending.

           The returned array encodes a distance to the patch borders and is
           used to smoothly blend overlapping predictions when processing
           large images tile-by-tile.

           Parameters
           ----------
           img_size : int
               Size (in pixels/voxels) of one side of the patch.
           mode : {"2D", "3D"}
               Dimensionality of the weighting array.
           dim : int, optional
               Unused in the current implementation but kept for backward
               compatibility.

           Returns
           -------
           numpy.ndarray
               An array of shape ``(img_size, img_size)`` or
               ``(img_size, img_size, img_size)`` depending on ``mode``.
    """
    dim = 1
    if mode=="2D":
        if shape is not None and len(shape) == 3: dim = shape[-1]
        borders = np.zeros([img_size, img_size], dtype=np.uint16)
        for x in range(img_size):
            xv = min(x, img_size - x)
            for y in range(img_size):
                yv = min(y, img_size - y)
                borders[x, y] = min(xv, yv)

    else: #3D
        if shape is not None and len(shape) == 4: dim = shape[-1]
        borders = np.zeros([img_size, img_size, img_size], dtype=np.uint16)
        for x in range(img_size):
            xv = min(x, img_size - x)
            for y in range(img_size):
                yv = min(y, img_size - y)
                for z in range(img_size):
                    zv = min(z, img_size - z)
                    borders[x, y, z] = min(zv, min(xv, yv))
    bordersdim=np.zeros(borders.shape+(dim,), dtype=np.uint16)
    for i in range(dim): bordersdim[...,i]=borders
    return bordersdim
    #return borders

def get_border(bx,ex,sx):
    """Clamp patch indices so that they stay within the image bounds.

            Parameters
            ----------
            bx : int
                Initial begin index along one dimension.
            ex : int
                Initial end index along the same dimension.
            sx : int
                Size of the full image along this dimension.

            Returns
            -------
            (int, int)
                Corrected (begin, end) indices such that
                ``0 <= bx < ex <= sx``.
        """
    if ex>sx:
        pc=ex-bx #patch size
        bx=sx-pc-1
        ex=bx+pc
        if bx<0:
            ex-=bx
            bx=0
    return bx,ex

def get_z_axis(img,axis,z):
    if axis == 0:
        return img[z, :, :]
    elif axis == 1:
        return img[:, z, :]
    elif axis == 2:
        return img[:, :, z]
    return None


def sort_dict_by_values(dict1):
    sorted_values = sorted(dict1.values(), reverse=True)  # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dict1.keys():
            if dict1[k] == i:
                sorted_dict[k] = dict1[k]
                break
    return sorted_dict



def get_neigbhors(seg, c):
    from skimage.morphology import binary_dilation
    cell = np.zeros_like(seg).astype(np.bool)
    cell[seg == c] = 1
    neigbhors = get_labels(seg[binary_dilation(cell)])
    neigbhors.pop(0, None)  # Remove the Background
    neigbhors.pop(c, None)  # Remove the Cell it self
    return neigbhors


def wait_threads(threads):
    for index, thread in enumerate(threads):
        thread.join()

def live_threads(threads,nb):
    while len(threads)>nb:
        thread=threads.pop(0)
        thread.join()

def thread(target,args):
    x = Thread(target=target, args=args)
    x.start()
    return x


def get_labels(omask):
    lab=np.unique(omask)
    list_labeld={}
    for l in lab:
        list_labeld[l]=len(np.where(omask==l)[0])
    return sort_dict_by_values(list_labeld)



def compute_matchs(input_img,output_img,c,labels,counts):
    if input_img.shape != output_img.shape: return None
    v=input_img[output_img == c]
    if len(v)==0:  return None
    #print(f"mask={mask.shape} and input_img={input_img.shape}  and output_img={output_img.shape}")
    input_labels, input_counts = np.unique(v, return_counts=True)
    index_sorted = input_counts.argsort()[::-1]
    labels[c] = input_labels[index_sorted]
    counts[c] = input_counts[index_sorted]

def re_label(input_img, output_img,background_threshold=0,verbose=False):
    if input_img is None : return output_img
    if output_img is None : return input_img
    cells = np.unique(output_img)
    cells = list(cells[cells > background_threshold])
    if len(cells)==0: return output_img
    #print(f"cells {cells}")
    labels = {}
    counts = {}
    list_counts = []
    # First we calculate all matches
    threads = list()
    for c in cells:
       threads.append(thread(target=compute_matchs, args=(input_img,output_img,c,labels,counts)))
    wait_threads(threads)

    #Class Counts
    for c in cells:
        if c in counts:
            list_counts.extend(list(counts[c]))
    list_counts = np.unique(list_counts)
    list_counts.sort()
    list_counts = list_counts[::-1]
    # Now we match by order
    Match = {}
    Founded = []
    for count in list_counts:
        for c in cells:
            if c not in Match:  # ALREADY MATCH
                for i in range(len(counts[c])):
                    if count == counts[c][i] and labels[c][i] not in Founded:
                        if verbose : print(" --> found a match for " + str(c) + " with " + str(labels[c][i]) + " with " + str(count) + " voxels ")
                        Match[c] = labels[c][i]
                        Founded.append(labels[c][i])

    # Add unsolved labels
    last_used =1 if len(Founded)==0 else np.max(Founded) +1
    for c in cells:
        if c not in Match:
            if verbose : print(" --> create cell  " + str(c) + " with " + str(last_used))
            Match[c] = last_used
            last_used += 1

    # Create the image
    output_img_label = np.zeros_like(output_img).astype(np.uint16)
    for c in cells:  output_img_label[output_img == c] = Match[c]

    return output_img_label



def paral_labelrgb(seg, palc,c,labeled):
    labeled[seg==c,:]=palc


def get_labelrgb(seg,background_threshold=0):
    import seaborn as sns
    cells=np.unique(seg)
    cells=cells[cells>background_threshold]
    max_label = cells.max() + 1
    pal= np.uint8(np.round(np.array(sns.color_palette(n_colors=max_label))*255))
    labeled = np.zeros(seg.shape + (3,), dtype=np.uint8)
    threads = list()
    for c in cells: threads.append(thread(target=paral_labelrgb, args=(seg, pal[c],c,labeled)))
    wait_threads(threads)
    return labeled

def find_two_seeds(seg, c):  # Take the 2 farest points
    from scipy.spatial.distance import cdist
    from skimage.segmentation import watershed

    mask = seg == c
    coords = np.where(mask)
    vT = np.zeros([len(coords[0]), len(coords)])
    for s in range(len(coords)):
        vT[:, s] = coords[s]
    try:
        dist = cdist(vT, vT)
        maxi = dist.max()
        coords_maxi = np.where(dist == maxi)
        del dist
    except:
        coords_maxi = [[0]]
    if len(coords_maxi[0]) >= 2:
        ipt1 = coords_maxi[0][0]
        ipt2 = coords_maxi[0][1]
        if len(coords) == 3:
            pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])
            pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])
        elif len(coords) == 2:
            pt1 = np.array([coords[0][ipt1], coords[1][ipt1]])
            pt2 = np.array([coords[0][ipt2], coords[1][ipt2]])

        v = pt2 - pt1
        # print(v)
        seed1 = np.int32(pt1 + v * 1.0 / 3.0)
        seed2 = np.int32(pt1 + v * 2.0 / 3.0)

        markers = np.zeros_like(seg)
        if len(coords) == 3:
            markers[seed1[0], seed1[1], seed1[2]] = 1
            markers[seed2[0], seed2[1], seed2[2]] = 2
        elif len(coords) == 2:
            markers[seed1[0], seed1[1]] = 1
            markers[seed2[0], seed2[1]] = 2
        mask = seg == c
        # print(mask.shape)
        water = watershed(mask, markers, mask=mask)
        return water
    return None



#SEGMENTATION METHOD
def gauss_seeded_watershed(im,sigma,h_value,background_mask):
    from skimage.filters import gaussian
    return seeded_watershed(im,gaussian(np.float32(im), sigma=sigma) * 255,h_value,background_mask)

def seeded_watershed(im,gauss,h_value,background_mask):
    from skimage.morphology import extrema
    from skimage.measure import label
    from skimage.segmentation import watershed
    if im.shape[-1]==1: im=np.reshape(im,im.shape[0:-1])
    if gauss.shape[-1]==1: gauss=np.reshape(gauss,gauss.shape[0:-1])
    if background_mask.shape[-1] == 1: background_mask = np.reshape(background_mask, background_mask.shape[0:-1])
    if background_mask.shape!=gauss.shape or im.shape!=gauss.shape or im.shape!=background_mask.shape:
        printe("Im, Bakcground , Gaussian must have the same shapoe ")
        return None
    local = extrema.h_minima(gauss, h_value)
    label_maxima = label(local)
    w=watershed(im, markers=label_maxima, mask=background_mask)
    return w

#To run in Parallele
def IOU_seeded_watershed(im,gauss,background_mask,gt,h_tested,values,verbose=False,rescale=1):
    labelw = seeded_watershed(im, gauss, h_tested, background_mask)
    values[h_tested]=IOU(gt, labelw,verbose=verbose,rescale=rescale)


def optimize_seeded_watershed(im,gt,background_mask,verbose=False):
    from skimage.filters import gaussian

    # Look for the best H_values
    best_values = None
    best_v = 0
    rescale=1 if len(im.shape) < 3  else 4
    sigma_range=[1,2,3,4]
    h_tested_range=[1,2,3,4,5,6,7,8,9]
    if len(im.shape)==4: #(512,512,512,1)
        sigma_range=[1]
        h_tested_range=[2,4,6,8]
    for sigma in sigma_range:
        gauss = gaussian(im, sigma=sigma) * 255
        values = {}
        threads = list()
        for h_tested in h_tested_range:
            values[h_tested]=None #Initialisation
            ts=thread(target=IOU_seeded_watershed, args=(im,gauss,background_mask,gt,h_tested,values,False,rescale))
            if len(im.shape)>=3:
                ts.join()
                print(" --> for SIGMA:" + str(sigma) + " HVALUE:" + str(h_tested) + " --> " + str(values[h_tested]))
            threads.append(ts)
        wait_threads(threads)
        for h_tested in  h_tested_range:
            v=values[h_tested]
            if verbose and len(im.shape)<3: print(" --> for SIGMA:" + str(sigma) + " HVALUE:" + str(h_tested) + " --> " + str(v))
            if v is not None and v > best_v:
                best_v = v
                best_values = (sigma, h_tested)
    if best_values is None :
        printe("in Seeded Watershed Optimization ")
        return (None,None)
    if verbose : print(" --> Best SIGMA: " + str(best_values[0]) +" H VALUE: "+str(best_values[1]) + " --> " + str(best_v))
    return best_values





def distance_watershed(image, markers,mask): #WITH MARKERS
    from scipy.ndimage import distance_transform_edt
    from skimage.segmentation import watershed

    distance = distance_transform_edt(image)
    if mask is None: mask=image
    labels = watershed(-distance, markers, mask=mask)
    return labels


def distance_transform_watershed(image,threshold=0.1,background_mask=None):
    from skimage.filters import gaussian
    from scipy.ndimage import distance_transform_edt
    from skimage.morphology import extrema
    from skimage.measure import label
    from skimage.segmentation import watershed

    image_th = (image > threshold).astype("uint32")
    dt = distance_transform_edt(1 - image_th)
    local = extrema.h_maxima(dt, 1)
    gauss = gaussian(local * 255, preserve_range=True)
    gauss[gauss > 0] = 1
    label_maxima = label(gauss)
    return watershed(image, markers=label_maxima, mask=background_mask)




def proc_optimal_seeds(filename_gt, im, gt, background_mask, verbose=True,load=True):
    output_segmented,sigma,h_value=None,None,None
    ###### GET THE BEST SEGMENTATION FROM THE INPUT
    if isfile(filename_gt+".tiff") and isfile(filename_gt+".npy"):  # Look for Optimize Ground Truth
        if verbose: print(" --> read "+filename_gt)
        if load:
            output_segmented = imread(filename_gt+".tiff")
            [sigma, h_value] = np.load(filename_gt+".npy")
    else:
        #We first check if seeds were already found in a different image size
        lower_file=filename_gt.replace("IMAGE_SIZE512","IMAGE_SIZE256")
        if isfile(lower_file + ".npy"):
            [sigma, h_value] = np.load(lower_file + ".npy")
        else:
            sigma, h_value = optimal_seeds(im, gt, background_mask)
        print(" --> sigma="+str(sigma))
        print(" --> h_value=" + str(h_value))
        output_segmented = gauss_seeded_watershed(im, sigma, h_value, background_mask)
        imsave(filename_gt+".tiff", output_segmented,thread=True)
        if verbose: print(" --> save " + filename_gt)
        np.save(filename_gt+".npy", [sigma, h_value])
    return output_segmented,sigma, h_value


def proc_gauss_seeded_watershed(filename_gt, im, sigma, h_value, background_mask, verbose=True,load=True):
    output_segmented=None
    ###### PERFORM A SEED WATESHED
    if isfile(filename_gt+".tiff"):  # Look for Optimize Ground Truth
        if verbose: print(" --> read "+filename_gt+".tiff")
        if load:
            output_segmented=imread(filename_gt+".tiff")
    else:
        output_segmented = gauss_seeded_watershed(im, sigma, h_value, background_mask)
        if verbose: print(" --> save " + filename_gt+".tiff")
        imsave(filename_gt+".tiff", output_segmented,thread=True)
    return output_segmented



def optimal_seeds(im, gt, background_mask, verbose=True):
    from skimage.morphology import extrema
    from skimage.filters import gaussian

    if im.shape[-1] == 1: im = np.reshape(im, im.shape[0:-1])
    if gt.shape[-1] == 1: gt = np.reshape(gt, gt.shape[0:-1])
    if background_mask.shape[-1] == 1: background_mask = np.reshape(background_mask, background_mask.shape[0:-1])

    labels = np.unique(gt)
    if 0 in labels: labels = np.delete(labels, np.where(labels == 0))
    # Look for the best H_AND SIGMA values
    best_values = None
    best_errors = 100000
    sigma_range = [1, 2, 3, 4]
    h_tested_range = [1, 3, 5, 7, 9, 11,13]
    if len(im.shape)==3:
        sigma_range=[2,4]
        h_tested_range=[1,5,9,12,]

    for sigma in sigma_range:
        #print(" --> apply gaussian filter with sigma=" + str(sigma))
        gauss = gaussian(im, sigma=sigma) * 255
        gauss[background_mask == 0] = 255  # REMOVE THE BACKGROUND SEED MASK
        for h_tested in h_tested_range:
            #print(" --> apply h_minima with h value=" + str(h_tested))
            seeds = extrema.h_minima(gauss, h_tested)
            e = 0
            vals = gt[seeds == 1]
            for l in labels:  e += abs(1 -  len(np.where(vals == l)[0]))
            if verbose : print("( sigma="+str(sigma) + ", h value=" + str(h_tested) + " ) --> found " + str(e) + " errors seeds")
            if e < best_errors:
                best_values = [sigma, h_tested]
                best_errors=e
    if verbose : print(" --> Best SIGMA: " + str(best_values[0]) +" H VALUE: "+str(best_values[1]) + " --> " + str(best_errors))
    return best_values



def semantic_to_segmentation(semantic,footprint=4):
    """Convert a semantic prediction into an instance segmentation.

            The semantic prediction is assumed to contain at least:

            - background class
            - membrane / boundary class
            - interior / object class

            A watershed transform is applied on eroded interiors with the
            membrane acting as a barrier, producing a label image where each
            instance receives a unique integer id.

            Parameters
            ----------
            semantic : numpy.ndarray
                Semantic logits or class indices, typically the output of the
                U-Net (after argmax).
            footprint : int, optional
                Size of the structuring element used for erosion/dilation.

            Returns
            -------
            numpy.ndarray
                Integer label image with ``0`` = background and
                ``1..N`` = instances.
        """
    from skimage.segmentation import watershed
    from skimage.measure import label
    from skimage.morphology import binary_erosion,binary_dilation
    footprint=np.ones((footprint, footprint,footprint)) if len(semantic.shape)==3 else np.ones((footprint, footprint)) #3D vs 2D
    markers=None
    try:
        markers = np.uint16(label(np.uint16(binary_erosion(semantic == 1,footprint=footprint)), background=0))  # MARKERS
    except:
        a=1
    if markers is None:
        try:
            markers = np.uint16(label(np.uint16(binary_erosion(semantic == 1,selem=footprint)), background=0))  # MARKERS
        except:
            a=1
    if markers is None:
        print("failed compute makers with this skimage version")
        quit()
    background = binary_dilation(semantic == 0)  # BACKGROUND
    membrane = np.uint8(semantic > 1)  # NICE MEMBRANE
    return np.uint16(watershed(np.float32(membrane), markers=markers, mask=1 - background))


def segmentation_to_instance(seg):
    from skimage.measure import label
    cells = np.unique(seg)
    segl = np.zeros_like(seg, dtype=np.uint16)
    l = 1  # Labels number
    for c in cells:
        if c > 0:
            segc = np.uint16(label(np.uint16(seg == c)))
            segc[segc > 0] += l
            segl += segc
            l += len(np.unique(segc))
    return segl
