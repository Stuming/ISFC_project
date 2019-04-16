"""
Used to evaluate clusters or parcellations.
"""
import numpy as np

from scipy.stats import zscore
from scipy.spatial.distance import cdist

from nsnt.algorithms.fctools import wsfc
from nsnt.utils.utils import apply_1d_mask
from nsnt.utils.adj_tools import nonconnected_labels, mk_label_adjfaces, faces_to_dict


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
    1. the label 0 in labels should be assigned to the medial wall, and it will be ommited.
    """
    from scipy.spatial.distance import dice

    label_list1 = np.unique(labels1)
    label_list2 = np.unique(labels2)

    # label 0 will not be concerned.
    label_list1 = label_list1[np.where(label_list1 != 0)]
    label_list2 = label_list2[np.where(label_list2 != 0)]

    row_num, column_num = np.shape(label_list1)[0], np.shape(label_list2)[0]

    dice_mat = np.zeros((row_num, column_num))
    for i, l1 in enumerate(label_list1):
        for j, l2 in enumerate(label_list2):
            dice_mat[i, j] = 1 - dice(labels1 == l1, labels2 == l2)  # dice() measures dice dissimilarity
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


def mean_data_cdist_max(data, labels, metric='euclidean', coef=True, doing_zscore=False):
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


def mean_data_cdist_adj(data, labels, label_faces, metric='euclidean', coef=True, integrate='mean', doing_zscore=False):
    """
    Calculate euclidean distance coefficient between label and its neighbors,
    based on its mean data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    label_faces: Triangle meshes of labels. 2d array of shape (n_meshes, 3)
    metric: measurement, see help of scipy.spatial.distance.
    coef: whether return coef(float) or matrix(array), default is True.
    integrate: decide how to merge data of label and its neighbors, default is 'mean'.
        Options: 'max': keep the max metric as the result.
            'mean': use mean metric as the result.
            'min': keep the min metric as the result.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coef_label: float, reflects mean dissimilarity, based on metric.
    cdist_map_label: matrix, reflects dissimilarity of all label pair, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        np.nan_to_num(zscore(data, axis=1))

    assert integrate in ['min', 'max', 'mean'], "integrate could only be one of ['min', 'max', 'mean']."

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = list(np.unique(labels))
    label_number = np.shape(label_list)[0]
    time_point = np.shape(data)[-1]
    data_mean = np.zeros((label_number, time_point), dtype=np.float64)

    for i, label in enumerate(label_list):
        data_vertices = data[np.where(labels == label)]
        data_mean[i] = np.mean(data_vertices, axis=0)

    # get neighbor of labels
    label_neighbor = faces_to_dict(label_faces)
    cdist_map = np.zeros(label_number, dtype=np.float64)

    for i, label in enumerate(label_list):
        data_label = data_mean[[label_list.index(label)]]
        data_neighbors = data_mean[[label_list.index(l) for l in label_neighbor[label]]]
        print('shape of data_neighbors: {}'.format(data_neighbors.shape))
        cdist_map_neighbor = np.nan_to_num(cdist(data_label, data_neighbors, metric=metric))

        if integrate == 'max':
            cdist_map[i] = np.max(cdist_map_neighbor)
        elif integrate == 'min':
            cdist_map[i] = np.min(cdist_map_neighbor)
        else:
            cdist_map[i] = np.mean(cdist_map_neighbor)

    if coef:
        # Use the mean of upper triangle in cdist matrix as cdist coef.
        return np.mean(cdist_map)
    return cdist_map


def cdist_adj(data, labels, label_faces, metric='euclidean', integrate='mean', label_size_count=False, doing_zscore=False):
    """
    Calculate euclidean distance coefficient between label and its neighbors,
    based on its mean data.

    Parameters
    ----------
    data: time series, shape = [n_samples, n_features].
    labels: cluster labels, shape = [n_samples].
    label_faces: Triangle meshes of labels. 2d array of shape (n_meshes, 3)
    metric: measurement, see help of scipy.spatial.distance.
    integrate: decide how to merge data of label and its neighbors, default is 'mean'.
        Options: 'max': keep the max metric as the result.
            'mean': use mean metric as the result.
            'min': keep the min metric as the result.
    label_size_count: whether balance size of label or not.
    doing_zscore: whether doing zscore to data or not.

    Returns
    -------
    cdist_coef_label: float, reflects mean dissimilarity, based on metric.
    cdist_map_label: matrix, reflects dissimilarity of all label pair, based on metric.
    """
    if doing_zscore:
        print('Doing zscore to data.')
        np.nan_to_num(zscore(data, axis=1))

    assert integrate in ['min', 'max', 'mean'], "integrate could only be one of ['min', 'max', 'mean']."

    # here we use unique labels for loop instead of max label number, to avoid error
    # caused by discontinuity labels, which may lead to nan in result.
    label_list = list(np.unique(labels))
    label_number = np.shape(label_list)[0]
    label_size = np.zeros_like(label_list, dtype=np.int)

    # get neighbor of labels
    label_neighbor = faces_to_dict(label_faces)
    cdist_map = np.zeros(label_number, dtype=np.float64)

    for i, label in enumerate(label_list):
        vert_list = np.array(np.where(labels == label))[0]
        label_size[i] = vert_list.shape[0]

        data_label = data[[label_list.index(label)]]
        print('shape of data_label: {}'.format(data_label.shape))
        cdist_neighbor = []
        for neighbor in label_neighbor[label]:
            data_neighbor = data[np.where(labels == neighbor)[0]]
            print('shape of data_neighbor: {}'.format(data_neighbor.shape))
            cdist_map_neighbor = np.nan_to_num(cdist(data_label, data_neighbor, metric=metric))

            # TODO change np.mean(data) to np.mean(data**2)
            cdist_neighbor.append(np.mean(cdist_map_neighbor))
        if integrate == 'max':
            cdist_map[i] = np.max(cdist_neighbor)
        elif integrate == 'min':
            cdist_map[i] = np.min(cdist_neighbor)
        else:
            cdist_map[i] = np.mean(cdist_neighbor)

    if label_size_count:
        return np.sum(label_size * cdist_map) / np.sum(label_size)
    return np.mean(cdist_map)


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
