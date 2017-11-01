"""
Calculate based on mgh data.
Input file format: *.mgh (output format: *.mgh)
the input file(*.mgh) is converted from *.nii.gz file, in order to visualisation by pysurfer
"""
import os
import numpy as np
from NSNT.algorithms.evaltools import dice_matrix


def match_datashape(data1, data2):
    """
    Check if the shape of data1 and data2 is equal.

    Parameters
    ----------
        data1: data that should be checked .
        data2: data that should be checked.

    Returns
    -------
        boolean value, `True` stands for match, `False` stands for mismatch.
    """
    if data1.get_shape() == data2.get_shape():
        return True
    return False


def corr(array1, array2, method_name="pearson"):
    """
    Calculate correlation between array1 and array2.

    Parameters
    ----------
        array1: 1-D array
        array2: 1-D array
        method_name: `pearson` or `spearman` correlation

    Returns
    -------
        r: correlation coefficient of array1 and array2.

    Notes
    -----
        1. if correlation coefficient is nan, then it would be assigned to 0.
    """
    from scipy import stats

    if method_name == "pearson":
        r, pval = stats.pearsonr(array1, array2)
    elif method_name == "spearman":
        r, pval = stats.spearmanr(array1, array2)
    else:
        raise Exception("Wrong correlation method name: %s." % method_name)
    if np.isnan(r):
        r = 0
    return r


def check_list(list_data):
    """
    Check type of list_data.
    If list_data is read from text file(eg. waveforms), then element in list would be string and have `\n`,
        which should be striped.
    If list_data is got from calculation, then element in list would be numbers.

    Parameters
    ----------
        list_data: input data that needs to be checked.

    Returns
    -------
        list_data: data without `\n` in it.
    """
    if isinstance(list_data, list):
        num = list_data[0]
        if isinstance(num, str):
            list_data = [num.rstrip("\n") for num in list_data]
    return list_data


def check_dir(dirpath, new=True):
    """
    Check whether dirpath exists, and create it if `new == True`.

    Parameters
    ----------
        dirpath: input path which needs to be checked.
        new: default is True, which stands for making dir if dirpath does not exist.

    Returns
    -------
        boolean value, return 0 for dir not exists(not found or not created), otherwise return 1.
    """
    if not os.path.exists(dirpath):
        if not new:
            print("%s is not found." % dirpath)
            return 0
        print ("Creating dir: %s" % dirpath)
        os.makedirs(dirpath)
    return 1


def mk_rand_lut(row, rand_range=(0, 255), alpha=255):
    """
    Make random lookup table, use as colormap.

    Parameters
    ----------
        row: set number of colors in lut
        rand_range: set extent of lut value.
        alpha: opacity, range from 0 to 255.

    Returns
    -------
        ltable: an (row, 4) shaped lookup table.
    """
    ltable = np.zeros([row, 4])
    for i in range(row):
        ltable[i, 0] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 1] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 2] = np.random.randint(rand_range[0], rand_range[1])
        ltable[i, 3] = alpha
    return ltable


def get_label_contour(labels, faces, contour_label=None):
    """
    Get contour line of labels based on faces.
    Parameters
    ----------
        labels: labels of vertexes, shape = (n, 1), n is number of vertexes.
        faces: triangles mesh of brain surface, shape=(n_mesh, 3).
        contour_label: set label to contour line.

    Returns
    -------
        labels with contour line.

    Notes
    -----
        1. the max label number in labels should be assigned to the medial wall.
        2. data with the max label number will be omitted.
        3. contour line would be setting to the same label as medial wall by default.
    """
    n_vertexes = np.max(labels)
    if not contour_label:
        contour_label = n_vertexes

    visited = []
    for i in range(n_vertexes):
        vertexes = np.where(labels == i)[0]
        for vertex in vertexes:
            visited.append(vertex)

            for neigh in np.unique(faces[np.where(faces == vertex)[0]]):
                if (neigh not in vertexes) and (not labels[neigh] == contour_label):
                    labels[vertex] = contour_label
                    break
    return labels


def relabel(labels1, labels2, reorder=False):
    """
    Relabel labels1 and labels2 to make two most overlapped labels have the same label number,
      new_label_number = parcel_num + label_number of labels1,
      otherwise label number would be kept.

    Judging whether overlapped:
      If a label in labels1 has max dice coef with the label in labels, and vice versa, then
      these two labels would be judged as the most overlapped label.

    Parameters
    ----------
        labels1: cluster labels, shape = [n_samples].
        labels2: cluster labels, shape = [n_samples].
        reorder: since relabel makes label number discontinuous and same label number may not
                 be able to have the same color in colormap, it would be helpful to reorder
                 label number before display.
                 Reorder makes label number grow from 0 if two labels are same, otherwise
                 reduces from 'parcel_num - 1'.

    Returns
    -------
        relabels1: cluster labels after relabeling, shape = [n_samples].
        relabels2: cluster labels after relabeling, shape = [n_samples].

    Notes
    -----
        1. Label of medial wall would not be changed, whether reorder or not.
    """
    dice_mat = dice_matrix(labels1, labels2)
    parcel_num = int(np.max(labels1))

    # if dice_mat[i,j]==dice_mat[j,i], this two labels([i,j]) would have same label number.
    for i in range(parcel_num):
        j = np.where(dice_mat[i, :] == np.max(dice_mat[i, :]))[0][0]
        max_dice_vert = np.where(dice_mat[:, j] == np.max(dice_mat[:, j]))[0][0]
        if i == max_dice_vert:
            print("Relabel %i & %i into %i" % (i, j, parcel_num + i))
            labels1[np.where(labels1 == i)] = parcel_num + 1 + i
            labels2[np.where(labels2 == j)] = parcel_num + 1 + i
    if reorder:
        labels1_ro = _reorder(labels1, parcel_num)
        labels2_ro = _reorder(labels2, parcel_num)
        return labels1_ro, labels2_ro
    return labels1, labels1


def _reorder(labels, parcel_num):
    """
    Since relabel makes label number discontinuous and same label number may not be able to
      have the same color in colormap, it would be helpful to reorder label number before display.
      Reorder makes label number grow from 0 if two labels are same(label number > parcel_num),
      otherwise(label number < parcel_num) reduces from 'parcel_num - 1'.

    Parameters
    ----------
        labels: cluster labels, shape = [n_samples].
        parcel_num: number of labels, which equal to label number of medial wall.

    Returns
    -------
        labels_ro: cluster labels after reordering, shape = [n_samples].

    Notes
    -----
        1. Label of medial wall would not be changed, whether reorder or not.
    """
    label_num = np.unique(labels)
    labels_ro = np.copy(labels)
    i = 0
    j = 0
    for label in label_num:
        if label >= parcel_num + 1:
            labels_ro[np.where(labels == label)] = i
            i = i + 1
        else:
            labels_ro[np.where(labels == label)] = parcel_num - 1 - j
            j = j + 1
    print("Number of matched label: %i" % i)
    print("Number of unmatched label: %i" % j)
    return labels_ro
