"""
Used to evaluate clusters or parcellations.
"""
import numpy as np
from .fctools import wsfc
from sklearn.metrics.cluster import adjusted_rand_score, adjusted_mutual_info_score, silhouette_samples


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
    for label in range(max_label):
        wsfc(data[np.where(parcel == label)])


def dice_coef(parcel1, parcel2):
    """
    Calculate dice coefficient of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        dice coef: ranges from (0, 1), 1.0 stands for perfect match, 0 stands for random labels.
    """
    pass


def silhouette_coef(parcel1, parcel2):
    """
    Calculate silhouette coefficient of parcel1 and parcel2.

    Parameters
    ----------
        parcel1: cluster labels, shape = [n_samples].
        parcel2: cluster labels, shape = [n_samples].

    Returns
    -------
        silhouette coefficient
    """
    pass
