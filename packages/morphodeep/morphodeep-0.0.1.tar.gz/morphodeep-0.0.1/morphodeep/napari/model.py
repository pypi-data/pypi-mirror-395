# src/morphodeep/model.py
from typing import Optional
import numpy as np
from tqdm import tqdm

from .get_model import cache_model_path
from skimage.transform import resize

from ..tools.image import get_gaussian, normalize, get_border, semantic_to_segmentation

_model = None


def UNET(mode=3,inputs=(256,256,256,1),outputs=(256,256,256,5)):
    """Build the U-Net architecture used by MorphoDeep.

    The implementation is adapted from:

    - https://github.com/zhixuhao/unet/blob/master/model.py
    - https://www.mdpi.com/2076-3417/9/3/404

    Parameters
    ----------
    mode : int or str, optional
        Dimensionality of the network (2 or 3).  The value may be given
        as an integer or a string such as ``"2D"`` or ``"3D"``.
    inputs : tuple of int, optional
        Shape of the input tensor, including channels.
    outputs : tuple of int, optional
        Shape of the output tensor, including number of semantic classes.

    Returns
    -------
    keras.Model
        A compiled U-Net model ready for inference.
    """
    from tensorflow.keras.layers import Input, concatenate
    from tensorflow.keras.models import Model
    if mode == 3:
        from tensorflow.keras.layers import Conv3D as Conv
        from tensorflow.keras.layers import MaxPooling3D as MaxPooling
        from tensorflow.keras.layers import Conv3DTranspose as ConvTranspose
    else:
        from tensorflow.keras.layers import Conv2D as Conv
        from tensorflow.keras.layers import MaxPooling2D as MaxPooling
        from tensorflow.keras.layers import Conv2DTranspose as ConvTranspose

    filters = (32, 64, 128, 256, 512)
    filters = list(filters)

    ks = (3, ) * mode
    out = (1, ) * mode
    strides = (2,) * mode
    pool_size = (2, ) * mode
    axis = mode + 1
    inputs = Input(inputs)
    i = 1
    convs = {}
    x = inputs

    for filter in filters:
        conv1 = Conv(filter, ks, activation='relu', padding='same')(x)
        convs[i] = Conv(filter, ks, activation='relu', padding='same')(conv1)

        if i<len(filters): #No MaxPooling for the last layer
            x = MaxPooling(pool_size=pool_size)(convs[i])
        else:
            x = convs[i]
        i += 1


    filters.reverse()
    filters.pop(0)

    i = len(filters)
    for filter in filters:
        ct = ConvTranspose(filter, pool_size, strides=strides, padding='same')(x)
        up = concatenate([ct, convs[i]], axis=axis)
        x = Conv(filter, ks, activation='relu', padding='same')(up)
        x = Conv(filter, ks, activation='relu', padding='same')(x)
        i -= 1

    last = Conv(outputs[-1], out, activation="softmax")(x)

    model = Model(inputs=[inputs], outputs=[last])

    return model



