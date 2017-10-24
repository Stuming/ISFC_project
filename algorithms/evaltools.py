"""
Used to evaluate clusters or parcellations.
"""
import numpy as np
from .fctools import wsfc
from ATT.algorithm.tools import calc_overlap
from sklearn.metrics.cluster import adjusted_rand_score, adjusted_mutual_info_score, silhouette_score


def ari(parcel1, parcel2):
    """
    Calculate adjusted rand index(ARI) of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        ARI: ranges from (-1.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    return adjusted_rand_score(parcel1, parcel2)


def ami(parcel1, parcel2):
    """
    Calculate adjusted mutual information(AMI) of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        AMI: ranges from (0.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    return adjusted_mutual_info_score(parcel1, parcel2)


def homogeneity(data, parcel):
    """
    Calculate homogeneity of a parcel based on its data.

    Parameters
    ----------
        data: time series, shape = [n_samples, n_features].
        parcel: cluster labels, shape = [n_samples].

    Returns
    -------
        homogeneity: ranges from (0.0, 1.0).

    Notes
    -----
        1. the max label number in parcel should be assigned to the medial wall.
    """
    max_label = np.max(parcel)
    homo_list = np.zeros(max_label)
    for label in range(max_label):
        vert_list = np.where(parcel == label)
        vert_num = vert_list.shape[0]
        fcmap = wsfc(data[vert_list, :])
        homo_list[label] = 2 * np.sum(fcmap - vert_num) / (vert_num * (vert_num - 1))
    return np.mean(homo_list)


def dice_mat(parcel1, parcel2):
    """
    Calculate dice coefficient matrix of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        dice matrix: array, ranges from (0, 1), shape = (label_number1, label_number2).

    Notes
    -----
        1. the max label number in parcel should be assigned to the medial wall.
    """
    row_num = np.max(parcel1)
    column_num = np.max(parcel2)
    dice_matrix = np.zeros((row_num, column_num))
    for i in range(row_num):
        for j in range(column_num):
            dice_matrix[i, j] = calc_overlap(parcel1, parcel2, i, j)
    return dice_matrix


def dice_coef(parcel1, parcel2):
    """
    Calculate mean dice coefficient of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        dice coef: float, ranges from (0.0, 1.0).

    Notes
    -----
        1. the max label number in parcel should be assigned to the medial wall.
    """
    return np.mean(dice_mat(parcel1, parcel2))


def silhouette_coef(data, parcel):
    """
    Calculate silhouette coefficient of parcel1 and parcel2.

    Parameters
    ----------
        data: time series, shape = [n_samples, n_features].
        parcel: cluster labels, shape = [n_samples].

    Returns
    -------
        silhouette coefficient
    """
    return silhouette_score(data, parcel)
