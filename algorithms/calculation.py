"""Calculate based on mgh data.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer.
"""
# TODO refactor code to match nifti data.

import nibabel as nib
import numpy as np
import os
import array


def cal_ISFC(data1, data2, vertex_num, shape):
    """Cal ISFC between vertex_num in data1 and all vertexs in data2."""
    i1=vertex_num
    result=np.zeros((shape[0],1,1))
    array1=data_to_array(data1,i1) # TODO this only match mgh format, not match nifti.

    for i2 in range(0,shape[0]):
        array2=data_to_array(data2,i2)
        result[i2,0,0]=do_corrcoef(array1,array2)
    return(result)


def cal_ISC(data1, data2, shape):
    """Cal ISC between data1 and data2 per vertex."""
    result=np.zeros((shape[0],1,1))

    for i in range(0,shape[0]):
        array1=data_to_array(data1,i)
        array2=data_to_array(data2,i)
        result[i,0,0]=do_corrcoef(array1,array2)
    return(result)


def cal_FC(data, vertex_num, shape):
    """Cal functional connectivity between vertex_num and other vertex in data."""
    result=np.zeros((shape[0],1,1))
    array1=data_to_array(data,vertex_num)

    for i in range(0,shape[0]):
        array2=data_to_array(data,i) 
        result[i,0,0]=do_corrcoef(array1,array2)
    return(result)


def data_to_array(data, i, j=0, k=0):
    """Convert data format(memmap) from nib.get_data() into array.
    The function np.corrcoef need array as input."""
    data_array=array.array('f')
    data_array.fromlist(data[i,j,k,:].tolist())
    return(data_array)


def do_corrcoef(array1, array2):
    """Calculate corrcoef between array1 and array2.
    If corrcoef is nan, then take it as 0."""
    temp=np.corrcoef(array1,array2)[0,1] # Get corrcoef from corr matrix
    if np.isnan(temp): # Prevent nan in result.
        temp=0
    return(temp)

