# based on https://medium.com/@draj0718/image-classification-and-prediction-using-transfer-learning-3cf2c736589d
#
# pip install tensorflow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import sklearn.metrics as metrics
import tensorflow as tf
import os
import os.path
import sys
import random
import shutil
import math
import json
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications import VGG16


# Haengt mit der verwendeten Neuronalen Netz zusammen
IMAGE_SHAPE = [224, 224]


def build_model(num_classes=3):
    vgg = VGG16(input_shape = (224,224,3), weights = 'imagenet', include_top = False)
    for layer in vgg.layers:
        layer.trainable = False
    x = Flatten()(vgg.output)
    x = Dense(128, activation = 'relu')(x) 
    x = Dense(64, activation = 'relu')(x) 
    x = Dense(num_classes, activation = 'softmax')(x) 
    model = Model(inputs = vgg.input, outputs = x)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train(epochs = 5, batch_size=32, num_classes=None, model_file = 'model.h5'):
    """
     Struktur
       train
         label1
            001.jpg
            ...
         label2
            ...
       test
         ...
    """
    print("train()")
    if num_classes is None:
        num_classes = len(os.listdir('train'))
    model = build_model(num_classes)
    
    trdata = ImageDataGenerator()
    train_data_gen = trdata.flow_from_directory(directory="train",target_size=(224,224), shuffle=False, class_mode='categorical')
    tsdata = ImageDataGenerator()
    test_data_gen = tsdata.flow_from_directory(directory="test", target_size=(224,224),shuffle=False, class_mode='categorical')
    print("Data Complete")

    training_steps_per_epoch = np.ceil(train_data_gen.samples / batch_size)
    validation_steps_per_epoch = np.ceil(test_data_gen.samples / batch_size)
    # was fit_generator
    model.fit(train_data_gen, workers=1, steps_per_epoch = training_steps_per_epoch, validation_data=test_data_gen, validation_steps=validation_steps_per_epoch,epochs=epochs, verbose=1)
    print('Training Completed!')

    Y_pred = model.predict(test_data_gen, test_data_gen.samples / batch_size)
    val_preds = np.argmax(Y_pred, axis=1)
    import sklearn.metrics as metrics
    val_trues =test_data_gen.classes
    from sklearn.metrics import classification_report
    print(classification_report(val_trues, val_preds))

    tf.keras.models.save_model(model,model_file)
    config = { 'classes': os.listdir('train') }
    json_object = json.dumps(config, indent=4)
    with open(model_file + ".config.json", "w") as outfile:
        outfile.write(json_object)
    
def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def mv_test_data(train_dir = './', test_dir = './../test/'):
    dirs = os.listdir(train_dir)
    for tag in dirs:
        files = os.listdir(train_dir + tag)
        file_max = math.floor(len(files)/10)
        print("Moving Test-Data for " + tag + " 10%: "+ str(file_max))
        for i in range(file_max):
            file = files.pop(random.randrange(len(files)))
            mkdir(test_dir + tag)
            shutil.move(train_dir + tag+'/'+file, test_dir + tag+'/'+file)


def predict(img_path, model_file = 'model.h5', class_labels = None):
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
    import numpy as np
    if class_labels is None:
        with open(model_file+'.config.json', 'r') as openfile:
            json_object = json.load(openfile)
            class_labels = json_object['classes']
    model = load_model(model_file) 
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds=model.predict(x)
    pred = np.argmax(preds, axis=-1)
    print(class_labels[pred[0]])

def gen(tags):
    print("Downloading Image Dataset")
    from nwebclient import NWebClient
    n = NWebClient(None)
    n.downloadImageDataset(tags=tags)

# python -m nwebclient.image_classification train
if __name__ == '__main__':
    print("")
    print("Args: train predict gen mv_test")
    print("")
    print(" train: Traineirt das Netz auf dem Datensatz im aktuellen Verzeichnis")
    print(" predict file")
    print(" gen: Lädt ein Datenset von einer nweb Instanz herrunter")
    print(" mv_test ./train/ ./test/: Verschiebt 10% der Bilder in das Verzeichnis test")
    print("")
    if len(sys.argv)>1:
        arg = sys.argv[1]
        if arg == 'train':
            train()
        elif arg == 'predict':
            print("Predict")
            predict(sys.argv[2])
        elif arg == 'gen':
            gen(sys.argv[2:])
        elif arg == 'mv_test':
            mv_test_data(sys.argv[2], sys.argv[3])
        else:
            print("Unknown Arg")
    print(sys.argv) # ab 1
    #print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
    #physical_devices = tf.config.experimental.list_physical_devices('CPU')
    #print("physical_devices-------------", len(physical_devices))
    #tf.config.experimental.set_memory_growth(physical_devices[0], True)
    #train(num_classes=2)
    #predict('test/landscape/2673.jpg', class_labels=['landscape', 'underground'])
    #predict('test/underground/14433.jpg', class_labels=['landscape', 'underground'])
