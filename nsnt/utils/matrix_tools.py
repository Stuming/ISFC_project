import numpy as np

from nsnt.utils.adj_tools import SurfaceGeometry


class MatrixFunction:
    """
    This class records operation that be used to matrix, and can query operation state.
    """
    def __init__(self, de_zero=False, pos=False, adj=False, exp_rs=False):
        self.state = {"de_zero": de_zero, "pos": pos, "adj": adj, "exp_rs": exp_rs}

    def del_zeros(self, smatrix, show_zeros=False):
        """
        Check if zeros in column(and row) of smatrix.

        Parameters
        ----------
        smatrix: 2-dimension similarity matrix.
        show_zeros: whether to show zeros array.

        Returns
        -------
        data1: matrix after delete zeros.
        zeros: indexes of zero column.
        """
        state = "de_zero"
        if self.query_state(state):
            print("del zeros has already been done.")
            return smatrix, 0

        zeros0 = np.where(~smatrix.any(axis=0))[0]
        zeros1 = np.where(~smatrix.any(axis=1))[0]
        if not zeros0 == zeros1:
            print("zeros in column and row does not match, cannot operate, please check.")
            return smatrix, 0

        if show_zeros:
            print(zeros0)

        dsmatrix = np.delete(smatrix, zeros0, axis=0)
        dsmatrix = np.delete(dsmatrix, zeros0, axis=1)
        del_num = dsmatrix.shape[0] - smatrix.shape[0]
        print("Delete %i vertexes from data." % del_num)

        self.state[state] = True
        return dsmatrix, zeros0

    def positive(self, smatrix, show_index=False):
        """
        Replace negative data to zero in smatrix.

        Parameters
        ----------
        smatrix: 2-dimension similarity matrix.
        show_index: whether to show index array.

        Returns
        -------
        smatrix: after positive operation
        neg_index: index of negative value in origin smatrix.
        """
        state = "pos"
        if self.query_state(state):
            print("positive has already been done.")
            return smatrix, 0

        neg_index = np.where(smatrix < 0)
        smatrix[neg_index[0], neg_index[1]] = 0

        if show_index:
            print(neg_index)

        self.state[state] = True
        return smatrix, neg_index

    def adj_constrain(self, smatrix, subj_id, hemi, surf, zeros=None, adjm=None):
        """
        Add adjacency constrain to smatrix.

        Parameters
        ----------
        smatrix: similarity matrix that want to remove negative value.
        zeros: get from del_zeros(), and will be used to delete zero columns(rows) in adjacent matrix.
        subj_id: subject id that get adj constrain matrix from.
        hemi: hemi that do things as above.
        surf: surf that do things as above.
        adjm: adjacency matrix that was applied, if not given, it will be calculalted based on surf params.

        Returns
        -------
        smatrix: smatrix after adding adjacency constraint.
        adjm: adjacency matrix that was applied.

        Examples
        --------
        smatrix_adj, adjm = adj_constrain(smtrix_origin, zeros, "fsaverage", "lh", "inflated")
        """
        state = "adj"
        if self.query_state(state):
            print("adjacency constrain has already been done.")
            return smatrix, 0

        if not adjm:
            surface_geo = SurfaceGeometry(subj_id, hemi, surf)
            adjm = surface_geo.adjmatrix

        if zeros:
            adjm = np.delete(adjm, zeros, axis=0)
            adjm = np.delete(adjm, zeros, axis=1)
        smatrix = smatrix * adjm

        self.state[state] = True
        return smatrix, adjm

    def exp_rescale(self, smatrix, l=1):
        """
        Rescale smatrix as exponential function.

        Parameters
        ----------
        l: exp index.
        smatrix: similarity matrix.

        Returns
        -------
        rsmatrix: rescaled matrix, rsmatrix = exp(-1*l*(1-smatrix)).
        """
        state = "exp_rs"
        if self.query_state(state):
            print("exponential has already been done.")
            return smatrix

        index = -1 * l * (1 - smatrix)
        rsmatrix = np.exp(index)
        self.state[state] = True
        return rsmatrix

    def query_state(self, state=None):
        """
        Query state in class.

        Parameters
        ----------
        state: the state that will be queried. True means done, False means undone. If None, then print all state.

        Returns
        -------
        status of state, -1 stands for get nothing, 0 for state is not done, 1 for state is done.
        """
        if not state:
            print(self.state)
            return -1
        if state in self.state:
            return self.state[state]
        print("`state` should in %s" % state.keys())
        return -1

    def make_filename(self, filename):
        """
        Make filename based on state.

        Parameters
        ----------
        filename: string that contains filename.

        Returns
        -------
        filename: filename after adding states.
        """
        fname = filename.split('.')
        postfix = fname[-1]
        fname.pop(-1)
        for state in self.state.keys():
            if self.query_state(state):
                fname.append("-%s" % state)
        fname.append(postfix)
        filename = "".join(fname)
        return filename
