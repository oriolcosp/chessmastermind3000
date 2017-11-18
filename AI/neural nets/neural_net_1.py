import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import h5py
from keras.models import load_model
import copy

from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend as K
K.set_image_dim_ordering('th')

def train_net(datafile, model_origin, model_save):
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)

    # load data
    h5f = h5py.File(datafile,'r')
    X_train = h5f['taulells'][:]
    y_train = h5f['results'][:]
    h5f.close()

    # codificar en 2 matrius separades
    X_train_1s = (X_train == 1) * 1
    X_train_m1s = (X_train == -1) * 1
    X_train = np.column_stack( (X_train_1s, X_train_m1s) )
    
    # flatten 28*28 images to a 784 vector for each image
    num_pixels = X_train.shape[1] * X_train.shape[2]
    X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('int8')

    # X_train = X_train.reshape(X_train.shape[0], 2, 3, 3).astype('int8')

    # one hot encode outputs
    y_train = np_utils.to_categorical( y_train - y_train.min() )
    num_classes = y_train.shape[1]

    # define baseline model
    if model_origin is None:
        # create model
        model = Sequential()

        model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
        model.add(Dense(20, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))

        # model.add(Conv2D(9, (3, 3), input_shape=(2, 3, 3), activation='relu'))
        # model.add(Flatten())
        # model.add(Dense(18, activation='relu'))
        # model.add(Dense(num_classes, activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    else:
        model = load_model(model_origin)

    # Fit the model
    model.fit(X_train, y_train, validation_data=(X_train, y_train), epochs=10, batch_size=200, verbose=2)
    # Final evaluation of the model
    scores = model.evaluate(X_train, y_train, verbose=0)

    model.save(model_save)  # creates a HDF5 file 'my_model.h5'
