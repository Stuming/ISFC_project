# Create session folder and copy fmri data into run dir

import os
from shutil import copyfile

path_project='/s1/data/gumpdata/project'
path_rawdata='/s1/data/gumpdata/ds000113d_R2.0.0'
fmri_suffix='ses-movie/func'

# TODO 
runid=1
for i in range(1,21):

    subid_str=str(i)
    while len(subid_str)<2:
        subid_str='0'+subid_str
    subid='sub-'+subid_str

    sessid=str(i)
    while len(sessid)<3:
        sessid='0'+sessid
    sessdir='S'+sessid
    sessdir=os.path.join(path_project,sessdir)

    # Make session/bold dir
    bold_folder=os.path.join(sessdir,'bold')
    if os.path.exists(bold_folder):
        continue
    os.makedirs(bold_folder)

    for runid in range(1,9):
        # Make run dir
        runid_str=str(runid)
        while(len(runid_str)<3):
            runid_str='0'+runid_str

        rundir=os.path.join(bold_folder,runid_str)
        if not os.path.exists(rundir):
            os.makedirs(rundir)
        newdata_path=os.path.join(path_project,rundir,'f.nii.gz')

        # Get raw data path
        rawdata_dir=os.path.join(path_rawdata,subid,fmri_suffix)
        filename=subid+'_ses-movie_task-movie_run-'+str(runid)+'_bold.nii.gz'
        rawdata_path=os.path.join(rawdata_dir,filename)

        if os.path.isdir(rawdata_dir):
            copyfile(rawdata_path,newdata_path)
        else:            
            print('Error when copy run '+runid_str)
            print(rawdata_dir)

print('done')
