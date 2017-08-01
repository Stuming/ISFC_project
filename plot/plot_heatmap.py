import numpy as np
import nibabel as nib
from seaborn import heatmap
from surfer import Brain
import matplotlib.pyplot as plt


# TODO not finished.
def plot_heatmap(filepath):
    data1 = nib.load("result.mgh")
    result = data1.get_data()
    
    brain = Brain('fsaverage', 'lh', 'inflated')
    brain.add_data(result[:,0,0])

