import os

import numpy as np
import nibabel as nib

# TODO specify this function
# TODO def save_data function for saving data.


def load_data(filepath, npz_key='arr_0'):

    assert os.path.isfile(filepath), '"filepath" is invalid, please check.'

    print("Loading: %s" % filepath)
    filename = os.path.basename(filepath)
    nifti_file = ('.mgz', '.mgh', '.nii', '.nii.gz')

    if filename.endswith(nifti_file):
        data = nib.load(filepath).get_data()
        if data.ndim > 2 and (data.shape[1] == 1, data.shape[2] == 1):
            return data[:, 0, 0]
        return data

    if filename.endswith('.annot'):
        data = nib.freesurfer.read_annot(filepath)[0]
        return data

    if filename.endswith('.npz'):
        data = np.load(filepath)[npz_key]
        return data

    if filename.endswith('.label.gii'):
        data = nib.load(filepath).darrays[0].data
        return data

    raise ValueError('filepath is invalid')


# TODO specify this function
def save_img(data_dir, data_type, filename, data, affine):
    """Save data into data_dir/data_type/filename.
    Data is saved as nifti format."""
    result_dir = os.path.join(data_dir, data_type)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    filepath = os.path.join(result_dir, filename)
    data_file = nib.Nifti1Image(data, affine)
    nib.save(data_file, filepath)
    print("Saving %s" % filepath)
