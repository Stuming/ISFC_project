"""Calculate different types of functional correlation that maybe useful in natural stimulus analysis.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to display by pysurfer.
isfc: Inter-subject functional correlation.
isc: Inter-subject correlation.
fc: Functional correlation.
"""
import numpy as np
from scipy.spatial.distance import cdist, pdist
from utils.utils import corr, data_to_array


# TODO refactor code to match nifti data(change index of var 'shape').
def isfc(data1, data2):
    """Cal ISFC between data1 and data2.
    data1, data2: matrix data, if data1 or data2 is 1-dimensional, then change it to 2-dimensional data.
    """
    if data1.shape == 1:
        data1 = np.array(data1, ndmin=2)
    if data2.shape == 1:
        data2 = np.array(data2, ndmin=2)
    return 1 - cdist(data1, data2, metric='correlation')


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
def wsfc(data):
    """Cal within subject functional connectivity of data.
    data: brain image data.
    vertex_num: the vertex in data1 used to cal isfc, default is None, means cal fc matrix.
    """
    # TODO pdist seems return different value compared to cdist, so use cdist.
    return isfc(data, data)
