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


def check_zeros(f_img, num=0, show_index=True):
    """Check if `num` in column of f_img.
    f_img should be .mgz format, since `data = f_img.get_data()[:, 0, 0, :]`
    show_index decide whether return index list or not."""
    # TODO modify func to make para `num` work
    data = f_img.get_data()[:, 0, 0, :]
    zeroindex = np.where(~data.any(axis=1))[0]
    sum = len(zeroindex)
    if show_index:
        return zeroindex, sum
    return sum
