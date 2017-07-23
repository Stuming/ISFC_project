# Calculate based on mgh data.
# Input file format: *.mgh (output format: *.mgh)
# the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer

import nibabel as nib
import numpy as np
import os
import array


def show_shape(datadir,sessid,funcname,filename):
    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid
        rundatadir=os.path.join(datadir,sessid,funcname,runid)
        filepath=os.path.join(rundatadir,filename)

        f1=nib.load(filepath)
        print(runid+": ")
        print(f1.get_shape())

def cal_ISFC(data1,data2,vertex,shape):
    i1=vertex
    result=np.zeros((shape[0],1,1))
    temp1=array.array('f')
    temp1.fromlist(data1[i1,0,0,:].tolist()) # np.corrcoef need array as input
    for i2 in range(0,shape[0]):
        if i1==i2:
            result[i2,0,0]=1
            continue
        temp2=array.array('f')
        temp2.fromlist(data2[i2,0,0,:].tolist())
        print(i2)
        result[i2,0,0]=np.corrcoef(temp1,temp2)[0,1] # Get corrcoef from corr matrix
        if np.isnan(result[i2,0,0]):
            result[i2,0,0]=0 # Or use mri_convert to finish this
    return(result)


def cal_ISC(data1,data2,shape):
    result=np.zeros((shape[0],1,1))

    for i in range(0,shape[0]):
        temp1=array.array('f')
        temp1.fromlist(data1[i,0,0,:].tolist()) # np.corrcoef need array as input
        temp2=array.array('f')
        temp2.fromlist(data2[i,0,0,:].tolist())
        print(i)
        result[i,0,0]=np.corrcoef(temp1,temp2)[0,1] # Get corrcoef from corr matrix
        if np.isnan(result[i,0,0]):
            result[i,0,0]=0 # Or use mri_convert to finish this
    return(result)


def load_file(datadir,sessid,funcname,runid,filename):
    rundatadir=os.path.join(datadir,sessid,funcname,runid)
    filepath=os.path.join(rundatadir,filename)
    if not os.path.isfile(filepath):
        print(filepath+" is not a file path, please check!")
        exit(0)

    f=nib.load(filepath)
    return(f)


def match_datashape(f1,f2):
    if f1.get_shape()==f2.get_shape():
        return(1)

    print("The shape of data do not match! ")
    print(f1.get_filename())
    print(f2.get_filename())

    return(0)


def save_result(method_name,result_f,sessid,trg_sessid,runid,vertex_num):
    # method_name refer to "ISFC", "ISC".
    # result_f means result should pass over as file format such as .mgh.
    # trg_sessid used to distinguish which data was used to cal ISFC/ISC with sessid.

    result_path=method_name+"_"+sessid+"_"+trg_sessid+"_"+"run"+runid+"_"+str(vertex_num)+".mgh"
    nib.save(result_f,result_path)

