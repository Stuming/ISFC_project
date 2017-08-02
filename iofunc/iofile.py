import nibabel as nib
import os

# TODO specify this function
# TODO def load_file(filepath):


def load_imgfile(filepath):
    """Load brain image file, the postfix should be one of ('mgz','mgh','nii','nii.gz')."""
    if not os.path.isfile(filepath):
        raise Exception("File does not exist, please check the path: %s" % filepath)
    if not os.path.basename(filepath).endswith(("mgz","mgh","nii","nii.gz")):
        raise Exception("File suffix should be one of ('mgz','mgh','nii','nii.gz').")
    f = nib.load(filepath)
    return(f)


def load_textfile(filepath):
    """Load text like file, such as global.waveform.dat.
    """
    if not os.path.isfile(filepath):
        raise Exception("File does not exist, please check path: %s" % filepath)
    f = open(filepath, "r")
    data = f.readlines()
    f.close()
    return (data)


# TODO specify this function
def save_img(data_dir, data_type, filename, data, affine):
    """Save data into data_dir/data_type/filename.
    Data is saved as nifti format."""
    filepath = os.path.join(data_dir, data_type, filename)
    data_file = nib.Nifti1Image(data, affine)
    nib.save(data_file, filepath)
    print("Saving %s" % filepath)
