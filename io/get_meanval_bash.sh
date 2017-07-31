# modified from freesurfer/fsfast/bin/mkbrainmask-sess

SubjectDIR="/s1/data/gumpdata/project"
# TODO
# SubjectList="/s1/data/gumpdata/project/sessid"
SubjectList="S001 S002 S003 S004 S005 S006 S009 S010 S014 S015 S016 S017 S018 S019 S020"
# SubjectList="S001 S002"
# RunList="/s1/data/gumpdata/project/runid"
RunList="001 002 003 004 005 006 007 008"

mcpr="fmcpr"
stc="up"
sm="sm5"
surf="fsaverage"
side="lh"
outfmt="nii.gz"

# filename="$mcpr.$stc.$sm.$surf.$side.$outfmt"
prefix="$mcpr.$stc" # In order to change different file
filename="$prefix.$outfmt"

for SubjectID in $SubjectList ; do
    for RunID in $RunList ; do
        datadir="$SubjectDIR/$SubjectID/bold/$RunID"
        meanval_path="$datadir/global.meanval.$prefix.dat" # path of meanval
        gwf_path="$datadir/global.waveform.$prefix.dat" # path of global waveform
        filepath="$datadir/$filename"

        #mask_path="$datadir/masks/brain.$surf.$side.nii.gz" # brain.fsaverage.lh.nii.gz
        mask_path="$datadir/masks/brain.e3.nii.gz" # used in freesurfer mkbrainmask-sess

        # Initial meanval steps
        echo "Compute global meanval and waveform of $SubjectID $RunID"
        meanval --i $filepath --m $mask_path --o $meanval_path --avgwf $gwf_path

    done
done
echo "All done"

