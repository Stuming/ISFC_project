import numpy as np
import nibabel as nib
from seaborn import heatmap
import matplotlib.pyplot as plt


data1=nib.load("result.mgh")
result=data1.get_data()
from surfer import Brain
brain = Brain('fsaverage', 'lh', 'inflated')
brain.add_data(result[:,0,0])

