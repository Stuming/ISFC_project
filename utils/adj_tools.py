import numpy as np


def mk_label_adjmatrix(label_image, adjmatrix):
    """
    Calculate adjacent matrix of labels from adjacent matrix of vertexes.
    :param label_image: labels of vertexes (n x 1).
    :param adjmatrix: adjacent matrix of vertexes (n x n, n is number of vertexes).
    :return: adjacent matrix of labels (l x l, l is number of labels).
    Note: 1. labels in label_image should in the range from 0 to max label number.
          2. may cause memory error, try to use mk_label_adjfaces() inplace.
    """
    labels = np.unique(label_image)
    l = len(labels)
    n = len(label_image)
    temp_matrix = np.zeros((l, n))
    label_adjmatrix = np.zeros((l, l))
    for label in range(l):
        temp_matrix[label, :] = np.sum(adjmatrix[np.where(label_image == label)[0], :], axis=0)

    for label in range(l):
        label_adjmatrix[:, label] = np.sum(temp_matrix[:, np.where(label_image == label)[0]], axis=1).T

    # adj matrix binaryzation
    label_adjmatrix[np.where(label_adjmatrix > 0)] = 1
    label_adjmatrix[range(l), range(l)] = 0
    return label_adjmatrix


def mk_label_adjfaces(label_image, faces):
    """
    Calculate faces of labels based on faces of vertexes.
    :param label_image: labels of vertexes (n x 1).
    :param faces: faces of vertexes, its shape depends on surface (m x 3).
    :return: faces of labels (l x 3).
    """
    label_faces = np.copy(faces)
    for i in faces:
        label_faces[np.where(faces == i)[0]] = [label_image[i[0]], label_image[i[1]], label_image[i[2]]]
    label_faces = np.array(list(set([tuple(column) for column in label_faces])))  # remove duplicate elements
    for i in label_faces:
        if np.unique(i).shape[0] == 1:
            label_faces = np.delete(label_faces, np.where(label_faces == i), axis=0)  # delete none faces elements
    return label_faces
