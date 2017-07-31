# Average nifti data for group ISFC/ISC analysis
# Result name would like: avg_data_except_S001_run1.mgh
# means average all data in sessidlist except S001

import nibabel as nib
import numpy as np
import os
import array
from ISFC_tools import match_datashape, load_file

datadir="/s1/data/gumpdata/project"
sessidlist=["S001", "S002", "S003", "S004", "S005", "S006", "S009", "S010", "S014", "S015", "S016", "S017", "S018", "S019", "S020"]
funcname="bold"
filename="fmcpr.up.sm0.fsaverage.lh.mgh" # Do analysis after mri_convert


for sessid1 in sessidlist:
#sessid1="S001"
#if 1==1:
    for r in range(1,9):
        i=0 # count sess number
        avg_data=0 # init data

        runid=str(r)
        while len(runid)<3:
            runid="0"+runid
        f1=load_file(datadir, sessid1, funcname, runid, filename)

        for sessid_temp in sessidlist:
            if sessid1 == sessid_temp:
                continue
            print("add "+sessid_temp+" run "+runid)

            f2=load_file(datadir, sessid_temp, funcname, runid, filename)
            if not match_datashape(f1,f2):
                exit(0)

            avg_data=avg_data+f2.get_data()
            i=i+1

        avg_data=avg_data/i
        avg_data_path="avg_data_except_"+sessid1+"_"+runid+".mgh" # means average all data except sessid1, then use it cal ISFC/ISC with sessid1.
        avg_data_mgh=nib.MGHImage(avg_data,f1.get_affine())
        nib.save(avg_data_mgh,avg_data_path)
        print("Finish saving "+avg_data_path)

