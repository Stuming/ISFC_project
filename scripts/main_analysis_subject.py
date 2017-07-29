import nibabel as nib
import numpy as np
import os
import array
from ISFC_tools import cal_ISFC,cal_ISC,cal_FC,load_file,match_datashape,save_result

# sessid="/s1/data/gumpdata/project/sessid"
datadir="/s1/data/gumpdata/project"
sessidlist=["S002", "S003", "S004", "S005", "S006", "S009", "S010", "S014", "S015", "S016", "S017", "S018", "S019", "S020"]
sessid1="S001"
sessid2="S002"
funcname="bold"
filename="fmcpr.up.sm0.fsaverage.lh.mgh" # Do analysis after mri_convert

for sessid1 in sessidlist:
#if 1==1:
    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid
    
        # load f1 because all method need at least 1 input.
        f1=load_file(datadir, sessid1, funcname, runid, filename)
        data1=f1.get_data()
        shape1=f1.get_shape()
        vertex_num=86217
        method_name="FC"
    
        if method_name=="ISFC" or method_name=="ISC":
            f2=load_file(datadir, sessid2, funcname, runid, filename)
            if not match_datashape(f1,f2):
                exit(0)
            data2=f2.get_data()
    
            if method_name=="ISFC":
                result=cal_ISFC(data1,data2,vertex_num,shape1)
            elif method_name=="ISC":
                result=cal_ISC(data1,data2,shape1)
    
            # TODO merge save part of ISFC/ISC and FC into one.
            print("-----")
            result_f=nib.Nifti1Image(result,f1.get_affine())
            # TODO change NiftiImage to MGHImage would raise type error
            # result_f=nib.MGHImage(result,f1.get_affine())
            print("-----")
            save_result(method_name,result_f,sessid1,sessid2,runid,vertex_num)
    
        elif method_name=="FC":
            result=cal_FC(data1,vertex_num,shape1)
            result_f=nib.Nifti1Image(result,f1.get_affine())
            trg_sessid="self"
            save_result(method_name,result_f,sessid1,trg_sessid,runid,vertex_num)

print("-----------End-----------")
