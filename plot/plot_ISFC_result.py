# Save ISC/ISFC data into jpg

import nibabel as nib
from surfer import Brain
import numpy as np
import os


Subjectdir = "/usr/local/freesurfer/subjects"
datadir = "/s1/data/gumpdata/project"
sessidlist = ["S001", "S002", "S003", "S004", "S005", "S006", "S009", "S010", "S014", "S015", "S016", "S017", "S018", "S019", "S020"]
runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]
funcname = "bold"


# TODO change it into function and opt it.
for sessid in sessidlist:
#sessid="S001"
#if 1==1:
    for runid in runidlist:
        method_name = "ISFC"
        vertex_num = 86217
        outfmt = "mgh"
        brain = Brain("fsaverage","lh","inflated",views=["lat","med"],subjects_dir=Subjectdir)

        if method_name == "ISC":
            # plot ISC image
            trg_sessid = "group"
            prefix = method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)
            filename = prefix+"."+outfmt
            figname = "images/"+prefix+".jpg"

            img = nib.load(filename)
            brain.add_data(img.get_data()[:,0,0],min=-1,max=1)
            brain.save_image(figname)
            brain.close()
            print("Saving "+figname)

            # In Windows system, split windows mode may not save the image.
            """brain = Brain("fsaverage","lh","inflated",views=["med"],subjects_dir=Subjectdir)
            figname = "img_ISFC/"+prefix+"_med"+".jpg"
            brain.add_data(img.get_data()[:,0,0],min=-1,max=1)
            brain.save_image(figname)
            brain.close()
            print("Saving "+figname)"""

        elif method_name == "ISFC":
            # plot ISFC image

            """trg_sessid = "group"
            prefix = method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)
            filename = prefix+"."+outfmt
            figname = "img_ISFC/"+prefix+".jpg"
            """
            prefix = "avg_"+method_name+"_"+sessid+"_"+"group"+"_"+str(vertex_num)
            filename = "avg_result/"+prefix+"."+outfmt
            figname = "images/"+prefix+".jpg"

            img = nib.load(filename)
            brain.add_data(img.get_data()[:,0,0],min=-1,max=1)
            brain.save_image(figname)
            brain.close()
            print("Saving "+figname)

            # In Windows system, split windows mode may not save the image.
            """brain = Brain("fsaverage","lh","inflated",views=["med"],subjects_dir=Subjectdir)
            figname = "img_ISFC/"+prefix+"_med"+".jpg"
            brain.add_data(img.get_data()[:,0,0],min=-1,max=1)
            brain.save_image(figname)
            brain.close()
            print("Saving "+figname)"""
