"""Display value info about data."""
import numpy as np


def data_stats(f_img):
    """Print stats about data in f_img, and f_img should be got from nib.load()"""
    # f.get_data()  std(), min(), max(), mean(), argmax(), any()
    data = f_img.get_data()
    print("Data shape: " + str(f_img.get_shape()))
    # FIXME argmax may get huge index bigger than data shape.
    print("Max value: %.2f" % np.max(data)+"  index: %i" % np.argmax(data))
    print("Min value: %.2f" % np.min(data)+"  index: %i" % np.argmin(data))
    print("Mean value: %.2f" % np.mean(data))
    print("Std: %.2f" % np.std(data))
    # if data.any(None):
    #     print("The data has nan value, please check out.")


def del_zeros(data, show_zeros=False):
    """Check if zeros in column of data.
    data: 2-dimension array.
    show_zeros: whether to show zeros list.
    return:
        data1: data after delete zeros.
        zeros: indexes of zero column."""
    # TODO modify func to make para `num` work
    zeros = np.where(~data.any(axis=1))[0]
    if show_zeros:
        print(zeros)
    data1 = np.delete(data, zeros, axis=0)
    del_num = data.shape[0] - data1.shape[0]
    print("Delete %i vertexes from data." % del_num)
    return data1, zeros
