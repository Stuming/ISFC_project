import nibabel as nib
import numpy as np
import os

# TODO specify this function
# TODO def load_file(filepath):


def load_file(datadir, sessid, funcname, runid, filename):
    rundatadir = os.path.join(datadir,sessid,funcname,runid)
    filepath = os.path.join(rundatadir,filename)
    if not os.path.isfile(filepath):
        print(filepath+" is not a file path, please check!")
        exit(0)

    f=nib.load(filepath)
    return(f)


# TODO specify this function
# TODO def save_result(result_f,filename):
def save_result(method_name, result_f, sessid, trg_sessid, runid, vertex_num):
    # method_name refer to "ISFC", "ISC".
    # result_f means result should pass over as file format such as .mgh.
    # trg_sessid used to distinguish which data was used to cal ISFC/ISC with sessid.
    filename = method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)+".mgh"
    file_path = os.path.join("result",filename)
    nib.save(result_f,file_path)
    print("Saving "+file_path+" is done.")
