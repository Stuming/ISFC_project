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

# TODO merge cal_ISFC, cal_ISC, cal_FC into one function.
# TODO get shape from data, or change data to loaded file.
# TODO check input.
# TODO this function input need to be specified.
def do_cal(method_name,data1,shape,data2=None,vertex_num=None):
    # The shape of data1 and data2(if exist) should be same.

    if method_name=="ISFC":
        return(cal_ISFC(data1,data2,vertex_num,shape))
    elif method_name=="ISC":
        return(cal_ISC(data1,data2,shape))
    elif method_name=="FC":
        return(cal_FC(data1,vertex_num,shape))
    else:
        print("Wrong input, please check out.")
        exit(0)

def cal_ISFC(data1,data2,vertex_num,shape):
    # Cal ISFC between vertex_num in data1 and all vertexs in data2.
    i1=vertex_num
    result=np.zeros((shape[0],1,1))
    temp1=array.array('f')
    temp1.fromlist(data1[i1,0,0,:].tolist()) # np.corrcoef need array as input
    for i2 in range(0,shape[0]):
        temp2=array.array('f')
        temp2.fromlist(data2[i2,0,0,:].tolist())
        print(i2)
        result[i2,0,0]=np.corrcoef(temp1,temp2)[0,1] # Get corrcoef from corr matrix
        if np.isnan(result[i2,0,0]):
            result[i2,0,0]=0 # Or use mri_convert to finish this
    return(result)


def cal_ISC(data1,data2,shape):
    # Cal ISC between data1 and data2 per vertex.
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

def cal_FC(data,vertex_num,shape):
    # Cal functional connectivity between vertex_num and other vertex in data.
    result=np.zeros((shape[0],1,1))
    temp1=array.array('f')
    temp1.fromlist(data[vertex_num,0,0,:].tolist()) # np.corrcoef need array as input

    for i in range(0,shape[0]):
        temp2=array.array('f')
        temp2.fromlist(data[i,0,0,:].tolist())
        print(i)
        result[i,0,0]=np.corrcoef(temp1,temp2)[0,1] # Get corrcoef from corr matrix
        if np.isnan(result[i,0,0]):
            result[i,0,0]=0 # Or use mri_convert to finish this
    return(result)


# TODO specify this function
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


# TODO specify this function
def save_result(method_name,result_f,sessid,trg_sessid,runid,vertex_num):
    # method_name refer to "ISFC", "ISC".
    # result_f means result should pass over as file format such as .mgh.
    # trg_sessid used to distinguish which data was used to cal ISFC/ISC with sessid.

    result_path="results/"+method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)+".mgh"
    nib.save(result_f,result_path)

