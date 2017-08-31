# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
caffe_root = "../libraries/caffe-master"

import sys
import caffe
MODEL_FILE = "../libraries/caffe-master/models/bvlc_reference_caffenet/deploy.prototxt"
PRETRAINED = "../libraries/caffe-master/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"
IMAGE_FILE='../test.jpg'

caffe.set_phase_test()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.load(caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy'),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))
input_image = caffe.io.load_image(IMAGE_FILE)
plt.imshow(input_image)
prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print 'prediction shape:', prediction[0].shape
plt.plot(prediction[0])
print 'predicted class:', prediction[0].argmax()