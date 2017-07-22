SubjectDIR="/s1/data/gumpdata/project/anatomy"
SubjectList="sub002 sub003 sub004 sub005 sub006 sub009 sub010 sub014 sub015 sub016 sub017 sub018 sub019 sub020"

for SubjectID in $SubjectList ; do
    T1wImage="/s1/data/gumpdata/Anat-data/$SubjectID/anatomy/highres001.nii.gz"
    T2wImage="/s1/data/gumpdata/Anat-data/$SubjectID/anatomy/other/t2w001.nii.gz"
    T1wImageFile='highres001_1mm.nii.gz';

# Make Spline Interpolated Downsample to 1mm
# echo "Make Spline Interpolated Downsample to 1mm"
# Mean=`fslstats $T1wImage -M`
# flirt -interp spline -in "$T1wImage" -ref "$T1wImage" -# applyisoxfm 1 -out "$T1wImageFile"
# applywarp --rel --interp=spline -i "$T1wImage" -r "$T1wImageFile" --premat=$FSLDIR/etc/flirtsch/ident.mat -o "$T1wImageFile"
# fslmaths "$T1wImageFile" -div $Mean -mul 150 -abs "$T1wImageFile"

    # Initial Recon-all Steps
    echo "Initial Recon-all Steps"
    recon-all -i "$T1wImageFile" -subjid "$SubjectID" -sd "$SubjectDIR" -T2 "$T2wImage" -T2pial -all

done
echo "Done"
