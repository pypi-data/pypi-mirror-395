
import tensorflow as tf
from os.path import join

from morphodeep.networks.losses import semantic_loss
from morphodeep.tools.utils import get_path, mkdir
import numpy as np
from matplotlib import pyplot as plt


class PixToSem:

    def __init__(self, mode=2, inputs=(512, 512, 1), outputs=(512, 512, 1)):
        self.mode = 2 if mode == "2D" else 3
        if self.mode == 3:
            from tensorflow.keras.layers import Conv3D as Conv
            from tensorflow.keras.layers import Conv3DTranspose as ConvTranspose
            from tensorflow.keras.layers import ZeroPadding3D as ZeroPadding
        elif self.mode == 2:
            from tensorflow.keras.layers import Conv2D as Conv
            from tensorflow.keras.layers import Conv2DTranspose as ConvTranspose
            from tensorflow.keras.layers import ZeroPadding2D as ZeroPadding

        self.loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        self.LAMBDA = 100

        self.Conv = Conv
        self.ConvTranspose = ConvTranspose
        self.ZeroPadding = ZeroPadding

        self.inputs = inputs
        self.outputs = outputs
        self.generator = self.Generator()

        self.discriminator = self.Discriminator()
        self.generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
        self.discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        self.checkpoint = tf.train.Checkpoint(generator_optimizer=self.generator_optimizer,
                                              discriminator_optimizer=self.discriminator_optimizer,
                                              generator=self.generator, discriminator=self.discriminator)

    def downsample(self,filters, size, apply_batchnorm=True):
        initializer = tf.random_normal_initializer(0., 0.02)

        result = tf.keras.Sequential()
        result.add( self.Conv(filters, size, strides=2, padding='same',  kernel_initializer=initializer, use_bias=False))

        if apply_batchnorm:
            result.add(tf.keras.layers.BatchNormalization())

        result.add(tf.keras.layers.LeakyReLU())

        return result

    def upsample(self,filters, size, apply_dropout=False):
        initializer = tf.random_normal_initializer(0., 0.02)

        result = tf.keras.Sequential()
        result.add(
            self.ConvTranspose(filters, size, strides=2,
                                            padding='same',
                                            kernel_initializer=initializer,
                                            use_bias=False))

        result.add(tf.keras.layers.BatchNormalization())

        if apply_dropout:
            result.add(tf.keras.layers.Dropout(0.5))

        result.add(tf.keras.layers.ReLU())

        return result

    def Generator(self):
        inputs = tf.keras.layers.Input(shape=self.inputs)

        down_stack = [
            self.downsample(64, 4, apply_batchnorm=False),  # (batch_size, 128, 128, 64)
            self.downsample(128, 4),  # (batch_size, 64, 64, 128)
            self.downsample(256, 4),  # (batch_size, 32, 32, 256)
            self.downsample(512, 4),  # (batch_size, 16, 16, 512)
            self.downsample(512, 4),  # (batch_size, 8, 8, 512)
            self.downsample(512, 4),  # (batch_size, 4, 4, 512)
            self.downsample(512, 4),  # (batch_size, 2, 2, 512)
            self.downsample(512, 4),  # (batch_size, 1, 1, 512)
        ]

        up_stack = [
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 2, 2, 1024)
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 4, 4, 1024)
            self.upsample(512, 4, apply_dropout=True),  # (batch_size, 8, 8, 1024)
            self.upsample(512, 4),  # (batch_size, 16, 16, 1024)
            self.upsample(256, 4),  # (batch_size, 32, 32, 512)
            self.upsample(128, 4),  # (batch_size, 64, 64, 256)
            self.upsample(64, 4),  # (batch_size, 128, 128, 128)
        ]

        initializer = tf.random_normal_initializer(0., 0.02)
        last = self.ConvTranspose(self.outputs[-1], 4,
                                               strides=2,
                                               padding='same',
                                               kernel_initializer=initializer,
                                               activation='tanh')  # (batch_size, 256, 256, 3)

        x = inputs

        # Downsampling through the model
        skips = []
        for down in down_stack:
            x = down(x)
            skips.append(x)

        skips = reversed(skips[:-1])

        # Upsampling and establishing the skip connections
        for up, skip in zip(up_stack, skips):
            x = up(x)
            x = tf.keras.layers.Concatenate()([x, skip])

        x = last(x)

        return tf.keras.Model(inputs=inputs, outputs=x)

    def generator_loss(self,disc_generated_output, gen_output, target):
        gan_loss = self.loss_object(tf.ones_like(disc_generated_output), disc_generated_output)

        # Mean absolute error
        l1_loss = tf.reduce_mean(semantic_loss(target,gen_output))

        total_gen_loss = gan_loss + (self.LAMBDA * l1_loss)

        return total_gen_loss, gan_loss, l1_loss

    def Discriminator(self):
        initializer = tf.random_normal_initializer(0., 0.02)

        inp = tf.keras.layers.Input(shape=[256, 256, self.inputs[-1]], name='input_image')
        tar = tf.keras.layers.Input(shape=[256, 256, self.outputs[-1]], name='target_image')

        x = tf.keras.layers.concatenate([inp, tar])  # (batch_size, 256, 256, channels*2)

        down1 = self.downsample(64, 4, False)(x)  # (batch_size, 128, 128, 64)
        down2 = self.downsample(128, 4)(down1)  # (batch_size, 64, 64, 128)
        down3 = self.downsample(256, 4)(down2)  # (batch_size, 32, 32, 256)

        zero_pad1 = self.ZeroPadding()(down3)  # (batch_size, 34, 34, 256)
        conv = self.Conv(512, 4, strides=1,    kernel_initializer=initializer,   use_bias=False)(zero_pad1)  # (batch_size, 31, 31, 512)

        batchnorm1 = tf.keras.layers.BatchNormalization()(conv)

        leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)

        zero_pad2 = self.ZeroPadding()(leaky_relu)  # (batch_size, 33, 33, 512)

        last = self.Conv(1, 4, strides=1,   kernel_initializer=initializer)(zero_pad2)  # (batch_size, 30, 30, 1)

        return tf.keras.Model(inputs=[inp, tar], outputs=last)

    def discriminator_loss(self,disc_real_output, disc_generated_output):
        real_loss = self.loss_object(tf.ones_like(disc_real_output), disc_real_output)

        generated_loss = self.loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)

        total_disc_loss = real_loss + generated_loss

        return total_disc_loss

    def load_weights(self,filename):
        status = self.checkpoint.restore(tf.train.latest_checkpoint(get_path(filename)))
        #status =  self.checkpoint.restore(filename) #TODO RESTORE THE SPECIFIC FILENAME

    def summary(self, line_length=150):
        print(" --> GENERATOR")
        self.generator.summary(line_length=line_length)
        print(" --> DISCRIMINATOR")
        self.discriminator.summary(line_length=line_length)

    ## @tf.function
    def train_step(self, input_image, target, epochs):
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            gen_output = self.generator(input_image, training=True)

            disc_real_output = self.discriminator([input_image, target], training=True)
            disc_generated_output = self.discriminator([input_image, gen_output], training=True)

            gen_total_loss, gen_gan_loss, gen_l1_loss = self.generator_loss(disc_generated_output, gen_output, target)
            disc_loss = self.discriminator_loss(disc_real_output, disc_generated_output)
        generator_gradients = gen_tape.gradient(gen_total_loss, self.generator.trainable_variables)
        discriminator_gradients = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)

        self.generator_optimizer.apply_gradients(zip(generator_gradients, self.generator.trainable_variables))
        self.discriminator_optimizer.apply_gradients(
            zip(discriminator_gradients, self.discriminator.trainable_variables))
        if self.tensorboard is not None:
            with self.tensorboard.as_default():
                tf.summary.scalar('gen_total_loss', gen_total_loss, step=epochs)
                tf.summary.scalar('gen_gan_loss', gen_gan_loss, step=epochs)
                tf.summary.scalar('gen_l1_loss', gen_l1_loss, step=epochs)
                tf.summary.scalar('disc_loss', disc_loss, step=epochs)

        return gen_total_loss, gen_gan_loss, gen_l1_loss, disc_loss

    def fit(self, train_ds,validation_data=None, validation_steps=0,initial_epoch=0, steps_per_epoch=10000, epochs=1000, callbacks=[]):
        steps_per_test = 1000
        # steps_per_epoch=100
        e = initial_epoch
        step = 0
        test_image = None
        test_target = None
        self.tensorboard = None
        output_path = join(get_path(callbacks[0].filepath), "Predict")
        mkdir(output_path)
        if len(callbacks) >= 2:
            self.tensorboard = tf.summary.create_file_writer(join(callbacks[1].log_dir, "train"))
        print("Epoch " + str(initial_epoch) + "/" + str(epochs))
        while e < epochs:
            for (input_image, target) in train_ds:
                # print(len(np.where(input_image==1)[0]))
                # print(target.mean())
                if test_image is None and len(np.where(input_image == 1)[0]) > 60000:
                    test_image = np.copy(input_image)
                    test_target = np.copy(target)
                gen_total_loss, gen_gan_loss, gen_l1_loss, disc_loss = self.train_step(input_image, target, e)
                pts = " [" + "=" * round(step * 30.0 / steps_per_epoch) + ">" + "." * round(
                    29 - step * 30.0 / steps_per_epoch) + "]"
                print(str(step).rjust(5) + "/" + str(steps_per_epoch) + pts + " - total loss: " + str(
                    gen_total_loss.numpy()) + " - gan loss: " + str(gen_gan_loss.numpy()) + " - l1 loss: " + str(
                    gen_l1_loss.numpy()) + " - disc loss:" + str(disc_loss.numpy()))

                if (step + 1) % steps_per_test == 0:
                    if test_image is not None:
                        self.generate_images(test_image, test_target,
                                             join(output_path, "prediction_" + str(e) + "-" + str(step) + ".tiff"))

                step += 1
                if (step + 1) % steps_per_epoch == 0:
                    e = e + 1
                    print("Epoch " + str(e) + "/" + str(epochs))
                    self.checkpoint.save(callbacks[0].filepath.split('.')[0])
                    step = 0

    def generate_images(self, test_input, ground_truth,figname):
        prediction = self.generator(test_input, training=False)
        fig=plt.figure(figsize=(15, 15))
        display_list = [test_input[0], ground_truth[0], prediction[0]]
        title = ['Input Image', 'Ground Truth', 'Predicted Image']
        for i in range(3):
            plt.subplot(1, 3, i + 1)
            plt.title(title[i])
            # Getting the pixel values in the [0, 1] range to plot.
            im=display_list[i]
            if len(im.shape)==2 or (len(im.shape)==3 and im.shape[-1]==3) or (len(im.shape)==3 and im.shape[-1]==1): #Gray or RGB
                plt.imshow(im * 0.5 + 0.5)
            elif  len(im.shape)==3:
                if im.shape[-1]==2:
                    im2=np.zeros([im.shape[0]+im.shape[0],im.shape[1]])
                    im2[0:im.shape[0],:]=im[:,:,0]
                    im2[im.shape[0]:im.shape[0]+im.shape[0], :] = im[:, :, 1]
                    plt.imshow(im2 * 0.5 + 0.5)

            plt.axis('off')

        plt.savefig(figname)
        plt.close(fig)

    def predict(self, data_input):
        prediction = self.generator(data_input, training=False)
        return prediction.numpy()

