import nibabel as nib
import numpy as np
import os
import array

# sessid="/s1/data/gumpdata/project/sessid"
datadir="/s1/data/gumpdata/project"
sessid1="S002"
sessid2="S001"
funcname="bold"
filename="fmcpr.up.sm0.fsaverage.lh.mgh" # Do analysis after mri_convert

def show_shape(datadir,sessid,funcname,filename):
    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid
        rundatadir=os.path.join(datadir,sessid,funcname,runid)
        filepath=os.path.join(rundatadir,filename)

        f1=nib.load(filepath)
        print(runid+": ")
        print(f1.get_shape())


for r in range(1,9):
    runid=str(r)
    while len(runid)<3:
        runid="0"+runid
    rundatadir1=os.path.join(datadir,sessid1,funcname,runid)
    rundatadir2=os.path.join(datadir,sessid2,funcname,runid)
    filepath1=os.path.join(rundatadir1,filename)
    filepath2=os.path.join(rundatadir2,filename)

    f1=nib.load(filepath1)
    f2=nib.load(filepath2)

    shape1=f1.get_shape()
    shape2=f2.get_shape()
    if shape1==shape2:
        print(shape1)
        data1=f1.get_data()
        data2=f2.get_data()
        result=np.zeros((shape1[0],1,1))

        temp1=array.array('f')
        i1=0 # Cal corr between sub1(i1,j1) and sub2(:,:)
        temp1.fromlist(data1[i1,0,0,:].tolist()) # np.corrcoef need array as input
        for i2 in range(0,shape2[0]):
            if i1==i2:
                result[i2,0,0]=1
                continue
            temp2=array.array('f')
            temp2.fromlist(data2[i2,0,0,:].tolist())
            print(i2)
            result[i2,0,0]=np.corrcoef(temp1,temp2)[0,1] # Get corrcoef from corr matrix
            if np.isnan(result[i2,0,0]):
                result[i2,0,0]=0 # Or use mri_convert to finish this
        print(result)

    result_nii=nib.Nifti1Image(result,f1.get_affine())
    print("-----")
    result_filename="result_"+sessid1+"_"+"run"+runid+"_"+str(i1)+".mgh"
    nib.save(result_nii,result_filename)

print("-----------End-----------")
