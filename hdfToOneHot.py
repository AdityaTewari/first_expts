'''
Created on 21 Apr 2015

@author: atw
'''
import h5py
import sys
import time
import os
import numpy as np




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

def createH5File(hdf_name):
    f = h5py.File(hdf_name, "w")
    return f

def changeVectortoOnehot(leng, vals):
    print vals
    check_mat=np.zeros((len(vals),leng))
    ind=0
    for val in vals:
        check_mat[ind][val]=1.0
        ind+=1
    return check_mat

def changeOnehottoVector(leng, vals):
    print vals
    labels= np.argmax(vals,1)
    return labels+1
    

def readWriteFileLines(file_names,dir_path,form='pose'):
    st_str=['in','fl','op','fi','jo','po']

    file_names=[file_name for file_name in file_names if (file_name[:2] in st_str and not file_name.endswith('new.h5'))]
    for file_name in file_names:
        file_path_h5=os.path.join(dir_path,file_name)   

        file_    = h5py.File(file_path_h5, 'r')   # 'r' means that hdf5 file is open in read-only mod
        dataset = file_['data']
        labels = file_['label']

        dataset_mat=dataset[:,:,:,:]
        labels_mat=labels[:]
        
        file_.close()


        labels_mat=changeVectortoOnehot(5, labels_mat)
        new_file_path=os.path.join(dir_path,file_name[:-3]+'_new.h5')
        h_f=createH5File(new_file_path)
        data_set=h_f.create_dataset("data", data=dataset_mat, dtype=float)
        label_set=h_f.create_dataset("label",data=labels_mat, dtype=float)
        h_f.close()


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

def reshapeFileLine(row):
    row_ = row.split(",")[:-1]
    row_= [float(num) for num in row_]
    if(len(row_)!=19800):
        print row_
        #sys.exit()
        return None
    image = np.reshape(np.array(row_), (120, 165))
    return np.array(image)

def processImage(image_a,image_d):

    mask_mat=(image_d==x)
    image_dm=np.ma.masked_array(image_d,mask=mask_mat)
    if (median==True):
        t_h=np.ma.median(image_dm)+10
    else:
        t_h=t_d

    mask_copy_a= np.ones(np.shape(image_a))
    mask_copy_a[image_d > t_h + t_ha] = 0
    image_d[image_d > t_h + t_ha] = 0


    image_a= np.multiply(image_a, mask_copy_a)
    image_a[image_a<t_a] =0

    mask_copy_d= np.ones(np.shape(image_a))
    mask_copy_d[image_a<t_a] =0

    image_a[100:120,:]=0
    #image_a[0:20,120:165]=0
    image_d[100:120,:]=0
    #image_d[0:20,120:165]=0

    return image_a,np.multiply(image_d, mask_copy_d)


def chooselabel(file_name):
    x=1

def saveImages(self):
    self.convertToImage()

    #save

def convertTolabel(file_name,form):
    f_s=file_name[:2]
    options_pos = {'in': 0.0,
               'fl': 1.0,
               'op': 2.0,
               'fi': 3.0,
               'jo': 4.0,
               'be': 5.0,
               'po': 0.0,
               }
    options_gest = {'ac': 0.0,
               'de': 1.0,
               'gr': 2.0,
               'le': 3.0,
               'cl': 4.0,
               'po': 4.0,
               're': 5.0,
               'ri': 6.0,
               }
    if form=='gest':
        return options_gest[f_s]
    elif form== 'pos':
        return options_pos[f_s]
    else :
        print 'incorrect form name, use \'gest\' or \' pose\' '
        sys.exit

def main():
    for person_num in [1,3,4,5,6,7,9,10,11]:
        l='p'+str(person_num)
        form='pose'
        loc= os.path.join(l,form)
        dir_path= os.path.join(DATA_ORIGIN,loc)
        file_names = [f for f in os.listdir(dir_path) if f.endswith('.h5')]
        #file_names=['open_20150414_15_17_57']
        readWriteFileLines(file_names,dir_path,form)


if __name__ == '__main__':
    main()
