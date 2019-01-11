"""
Calculate based on mgh data.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
"""
import os
import re
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


def change_subid(subid, target):
    """
    Change subid prefix to match different data dir name.

    Parameters
    ----------
    subid: id of subject, used in dir name.
    target: change prefix of subid to target.

    Return
    ------
    New id of subject with target as prefix.

    Example
    -------
    >>> change_subid('S001', 'sub')
    'sub001'
    >>> change_subid('sub001', 'S')
    'S001'
    """
    prefix = {'S': 'sub', 'sub': 'S'}
    assert target in prefix, 'target should be "sub" or "S"!'
    return re.sub(prefix[target], target, subid)


def make_subid(prefix, num, digits=0):
    """
    Make subid by num and prefix, if length of num
    is shorter than digits, the extra digits will
    be filled with '0'.

    Parameters
    ----------
    prefix: change prefix of subid to target, string.
    num: id of subject, used in dir name, int or string.
    digits: digits of num, if digits is lower than the length of num,
            no 0 will be add. Default is 0, int.

    Return
    ------
    New id of subject formed as prefix+num, with digits of num.

    Example
    -------
    >>> make_subid('sub', 1, 3)
    'sub001'
    >>> make_subid('S', 1, 3)
    'S001'
    """
    s = str(num)
    while len(s) < digits:
        s = '0' + s
    return str(prefix) + s


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


def apply_1d_mask(data, mask):
    """
    Apply 1 dimension mask onto data.

    Parameters
    ----------
    data: array or sequence, length of its first dim should b equal to length of mask.
    mask: binary array, 1 for region of interest and 0 for others, shape=(n_vertices,).

    Return
    ------
    data: array or sequence after masked.
    """
    if mask is None:
        return data

    if np.any(mask < 0) or np.any(mask > 1):
        raise ValueError('value of mask should be 0 or 1.')
    if np.ndim(mask) != 1:
        mask = np.reshape(mask, (-1))
    return np.copy(data[np.where(mask == 1)])