# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 17:34:07 2015

@author: aditya
"""
import numpy as np
DATA_PATH_FL= '/home/aditya/pythonExperiments/datapath'

DATA_PATH= np.loadtxt(DATA_PATH_FL,dtype='str')[0]
print DATA_PATH
#PATH=DATA_PATH+'/all-handgesture/cambridge-hand-gesture/'
    
def pickFrames(set_no, label, sequence=None, frames=None ):
    sets=range(set_no,set_no+1)
    labels=range(label,label+1)
    if(sequence!=None):
        sequences=range(sequence,sequence+1)
    else:
        sequences=sequence
    #frames= range(frame, frame+1)
    image_path_list, label_list=populateModel(PATH,sets,labels,sequences,frames)
    return image_path_list

def populateModel(PATH=DATA_PATH,sets=range(1,6),labels=range(0,5),sequences=None,frames=None):
    '''
    stores and returns a list of image path and a list of corresponding labels

    
    '''
    PATH=DATA_PATH+'aditya-data/all-handgesture/cambridge-hand-gesture/'
    image_path_list=[]
    label_list=[]
    
    ####
    #generate random subregion
    # sequences
    for label_no in labels:
        label_folder=setLabelName(label_no)+ '/'
        for set_no in sets:
            set_path=setSetPath(PATH,set_no)
            label_path = set_path+label_folder

            if (sequences==None):
                num_sequence = int(np.loadtxt(label_path + 'count.txt'))
                sequences_=range(num_sequence)
            else:
                sequences_=sequences
            for seq_no in sequences_:
                seq = setSeqNo(seq_no)
                seq_path=label_path+seq+'/'
                if(frames==None):
                    num_frames=int(np.loadtxt(seq_path + 'count.txt'))
                    frames_=range(0,num_frames)
                else:
                    frames_=frames
                for frame_no in frames_:
                    image_path=readFromCambridge(seq_path,frame_no)
                    image_path_list.append(image_path)
                    label_list.append(label_list)
    return image_path_list , label_list
    
def setLabelName(label_no):
    label='000'+str(label_no)
    return label

def setSeqNo(seq_no):
    if (seq_no>99):
        seq_iter= '0' + str(seq_no)
    elif (seq_no>9 and seq_no<99):
        seq_iter= '00' + str(seq_no)
    else:
        seq_iter='000' + str(seq_no)
    return seq_iter

def setSetPath(PATH,set_no):
    set_name = 'Set' + str(set_no)
    set_path = PATH + set_name + '/'
    return set_path


def readFromCambridge(seq_path,image_no=0):
    if (image_no>99):
        image_name= '0' + str(image_no)
    elif (image_no>9 and image_no<100):
        image_name= '00' + str(image_no)
    else:
        image_name='000' + str(image_no)
    image_path= seq_path+'frame-' + image_name + '.jpg'
    return image_path