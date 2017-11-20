from keras import layers
from keras import models

class residual_net1():

    def __init__(self, filename = None, n_residual = 1):

            if filename is None:
                self.create(n_residual)
            else:
                self.model = models.load_model( filename )


    def residual_block(self,
                        y,
                        nb_channels=100,
                        _kernel_size=3,
                        _strides=1,
                        _project_shortcut=False,
                        batch_momentum=0.9,
                        batch_epsilon=0.001):
            shortcut = y

            # down-sampling is performed with a stride of 2
            y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides, padding='same')(y)
            y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)
            y = layers.LeakyReLU()(y)

            y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides, padding='same')(y)
            y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)

            if _project_shortcut or _strides != (1, 1):
                    shortcut = layers.Conv2D(nb_channels, kernel_size=(1, 1), strides=_strides, padding='same')(shortcut)
                    shortcut = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(shortcut)
            
            y = layers.add([shortcut, y])
            y = layers.LeakyReLU()(y)

            return y


    def conv_block(self,
                    y,
                    nb_channels=100,
                    _kernel_size=3,
                    _strides=1,
                    batch_momentum=0.9,
                    batch_epsilon=0.001):

            # down-sampling is performed with a stride of 2
            y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides, padding='same')(y)
            y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)
            y = layers.LeakyReLU()(y)

            return y


    def value_head(self,
                    y,
                    batch_momentum = 0.9,
                    batch_epsilon = 0.001,
                    conv2_filters = 1,
                    nb_channels=100,
                    _kernel_size=3,
                    _strides=1,
                    fully1_neurons = 100,
                    fully2_neurons = 3):

            y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides, padding='same')(y)
            y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)
            y = layers.LeakyReLU()(y)
            y = layers.core.Flatten()(y)
            y = layers.Dense(fully1_neurons, activation=None)(y)
            y = layers.LeakyReLU()(y)
            y = layers.Dense(fully2_neurons, activation=None)(y)

            return y


    def create(self, n_residual):
        
            input_tensor = layers.Input(shape=(13, 8, 8))
            self.model = self.conv_block( input_tensor )
            for i in range(n_residual):
                self.model = self.residual_block(self.model)

            self.model = self.value_head(self.model)

            self.model = models.Model(inputs=[input_tensor], outputs=[self.model])
            print(self.model.summary())

            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


    def predict(self, imgs, details=False):
            return 1
            all_preds = self.model.predict(imgs)
            # for each image get the index of the class with max probability
            idxs = np.argmax(all_preds, axis=1)
            # get the values of the highest probability for each image
            preds = [all_preds[i, idxs[i]] for i in range(len(idxs))]
            # get the label of the class with the highest probability for each image
            classes = [self.classes[idx] for idx in idxs]
            return np.array(preds), idxs, classes


    def fit_data(self, X_train, y_train, nb_epoch=1, batch_size=200):
            
            self.model.fit(X_train, y_train, validation_data=(X_train, y_train),
                            epochs=nb_epoch, batch_size=batch_size, verbose=2)



