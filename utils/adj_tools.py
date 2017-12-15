"""
Provide tools for get or make matrix, faces, or other forms that reflect adjacent relationships of brain surface.
"""
import numpy as np
from surfer import Surface
# FIXME import Surface may cause error:
# FIXME     ValueError: API 'QString' has already been set to version 1.


def faces_to_edges(faces):
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

    edges = np.empty((0, 2))
    for face in faces:
        for edge in combinations(face, 2):
            if np.any(np.all(edge == edges, axis=1)):  # check whether edge in edges
                continue
            if np.any(np.all(edge[::-1] == edges, axis=1)):  # check whether edge in edges
                continue
            edges = np.append(edges, np.reshape(edge, (1, 2)),  axis=0)
    return edges


def edges_to_adjmatrix(edges):
    """
    Build edges array from faces.
    Parameters
    ----------
        edges: edges of brain surface mesh, shape=(n_edges, 2)

    Returns
    -------
        adj_matrix: adj matrix that reflect linkages of edges, shape = (n_vertexes, n_vertexes).
    """
    vertexes = np.unique(edges)
    n_vertexes = len(vertexes)
    adj_matrix = np.zeros((n_vertexes, n_vertexes))
    for edge in edges:
        adj_matrix[np.where(vertexes == edge[0]), np.where(vertexes == edge[1])] = 1
    adj_matrix[np.where((adj_matrix + adj_matrix.T) > 0)] = 1
    return adj_matrix


def faces_to_adjmatrix(faces):
    """
    Build adjacency matrix by faces.

    Parameters
    ----------
        faces: triangles mesh of brain surface, shape=(n_mesh, 3).

    Returns
    -------
        adj_matrix: adj matrix that reflect linkages of faces, shape = (n_vertexes, n_vertexes).

    Examples
    --------
        from NSNT.utils.adj_tools import get_faces, get_adjmatrix
        faces = get_faces("fsaverage", "lh", "inflated")
        adjm = get_adjmatrix(faces)
    """
    return edges_to_adjmatrix(faces_to_edges(faces))


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


def get_faces(subj_id, hemi, surf="inflated"):
    """
    Get faces of (subj_id, hemi, surf).

    Parameters
    ----------
        subj_id: subject id (eg. "fsaverage").
        hemi: hemisphere (eg. "lh").
        surf: surface (eg. "inflated"), can be omitted.

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
        coords: coordinates of (subj_id, hemi, surf), shape = (n_vertexes, 3).

    Examples
    --------
        coords = get_coords("fsaverage", "lh", "inflated")
    """
    return _get_geo(subj_id, hemi, surf).coords


def mk_label_adjmatrix(label_image, adjmatrix):
    """
    Calculate adjacent matrix of labels in label_image, based on adjacent matrix of vertexes.

    Parameters
    ----------
        label_image: labels of vertexes, shape = (n, ), n is number of vertexes.
        adjmatrix: adjacent matrix of vertexes, shape = (n, n).

    Returns
    -------
        label_adjmatrix: adjacent matrix of labels, shape = (l, l), l is number of labels.

    Notes
    -----
        1. for large number of vertexes, this method may cause memory error, try to use mk_label_adjfaces().
    """
    labels = np.unique(label_image)
    l = len(labels)
    n = len(label_image)
    temp_matrix = np.zeros((l, n))
    label_adjmatrix = np.zeros((l, l))
    for i, label in enumerate(labels):
        temp_matrix[i, :] = np.sum(adjmatrix[np.where(label_image == label)[0], :], axis=0)

    for i, label in enumerate(labels):
        label_adjmatrix[:, i] = np.sum(temp_matrix[:, np.where(label_image == label)[0]], axis=1).T

    # making binary adjmatrix
    label_adjmatrix[np.where(label_adjmatrix > 0)] = 1
    label_adjmatrix[range(l), range(l)] = 0
    return label_adjmatrix


def mk_label_adjfaces(label_image, faces):
    """
    Calculate faces of labels in label_image, based on faces of vertexes.

    Parameters
    ----------
        label_image: labels of vertexes, shape = (n, ).
        faces: faces of vertexes, its shape depends on surface, shape = (m, 3).

    Returns
    -------
        label_faces: faces of labels, shape = (l, 3).
    """
    label_face = np.copy(faces)
    for i in faces:
        label_face[np.where(faces == i)[0]] = [label_image[i[0]], label_image[i[1]], label_image[i[2]]]
    label_faces_rde = np.array(list(set([tuple(column) for column in label_face])))  # remove duplicate elements
    label_faces = np.empty((0, 3))
    for column in label_faces_rde:
        if np.unique(column).shape[0] != 1:
            label_faces = np.append(label_faces, column, axis=0)  # keep face elements only
    return np.array(label_faces)


def concat_coords_to_data(data, coords, w1=1, w2=1):
    """
    Concatenate coordinates to data.

    Parameters
    ----------
        data: time series, shape = (n, l).
        coords: coordinates of vertexes, shape = (n, 3).
        w1: control weight of data.
        w2: control weight of coords.

    Returns
    -------
        data: after concatenating coordinates by multiplying weight, shape = (n, l + 3).

    Notes
    -----
        1. w1 (same as w2) works by multiplication, default is 1.
    """
    assert data.shape[0] == coords.shape[0], "The first shape of input is not match."
    data = np.concatenate((data * w1, coords * w2), axis=1)
    return data


def get_verts_faces(verts, faces):
    """
    Get faces of verts based on faces of all vertexes.

    Parameters
    ----------
        verts: a set of vertices, shape = (k,)
        faces: faces of vertexes, its shape depends on surface, shape = (n_faces, 3).

    Returns
    -------
        faces of verts, shape = (m, 3)
    """
    verts_faces = np.empty((0, 3))
    for vert in verts:
        verts_faces = np.append(verts_faces, faces[np.where(faces == vert)[0]], axis=0)
    verts_faces_rde = np.array(list(set([tuple(column) for column in verts_faces])))  # remove duplicate elements
    return verts_faces_rde


def get_verts_edges(verts, edges):
    """
    Get edges of verts based on edges of all vertexes.

    Parameters
    ----------
        verts: a set of vertices, shape = (k,)
        edges: edges of brain surface mesh, shape=(n_edges, 2)

    Returns
    -------
        edges of verts, shape = (m, 2)
    """
    verts_edges = np.empty((0, 2))
    for vert in verts:
        verts_edges = np.append(verts_edges, edges[np.where(edges == vert)[0]], axis=0)
    verts_edges_rde = np.array(list(set([tuple(column) for column in verts_edges])))  # remove duplicate elements
    return verts_edges_rde
