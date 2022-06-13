import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam, SGD
from model_def import get_custom_model
import time
import argparse
import os
import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# Copy inference pre/post-processing script so that it'll be included in the model package
os.system('mkdir /opt/ml/model/scripts')
os.system('cp inference.py /opt/ml/model/scripts')
os.system('cp requirements.txt /opt/ml/model/scripts')

def get_dataset(filename, usecase="training"):
    data = pd.read_csv(filename)

    X = data.drop(['Species'], axis = 1)
    y = data['Species']

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_rem, y_train, y_rem = train_test_split(X, y, test_size = 0.2, stratify = y, random_state = 0)
    
    X_val, X_test, y_val, y_test = train_test_split(X_rem, y_rem, test_size = 0.5, stratify = y_rem, random_state = 0)
    
    if usecase == "testing":
        return [X_test, y_test]
    
    if usecase == "validation":
        return [X_val, y_val]
       
    return [X_train, y_train]

def get_model(learning_rate, weight_decay, optimizer, momentum):
    model = get_custom_model(learning_rate, weight_decay, optimizer, momentum)
        
    return model

def main(args):
    # Hyper-parameters
    epochs       = args.epochs
    lr           = args.learning_rate
    momentum     = args.momentum
    weight_decay = args.weight_decay
    optimizer    = args.optimizer

    train_dataset = get_dataset(args.training + '/Iris.csv')
    val_dataset = get_dataset(args.training + '/Iris.csv', "validation")
    eval_dataset   = get_dataset(args.training + '/Iris.csv', "testing")
    
    
    # Load model
    model = get_model(lr, weight_decay, optimizer, momentum)
            
    # Optimizer
    if optimizer.lower() == 'sgd':
        opt = SGD(lr=lr, decay=weight_decay, momentum=momentum)
    else:
        opt = Adam(lr=lr, decay=weight_decay)

    # Compile model
    model.compile(optimizer=opt,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Train model
    history = model.fit(train_dataset[0],
                        train_dataset[1],
                        validation_data=(val_dataset[0], val_dataset[1]), 
                        epochs=epochs)
    
    # Evaluate model performance
    score = model.evaluate(eval_dataset[0], eval_dataset[1], verbose=1)
    print('Test loss    :', score[0])
    print('Test accuracy:', score[1])
    
    # Save model to model directory
    model.save(f'{os.environ["SM_MODEL_DIR"]}/{time.strftime("%m%d%H%M%S", time.gmtime())}', save_format='tf')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    # Hyper-parameters
    parser.add_argument('--epochs',        type=int,   default=10)
    parser.add_argument('--learning-rate', type=float, default=0.01)
    parser.add_argument('--weight-decay',  type=float, default=2e-4)
    parser.add_argument('--momentum',      type=float, default='0.9')
    parser.add_argument('--optimizer',     type=str,   default='sgd')


    # SageMaker parameters
    parser.add_argument('--model_dir',        type=str,   default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--training',         type=str,   default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--validation',       type=str,   default=os.environ['SM_CHANNEL_VALIDATION'])
    parser.add_argument('--eval',             type=str,   default=os.environ['SM_CHANNEL_EVAL'])
    
    args = parser.parse_args()
    main(args)
