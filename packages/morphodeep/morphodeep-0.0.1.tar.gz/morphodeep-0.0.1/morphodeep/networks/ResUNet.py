from tensorflow.keras.layers import Activation, Add
from tensorflow.keras.layers import Concatenate, BatchNormalization
from morphodeep.networks.losses import sem_loss_membrane, sem_loss_face, sem_loss_junctions, sem_loss_mse, \
    semantic_loss, erosion_loss, loss_bckgd_cytoplasm
def bn_act(x, act=True):
    x = BatchNormalization()(x)
    if act == True:
        x = Activation("relu")(x)
    return x


def conv_block(mode,x, filters, kernel_size=(3, 3), padding="same", strides=1):
    kernel_size = (kernel_size[0],)* mode
    conv = bn_act(x)
    conv = Conv(filters, kernel_size, padding=padding, strides=strides)(conv)
    return conv


def stem(mode,x, filters, kernel_size=(3, 3), padding="same", strides=1):
    kernel_size = (kernel_size[0],)* mode
    conv = Conv(filters, kernel_size, padding=padding, strides=strides)(x)
    conv = conv_block(mode,conv, filters, kernel_size=kernel_size, padding=padding, strides=strides)

    shortcut = Conv(filters, kernel_size=(1,)* mode, padding=padding, strides=strides)(x)
    shortcut = bn_act(shortcut, act=False)

    output = Add()([conv, shortcut])
    return output


def residual_block(mode,x, filters, kernel_size=(3, 3), padding="same", strides=1):
    kernel_size = (kernel_size[0],)* mode
    res = conv_block(mode,x, filters, kernel_size=kernel_size, padding=padding, strides=strides)
    res = conv_block(mode,res, filters, kernel_size=kernel_size, padding=padding, strides=1)

    shortcut = Conv(filters, kernel_size=(1,)* mode, padding=padding, strides=strides)(x)
    shortcut = bn_act(shortcut, act=False)

    output = Add()([shortcut, res])
    return output


def upsample_concat_block(mode,x, xskip):
    u = UpSampling((2,)* mode)(x)
    c = Concatenate()([u, xskip])
    return c



