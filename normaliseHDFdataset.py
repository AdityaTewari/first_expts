'''
Created on 21 Apr 2015

@author: atw
'''
import h5py
import sys
import time
import os
import numpy as np

from src.DataProcessing.updateHDFile import findMinMax
from src.DataProcessing.updateHDFile import normUnityMax
#from src.DataProcessing.onehotTransforms import changeOnehottoVector


null_label=100
pixel_nos=100
x=65535.0

t_a=100
t_d=10000
median=False

t_ha=10 #adds to median
show_plot=True
DATA_ORIGIN='/media/aditya/data/allData/DFKI_pose_Gest'


skip_empty=False

def setNormMats():
    file_name='home/aditya/pythonExperiments/norm_file.h5'
    file_ = h5py.File(file_name, 'r')   # 'r' means that hdf5 file is open in read-only mod
    dataset = file_['data']
    return dataset[:,:,:]

def normFind(file_names,dir_path,l):
    maxmat=findMinMax(file_names,dir_path,l)
    return maxmat

def createH5File(hdf_name):
    f = h5py.File(hdf_name, "w")
    return f

    

def editHDF5(file_names,dir_path,norm=True,one_hot=True):
    st_str=['in','fl','op','fi','jo','po']
    norm_pers=[np.zeros((120,165),dtype=np.float32), np.zeros((120,165),dtype=np.float32)]
    file_names=[os.path.join(dir_path,file_name) for file_name in file_names if (file_name[:2] in st_str)]
    print file_names
    for file_name in file_names:
        print file_name
        file_    = h5py.File(file_name, 'r')   # 'r' means that hdf5 file is open in read-only mod
        dataset = file_['data']
        labels = file_['label']

        dataset_=dataset[:,:,:,:]
        norm_pose=[np.zeros((120,165),dtype=np.float32), np.zeros((120,165),dtype=np.float32)]
        for  image_no in xrange(np.shape(dataset_)[0]):
            norm_pose=[norm_pose[0]+dataset_[image_no,0,:,:], norm_pose[1]+dataset_[image_no,1,:,:]]
        file_.close()
        norm_pers=[norm_pose[0]+ norm_pose[0]/float(np.shape(dataset_)[0]), norm_pose[1]+ norm_pose[1]/float(np.shape(dataset_)[0])]
    return norm_pers

    #===========================================================================
    #     lines_a = f_a.readlines()
    # with open(file_path_dep, "rb") as f_d:
    #     lines_d = f_d.readlines()
    # try:
    #     for row_a,row_d in zip(lines_a,lines_d):
    #         print 'Row read successfully!'
    #         image_a=reshapeFileLine(row_a)
    #         image_d=reshapeFileLine(row_d)
    #         plot_ob.set_data([image_a,image_d])
    #         plot_ob.on_running()
    #         time.sleep(.0001)
    # except csv.Error, e:
    #     print 'file %s, line %d: %s' % (file_name, lines_a.line_num, e)
    #     sys.exit('file %s, line %d: %s' % (file_name, lines_a.line_num, e))
    #===========================================================================


    #save

def main():
    #norm_data=[np.zeros((120,165),dtype=np.float32), np.zeros((120,165),dtype=np.float32)]
    #norms=setNormMats()
    persons=[3]
    for person_num in persons:
        l='p'+str(person_num)
        form='pose'
        loc= os.path.join(l,form)
        dir_path= os.path.join(DATA_ORIGIN,loc)
        print DATA_ORIGIN
        file_names = [f for f in os.listdir(dir_path) if (f.endswith('merged_normed.h5'))]# and not f.endswith('merged.h5') and not f.endswith('norm.h5') )]
        #file_names=['open_20150414_15_17_57']
        normUnityMax(file_names,dir_path,norm=False,one_hot=False)
        #print minmax
        
#==============================================================================
#         norm_data=[norm_data[0]+norm_pers[0],norm_data[1]+norm_pers[1]]
#     norm_=[norm_data[0]/float(len(persons)), norm_data[1]/float(len(persons))]
#     h_f_n=createH5File('norm_file,h5')
#     data_set=h_f_n.create_dataset("norm", data=norm_, dtype=float)
#     h_f_n.close()
#==============================================================================


if __name__ == '__main__':
    main()
