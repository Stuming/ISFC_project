"""
This package provides function to analysis fMRI data.

fctools:
  calculate functional connectivity(wsfc, isfc, etc.).

evaltools:
  provide tools for evaluating effect of parcellation / clustering result.

"""

# module import
from .evaltools import ari, ami, homogeneity, dice_coef, silhouette_coef
from .fctools import wsfc, isc, isfc
