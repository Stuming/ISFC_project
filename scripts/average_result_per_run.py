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
method_name="ISFC"
vertex_num=86217

for sessid in sessidlist:
#sessid="S001"
#if 1==1:
    i=0
    avg_run=0

    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid

        trg_sessid="group"
        result_path=method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)+".mgh"
        result_run=nib.load(result_path)

        avg_run=avg_run+result_run.get_data()
        i=i+1

    avg_run=avg_run/i
    avg_run_path="avg_result/avg_"+method_name+"_"+sessid+"_"+trg_sessid+"_"+str(vertex_num)+".mgh" # means average all data of sessid.
    avg_run_f=nib.MGHImage(avg_run,result_run.get_affine())
    nib.save(avg_run_f,avg_run_path)
    print("Finish saving "+avg_run_path)

