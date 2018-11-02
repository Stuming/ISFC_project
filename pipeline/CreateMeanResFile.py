import nibabel as nib
import os
import numpy as np
from nsnt.utils.utils import check_dir
import scipy.stats as stats


# TODO this method rely on freesurfer data struct heavily, so it's hard to expand its usage.
def avgerage_brainimg_pr(projectdir, sessidlist, funcname, analysis_name, runlist, savepath, outfmt="mgz"):
    """Average result per run after doing zscore, doing to all sessions.

    Parameters
    ----------
        projectdir: name of where your session data placed, type: str.
        sessidlist: list of sessid, type: list[str].
        funcname: name of your func, under sessid dir.
        analysis_name: analysis dir name in mkanalysis-sess.
        runlist: list of runid.
        savepath: dir of where to put average result file.
        outfmt: suffix of out file.
    """
    for runid in runlist:
        prid = "pr%s" % runid

        check_dir(savepath)
        result_name = "mean_res_%s.%s" % (runid, outfmt)
        result_path = os.path.join(savepath, result_name)

        data = []
        for sessid in sessidlist:
            fileroot = os.path.join(projectdir, sessid, funcname, analysis_name, prid, "res")
            filename = "res-%s.nii.gz" % runid
            filepath = os.path.join(fileroot, filename)

            print("loading %s" % filepath)
            result_run = nib.load(filepath)
            result_data = stats.zscore(result_run.get_data()[:, 0, 0, :], axis=1)  # doing zscore before average.
            data.append(result_data)
        print("Shape of img: {}: ".format(np.shape(data)))
        avg_data = np.mean(data, axis=0)
        print("Shape of avg_data: {}: ".format(np.shape(avg_data)))

        avg_data = np.reshape(avg_data, result_run.shape)
        data_file = nib.MGHImage(avg_data, None, result_run.get_header())

        nib.save(data_file, result_path)
        print("Saving %s" % result_path)
        print("===" * 10)

if __name__ == "__main__":
    projectdir = "/nfs/s1/studyforrest"
    funcname = "audiovisual3T"
    analysis_name = "preproc.fs5.lh"

    if True:
        # Doing zscore to every res data and then average inside run.
        sessidlist = ['sub001', 'sub002', 'sub003', 'sub004', 'sub005', 'sub006', 'sub009', 'sub010', 'sub014',
                      'sub015', 'sub016', 'sub017', 'sub018', 'sub019', 'sub020']
        runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]
        savepath = "/nfs/t3/workingshop/baihaohao/studyforrest/meandata"
        avgerage_brainimg_pr(projectdir, sessidlist, runidlist, funcname, analysis_name, savepath, outfmt="mgz")
