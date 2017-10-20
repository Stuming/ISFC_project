"""
Provide tools for get or make matrix, faces, or other forms that reflect adjacent relationships of brain surface.
"""
import numpy as np
from surfer import Surface
from ATT.algorithm import surf_tools


def get_adjmatrix(faces):
    """
    Build adjmatrix by faces.
    :param faces: contain triangles of brain surface.
    :return: adjm: adj matrix that reflect linkages of (subj_id, hemi, surf), its shape is (vert_num, vert_num).
    Example:
            faces = get_faces("fsaverage", "lh", "inflated")
            adjm = get_adjmatrix(faces)
    """
    edges = surf_tools.extract_edge_from_faces(faces)
    mk_adjm = surf_tools.GenAdjacentMatrix()
    adjm = mk_adjm.from_edge(edges)
    return adjm


def get_faces(subj_id, hemi, surf):
    """
    Get faces by (subj_id, hemi, surf).
    :param subj_id: subject id (eg. "fsaverage").
    :param hemi: hemisphere (eg. "lh").
    :param surf: surface (eg. "inflated").
    :return: faces that contain triangle of (subj_id, hemi, surf).
    Example:
            faces = get_faces("fsaverage", "lh", "inflated")
    """
    geo = Surface(subj_id, hemi, surf)
    geo.load_geometry()
    return geo.faces


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

    # make binary adjmatrix
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
    label_face = np.copy(faces)
    for i in faces:
        label_face[np.where(faces == i)[0]] = [label_image[i[0]], label_image[i[1]], label_image[i[2]]]
    label_faces_rde = np.array(list(set([tuple(column) for column in label_face])))  # remove duplicate elements
    label_faces = []
    for column in label_faces_rde:
        if np.unique(column).shape[0] != 1:
            label_faces.append(column)  # only keep face elements
    return np.array(label_faces)
