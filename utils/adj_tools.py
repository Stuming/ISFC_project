"""
Provide tools for get or make matrix, faces, or other forms that reflect adjacent relationships of brain surface.
"""
import numpy as np
from surfer import Surface
# FIXME import Surface may cause error:
# FIXME     ValueError: API 'QString' has already been set to version 1.


def _faces_to_edges(faces):
    """
    Build edges array from faces.
    Parameters
    ----------
        faces: triangles mesh of brain surface, shape=(n_mesh, 3).

    Returns
    -------
        edges: array, edges of brain surface mesh, shape=(n_edges, 2)
    """
    from itertools import combinations
    edges = []
    for face in faces:
        for edge in combinations(face, 2):
            if edge not in edges:
                edges.append(edge)
    return edges


def _edges_to_adjmatrix(edges):
    """
    Build edges array from faces.
    Parameters
    ----------
        edges: edges of brain surface mesh, shape=(n_edges, 2)

    Returns
    -------
        adj_matrix: adj matrix that reflect linkages of edges, shape = (n_vertexes, n_vertexes).
    """
    n_vertexes = np.max(edges) + 1
    adj_matrix = np.zeros((n_vertexes, n_vertexes))
    for edge in edges:
        adj_matrix[edge[0], edge[1]] = 1
    return adj_matrix


def faces_to_adjmatrix(faces):
    """
    Build adjacency matrix by faces.

    Parameters
    ----------
        faces: contain triangles of brain surface.

    Returns
    -------
        adj_matrix: adj matrix that reflect linkages of (subj_id, hemi, surf), shape = (vert_num, vert_num).

    Examples
    --------
        faces = get_faces("fsaverage", "lh", "inflated")
        adjm = get_adjmatrix(faces)
    """
    return _edges_to_adjmatrix(_faces_to_edges(faces))


def _get_geo(subj_id, hemi, surf):
    """
    Get geometry of (subj_id, hemi, surf).

    Parameters
    ----------
        subj_id: subject id (eg. "fsaverage").
        hemi: hemisphere (eg. "lh").
        surf: surface (eg. "inflated").

    Returns
    -------
        geo: geometry of (subj_id, hemi, surf).
    """
    geo = Surface(subj_id, hemi, surf)
    geo.load_geometry()
    return geo


def get_faces(subj_id, hemi, surf):
    """
    Get faces of (subj_id, hemi, surf).

    Parameters
    ----------
        subj_id: subject id (eg. "fsaverage").
        hemi: hemisphere (eg. "lh").
        surf: surface (eg. "inflated").

    Returns
    -------
        faces that contain triangle of (subj_id, hemi, surf).

    Examples
    --------
        faces = get_faces("fsaverage", "lh", "inflated")
    """
    return _get_geo(subj_id, hemi, surf).faces


def get_coords(subj_id, hemi, surf):
    """
    Get coordinates by (subj_id, hemi, surf).

    Parameters
    ----------
        subj_id: subject id (eg. "fsaverage").
        hemi: hemisphere (eg. "lh").
        surf: surface (eg. "inflated").

    Returns
    -------
        coords: coordinates of (subj_id, hemi, surf).

    Examples
    --------
        coords = get_coords("fsaverage", "lh", "inflated")
    """
    return _get_geo(subj_id, hemi, surf).coords


def mk_label_adjmatrix(label_image, adjmatrix):
    """
    Calculate adjacent matrix of labels from adjacent matrix of vertexes.

    Parameters
    ----------
        label_image: labels of vertexes, shape = (n, 1), n is number of vertexes.
        adjmatrix: adjacent matrix of vertexes, shape = (n, n).

    Returns
    -------
        label_adjmatrix: adjacent matrix of labels, shape = (l, l), l is number of labels.

    Notes
    -----
        1. labels in label_image should in the range from 0 to max label number.
        2. for large number of vertexes, this method may cause memory error, try to use mk_label_adjfaces() inplace.
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

    Parameters
    ----------
        label_image: labels of vertexes, shape = (n, 1).
        faces: faces of vertexes, its shape depends on surface, shape = (m, 3).

    Returns
    -------
        label_faces: faces of labels, shape = (l, 3).
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


def concat_coords_to_data(data, coords, w1=1, w2=1):
    """
    Concatenate coordinates to data, which is used as adj constraint.

    Parameters
    ----------
        data: time series, shape = (n, l).
        coords: coordinates of vertexes, shape = (n, 3).
        w1: weight of data.
        w2: weight of coords.

    Returns
    -------
        data: after concatenating coordinates by multiplying weight.
    Notes
    -----
        1. w1 (same as w2) works by multiplication, default is 1.
    """
    assert data.shape[0] == coords.shape[0], "The first shape of input is not match."
    data = np.concatenate((data * w1, coords * w2), axis=1)
    return data

