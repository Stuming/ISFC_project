# Preproccess functional MRI data.
Sesslist="/s1/data/gumpdata/project/sessid"
SubjectFolder="/s1/data/gumpdata/project/anatomy"
export SUBJECTS_DIR=$SubjectFolder

# fsaverage templete
preproc-sess -sf $Sesslist -sliceorder up -fsd "bold" -surface fsaverage lhrh -fwhm 0 -per-run

# self templete
# preproc-sess -sf $Sesslist -sliceorder up -fsd "bold" -surface self lhrh -fwhm 0 -per-run
