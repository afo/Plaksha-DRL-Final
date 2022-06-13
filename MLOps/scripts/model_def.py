import tensorflow as tf
from tensorflow.keras.layers import Activation, Conv2D, Dense, Dropout, Flatten, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam, SGD, RMSprop


def get_custom_model(learning_rate, weight_decay, optimizer, momentum):
    
    model = Sequential()
    model.add(Dense(3))
    model.add(Activation('relu'))
    model.add(Dense(5))
    model.add(Activation('relu'))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    if optimizer.lower() == 'sgd':
        opt = SGD(learning_rate=learning_rate, decay=weight_decay, momentum=momentum)
    elif optimizer.lower() == 'rmsprop':
        opt = RMSprop(learning_rate=learning_rate, decay=weight_decay)
    else:
        opt = Adam(learning_rate=learning_rate, decay=weight_decay)
    
    return model