def run_instance_segmentation(
    image: np.ndarray,
    net_size: int = 128,
    mode: str = "2D",
    isotrope: bool = True,
    patches: bool = True,
    voxel_size: tuple[float, float, float] = (1.0, 1.0, 1.0),
    z_axis: int = 0,
) -> np.ndarray:
    """Run MorphoDeep instance segmentation on a NumPy image.

    This is the main entry point to the segmentation pipeline.  It:

    1. Loads (or downloads) the appropriate pre-trained U-Net model.
    2. Optionally rescales the volume to reduce voxel anisotropy.
    3. Processes the image either in a single pass or in overlapping
       patches, depending on the ``patches`` flag and image size.
    4. Converts the semantic prediction to an instance label image.

    Parameters
    ----------
    image : numpy.ndarray
        Input image data.  For 2D mode, shape is typically ``(Y, X)``;
        for 3D mode, ``(Z, Y, X)``.
    net_size : int, optional
        Patch size of the network (e.g. 128 or 256).
    mode : {"2D", "3D"}, optional
        Dimensionality of the model used for prediction.
    isotrope : bool, optional
        If ``True`` and ``mode == "3D"``, the volume is rescaled to
        reduce anisotropy using the provided voxel spacing.
    patches : bool, optional
        If ``True``, the image is processed tile-by-tile using a sliding
        window; if ``False``, the full image is processed at once (when
        feasible).
    voxel_size : tuple of float, optional
        Physical voxel spacing in the order ``(Z, Y, X)`` or equivalent,
        used for anisotropy correction.
    z_axis : int, optional
        Index of the axis corresponding to Z in the input array.

    Returns
    -------
    numpy.ndarray
        Integer label image with ``0`` = background and ``1..N`` =
        segmented instances.
    """
    dim=int(mode[0])
    model_filename = cache_model_path( "ALL-all", net_size,mode)
    if model_filename is None:
        print(f"No model in {mode} found for morphodeep ", 1)
    else:

        model = UNET(mode=dim, inputs=(net_size,)*dim+(1,), outputs=(net_size,)*dim+(2+dim,))
        print(f"load model {model_filename}")
        model.load_weights(model_filename)

        rawdata = image.astype("float32")
        init_shape = rawdata.shape
        if len(rawdata.shape) < dim:
            raise ValueError(f"Please provide a {dim}D image for  {dim}D networks")
        elif len(rawdata.shape) > dim:
            print(f"Crop image last dimension to {dim}")
            while len(rawdata.shape) > dim:
                rawdata = rawdata[..., 0]

        if mode=="3D":
            if isotrope:
                anisotropy = (voxel_size[2] / voxel_size[1])
                if anisotropy != 1:
                    if z_axis == 0:
                        new_shape=[int(anisotropy * rawdata.shape[0]),rawdata.shape[1], rawdata.shape[2]]
                    elif z_axis == 1:
                        new_shape = [rawdata.shape[0], int(anisotropy * rawdata.shape[1]),rawdata.shape[2]]
                    else :#z_axis == 2:
                        new_shape=[rawdata.shape[0], rawdata.shape[1],  int(anisotropy * rawdata.shape[2])]
                    rawdata = resize(rawdata, new_shape, preserve_range=True).astype(rawdata.dtype)
                    print(f"found anisotropy of {anisotropy}, image shape is now {rawdata.shape}")


        if patches:  # PREDICT TILES
            rawdata = normalize(rawdata)
            predict_shape = rawdata.shape + (dim+2,)
            image_predict = np.zeros(predict_shape, dtype=np.float32)
            print(f"predict semantic with shape {rawdata.shape} using tiles of {net_size} voxels")
            nb_image_predict = np.ones(predict_shape, dtype=np.uint16)
            borders = get_gaussian(net_size,mode,predict_shape)
            slidingWindow = int(round(net_size / 2))

            if mode=="3D":
                nbTotal = float(len(range(0, rawdata.shape[0], slidingWindow)) * len(
                    range(0, rawdata.shape[1], slidingWindow)) * len(
                    range(0, rawdata.shape[2], slidingWindow)))
                with tqdm(total=nbTotal, desc=f"Predict from tiles") as pbar:
                    for x in range(0, rawdata.shape[0], slidingWindow):
                        for y in range(0, rawdata.shape[1], slidingWindow):
                            for z in range(0, rawdata.shape[2], slidingWindow):
                                bx, ex = get_border(x, x + net_size, rawdata.shape[0])
                                by, ey = get_border(y, y + net_size, rawdata.shape[1])
                                bz, ez = get_border(z, z + net_size, rawdata.shape[2])
                                input = rawdata[bx:ex, by:ey, bz:ez]
                                original_shape = input.shape
                                if original_shape[0] < net_size or original_shape[1] < net_size or \
                                        original_shape[2] < net_size:  # Need To Resize Image
                                    input = resize(input, [net_size, net_size, net_size],
                                                   preserve_range=True).astype(input.dtype)
                                    if ex - bx > original_shape[0]:
                                        ex = original_shape[0]
                                    if ey - by > original_shape[1]:
                                        ey = original_shape[1]
                                    if ez - bz > original_shape[2]:
                                        ez = original_shape[2]
                                patch_predict = model.predict(
                                    np.reshape(input, (1, net_size, net_size, net_size)), verbose=0)
                                patch_predict = patch_predict[0, ...] * borders
                                borders_reshape = borders
                                if original_shape[0] < net_size or original_shape[1] < net_size or \
                                        original_shape[2] < net_size:  # Need To Resize Image
                                    patch_predict = resize(patch_predict, original_shape + (5,),
                                                           preserve_range=True).astype(input.dtype)
                                    borders_reshape = resize(borders, original_shape,
                                                             preserve_range=True).astype(input.dtype)

                                image_predict[bx:ex, by:ey, bz:ez] += patch_predict
                                nb_image_predict[bx:ex, by:ey, bz:ez] += borders_reshape
                                pbar.update(1)
            elif mode=="2D":
                nbTotal = float(len(range(0, rawdata.shape[0], slidingWindow)) * len(range(0, rawdata.shape[1], slidingWindow)) )
                with tqdm(total=nbTotal, desc=f"Predict from tiles") as pbar:
                    for x in range(0, rawdata.shape[0], slidingWindow):
                        for y in range(0, rawdata.shape[1], slidingWindow):
                                bx, ex = get_border(x, x + net_size, rawdata.shape[0])
                                by, ey = get_border(y, y + net_size, rawdata.shape[1])
                                input = rawdata[bx:ex, by:ey]
                                original_shape = input.shape
                                if original_shape[0] < net_size or original_shape[1] < net_size :  # Need To Resize Image
                                    input = resize(input, [net_size, net_size],  preserve_range=True).astype(input.dtype)
                                    if ex - bx > original_shape[0]:  ex = original_shape[0]
                                    if ey - by > original_shape[1]: ey = original_shape[1]
                                patch_predict = model.predict( np.reshape(input, (1, net_size, net_size)), verbose=0)
                                patch_predict = patch_predict[0, ...] * borders
                                borders_reshape = borders
                                if original_shape[0] < net_size or original_shape[1] < net_size:  # Need To Resize Image
                                    patch_predict = resize(patch_predict, original_shape + (4,),  preserve_range=True).astype(input.dtype)
                                    borders_reshape = resize(borders, original_shape, preserve_range=True).astype(input.dtype)
                                image_predict[bx:ex, by:ey] += patch_predict
                                nb_image_predict[bx:ex, by:ey] += borders_reshape
                                pbar.update(1)

            image_predict /= nb_image_predict
            del nb_image_predict
            image_predict = np.uint8(np.argmax(image_predict, axis=-1))  # Convert probabilities in 5 class
        else:
            rawdata = resize(rawdata, (net_size,)*dim, preserve_range=True).astype(rawdata.dtype)
            rawdata = normalize(rawdata)
            print(f"predict semantic with shape {rawdata.shape}")
            image_predict = model.predict(np.reshape(rawdata, (1,) + rawdata.shape), verbose=0)[0, ...]
            image_predict = np.uint8(np.argmax(image_predict, axis=-1))

        if init_shape!=image_predict.shape:
            print("restore initial shape")
            image_predict = resize(image_predict, init_shape, preserve_range=True, order=0)
        print("convert semantic to instance segmentation")
        labels = semantic_to_segmentation(image_predict)
        print(f"Found {len(np.unique(labels))} labels")

        return labels
    return None