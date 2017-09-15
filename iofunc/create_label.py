import os
import numpy as np
import nibabel as nib
from utils.utils import check_dir
from surfer import utils
from surfer.utils import Surface


def cl_nsteps(coord, label_name, output_dir=os.getcwd(), subj_id="fsaverage", hemi="lh", map_surface="white",
                 n_steps=10, update=False):
    """Create label by coord or vertex within its n_steps.
    coord: coord(x, y, z) or vertex(number) that used for creating label.
    label_name: label name used for saving label, final label file name would be:
        "%s-%s.label" % (label_name, hemi)
    output _dir: set dir to save label, default is current dir.
    subj_id: specify the subject, default is fsaverage.
    hemi: set hemisphere, default is lh.
    map_surface: set map surface, default is white.
    n_steps: set to specify the label in n steps range of coord.
    update: set to overwrite output file or not."""
    if isinstance(coord, int):
        state = True
    elif isinstance(coord, list):
        state = False
    else:
        raise Exception("Please check your coord!")

    try:
        check_dir(output_dir, new=True)
        os.chdir(output_dir)
        print("Output dir is: %s" % output_dir)
    except:
        raise Exception("Please check output_dir: %s" % output_dir)

    label_file = "%s-%s.label" % (label_name, hemi)
    if (not update) and os.path.exists(label_file):
        print("Not updated: %s exists, file is not saved." % label_file)
        return 0
    utils.coord_to_label(subj_id, coord, hemi=hemi, label=label_name, n_steps=n_steps, map_surface=map_surface,
                         coord_as_vert=state)
    return 1


def cl_index(filepath, index_dict, output_dir=os.getcwd(), update=False):
    """Create label by index from atlas file.
    filepath: should be atlas file path(like van essen map).
    index_dict: dict that contain index and its region name.
    output _dir: set dir to save label, default is current dir.
    update: set to overwrite output file or not."""
    check_dir(output_dir)
    print("Output dir is: %s" % output_dir)

    for index in index_dict:
        label_name = "%s.label" % index_dict[index]
        label_path = os.path.join(output_dir, label_name)

        if (not update) and os.path.exists(label_name):
            print("Not updated: %s exists, file is not saved." % label_path)
            continue

        vertex = get_vertexes(filepath, index)
        geo = Surface("fsaverage", "lh", "inflated")
        geo.load_geometry()

        with open(label_path, "w") as f:
            f.write("%d\n" % len(vertex))
            for i in vertex[0]:
                x, y, z = geo.coords[i]
                f.write("%d  %f  %f  %f  0.000000\n" % (i, x, y, z))


def get_vertexes(file_path, index):
    """Get vertexes by index in atlas file."""
    f = nib.load(file_path)
    img = f.get_data()[:,0,0]
    vertex = np.where(img == index)
    return vertex
