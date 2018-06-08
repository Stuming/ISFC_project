"""
Calculate based on mgh data.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
"""
import os
import functools
from time import time

import numpy as np


def running_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print("Running {}".format(func.__name__))
        t0 = time()
        p = func(*args, **kw)
        print("Spend time: %f" % (time() - t0))
        return p
    return wrapper


def check_list(list_data):
    """
    Check type of list_data.
    If list_data is read from text file(eg. waveforms), then element in list would be string and have `\n`,
        which should be striped.
    If list_data is got from calculation, then element in list would be numbers.

    Parameters
    ----------
    list_data: input data that needs to be checked.

    Return
    ------
    list_data: data without `\n` in it.
    """
    if isinstance(list_data, list):
        if isinstance(list_data[0], str):
            list_data = [np.double(num.rstrip("\n")) for num in list_data]
    return list_data


def check_dir(dirpath, new=True):
    """
    Check whether dirpath exists, and create it if `new == True`.

    Parameters
    ----------
    dirpath: input path which needs to be checked.
    new: default is True, which stands for making dir if dirpath does not exist.

    Return
    ------
    boolean value, return 0 for dir not exists(not found or not created), otherwise return 1.
    """
    if not os.path.exists(dirpath):
        if not new:
            print("%s is not found." % dirpath)
            return 0
        print ("Creating dir: %s" % dirpath)
        os.makedirs(dirpath)
    return 1


def mk_rand_lut(row, rand_range=(0, 255), alpha=255):
    """
    Make random lookup table, use as colormap.

    Parameters
    ----------
    row: set number of colors in lut
    rand_range: set extent of lut value.
    alpha: opacity, range from 0 to 255.

    Return
    ------
    ltable: an (row, 4) shaped lookup table.
    """
    ltable = np.zeros([row, 4])
    for i in range(row):
        ltable[i, 0] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 1] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 2] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 3] = alpha
    return ltable
