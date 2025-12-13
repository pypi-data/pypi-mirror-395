from tensorflow.keras.layers import Input, concatenate,BatchNormalization,Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD
from morphodeep.networks.losses import sem_loss_membrane, sem_loss_face, sem_loss_junctions, sem_loss_mse, \
    semantic_loss, erosion_loss, loss_bckgd_cytoplasm


def UNET(mode=2,inputs=(512,512,1),outputs=(512,512,1),filters=[32,64,128,256,512],dense=False,batch_normalization=False, apply_dropout=False,decode=True,loss='mse',compile=True,activation=None,optimizer=None):
    '''
    UNET
    Adapted from https://github.com/zhixuhao/unet/blob/master/model.py
    Adapted from https://www.mdpi.com/2076-3417/9/3/404
    Adapted from https://github.com/mrkolarik/3D-brain-segmentation
    '''

    if mode == 3:
        from tensorflow.keras.layers import Conv3D as Conv
        from tensorflow.keras.layers import MaxPooling3D as MaxPooling
        from tensorflow.keras.layers import Conv3DTranspose as ConvTranspose
    elif mode == 2:
        from tensorflow.keras.layers import Conv2D as Conv
        from tensorflow.keras.layers import MaxPooling2D as MaxPooling
        from tensorflow.keras.layers import Conv2DTranspose as ConvTranspose

    ratio = outputs[0] / inputs[0]
    ratioz=1
    if mode==3:
        ratioz=1 if len(outputs)<2 else int(outputs[2] / inputs[2])
    if ratio == ratioz:ratioz=1

    ks = (3, )*mode
    out = (1, )*mode
    strides = (2,)* mode
    pool_size = (2, )*mode
    axis = mode + 1
    inputs = Input(inputs)
    i=1
    convs={}
    x=inputs


    for filter in filters:
        if ratioz > 1 and i==1:
            conv1 = Conv(filter, (3,3,1), activation='relu', padding='same')(x)
            convs[i] = Conv(filter, (3,3,1), activation='relu', padding='same')(conv1)

        else:
            conv1 = Conv(filter, ks, activation='relu', padding='same')(x)
            if dense:   conv1= concatenate([x, conv1], axis=axis)
            convs[i] = Conv(filter, ks, activation='relu', padding='same')(conv1)
            if dense: convs[i] = concatenate([x, convs[i]], axis=axis)

        if batch_normalization:  convs[i] = BatchNormalization()(convs[i])

        if i<len(filters): #No MaxPooling for the last layer
            if ratioz > 1 and i == 1:
                x = MaxPooling(pool_size=(ratioz,ratioz,1))(convs[i])
            else:
                x = MaxPooling(pool_size=pool_size)(convs[i])
        else:
            x=convs[i]
        i+=1



    if decode:
        filters.reverse()
        filters.pop(0)

        i = len(filters)
        for filter in filters:
            ct=ConvTranspose(filter, pool_size, strides=strides, padding='same')(x)
            if ratioz>1 and i==1: # We cannot concatne different shape
                x = Conv(filter, ks, activation='relu', padding='same')(ct)
            else:
                up = concatenate([ct, convs[i]], axis=axis)
                x = Conv(filter, ks, activation='relu', padding='same')(up)
                if dense:  x = concatenate([up, x], axis=axis)


            x = Conv(filter, ks, activation='relu', padding='same')(x)
            if dense:
                x = concatenate([up, x], axis=axis)
            if batch_normalization:
                x = BatchNormalization()(x)
            if apply_dropout:
                x=Dropout(0.5)(x)
            i-=1

        if ratio > 1: #Change Image Size between input and output
            for r in range(int(ratio / 2.0)):
                filter=round(filter/2)
                if filter<1:
                    filter=1
                x = ConvTranspose(filter, pool_size, strides=strides, padding='same')(x)
                x = Conv(filter, ks, activation='relu', padding='same')(x)
                x = Conv(filter, ks, activation='relu', padding='same')(x)
                if batch_normalization:
                    x = BatchNormalization()(x)


        if activation is not None:
            last = Conv(outputs[-1], out, activation=activation)(x) # Original with activation='sigmoid'
        else:
            last = Conv(outputs[-1], out)(x)

    else:
        from tensorflow.keras.layers import Flatten, Dense
        flat = Flatten()(x)
        last = Dense(outputs[0],activation=activation)(flat)

    model = Model(inputs=[inputs], outputs=[last])
    if compile:
        if optimizer is None: optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
        model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    return model


####################### FOR SEMANTIC SEGMENTATION
def JUNNET(mode="2D",inputs=(512,512,1),outputs=(512,512,1)):
    mode = 2 if mode == "2D" else 3
    optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
    model=UNET(mode=mode, inputs=inputs, outputs=outputs, filters=[32, 64, 128, 256, 512], dense=False,compile=False,activation="softmax")
    if mode==3:
        model.compile(optimizer=optimizer, loss=semantic_loss, metrics=['accuracy',sem_loss_mse, sem_loss_membrane,sem_loss_face,sem_loss_junctions,erosion_loss,loss_bckgd_cytoplasm])
    else:
        model.compile(optimizer=optimizer, loss=semantic_loss,  metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face,erosion_loss,loss_bckgd_cytoplasm])
    return model


def DUNNET(mode="2D",inputs=(512,512,1),outputs=(512,512,1)):
    mode = 2 if mode == "2D" else 3
    optimizer = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
    model=UNET(mode=mode, inputs=inputs, outputs=outputs, filters=[32, 64, 128, 256, 512,1024], dense=True,compile=False,activation="softmax")
    if mode==3:
        model.compile(optimizer=optimizer, loss=semantic_loss, metrics=['accuracy',sem_loss_mse, sem_loss_membrane,sem_loss_face,sem_loss_junctions,erosion_loss,loss_bckgd_cytoplasm])
    else:
        model.compile(optimizer=optimizer, loss=semantic_loss,  metrics=['accuracy', sem_loss_mse, sem_loss_membrane, sem_loss_face,erosion_loss,loss_bckgd_cytoplasm])
    return model
