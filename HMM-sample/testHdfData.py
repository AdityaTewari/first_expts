'''
Created on 8 Aug 2014

@author: atw
'''

import pickle
import numpy as np
from __future__ import print_function, division

from hmmpytk import hmm_faster

def defineStates():
    i=1
    #the basic method includes dividing data into small pieces
    #and doing a k mean clustering
    #and calculating variance for each cluster
    #each cluster than defines a state
    
    #closest mean can be a state
    #being inside a point may mean  being in a state
    
    #the k mean algorithm has to be modified to fit the left right model