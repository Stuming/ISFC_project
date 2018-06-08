"""
Used to evaluate clusters or parcellations.
"""
import numpy as np

from nsnt.algorithms.fctools import wsfc
from nsnt.utils.adj_tools import nonconnected_labels


def ari(labels1, labels2):
    """
    Calculate adjusted rand index(ARI) of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].

    Returns
    -------
    ARI: ranges from (-1.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    from sklearn.metrics.cluster import adjusted_rand_score

    return adjusted_rand_score(labels1, labels2)


def ami(labels1, labels2):
    """
    Calculate adjusted mutual information(AMI) of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].

    Returns
    -------
    AMI: ranges from (0.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    from sklearn.metrics.cluster import adjusted_mutual_info_score

    return adjusted_mutual_info_score(labels1, labels2)


def homogeneity(data, labels):
    """
    Calculate homogeneity of labels based on its data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].

    Returns
    -------
    label_list: a sorted array that contain labels.
    homo_list: homogeneity list that corresponding to label_list.

    Notes
    -----
    1. the max number of labels should be assigned to the medial wall.
    2. data with the max label number will be omitted.
    """
    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels which may lead to nan in result.
    label_list = np.unique(labels)
    homo_list = np.zeros_like(label_list, dtype=np.float64)

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        vert_num = vert_list.shape[0]
        fcmap = np.nan_to_num(wsfc(data[vert_list, :]))
        if vert_num == 1:  # some labels may be assigned to only one vertex.
            homo_list[i] = 1
        else:
            # ((np.sum(fcmap) - vert_num) / 2) / (vert_num * (vert_num - 1) / 2)
            homo_list[i] = (np.sum(fcmap) - vert_num) / (vert_num * (vert_num - 1))
    return label_list, homo_list


def dice_matrix(labels1, labels2):
    """
    Calculate dice similarity coefficient matrix of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].

    Returns
    -------
    dice_mat: array, ranges from (0, 1), shape = (label_number1, label_number2).

    Notes
    -----
    1. the max label number in labels should be assigned to the medial wall.
    2. data with the max label number will be omitted.
    """
    from scipy.spatial.distance import dice

    row_num, column_num = np.int(np.max(labels1)), np.int(np.max(labels2))
    dice_mat = np.zeros((row_num, column_num))
    for i in range(row_num):
        for j in range(column_num):
            dice_mat[i, j] = 1 - dice(labels1 == i, labels2 == j)  # dice() measures dice dissimilarity
    return np.nan_to_num(dice_mat)


def dice_coef(labels1, labels2):
    """
    Calculate mean dice similarity coefficient of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].

    Returns
    -------
    dice_coefficient: float, reflects mean dice similarity coefficient, ranges from (0.0, 1.0).

    Notes
    -----
    1. the max label number in labels should be assigned to the medial wall.
    2. data with the max label number will be omitted.
    """
    dice_mat = dice_matrix(labels1, labels2)
    row_max, column_max = np.max(dice_mat, axis=0), np.max(dice_mat, axis=1)
    dice_coefficient = (np.mean(row_max) + np.mean(column_max)) / 2
    return dice_coefficient


def silhouette_coef(data, labels):
    """
    Calculate silhouette coefficient of the inputs.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].

    Returns
    -------
    silhouette coefficient
    """
    from sklearn.metrics.cluster import silhouette_score

    return silhouette_score(data, labels)


def nonconnected_score(labels, faces):
    """
    Calculate the percentage of nonconnected component in labels.

    Parameters
    ----------
    labels: cluster labels, shape = [n_samples].
    faces: contain triangles of brain surface.

    Returns
    -------
    nonconnected score of labels, 1 stands for every label is nonconnected, 0 for no nonconnected label.

    Notes
    -----
    1. the max label number in labels should be assigned to the medial wall.
    2. data with the max label number will be omitted.
    """
    nonc_list = nonconnected_labels(labels, faces)
    print(nonc_list)
    return len(nonc_list) / len(np.unique(labels))
