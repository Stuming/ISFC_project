"""
Used to evaluate clusters or parcellations.
"""
import numpy as np


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
        homogeneity: ranges from (0.0, 1.0).

    Notes
    -----
        1. the max number of labels should be assigned to the medial wall.
        2. data with the max label number will be omitted.
    """
    from .fctools import wsfc

    max_label = np.int(np.max(labels))
    homo_list = np.zeros(max_label)
    for label in range(max_label):
        vert_list = np.array(np.where(labels == label))[0]
        vert_num = vert_list.shape[0]
        fcmap = np.nan_to_num(wsfc(data[vert_list, :]))
        if fcmap.shape[0] == 1:  # some labels may be assigned to only one vertex.
            homo_list[label] = 1
        else:
            # ((np.sum(fcmap) - vert_num) / 2) / (vert_num * (vert_num - 1) / 2)
            homo_list[label] = (np.sum(fcmap) - vert_num) / (vert_num * (vert_num - 1))
    return np.mean(homo_list)


def dice_mat(labels1, labels2):
    """
    Calculate dice similarity coefficient matrix of the inputs.

    Parameters
    ----------
        labels1: cluster labels, shape = [n_samples].
        labels2: cluster labels, shape = [n_samples].

    Returns
    -------
        dice matrix: array, ranges from (0, 1), shape = (label_number1, label_number2).

    Notes
    -----
        1. the max label number in labels should be assigned to the medial wall.
        2. data with the max label number will be omitted.
    """
    from scipy.spatial.distance import dice

    row_num = np.int(np.max(labels1))
    column_num = np.int(np.max(labels2))
    dice_matrix = np.zeros((row_num, column_num))
    for i in range(row_num):
        for j in range(column_num):
            dice_matrix[i, j] = 1 - dice(labels1 == i, labels2 == j)  # dice() measures dice dissimilarity
    return np.nan_to_num(dice_matrix)


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
    dm = dice_mat(labels1, labels2)
    row_max = np.max(dm, axis=0)
    column_max = np.max(dm, axis=1)
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


def nonconnected_labels(labels, faces):
    """
    Check if every label in labels is a connected component.

    Parameters
    ----------
        labels: cluster labels, shape = [n_samples].
        faces: contain triangles of brain surface.

    Returns
    -------
        label list of nonconnected labels, if None, return [].

    Notes
    -----
        1. the max label number in labels should be assigned to the medial wall.
        2. data with the max label number will be omitted.
    """
    max_label = np.max(labels)
    label_list = []
    for i in range(max_label):
        vertexes = np.array(np.where(labels == i)).flatten()
        visited = []
        neighbors = [vertexes[0]]

        while neighbors:
            vertex = neighbors.pop(0)
            visited.append(vertex)
            neigh = np.unique(faces[np.where(faces == vertex)[0]])
            for vert in neigh:
                if vert in vertexes:
                    if (vert not in visited) and (vert not in neighbors):
                            neighbors.append(vert)

        for vert in vertexes:
            if vert not in visited:
                print("Label %i is not a connected component." % i)
                label_list.append(i)
                break
    return label_list


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
    return len(nonc_list) / np.max(labels)
