# Calculate based on mgh data.
# Input file format: *.mgh (output format: *.mgh)
# the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
from scipy import stats
import numpy as np
from array import array
from algorithms.nsnt_fctools import isfc, isc, fc


# TODO get shape from data, or change data to loaded file.
# TODO check input.
# TODO this function's input need to be specified.
def nsnt_fc(method_name, data1, shape, data2=None, vertex_num=None):
    """The shape of data1 and data2(if exist) should be same.
    method_name: 'ISFC', 'ISC', or 'FC'."""
    if method_name=="ISFC":
        return(isfc(data1, data2, vertex_num, shape))
    elif method_name=="ISC":
        return(isc(data1, data2, shape))
    elif method_name=="FC":
        return(fc(data1, vertex_num, shape))
    else:
        raise Exception("Wrong input, please check out.")


def match_datashape(f1,f2):
    """Check if the shape of f1 and f2 is equal."""
    if f1.get_shape()==f2.get_shape():
        return(1)

    print("The shape is not right, please check!")
    print(f1.get_filename())
    print(f2.get_filename())
    return(0)


def corr(array1, array2, method_name="pearson"):
    """Calculate correlation between array1 and array2.
    array1, array2: should be 1-D array, output from nsnt.utils.data_to_array()
    method_name: "pearson" or "spearman" correlation
    If correlation coefficient is nan, then make it 0."""
    if method_name == "pearson":
        r, pval = stats.pearsonr(array1,array2)
    elif method_name == "spearman":
        r, pval =stats.spearmanr(array1,array2)
    else:
        raise Exception("Wrong method name.")
    if np.isnan(r):
        r = 0
    return(r)


def data_to_array(data, i, j=0, k=0):
    """Convert the format(memmap) of the data got from nib.get_data() into array.
    Output is sequence data of index(i,j,k), as array format.
    data: got from nib.get_data();
    i, j, k: the index of data, should be settled based on the data dimension."""
    data_array = array('f')
    data_array.fromlist(data[i,j,k,:].tolist())
    return(data_array)
