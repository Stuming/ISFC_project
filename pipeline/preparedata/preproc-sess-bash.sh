# Preproccess functional MRI data.
Sesslist="/nfs/s1/data/gumpdata/project/sessid"
SubjectFolder="/nfs/s1/studyforrest/anatomy"
export SUBJECTS_DIR=$SubjectFolder

# fsaverage5 templete
preproc-sess -sf $Sesslist -sliceorder up -fsd "bold" -surface fsaverage5 lhrh -fwhm 5 -per-run

# self templete
# preproc-sess -sf $Sesslist -sliceorder up -fsd "bold" -surface self lhrh -fwhm 5 -per-run
