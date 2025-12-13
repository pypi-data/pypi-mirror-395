import tensorflow as tf


############# SEMANTIC LOSSES
# Multi Classes :
#    0 : Background
#    1 : Inside the Cell (Cytoplasm)
#    2 : Junction Level 1 ( Membrane )
#    3 : Junction Level 2
#    4 : Junction Level 3


@tf.function
def semantic_loss(ground_truth, prediction):
    loss_background_and_cell = sem_loss_mse(ground_truth, prediction)
    loss_membrane = sem_loss_membrane(ground_truth, prediction)
    loss_face = sem_loss_face(ground_truth, prediction)
    loss_junctions =  sem_loss_junctions(ground_truth, prediction) if len(ground_truth.shape)==5 else 0 #3D Junctions
    loss_ero =erosion_loss(ground_truth, prediction)
    loss_bckgd_cyto=loss_bckgd_cytoplasm(ground_truth, prediction)
    return loss_background_and_cell + loss_membrane + loss_face + loss_junctions  + loss_ero+loss_bckgd_cyto



@tf.function
def too_big_loss(ground_truth, prediction):
    # Unsupervised loss which make that membrane cannot be to big
    result =tf.math.argmax(prediction, axis=-1,output_type=tf.dtypes.int32)
    nice_mask = tf.greater_equal(result, 2 * tf.ones(tf.shape(result), dtype=tf.dtypes.int32)) #2 Is to get Only Signal of the membrane as one simplement element
    mask = tf.where(nice_mask == True)
    nice_mask=tf.expand_dims(nice_mask, -1)
    kernel = tf.ones((3,)*(len(nice_mask.shape)-2)+(1,1))
    gauss = tf.nn.convolution(tf.cast(nice_mask, tf.float32), kernel, padding="SAME")
    cond =tf.cast( tf.equal(gauss, tf.ones(tf.shape(gauss)) * 9), tf.float32)
    loss_mask = tf.reduce_mean(tf.gather_nd(cond, mask))
    return loss_mask



@tf.function
def too_small_loss(ground_truth, prediction):
    # Unsupervised loss which make that membrane cannot be to small
    result =tf.math.argmax(prediction, axis=-1,output_type=tf.dtypes.int32)
    ndim = len(result.shape)-1
    nice_mask = tf.greater_equal(result, 2 * tf.ones(tf.shape(result), dtype=tf.dtypes.int32))  # 2 Is to get Only Signal of the membrane as one simplement element
    ###### MEMBRANE NOT TO SMALL
    nice_mask_expanded = tf.cast(tf.expand_dims(nice_mask, -1), tf.float32)
    # EROSION
    ksize = (1,) + (2,) * ndim + (1,)
    strides = (1,) * (2 + ndim)
    if ndim == 3:
        erode = -tf.nn.max_pool3d(-nice_mask_expanded, ksize=ksize, strides=strides, padding="SAME")
    else:
        erode = -tf.nn.max_pool2d(-nice_mask_expanded, ksize=ksize, strides=strides, padding="SAME")
    # DILATATON
    kernel = tf.ones((5,) * (ndim - 1) + (1, 1))
    gauss = tf.nn.convolution(erode, kernel, padding="SAME")
    cond = tf.cast(tf.greater_equal(gauss, tf.ones(tf.shape(gauss))), tf.float32)

    # RESTE
    diff = tf.cast(tf.greater_equal(tf.math.subtract(nice_mask_expanded, cond), tf.ones(tf.shape(gauss))), tf.float32)
    #loss_tosmall = tf.reduce_mean(diff)
    mask = tf.where(nice_mask == True)
    loss_tosmall=tf.reduce_mean(tf.gather_nd(diff, mask))
    return loss_tosmall


@tf.function
def erosion_loss(ground_truth, prediction):
    loss_too_big=too_big_loss(ground_truth, prediction)
    loss_too_small = too_small_loss(ground_truth, prediction)
    total_loss = tf.cast(0, tf.float32)
    if not tf.math.is_nan(loss_too_big): total_loss += loss_too_big
    if not tf.math.is_nan(loss_too_small): total_loss += loss_too_small
    return tf.cast(10, tf.float32)*total_loss




@tf.function
def sem_loss_mse(ground_truth, prediction):
    return tf.keras.metrics.mean_squared_error(ground_truth, prediction)

@tf.function
def sem_loss_membrane(ground_truth, prediction): #Membrane Signal
    return mse_on_mask(ground_truth, prediction,2)

@tf.function
def sem_loss_face(ground_truth, prediction):
    return mse_on_mask(ground_truth, prediction,3)

@tf.function
def sem_loss_junctions(ground_truth, prediction):
    return mse_on_mask(ground_truth, prediction,4)

@tf.function
def mse_on_mask(ground_truth, prediction,v):
    mask = tf.where(ground_truth[..., v] == 1) #The Mask of the GT for v ( 1 Correspond to TRUE)
    loss = tf.math.square(tf.cast(prediction, tf.float32) - tf.cast(ground_truth, tf.float32))  # Shape (None, 64,64,2)
    loss_mask = tf.reduce_mean(tf.gather_nd(loss, mask))
    if tf.math.is_nan(loss_mask): return tf.cast(0,tf.float32)
    return loss_mask

@tf.function
def loss_bckgd_cytoplasm(ground_truth, prediction):
    #Unsupervised loss which make that the background class cannot toutch the cytoplasm
    result = tf.math.argmax(prediction, axis=-1, output_type=tf.dtypes.int32)
    background = tf.math.equal(result, tf.zeros(tf.shape(result), dtype=tf.dtypes.int32))
    cytoplasm = tf.math.equal(result, tf.ones(tf.shape(result), dtype=tf.dtypes.int32))
    background = tf.expand_dims(background, -1)
    kernel = tf.ones((3,) * (len(background.shape) - 2) + (1, 1))
    gauss = tf.nn.convolution(tf.cast(background, tf.float32), kernel, padding="SAME")
    background_dilate = tf.greater(gauss,  tf.zeros(tf.shape(gauss)))
    mask = tf.math.logical_and(background_dilate==True,tf.cast(background, tf.float32)==False)
    cytoplasm = tf.expand_dims(cytoplasm, -1)
    loss_background= tf.reduce_mean(tf.gather_nd(tf.cast(cytoplasm,tf.float32), tf.where(mask)))
    if tf.math.is_nan(loss_background): return tf.cast(0,tf.float32)
    return tf.cast(10, tf.float32)*loss_background




