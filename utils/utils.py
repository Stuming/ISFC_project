# Calculate based on mgh data.
# Input file format: *.mgh (output format: *.mgh)
# the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
import os
from scipy import stats
import numpy as np


def match_datashape(f1,f2):
    """Check if the shape of f1 and f2 is equal."""
    if f1.get_shape() == f2.get_shape():
        return 1

    print("The shape is not right, please check!")
    print(f1.get_filename())
    print(f2.get_filename())
    return 0


def corr(array1, array2, method_name="pearson"):
    """Calculate correlation between array1 and array2.
    array1, array2: should be 1-D array, output from nsnt.utils.data_to_array()
    method_name: "pearson" or "spearman" correlation
    If correlation coefficient is nan, then make it 0."""
    if method_name == "pearson":
        r, pval = stats.pearsonr(array1, array2)
    elif method_name == "spearman":
        r, pval = stats.spearmanr(array1, array2)
    else:
        raise Exception("Wrong correlation method name: %s." % method_name)
    if np.isnan(r):
        r = 0
    return r


def data_to_array(data, i=None, j=0, k=0):
    # TODO modify it to adapt .nii data.
    """Convert the format(memmap) of the data got from nib.get_data() into array.
    Output is sequence data of index(i,j,k), as array format.
    data: got from nib.get_data();
    i, j, k: the index of data, should be settled based on the data dimension."""
    if i is None:
        data_array = np.asarray(data)
    else:
        data_array = np.asarray(data[i, j, k, :])
    return data_array


def check_list(list_data):
    """ Check list_data's type, if waveform read from file, then element in list would be string and have "\n",
    which should be striped.
    If waveform get from calculation, then element in list would be a number, and just return it.
    """
    if isinstance(list_data, list):
        num = list_data[0]
        if isinstance(num, str):
            list_data = [num.rstrip("\n") for num in list_data]
    return list_data


def check_dir(dirpath, new=True):
    """Check whether dirpath exists, and create it if needed.
    dirpath: input path used to check.
    new: make dir if not exists.
    :return: 0 for dir not exists(not found or not created)
             1 for dir exists."""
    if not os.path.exists(dirpath):
        if not new:
            print("%s is not found." % dirpath)
            return 0
        print ("Creating dir: %s" % dirpath)
        os.makedirs(dirpath)
    return 1
