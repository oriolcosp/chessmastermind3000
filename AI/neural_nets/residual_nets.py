from keras.layers import BatchNormalization, Dense, Conv2D, LeakyReLU



def residual_block(y,
                   nb_channels=100,
                   _kernel_size=3,
                   _strides=(1, 1),
                   _project_shortcut=False,
                   batch_momentum=0.9,
                   batch_epsilon=0.001):
    shortcut = y

    # down-sampling is performed with a stride of 2
    y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides)(y)
    y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)
    y = layers.LeakyReLU()(y)

    y = layers.Conv2D(nb_channels, kernel_size=_kernel_size, strides=_strides)(y)
    y = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(y)

    if _project_shortcut or _strides != (1, 1):
        shortcut = layers.Conv2D(nb_channels, kernel_size=(1, 1), strides=_strides)(shortcut)
        shortcut = layers.BatchNormalization(momentum=batch_momentum, epsilon=batch_epsilon)(shortcut)

    y = layers.add([shortcut, y])
    y = layers.LeakyReLU()(y)

    return y


def value_head(model,
               batch_momentum = 0.9,
               batch_epsilon = 0.001,
               conv2_filters = 1,
               conv2_kernel_size = 1,
               conv2_stride = 1,
               fully1_neurons = 100,
               fully2_neurons = 3):

    model.add(Conv2D(filters=conv2_filters, kernel_size=conv2_kernel_size, activation=None, strides=(conv2_stride, conv2_stride)))
    model.add(BatchNormalization(axis=1, momentum=batch_momentum, epsilon=batch_epsilon))
    model.add(LeakyReLU())
    model.add(Dense(fully1_neurons, activation=None))
    model.add(LeakyReLU())
    model.add(Dense(fully2_neurons, activation=None))
    return model