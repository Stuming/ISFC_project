import os
from time import time
from itertools import combinations

import numpy as np
import nibabel as nib
from scipy.sparse import csc_matrix

from nsnt.utils.adj_tools import get_faces, split_connected_components


def load_data(data_root, file_name):
    data_path = os.path.join(data_root, file_name)
    print("Loading: %s" % data_path)
    f = nib.load(data_path)
    data = f.get_data()[:, 0, 0]
    return data


def get_filename(method_name, runid, parcel_num):
    projectdir = "/nfs/s1/studyforrest"
    analysisname = "preproc.fs5.lh"

    if method_name in ["KMeans", "hier_clustering"]:
        dataroot = os.path.join(projectdir, "average", analysisname, runid, method_name)
        filename1 = "%s-res-%s-%i-by_vertex.mgz" % (method_name, runid, parcel_num)

    elif method_name in ["spectral_clustering"]:
        dataroot = os.path.join(projectdir, "average", analysisname, runid, method_name)
        filename1 = "%s-res-%s-%i-by_vertex-edist-0.10.mgz" % (method_name, runid, parcel_num)

    elif method_name in ["hier_clustering-adj"]:
        dataroot = os.path.join(projectdir, "average", analysisname, "hier_clustering")
        filename1 = "hier_clustering-res-%s-%i-by_vertex-adj.mgz" % (runid, parcel_num)

    elif method_name in ["spectral_clustering-adj"]:
        dataroot = os.path.join(projectdir, "average", analysisname, "spectral_clustering")
        filename1 = "ncut-res-%s-%i-sk-adj.mgz" % (runid, parcel_num)

    elif method_name in ["KMeans-hier_clustering"]:
        dataroot = os.path.join(projectdir, "average", analysisname, method_name)
        filename1 = "%s-res-%s-1000-%i-adj.mgz" % (method_name, runid, parcel_num)

    elif method_name in ["geo"]:
        dataroot = os.path.join(projectdir, "average", analysisname)
        filename1 = "%s-res-001-%i-by_vertex.mgz" % (method_name, parcel_num)

    else:
        raise Exception("Wrong method name.")
    return dataroot, filename1


if __name__ == "__main__":
    # sessid="/nfs/s1/data/gumpdata/project/sessid"
    datadir = "/nfs/s1/studyforrest"
    projectdir = '/nfs/t3/workingshop/baihaohao/studyforrest'
    runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]

    funcname = "audiovisual3T"
    analysisname = "preproc.fs5.lh"

    faces = get_faces("fsaverage5", "lh", "inflated")

    t0 = time()
    for runid in runidlist:

        parcels_list = range(50, 300, 50)
        # method_list = ["KMeans", "hier_clustering", "spectral_clustering", "geo"]
        method_list = ["KMeans", "hier_clustering", "spectral_clustering"]

        for method_name in method_list:
            for parcel_num in parcels_list:
                dataroot = os.path.join(projectdir, runid, method_name, "repeated")
                result = np.zeros((10242, 10242))

                for times in range(100):
                    filename1 = "%s-res-%s-%i-by_vertex-%i.mgz" % (method_name, runid, parcel_num, times)
                    print("Loading {}".format(filename1))
                    labelimg1 = load_data(dataroot, filename1)

                    labelimg2 = split_connected_components(labels=labelimg1, faces=faces)
                    labels = np.unique(labelimg2)

                    for label in labels:
                        for i, j in combinations(np.where(labelimg2 == label)[0], 2):
                            result[i, j] = result[i, j] + 1
                            result[j, i] = result[i, j]

                resultname = "%s-res-%s-%i-by_vertex-overlap-sec%i.npz" % (method_name, runid, parcel_num, 100)
                resultpath = os.path.join(dataroot, resultname)
                result = csc_matrix(result, dtype=np.int)
                np.savez(resultpath, result=result)
                print("Saving {}".format(resultpath))
                print("Spend time: %f" % (time() - t0))

print("-----------End-----------")
