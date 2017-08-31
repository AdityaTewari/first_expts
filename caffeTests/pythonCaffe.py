# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 16:00:15 2015

@author: aditya
"""

import numpy as np
import matplotlib.pyplot as plt
#import prepareCaffeData
caffe_root = "../../libraries/caffe-master"

import sys
import caffe
MODEL_FILE = "../../libraries/caffe-master/models_wrong/bvlc_reference_caffenet/deploy.prototxt"
PRETRAINED = "../../libraries/caffe-master/models_wrong/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"
IMAGE_FILE='../../test.jpg'


def main():
    testClassifier()

def prepareData():
    prepareCaffeData.populateModel()

def testClassifier():
    caffe.set_phase_test()
    net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                           mean=np.load(caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy'),
                           channel_swap=(2,1,0),
                           raw_scale=255,
                           image_dims=(256, 256))
    input_image = caffe.io.load_image(IMAGE_FILE)
    #plt.imshow(input_image)
    prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
    print 'prediction shape:', prediction[0].shape
    #x=plt.plot(prediction[0])
    print 'predicted class:', prediction[0].argmax()
    filters = net.params['conv1'][0].data
    visalise(filters.transpose(0, 2, 3, 1))
    visalise(net.blobs['conv3'].data[4], padval=.5)
#==============================================================================
#     for K,V in net.params.items():
#         print np.shape(V[0].data)
#         visalise(net,V[0].data)
#     for K,V in net.blobs.items():
#         print K, V.data.shape
#==============================================================================

def visalise(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
#    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
#     
#     # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    print np.shape(data)
#     
    plt.imshow(data)
    plt.show()
#==============================================================================
    
    
    

if __name__ == "__main__":
    main()