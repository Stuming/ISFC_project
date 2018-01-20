import numpy as np
from ..utils.utils import running_time
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering


@running_time
def _do_spectral(data, parcel_num, eigen_solver="arpack", affinity="rbf"):
    spectral_cluster = SpectralClustering(n_clusters=parcel_num, eigen_solver=eigen_solver, affinity=affinity)
    labelimg = spectral_cluster.fit(X=data.astype(np.float64)).labels_
    return labelimg


@running_time
def _do_kmeans(data, parcel_num):
    kmeans = KMeans(n_clusters=parcel_num)
    kmeans.fit(data)
    labelimg = kmeans.predict(data)
    return labelimg


@running_time
def _do_hier(data, n_clusters, adj=None):
    if adj is not None:
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward", connectivity=adj)
    else:
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    model.fit(data)
    labelimg = model.labels_
    return labelimg


def cal_knn_mat(data, n_neighbors=10):
    from sklearn.metrics.pairwise import rbf_kernel
    from sklearn.neighbors import kneighbors_graph

    rbf_mat = rbf_kernel(data)
    nbrs = kneighbors_graph(X=data, n_neighbors=n_neighbors)
    knn_mat = nbrs.toarray() * rbf_mat
    knn_mat = 0.5 * (knn_mat + knn_mat.T)
    return knn_mat


def cal_edist_mat(data, beta=1.0):
    from scipy.spatial.distance import cdist

    dist = cdist(data, data)
    print("std of dist: {}".format(dist.std()))
    edist = np.exp(-beta * dist / dist.std())
    return 0.5 * (edist + edist.T)


def do_clustering(data, parcel_num, method_name):
    # doing clustering
    data = np.nan_to_num(data)
    if method_name == "KMeans":
        labelimg = _do_kmeans(data, parcel_num)

    elif method_name == "hier_clustering":
        labelimg = _do_hier(data, parcel_num)

    elif method_name == "spectral_clustering":
        beta = 0.1  # used in spectral clustering
        smat = cal_edist_mat(data, beta=beta)
        labelimg = _do_spectral(np.nan_to_num(smat), parcel_num, affinity="precomputed")

    else:
        raise Exception("Wrong method name.")
    return labelimg

