# -*- coding: utf-8 -*-
"""Untitled16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QMDZmy5yiQgbM6-iwzSK7vj8nk3F0gwY

# **download data**
"""

import os
os.environ['KAGGLE_USERNAME'] = "belalagwa"  # username from the json file
os.environ['KAGGLE_KEY'] = "c30180e65b45212ab6c1fe4688732366"  # key from the json file
!kaggle datasets download -d fanconic/skin-cancer-malignant-vs-benign # api copied from kaggle

"""# unzip data"""

! unzip skin-cancer-malignant-vs-benign.zip

"""# **load picture and file**"""

#import libarary
import numpy as np
import random
import cv2
np.random.seed(42) #So that the result is constant
target_labels = ["benign" , "malignant"] #It is required to open the data
TARGET_HIGHET, TARGET_WIDTH = 100,100    #Scaling all images between 100,100
def load_images(base_base):
  filenames = []
  labels = []
  x_list = []
  for folder_name in os.listdir(base_base):
    folder_path = os.path.join(base_base, folder_name)
    if folder_name not in target_labels:
      continue 
    idx = target_labels.index(folder_name)
    for image_name in os.listdir(folder_path):
      image_path = os.path.join(folder_path, image_name)
      filenames.append(image_path)
      labels.append(idx)
  data = list(zip(filenames, labels))
  random.shuffle(data)
  filenames, labels = zip(*data)
  for file_name in filenames:
    gray_image = cv2.imread(file_name ) 
    resized_image = cv2.resize(gray_image, (TARGET_HIGHET, TARGET_WIDTH ))
    scaled_image = resized_image.astype("float32")/255.0
    x_list.append(scaled_image)

  x_data_array = np.array(x_list, dtype=np.float32)
  x_data_array = x_data_array.reshape(len(x_list) , TARGET_HIGHET, TARGET_WIDTH,3)
  y_array = np.array(labels , dtype= np.uint8)
  return x_data_array , y_array

"""# **Call Fenction load_images**"""

def load_data():
  TRAIN_DIR = "/content/data/train"
  TEST_DIR = "/content/data/test"
  (x_train, y_train) = load_images(TRAIN_DIR)
  (x_test, y_test) = load_images(TEST_DIR)
  return (x_train, y_train) , (x_test, y_test)

# Import packages and set numpy random seed
import tensorflow as tf
import matplotlib.pyplot as plt

# Load pre-shuffled training and test datasets
(x_train, y_train), (x_test, y_test) = load_data()
x_train.shape , x_test.shape

"""# **visualize sample from the  data **"""

# Store labels of dataset
labels = ["benign" , "malignant"]

# Print the first several training images, along with the labels
fig = plt.figure(figsize=(20,5))
for i in range(36):
    ax = fig.add_subplot(3, 12, i + 1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(x_train[i]))
    ax.set_title("{}".format(labels[y_train[i]]))
plt.show()

"""# **construct base model**"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization,LeakyReLU
from keras.applications import VGG16
model = Sequential()

model.add(VGG16(include_top=False, input_shape=(100, 100, 3,)))
model.add(Flatten())
model.add(Dense(32))
model.add(LeakyReLU(0.001))
model.add(Dense(16))
model.add(LeakyReLU(0.001))
model.add(Dense(1, activation='sigmoid'))
model.layers[0].trainable = False

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

"""# **plot model**"""

from keras.utils import plot_model
plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')

"""# **train model **"""

model.fit(x_train, y_train, epochs=20,verbose=2, batch_size=64,validation_split=0.2)

model.evaluate(x_test, y_test)

"""# **save model**"""

model.save("generated_model_keras.hdf5")