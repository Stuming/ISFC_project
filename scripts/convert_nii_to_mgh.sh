SubjectDIR="/s1/data/gumpdata/project"
# TODO
# SubjectList="/s1/data/gumpdata/project/sessid"
SubjectList="S003 S004 S005 S006 S009 S010 S014 S015 S016 S017 S018 S019 S020"
# SubjectList="S001 S002"
# RunList="/s1/data/gumpdata/project/runid"
RunList="001 002 003 004 005 006 007 008"

for SubjectID in $SubjectList ; do
    for RunID in $RunList ; do
        filepath="$SubjectDIR/$SubjectID/bold/$RunID"
        srcImage="$filepath/fmcpr.up.sm0.fsaverage.lh.nii.gz"
        trgImage="$filepath/fmcpr.up.sm0.fsaverage.lh.mgh"
        # Initial Recon-all Steps
        echo "Convert $SubjectID $RunID to mgh"
        mri_convert $srcImage $trgImage -ot mgh
    done
done
echo "All done"
