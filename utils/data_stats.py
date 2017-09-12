"""Display value info about data."""


def data_stats(f_img):
    """Print stats about data in f_img, and f_img should be got from nib.load()"""
    # f.get_data()  std(), min(), max(), mean(), argmax(), any()
    data = f_img.get_data()
    print("Data shape: " + str(f_img.get_shape()))
    # FIXME argmax may get huge index bigger than data shape.
    print("Max value: %.2f" % data.max()+"  index: %i" % data.argmax())
    print("Min value: %.2f" % data.min()+"  index: %i" % data.argmin())
    print("Mean value: %.2f" % data.mean())
    print("Std: %.2f" % data.std())
    # if data.any(None):
    #     print("The data has nan value, please check out.")
