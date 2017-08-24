"""Calculate different types of functional correlation that maybe useful in natural stimulus analysis.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to display by pysurfer.
isfc: Inter-subject functional correlation.
isc: Inter-subject correlation.
fc: Functional correlation.
"""
import numpy as np
from utils.utils import corr, data_to_array


# TODO refactor code to match nifti data(change index of var 'shape').
def isfc(data1, data2, vertex_num, shape):
    """Cal ISFC between vertex_num in data1 and all vertexs in data2.
    data1, data2: brain image data.
    vertex_num: the vertex in data1 used to cal isfc.
    shape: the shape of data1 and data2 should be the same."""
    result = np.zeros((shape[0], 1, 1))
    array1 = data_to_array(data1, vertex_num)  # TODO this only match mgh format, not match nifti.

    for i in range(0,shape[0]):
        array2 = data_to_array(data2, i)
        result[i, 0, 0] = corr(array1, array2)
    return result


# TODO refactor code to match nifti data(change index of var 'shape').
def isc(data1, data2, shape):
    """Cal ISC between data1 and data2 vertex by vertex.
    data1, data2: brain image data.
    shape: the shape of data1 and data2 should be the same."""
    result = np.zeros((shape[0], 1, 1))

    for i in range(0, shape[0]):
        array1 = data_to_array(data1, i)
        array2 = data_to_array(data2, i)
        result[i, 0, 0] = corr(array1, array2)
    return result


# TODO refactor code to match nifti data(change index of var 'shape').
def fc(data, vertex_num, shape):
    """Cal functional connectivity between vertex_num and other vertex in data.
    data: brain image data.
    vertex_num: the vertex in data1 used to cal isfc.
    shape: the shape of input data."""
    result = np.zeros((shape[0], 1, 1))
    array1 = data_to_array(data, vertex_num)

    for i in range(0, shape[0]):
        array2 = data_to_array(data, i)
        result[i, 0, 0] = corr(array1, array2)
    return result
