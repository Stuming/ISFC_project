# Modified from average_data.py
# Average result of every run into one.
# Input result name would like: avg_data_except_S001_run1.mgh
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


# for sessid in sessidlist:
sessid="S001"
if 1==1:
    i=0
    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid

        vertex_num=86217
        method_name="ISFC"
        trg_sessid="group"
        result_path=method_name+"_"+sessid+"_"+trg_sessid+"_"+"run"+runid+"_"+str(vertex_num)+".mgh"
        result_run=nib.load(result_path).get_data()

        # TODO check data shape

        if runid=="001":
            avg_run=result_run
            continue
        
        avg_run=avg_run+result_run
        i=i+1

    avg_run=avg_run/i
    avg_data_path="avg_data_except_"+sessid1+"_"+runid+".mgh" # means average all data except sessid1, then use it cal ISFC/ISC with sessid1.
    avg_data_mgh=nib.MGHImage(avg_data,f1.get_affine())
    nib.save(avg_data_mgh,avg_data_path)
    print("Finish saving "+avg_data_path)

