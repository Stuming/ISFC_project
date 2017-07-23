import nibabel as nib
import numpy as np
import os
import array
from ISFC_tools import cal_ISFC,cal_ISC,load_file,match_datashape,save_result

# sessid="/s1/data/gumpdata/project/sessid"
datadir="/s1/data/gumpdata/project"
sessid1="S001"
sessid2="S002"
funcname="bold"
filename="fmcpr.up.sm0.fsaverage.lh.mgh" # Do analysis after mri_convert

for r in range(1,2):
    runid=str(r)
    while len(runid)<3:
        runid="0"+runid

    f1=load_file(datadir, sessid1, funcname, runid, filename)
    f2=load_file(datadir, sessid2, funcname, runid, filename)
    if not match_datashape(f1,f2):
        exit(0)
    data1=f1.get_data()
    data2=f2.get_data()
    shape1=f1.get_shape()

    vertex_num=86217
    method_name="ISFC"
    # method_name="ISC"
    if method_name=="ISFC":
        result=cal_ISFC(data1,data2,vertex_num,shape1)
    elif method_name=="ISC":
        result=cal_ISC(data1,data2,shape1)

    print("-----")
    result_f=nib.Nifti1Image(result,f1.get_affine())
    # TODO change NiftiImage to MGHImage would raise type error
    # result_f=nib.MGHImage(result,f1.get_affine())
    print("-----")

    trg_sessid=sessid2
    save_result(method_name,result_f,sessid,trg_sessid,runid,vertex_num)

print("-----------End-----------")
