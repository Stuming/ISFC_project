"""
Used to evaluate clusters or parcellations.
"""
import numpy as np

from scipy.stats import zscore
from scipy.spatial.distance import cdist

from nsnt.algorithms.fctools import wsfc
from nsnt.utils.utils import apply_1d_mask
from nsnt.utils.adj_tools import nonconnected_labels, SurfaceGeometry, mk_label_adjfaces


def ari(labels1, labels2, mask=None):
    """
    Calculate adjusted rand index(ARI) of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].
    mask: binary array, 1 for region of interest and 0 for others, shape=(n_vertices,).

    Returns
    -------
    ARI: ranges from (-1.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    from sklearn.metrics.cluster import adjusted_rand_score

    labels1 = apply_1d_mask(labels1, mask)
    labels2 = apply_1d_mask(labels2, mask)
    return adjusted_rand_score(labels1, labels2)


def ami(labels1, labels2, mask=None):
    """
    Calculate adjusted mutual information(AMI) of the inputs.

    Parameters
    ----------
    labels1: cluster labels, shape = [n_samples].
    labels2: cluster labels, shape = [n_samples].
    mask: binary array, 1 for region of interest and 0 for others, shape=(n_vertices,).

    Returns
    -------
    AMI: ranges from (0.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
    """
    from sklearn.metrics.cluster import adjusted_mutual_info_score

    labels1 = apply_1d_mask(labels1, mask)
    labels2 = apply_1d_mask(labels2, mask)
    return adjusted_mutual_info_score(labels1, labels2)


def homogeneity_coef(data, labels, label_size_count=False):
    """
    Calculate homogeneity score of labels based on its data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    label_size_count: whether balance size of label or not.

    Returns
    -------
    homo_score: score of homogeneity.
    """
    label_list = np.unique(labels)
    homo_list = np.zeros_like(label_list, dtype=np.float64)
    label_size = np.zeros_like(label_list, dtype=np.int)

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        vert_num = vert_list.shape[0]
        label_size[i] = vert_num

        fcmap = np.nan_to_num(wsfc(data[vert_list, :]))
        if vert_num == 1:  # some labels may be assigned to only one vertex.
            homo_list[i] = 1
        else:
            homo_list[i] = np.mean(fcmap[np.triu_indices_from(fcmap, k=1)])
    if label_size_count:
        return np.sum(label_size * homo_list) / np.sum(label_size)
    return np.mean(homo_list)


def homogeneity_list(data, labels):
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
    """
    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = np.unique(labels)
    homo_list = np.zeros_like(label_list, dtype=np.float64)

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        vert_num = vert_list.shape[0]
        fcmap = np.nan_to_num(wsfc(data[vert_list, :]))
        if vert_num == 1:  # some labels may be assigned to only one vertex.
            homo_list[i] = 1
        else:
            homo_list[i] = np.mean(fcmap[np.triu_indices_from(fcmap, k=1)])
    return label_list, homo_list


def homogeneity_map(data, labels, mask=None):
    """
    Calculate homogeneity map of every vertex in labels, based on its data.

    Parameters
    ----------
    data: time series, shape=(n_vertices, n_features).
    labels: cluster labels, shape=(n_vertices,).
    mask: binary array, 1 for region of interest and 0 for others, shape=(n_vertices,).

    Returns
    -------
    homo_map: homogeneity of every vertex with other vertex in the same label.
    """
    data = apply_1d_mask(data, mask)
    labels = apply_1d_mask(labels, mask)

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels which may lead to nan in result.
    label_list = np.unique(labels)
    homo_map = np.zeros_like(labels, dtype=np.float64)

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        vert_num = vert_list.shape[0]
        fcmap = np.nan_to_num(wsfc(data[vert_list, :]))
        for j, vert in enumerate(vert_list):
            # calculate mean homo except vertex itself.
            homo_map[vert] = (np.sum(fcmap[j]) - 1) / (vert_num - 1)
    if mask:
        result = np.copy(mask)
        result[np.where(mask == 1)] = homo_map
        return result
    return homo_map


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


def cdist_coef(data, labels, metric='euclidean', label_size_count=False, doing_zscore=False):
    """
    Calculate euclidean distance coefficient of labels based on its vertices' cdist.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    metric: measurement, see help of scipy.spatial.distance.
    label_size_count: whether balance size of label or not.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coefficient: float, reflects mean dissimilarity, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        np.nan_to_num(zscore(data, axis=1))

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = np.unique(labels)
    cdist_list = np.zeros_like(label_list, dtype=np.float64)
    label_size = np.zeros_like(label_list, dtype=np.int)
    cdist_map = np.nan_to_num(cdist(data, data, metric=metric))

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        label_size[i] = vert_list.shape[0]
        cdist_map_label = cdist_map[:, vert_list][vert_list, :]

        cdist_list[i] = np.mean(cdist_map_label[np.triu_indices_from(cdist_map_label, k=1)])
    if label_size_count:
        return np.sum(label_size * cdist_list) / np.sum(label_size)
    return np.mean(cdist_list)


def cdist_mean(data, labels, metric='euclidean', coef=True, doing_zscore=False):
    """
    Calculate euclidean distance coefficient of labels based on its mean data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    metric: measurement, see help of scipy.spatial.distance.
    coef: whether return coef(float) or matrix(array), default is True.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coef_label: float, reflects mean dissimilarity, based on metric.
    cdist_map_label: matrix, reflects dissimilarity of all label pair, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        np.nan_to_num(zscore(data, axis=1))

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = np.unique(labels)
    label_number = np.shape(label_list)[0]
    time_point = np.shape(data)[-1]
    data_mean = np.zeros((label_number, time_point), dtype=np.float64)
    for i, label in enumerate(label_list):
        data_vertices = data[np.where(labels == label)]
        data_mean[i] = np.mean(data_vertices, axis=0)

    cdist_map_label = np.nan_to_num(cdist(data_mean, data_mean, metric=metric))
    if coef:
        # Use the mean of upper triangle in cdist matrix as cdist coef.
        cdist_coef_label = np.mean(cdist_map_label[np.triu_indices_from(cdist_map_label, k=1)])
        return cdist_coef_label
    return cdist_map_label


def cdist_max(data, labels, metric='euclidean', coef=True, doing_zscore=False):
    """
    Calculate euclidean distance coefficient of labels based on its mean data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    metric: measurement, see help of scipy.spatial.distance.
    coef: whether return coef(float) or matrix(array), default is True.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coef_label: float, reflects mean dissimilarity, based on metric.
    cdist_map_label: matrix, reflects dissimilarity of all label pair, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        data = np.nan_to_num(zscore(data, axis=1))

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = np.unique(labels)
    label_number = np.shape(label_list)[0]
    time_point = np.shape(data)[-1]
    data_mean = np.zeros((label_number, time_point), dtype=np.float64)
    for i, label in enumerate(label_list):
        data_vertices = data[np.where(labels == label)]
        data_mean[i] = np.mean(data_vertices, axis=0)

    cdist_map_label = np.nan_to_num(cdist(data_mean, data_mean, metric=metric))
    if coef:
        # Use the mean of upper triangle in cdist matrix as cdist coef.
        cdist_coef_label = np.mean(np.max(cdist_map_label, axis=0))
        return cdist_coef_label
    return cdist_map_label


def cdist_mean_adj(data, labels, metric='euclidean', coef=True, doing_zscore=False):
    """
    Calculate euclidean distance coefficient between label and its neighbors,
    based on its mean data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    metric: measurement, see help of scipy.spatial.distance.
    coef: whether return coef(float) or matrix(array), default is True.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coef_label: float, reflects mean dissimilarity, based on metric.
    cdist_map_label: matrix, reflects dissimilarity of all label pair, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        np.nan_to_num(zscore(data, axis=1))

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = np.unique(labels)
    label_number = np.shape(label_list)[0]
    time_point = np.shape(data)[-1]
    data_mean = np.zeros((label_number, time_point), dtype=np.float64)

    faces = SurfaceGeometry('fsaverage5', 'lh', 'inflated').faces
    label_faces = mk_label_adjfaces(labels, faces)

    for i, label in enumerate(label_list):
        data_vertices = data[np.where(labels == label)]
        data_mean[i] = np.mean(data_vertices, axis=0)

    cdist_map_label = np.nan_to_num(cdist(data_mean, data_mean, metric=metric))

    # get neighbor of labels


    if coef:
        # Use the mean of upper triangle in cdist matrix as cdist coef.
        cdist_coef_label = np.mean(cdist_map_label[np.triu_indices_from(cdist_map_label, k=1)])
        return cdist_coef_label
    return cdist_map_label


def silhouette_coef(data, labels, mask=None):
    """
    Calculate silhouette coefficient of the inputs.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    mask: binary array, 1 for region of interest and 0 for others, shape=(n_vertices,).

    Returns
    -------
    silhouette coefficient
    """
    from sklearn.metrics.cluster import silhouette_score

    data = apply_1d_mask(data, mask)
    labels = apply_1d_mask(labels, mask)

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


def loyalty_map(vote_matrix, labels):
    """
    Calculate loyalty of every vertex to its labels through vote matrix.

    Parameters
    ----------
    vote_matrix: created by parcellate the same data repeatedly,
        and count the times that two vertices in the same label,
        shape=(n_vertices, n_vertices).
    labels: cluster labels, shape=(n_vertices,).

    Return
    ------
    loyalty: loyalty of every vertex belong to its label.
    """
    n_vertices = np.shape(labels)[0]
    loyalty = np.zeros_like(labels)

    for vertex in range(n_vertices):
        label_vertices = np.where(labels == labels[vertex])
        label_vertices = np.delete(label_vertices, np.where(label_vertices == vertex))
        loyalty[vertex] = np.mean(vote_matrix[vertex][label_vertices])
    return loyalty
