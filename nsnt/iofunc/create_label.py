import os
import numpy as np
from ..utils.utils import check_dir
from ..utils.adj_tools import get_coords
from surfer.utils import coord_to_label


def cl_nsteps(coord, label_name, output_dir=os.getcwd(), subj_id="fsaverage", hemi="lh", map_surface="inflated",
                 n_steps=10, update=False):
    """
    Create label by coord or vertex within its n_steps.

    Parameters
    ----------
        coord: coord(x, y, z) or vertex(number) that used for creating label.
        label_name: label name used for saving label, final label file name would be:
                    "%s-%s.label" % (label_name, hemi)
        output_dir: set dir to save label, default is current dir.
        subj_id: specify the subject, default is 'fsaverage'.
        hemi: set hemisphere, default is 'lh'.
        map_surface: set map surface, default is 'inflated'.
        n_steps: set to specify the label in n steps range of coord.
        update: set to overwrite output file or not.

    Returns
    -------
        boolean value, 'True' stands for successfully saving labels  into out_dir, 'False' for file exists.
    """
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
        return False
    coord_to_label(subj_id, coord, hemi=hemi, label=label_name, n_steps=n_steps, map_surface=map_surface,
                   coord_as_vert=state)
    return True


def cl_index(data, indexes, output_dir=os.getcwd(), subj_id="fsaverage", hemi="lh", map_surface="inflated",
             update=False):
    """
    Create label by index from atlas file.

    Parameters
    ----------
        data: should be data of atlas file(like van essen map).
        indexes: collection of index, can be dict(with its region name) or list(indexes only).
        output_dir: set dir to save label, default is current dir.
        subj_id: specify the subject, default is 'fsaverage'.
        hemi: set hemisphere, default is 'lh'.
        map_surface: set map surface, default is 'inflated'.
        update: set to overwrite output file or not.
    """
    for index in indexes:
        if isinstance(indexes, dict):
            label_name = "%s-%s.label" % (indexes[index], hemi)
        elif isinstance(indexes, list) or isinstance(indexes, np.ndarray):
            label_name = "%i-%s.label" % (index, hemi)
        else:
            raise Exception("Excepted type of indexes: [dice, list, ndarray], receive: %s" % type(indexes))

        vertex = np.where(data == index)[0]
        cl_vertexes(vertex, label_name=label_name, output_dir=output_dir, subj_id=subj_id, hemi=hemi,
                    map_surface=map_surface, update=update)


def cl_vertexes(vertex_list, label_name, output_dir=os.getcwd(), subj_id="fsaverage", hemi="lh", map_surface="inflated",
                update=False):
    """
    Create label by a set of vertexes.

    Parameters
    ----------
        vertex_list: a set of vertexes that are used to create label.
        label_name: label name used for saving label, final label file name would be:
                    "%s-%s.label" % (label_name, hemi)
        output_dir: set dir to save label, default is current dir.
        subj_id: specify the subject, default is 'fsaverage'.
        hemi: set hemisphere, default is 'lh'.
        map_surface: set map surface, default is 'inflated'.
        update: set to overwrite output file or not.

    Returns
    -------
        boolean value, 'True' stands for successfully saving labels into out_dir, 'False' for file exists.
    """
    check_dir(output_dir)
    print("Output dir is: %s" % output_dir)

    label_path = os.path.join(output_dir, label_name)

    if (not update) and os.path.exists(label_name):
        print("Not updated: %s exists, file is not saved." % label_path)
        return 0

    coords = get_coords(subj_id, hemi, map_surface)

    with open(label_path, "w") as f:
        f.write("%d\n" % len(vertex_list))
        for i in vertex_list:
            x, y, z = coords[i]
            f.write("%d  %f  %f  %f  0.000000\n" % (i, x, y, z))
    return 1
