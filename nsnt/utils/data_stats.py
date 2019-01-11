"""Display value info about data."""
import numpy as np


def data_stats(data):
    """
    Print stats about data, used for formatting output.

    Parameters
    ----------
    data: should be array or list.
    """
    # f.get_data()  std(), min(), max(), mean(), argmax(), any(), unique(), bincount()
    # FIXME argmax may get huge index bigger than data shape.
    print("Max value: %.2f" % np.max(data)+"  index: %i" % np.argmax(data))
    print("Min value: %.2f" % np.min(data)+"  index: %i" % np.argmin(data))
    print("Mean value: %.2f" % np.mean(data))
    print("Std: %.2f" % np.std(data))
    # if data.any(None):
    #     print("The data has nan value, please check out.")


def del_zeros(data, show_zeros=False):
    """
    Check and split zeros in column of data.

    Parameters
    ----------
    data: 2-dimension array.
    show_zeros: whether to show zeros list, default is 'False'.

    Returns
    -------
    data1: data after delete zeros.
    zeros: indexes of zero column.
    """
    # TODO check dimension of data
    zeros = np.where(~data.any(axis=1))[0]
    if show_zeros:
        print(zeros)
    data1 = np.delete(data, zeros, axis=0)
    del_num = data.shape[0] - data1.shape[0]
    print("Delete %i vertexes from data." % del_num)
    return data1, zeros


def remove_outlier(data, thr=(-3, 3), flatten_order='F'):
    """
    Check data and remove/replace values that out of 3 times std.

    Parameters
    ----------
    data: array data.
    thr: define range of outlier
    flatten_order: define flatten order, 'C' for row-major, 'F' for column-order, or preserve C/F order from 'a'.
                    see more detail:
                        a = numpy.array([])
                        help(a.flatted)

    Returns
    -------
    result: data after removing outlier, with the same shape of the input.
    outlier_index: index of outliers.

    Notes
    -----
    1. this function remove outlier by average values locate both side of outlier index,
        and flatten data(by numpy.flatted()) before remove outlier.
    """
    # TODO make param `axis` work, which means remove outlier by row or column.
    axis = None

    result = np.copy(data)
    shape = result.shape

    dmean = np.mean(result, axis=axis)
    dstd = np.std(result, axis=axis)

    outlier_bool = (result < (dmean + thr[0] * dstd)) | (result > (dmean + thr[1] * dstd))
    outlier_bool = np.array(outlier_bool).flatten(flatten_order)
    result = result.flatten(flatten_order)
    outlier = np.where(outlier_bool)

    # FIXME if two outliers have close index, then average order would effect the result,
    # FIXME in another word, same outlier value may get different result(effected by its position).
    for i in outlier[0]:
        try:
            result[i] = (result[i-1] + result[i+1]) / 2
        except:
            result[i] = (result[i-1] + result[0]) / 2

    outlier_bool_rs = outlier_bool.reshape(shape, order=flatten_order)
    outlier_index = np.where(outlier_bool_rs)
    result = result.reshape(shape, order=flatten_order)

    return result, outlier_index
