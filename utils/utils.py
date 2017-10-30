"""
Calculate based on mgh data.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
"""
import os
import numpy as np


def match_datashape(data1, data2):
    """
    Check if the shape of data1 and data2 is equal.

    Parameters
    ----------
        data1: data that should be checked .
        data2: data that should be checked.

    Returns
    -------
        boolean value, `True` stands for match, `False` stands for mismatch.
    """
    if data1.get_shape() == data2.get_shape():
        return True
    return False


def corr(array1, array2, method_name="pearson"):
    """
    Calculate correlation between array1 and array2.

    Parameters
    ----------
        array1: 1-D array
        array2: 1-D array
        method_name: `pearson` or `spearman` correlation

    Returns
    -------
        r: correlation coefficient of array1 and array2.

    Notes
    -----
        1. if correlation coefficient is nan, then it would be assigned to 0.
    """
    from scipy import stats

    if method_name == "pearson":
        r, pval = stats.pearsonr(array1, array2)
    elif method_name == "spearman":
        r, pval = stats.spearmanr(array1, array2)
    else:
        raise Exception("Wrong correlation method name: %s." % method_name)
    if np.isnan(r):
        r = 0
    return r


def check_list(list_data):
    """
    Check type of list_data.
    If list_data is read from text file(eg. waveforms), then element in list would be string and have `\n`,
        which should be striped.
    If list_data is got from calculation, then element in list would be numbers.

    Parameters
    ----------
        list_data: input data that needs to be checked.

    Returns
    -------
        list_data: data without `\n` in it.
    """
    if isinstance(list_data, list):
        num = list_data[0]
        if isinstance(num, str):
            list_data = [num.rstrip("\n") for num in list_data]
    return list_data


def check_dir(dirpath, new=True):
    """
    Check whether dirpath exists, and create it if `new == True`.

    Parameters
    ----------
        dirpath: input path which needs to be checked.
        new: default is True, which stands for making dir if dirpath does not exist.

    Returns
    -------
        boolean value, return 0 for dir not exists(not found or not created), otherwise return 1.
    """
    if not os.path.exists(dirpath):
        if not new:
            print("%s is not found." % dirpath)
            return 0
        print ("Creating dir: %s" % dirpath)
        os.makedirs(dirpath)
    return 1


def mk_rand_lut(row, rand_range=(0,255), alpha=255):
    """
    Make random lookup table, use as colormap.

    Parameters
    ----------
        row: set number of colors in lut
        rand_range: set extent of lut value.
        alpha: opacity, range from 0 to 255.

    Returns
    -------
        ltable: an (row, 4) shaped lookup table.
    """
    ltable = np.zeros([row, 4])
    for i in range(row):
        ltable[i, 0] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 1] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 2] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 3] = alpha
    return ltable

