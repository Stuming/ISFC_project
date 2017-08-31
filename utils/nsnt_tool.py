# TODO get shape from data, or change data to loaded file.
# TODO check input.
# TODO this function's input need to be specified.
from algorithms.fctools import isfc, isc, fc


def nsnt_fc(method_name, data1, shape, data2=None, vertex_num=None):
    """The shape of data1 and data2(if exist) should be same.
    method_name: 'ISFC', 'ISC', or 'FC'."""
    if method_name == "ISFC":
        return isfc(data1, data2, vertex_num, shape)
    elif method_name == "ISC":
        return isc(data1, data2, shape)
    elif method_name == "FC":
        return fc(data1, vertex_num, shape)
    else:
        raise Exception("Wrong input, please check out.")