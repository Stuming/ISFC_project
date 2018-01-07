"""Average result of every run into one.
Input result name would like: avg_data_except_S001_run1.mgh
means average all data in sessidlist except S001."""
import os
from ..iofunc.iofile import load_imgfile, save_img


# TODO modify input to make sure this function work whether input raw data path or result path.
def avg_data_pr(projectdir, sessidlist, runlist, method_name, trg_sessid, vertex_num, funcname="bold", outfmt=".mgh"):
    """Average result per run, doing to all sessions."""
    for sessid in sessidlist:
        i = 0
        avg_run = 0

        for runid in runlist:
            filename = "%s_%s_%s_%s_%s%s" % (method_name, sessid, trg_sessid, runid, str(vertex_num), outfmt)
            filepath = os.path.join(projectdir,filename)
            result_run = load_imgfile(filepath)
            avg_run = avg_run + result_run.get_data()
            i = i+1

        avg_run = avg_run/i

        data_dir = "./"
        data_type = "avg_result"
        result_name = "avg_%s_%s_%s_%s%s" % (method_name, sessid, trg_sessid, str(vertex_num), outfmt)

        save_img(data_dir, data_type, result_name, avg_run, result_run.get_affine())