def RESUNET_graph(mode=2,inputs=(512,512,1),outputs=(512,512,1), filters = [16, 32, 64, 128, 256] ,loss='mse',metrics=['accuracy','kullback_leibler_divergence'],compile=True,activation=None):
    '''
    Adapted from https://github.com/nikhilroxtomar/Deep-Residual-Unet/blob/master/Deep%20Residual%20UNet.ipynb
    '''
    global Conv, MaxPooling, UpSampling, ConvTranspose, ZeroPadding
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Flatten, Dense
    from tensorflow.keras.optimizers import SGD
    if mode == 3:
        from tensorflow.keras.layers import Conv3D as Conv
        from tensorflow.keras.layers import UpSampling3D as UpSampling
    elif mode == 2:
        from tensorflow.keras.layers import Conv2D as Conv
        from tensorflow.keras.layers import UpSampling2D as UpSampling

    ratio = 1
    r = 2
    while r < outputs[0] / inputs[0]:
        r = r * 2
        ratio = ratio + 1

    inputs = Input(shape=inputs)

    ## Encoder
    e0 = inputs
    e1 = stem(mode,e0, filters[0])
    e2 = residual_block(mode,e1, filters[1], strides=2)
    e3 = residual_block(mode,e2, filters[2], strides=2)
    e4 = residual_block(mode,e3, filters[3], strides=2)
    e5 = residual_block(mode,e4, filters[4], strides=2)

    ## Bridge
    b0 = conv_block(mode,e5, filters[4], strides=1)
    b1 = conv_block(mode,b0, filters[4], strides=1)

    ## Decoder
    u1 = upsample_concat_block(mode,b1, e4)
    d1 = residual_block(mode,u1, filters[4])

    u2 = upsample_concat_block(mode,d1, e3)
    d2 = residual_block(mode,u2, filters[3])

    u3 = upsample_concat_block(mode,d2, e2)
    d3 = residual_block(mode,u3, filters[2])

    u4 = upsample_concat_block(mode,d3, e1)
    d4 = residual_block(mode,u4, filters[1])

    if ratio > 1:  # Change Image Size between input and output
        filter=filters[1]
        for r in range(ratio):
            filter = round(filter / 2)
            if filter < 1:
                filter = 1
            d4 = residual_block(mode, d4, filter)
            d4 = UpSampling((2,)* mode)(d4)

    if activation is None:
        outputs = Conv(outputs[-1], (1,)* mode, padding="same")(d4) #Originaly with activation="sigmoid"
    else:
        outputs = Conv(outputs[-1], (1,)* mode, padding="same",activation=activation)(d4)  # Originaly with activation="sigmoid"
    model = Model(inputs, outputs)

    if compile:
        optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def RESUNET_graph_filters(mode=2,inputs=(512,512,1),outputs=(512,512,1), filters = [16, 32, 64, 128, 256] ,loss='mse',metrics=['accuracy','kullback_leibler_divergence'],compile=True,activation=None):
    '''
    Adapted from https://github.com/nikhilroxtomar/Deep-Residual-Unet/blob/master/Deep%20Residual%20UNet.ipynb
    '''
    global Conv, MaxPooling, UpSampling, ConvTranspose, ZeroPadding
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Flatten, Dense
    from tensorflow.keras.optimizers import SGD
    if mode == 3:
        from tensorflow.keras.layers import Conv3D as Conv
        from tensorflow.keras.layers import UpSampling3D as UpSampling
    elif mode == 2:
        from tensorflow.keras.layers import Conv2D as Conv
        from tensorflow.keras.layers import UpSampling2D as UpSampling

    ratio = 1
    r = 2
    while r < outputs[0] / inputs[0]:
        r = r * 2
        ratio = ratio + 1

    inputs = Input(shape=inputs)

    #Filters
    nf=len(filters)

    ## Encoder
    e0 = inputs
    es = {}
    es[1]=stem(mode,e0, filters[0])
    for f in range(1,nf):
        es[f+1]=residual_block(mode,es[f], filters[f], strides=2)


    ## Bridge
    b0 = conv_block(mode,es[nf], filters[nf-1], strides=1)
    b1 = conv_block(mode,b0, filters[nf-1], strides=1)

    ## Decoder
    us={}
    ds={}
    us[1] = upsample_concat_block(mode, b1, es[nf - 1])
    ds[1] = residual_block(mode, us[1], filters[nf - 1])

    for f in range(2,nf):
        us[f]= upsample_concat_block(mode,ds[f-1], es[nf-f])
        ds[f] = residual_block(mode,us[f], filters[nf-f])


    if activation is None:
        outputs = Conv(outputs[-1], (1,)* mode, padding="same")(ds[nf-1]) #Originaly with activation="sigmoid"
    else:
        outputs = Conv(outputs[-1], (1,)* mode, padding="same",activation=activation)(ds[nf-1])  # Originaly with activation="sigmoid"
    model = Model(inputs, outputs)

    if compile:
        optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def RESUNET(mode=2,inputs=(512,512,1),outputs=(512,512,1)):
    return RESUNET_graph(mode=mode, inputs=inputs, outputs=outputs,activation="softmax")


def RESJUNET(mode=2,inputs=(512,512,1),outputs=(512,512,1)):
    mode = 2 if mode == "2D" else 3
    if mode == 3:
        return RESUNET_graph(mode=mode, inputs=inputs, outputs=outputs, loss=semantic_loss,
                      metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face, sem_loss_junctions,
                               erosion_loss, loss_bckgd_cytoplasm],activation="softmax")
    else:
        return RESUNET_graph(mode=mode, inputs=inputs, outputs=outputs, loss=semantic_loss,
                      metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face, erosion_loss,
                               loss_bckgd_cytoplasm],activation="softmax")


def RESDUNET(mode=2,inputs=(512,512,1),outputs=(512,512,1)):
    mode = 2 if mode == "2D" else 3
    if mode == 3:
        return RESUNET_graph_filters(mode=mode, inputs=inputs, outputs=outputs,filters = [16, 32, 64, 128, 256,512,1024], loss=semantic_loss,
                      metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face, sem_loss_junctions,
                               erosion_loss, loss_bckgd_cytoplasm],activation="softmax")
    else:
        return RESUNET_graph_filters(mode=mode, inputs=inputs, outputs=outputs,filters = [16, 32, 64, 128, 256,512,1024], loss=semantic_loss,
                      metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face, erosion_loss,
                               loss_bckgd_cytoplasm],activation="softmax")