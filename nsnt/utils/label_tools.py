import numpy as np
from NSNT.algorithms.evaltools import dice_matrix


def get_label_contour(labels, faces, medial_wall_label=None):
    """
    Get contour line of labels based on faces.

    Parameters
    ----------
        labels: labels of vertexes, shape = [n_samples].
        faces: triangles mesh of brain surface, shape=(n_mesh, 3).
        medial_wall_label: label number of medial wall of labels, default uses the max label number.

    Returns
    -------
        contour list that contain contour vertexes.

    Notes
    -----
        1. if not specify medial_wall_label, the max label number will be taken as medial_wall_label.
        2. contour of medial_wall_label will be omitted.
    """
    if not medial_wall_label:
        medial_wall_label = np.max(labels)

    label_list = np.unique(labels)
    visited = []
    contour_list = []
    for i, label in enumerate(label_list):
        vertexes = np.where(labels == i)[0]
        for vertex in vertexes:
            visited.append(vertex)

            for neigh in np.unique(faces[np.where(faces == vertex)[0]]):
                if (neigh not in vertexes) and (not labels[neigh] == medial_wall_label):
                    labels[vertex] = medial_wall_label
                    contour_list.append(vertex)
                    break
    return contour_list


def relabel(labels1, labels2, reorder=False, return_matched_number=False):
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
        return_matched_number: return marched number for other analysis, default is False.

    Returns
    -------
        relabels1: cluster labels after relabeling, shape = [n_samples].
                   if 'reorder=True', return labels after reordering.
        relabels2: cluster labels after relabeling, shape = [n_samples].
                   if 'reorder=True', return labels after reordering.
        matched_number: if 'return_matched_number=True', return number of matched labels.

    Notes
    -----
        1. medial wall label should be the max label of labels.
        2. label of medial wall would not be changed, whether reorder or not.
    """
    dice_mat = dice_matrix(labels1, labels2)
    parcel_num = int(np.max(labels1))
    matched_number = 0

    # if dice_mat[i,j]==dice_mat[j,i], this two labels([i,j]) would have same label number.
    for i in range(parcel_num):
        j = np.where(dice_mat[i, :] == np.max(dice_mat[i, :]))[0][0]
        max_dice_vert = np.where(dice_mat[:, j] == np.max(dice_mat[:, j]))[0][0]
        if i == max_dice_vert:
            print("Relabel %i & %i into %i" % (i, j, parcel_num + i))
            labels1[np.where(labels1 == i)] = parcel_num + 1 + i
            labels2[np.where(labels2 == j)] = parcel_num + 1 + i
            matched_number = matched_number + 1
    if reorder:
        labels1_ro = _reorder(labels1, parcel_num)
        labels2_ro = _reorder(labels2, parcel_num)

        if return_matched_number:
            return labels1_ro, labels2_ro, matched_number
        return labels1_ro, labels2_ro

    if return_matched_number:
        return labels1, labels1, matched_number
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
        1. medial wall label should be the max label of labels.
        2. label of medial wall would not be changed, whether reorder or not.
    """
    labels_ro = np.copy(labels)
    i = 0
    j = 0
    for label in np.unique(labels):
        if label >= parcel_num + 1:
            labels_ro[np.where(labels == label)] = i
            i = i + 1
        elif label < parcel_num:
            labels_ro[np.where(labels == label)] = parcel_num - 1 - j
            j = j + 1
        elif label == parcel_num:  # parcel number of medial wall
            continue
        else:
            raise ValueError("Please check value of input 'labels'.")
    print("Number of matched label: %i" % i)
    print("Number of unmatched label: %i" % j)
    return labels_ro
