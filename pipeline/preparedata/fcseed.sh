Sesslist="/nfs/s1/data/gumpdata/project/sessid"  # A file that contain sessid list, you may create by yourself.
SubjectDIR="/nfs/s1/studyforrest/anat/"
export SUBJECTS_DIR=$SubjectDIR

fsdname="audiovisual3T"  # You may want to modify it to "bold"

# For white matter, default use fmcpr.nii.gz
fcseed-config -fsd $fsdname -wm -fcname wm.dat -pca -cfg wm.config -overwrite
fcseed-sess -sf $Sesslist -cfg wm.config

# For CSF and ventricles
fcseed-config -fsd $fsdname -vcsf -fcname vcsf.dat -pca -cfg vcsf.config -overwrite
fcseed-sess -sf $Sesslist -cfg vcsf.config

# Project to -surface
analysisname="preproc.fs5.lh"
mkanalysis-sess -analysis $analysisname -fsd $fsdname -stc up -surface fsaverage5 lh -fwhm 5 -notask -nuisreg vcsf.dat 5 -nuisreg wm.dat 5 -mcextreg -polyfit 5 -nskip 0 -TR 2 -per-run -force

selxavg3-sess -sf $Sesslist -a $analysisname -svres -run-wise -no-con-ok -no-preproc -overwrite
