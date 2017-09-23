import numpy as np
from utils.utils import get_adjmatrix


def del_zeros(data, show_zeros=False):
    """Check if zeros in column of data.
    data: 2-dimension array.
    show_zeros: whether to show zeros array.

    Return:
        data1: data after delete zeros.
        zeros: indexes of zero column."""
    # TODO modify func to make para `num` work
    zeros = np.where(~data.any(axis=1))[0]
    if show_zeros:
        print(zeros)
    data1 = np.delete(data, zeros, axis=0)
    del_num = data.shape[0] - data1.shape[0]
    print("Delete %i vertexes from data." % del_num)
    return data1, zeros


def positive(smatrix, show_index=False):
    """Replace negative data in smatrix to zero.
    smatrix: similarity matrix that want to remove negative value.
    show_index: whether to show index array.

    Return:
        smatrix: after positive operation
        neg_index: index of negative value in origin smatrix."""
    neg_index = np.where(smatrix < 0)
    smatrix[neg_index[0], neg_index[1]] = 0
    if show_index:
        print(neg_index)
    return smatrix, neg_index


def adj_constrain(smatrix, zeros, subj_id, hemi, surf):
    """Add adjacency constrain to smatrix.
    smatrix: similarity matrix that want to remove negative value.
    zeros: get from del_zeros(), and will be used to delete zero columns(rows) in adjacent matrix.
    subj_id: subject id that get adj constrain matrix from.
    hemi: hemi that do things as above.
    surf: surf that do things as above.

    Example:
        smatrix_adj, adjm = adj_constrain(smtrix_origin, zeros, "fsaverage", "lh", "inflated")
    """
    adjm = get_adjmatrix(subj_id, hemi, surf)
    adjm = np.delete(adjm, zeros, axis=0)
    adjm = np.delete(adjm, zeros, axis=1)
    smatrix = smatrix * adjm
    return smatrix, adjm


def exp_rescale(rmatrix, l=1):
    """Rescale rmatrix as exponential function.
    l: exp index.
    rsmatrix = exp(-1*l*(1-rmatrix))

    Return:
        rsmatrix: rescaled matrix."""
    index = -1 * l * (1 - rmatrix)
    rsmatrix = np.exp(index)
    return rsmatrix
