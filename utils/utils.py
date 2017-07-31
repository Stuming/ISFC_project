# Calculate based on mgh data.
# Input file format: *.mgh (output format: *.mgh)
# the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer

import nibabel as nib
import numpy as np
import os
import array
from algorithms.calculation import cal_ISFC, cal_ISC, cal_FC


# TODO merge cal_ISFC, cal_ISC, cal_FC into one function.
# TODO get shape from data, or change data to loaded file.
# TODO check input.
# TODO this function's input need to be specified.
def do_cal(method_name,data1,shape,data2=None,vertex_num=None):
    """The shape of data1 and data2(if exist) should be same."""
    if method_name=="ISFC":
        return(cal_ISFC(data1,data2,vertex_num,shape))
    elif method_name=="ISC":
        return(cal_ISC(data1,data2,shape))
    elif method_name=="FC":
        return(cal_FC(data1,vertex_num,shape))
    else:
        print("Wrong input, please check out.")
        exit(0)


def match_datashape(f1,f2):
    """Check if the shape of f1 and f2 is equal."""
    if f1.get_shape()==f2.get_shape():
        return(1)

    print("The shape is not right, please check!")
    print(f1.get_filename())
    print(f2.get_filename())
    return(0)

