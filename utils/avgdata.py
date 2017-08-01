# Modified from average_data.py
# Average result of every run into one.
# Input result name would like: avg_data_except_S001_run1.mgh
# means average all data in sessidlist except S001
# TODO modify filename to average brain image data

import nibabel as nib
from iofunc.iofile import load_file


def avg_data_pr(projectdir, sessidlist, runlist, method_name, trg_sessid, vertex_num, outfmt=".mgh"):
    """Average result by run, doing to all sessions."""
    for sessid in sessidlist:
        i = 0
        avg_run = 0

        for runid in runlist:
            result_path = method_name+"_"+sessid+"_"+trg_sessid+"_"+runid+"_"+str(vertex_num)+outfmt

            # TODO load data should do by iofunc
            result_run = nib.load(result_path)
            avg_run = avg_run+result_run.get_data()
            i = i+1

        avg_run = avg_run/i

        # TODO save path maybe point to a sub folder.
        avg_run_path = "avg_result/avg_"+method_name+"_"+sessid+"_"+trg_sessid+"_"+str(vertex_num)+outfmt
        avg_run_f = nib.MGHImage(avg_run,result_run.get_affine())

        # TODO save result should do by iofunc
        nib.save(avg_run_f,avg_run_path)
        print("Finish saving %s" % avg_run_path)

