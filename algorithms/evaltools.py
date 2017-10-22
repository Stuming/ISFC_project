"""
Used to evaluate clusters or parcellations.
"""
from numpy import np
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score


class evaluatetools:
    """
    A method class provides multi evaluation methods.
    """
    def __init__(self):
        pass

    def ari(self, parcel1, parcel2):
        """
        Calculate adjusted rand index(ARI) of parcel1 and parcel2.
        :param parcel1: cluster labels, shape = n_samples.
        :param parcel2: cluster labels, shape = n_samples.
        :return: ARI ranges from (-1.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
        """
        return adjusted_rand_score(parcel1, parcel2)

    def ami(self, parcel1, parcel2):
        """
        Calculate adjusted mutual information(AMI) of parcel1 and parcel2.
        :param parcel1: cluster labels, shape = n_samples.
        :param parcel2: cluster labels, shape = n_samples.
        :return: AMI ranges from (0.0, 1.0), 1.0 stands for perfect match, 0 stands for random labels.
        """
        return adjusted_mutual_info_score(parcel1, parcel2)

    def homogeneity(self, parcel1, parcel2):
        """
        Calculate homogeneity of parcel1 and parcel2.
        :param parcel1: cluster labels, shape = n_samples.
        :param parcel2: cluster labels, shape = n_samples.
        :return: homogeneity
        """
        pass

    def dice_coef(self, parcel1, parcel2):
        """
        Calculate dice coefficient of parcel1 and parcel2.
        :param parcel1: cluster labels, shape = n_samples.
        :param parcel2: cluster labels, shape = n_samples.
        :return: dice coef ranges from (0, 1), 1.0 stands for perfect match, 0 stands for random labels.
        """
        pass

    def bic(self, parcel1, parcel2):
        """
        Calculate bayesian information criterion(BIC) of parcel1 and parcel2.
        :param parcel1: cluster labels, shape = n_samples.
        :param parcel2: cluster labels, shape = n_samples.
        :return: bic
        """
        pass
