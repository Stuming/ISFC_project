import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering

from nsnt.utils.utils import running_time


class Clustering(object):
    """
    Importing data and doing cluster.

    Parameters
    ----------
        data: input time series array, shape: (n_vertexes, n_features).
        mask: mask array of data, vertexes that value equals to 0 will not being used in clustering, \
              shape: (n_vertexes, )
    """

    def __init__(self, data, mask):
        self.data = np.nan_to_num(data)
        self.mask = mask
        self.method = None
        self.label = None

        if self.mask:
            self._apply_mask()

    def fit(self, parcel_num, method):
        self.method = method
        self.label = None

        # doing clustering
        if self.method == 'KMeans':
            self._do_kmeans(parcel_num)

        elif self.method == "hier_clustering":
            self._do_hier(parcel_num)

        elif self.method == "spectral_clustering":
            self._do_spectral(parcel_num, affinity="precomputed")

        else:
            raise Exception("Wrong method name.")

        self._rebuild_label(parcel_num)
        self.show_labelinfo()

    @running_time
    def _do_kmeans(self, n_clusters):
        """
        Doing KMeans clustering, see self.label for the result.

        Parameters
        ----------
            n_clusters: the number of clusters, type: int.

        Return
        ------
            label: clustering result, shape: (n_vertexes,)
        """
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(self.data)
        self.label = kmeans.predict(self.data)

        return self.label

    @running_time
    def _do_hier(self, n_clusters, adj=None):
        """
        Doing hierarchy clustering, see self.label for the result.

        Parameters
        ----------
            n_clusters: the number of clusters, type: int.
            adj: adjacency matrix, used for connectivity(adjacency constraint) if needed, default is None.

        Return
        ------
            label: clustering result, shape: (n_vertexes,)
        """
        if adj is not None:
            model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward", connectivity=adj)
        else:
            model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
        model.fit(self.data)
        self.label = model.labels_

        self._rebuild_label(n_clusters)
        self.show_labelinfo()
        return self.label

    @running_time
    def _do_spectral(self, n_clusters, eigen_solver="arpack", affinity="rbf"):
        """
        Doing spectral clustering, see self.label for the result.
        This method calculate similarity matrix of data first, then use this smat as input for
            spectral clustering, and the smat is calculated by the formula:
                smat = np.exp(-0.1 * Edist / Edist.std()), Edist stands for Euclidean distance

        Parameters
        ----------
            n_clusters: the number of clusters, type: int.
            eigen_solver: The eigenvalue decomposition strategy to use, default is 'arpack'.
                          For more information, see help(sklearn.cluster.SpectralClustering).
            affinity: Only kernels that produce similarity scores (non-negative values that
                      increase with similarity) should be used, default is 'rbf'.

        Return
        ------
            label: clustering result, shape: (n_vertexes,)
        """
        beta = 0.1  # used in spectral clustering
        smat = cal_edist_mat(self.data, beta=beta)

        spectral_cluster = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, affinity=affinity)
        self.label = spectral_cluster.fit(X=smat).labels_

        self._rebuild_label(n_clusters)
        self.show_labelinfo()
        return self.label

    def show_labelinfo(self):
        """
        Print information of labels, do clustering first.
        """
        if self.method and self.label:
            print('Clustering method: {}'.format(self.method))
            print('Shape of labels: {}'.format(np.shape(self.label)))
            print('Max label index: {}'.format(np.max(self.label)))
            print('Min label index: {}'.format(np.min(self.label)))
        else:
            print('Do clustering first')

    def add_geo_adj(self, coords, zeros, weight):
        coords = np.delete(coords, zeros, axis=0)
        print('w = {0:.2f}'.format(weight))
        data = np.concatenate((self.data, coords * weight), axis=1)
        print('Shape of data after concatenate: {}'.format(data.shape))
        return data

    def _apply_mask(self):
        """
        Apply self.mask onto self.data, remove vertexes that contain 0 value in mask array.
        """
        if self.data.shape[0] != self.mask.shape[0]:
            print('Shape of data and mask is not match, apply mask failed.')
            return -1
        zeros = np.where(self.mask == 0)[0]
        data = np.delete(self.data, zeros, axis=0)
        del_num = self.data.shape[0] - data.shape[0]
        print("Delete %i vertexes from data." % del_num)
        print("Shape of data after del zeros: {0.shape}".format(data))
        self.data = data

    def _rebuild_label(self, index):
        """
        Rebuild labels based on mask, and assign vertexes that out of mask an label index.

        Parameters
        ----------
            index: assign index to vertexes that are out of mask, which means vertexes that \
                   were deleted by self._apply_mask().
        """
        zeros = np.where(self.mask == 0)[0]
        label = self.label
        for i in zeros:
            label = np.insert(label, i, index)  # KMeans create label number range: (0, parcel_num-1)
        self.label = label


@running_time
def cal_knn_mat(data, k=10):
    """
    Find k nearest neighbor of data and return knn matrix. For more information,
        see sklearn.neighbors.kneighbors_graph

    Parameters
    ----------
        data: input 2-d array.
        k:  the number of nearest neighbors, default is 10.

    Return
    ------
        knn_mat: k nearest neighbor matrix.
    """
    rbf_mat = rbf_kernel(data)
    nbrs = kneighbors_graph(X=data, n_neighbors=k)
    knn_mat = nbrs.toarray() * rbf_mat
    knn_mat = 0.5 * (knn_mat + knn_mat.T)
    # print("gamma: {}".format(np.mean(np.min(rbf_mat[np.where(rbf_mat != 0)], axis=0))))
    return knn_mat


def cal_edist_mat(data, beta=1.0):
    """
    Calculate similarity matrix of data by Euclidean distance, see the formula:
        smat = np.exp(-beta * Edist / Edist.std()), Edist stands for Euclidean distance

    Parameters
    ----------
        data: input 2-d array.
        beta: factor of exp, default is 1.0.

    Return
    ------
        smat: asymmetric similarity matrix.
    """
    dist = cdist(data, data)
    print("std of dist: {}".format(dist.std()))
    edist = np.exp(-beta * dist / dist.std())
    return 0.5 * (edist + edist.T)
