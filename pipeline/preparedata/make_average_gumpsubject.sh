echo "This script try to make average subject based on studyforrest anat data after recon-all."
echo "In my research, the result is quite similar to freesurfer, try by your need."
echo "----------"

export SUBJECTS_DIR=/nfs/s1/studyforrest/anat

# make average subject first, output name is gumpaverage
make_average_subject --out gumpaverage --surf-reg sphere.reg.gumpaverage --subjects sub001 sub002 sub003 sub004 sub005 sub006 sub009 sub010 sub014 sub015 sub016 sub017 sub018 sub019 sub020

# project every subject onto gumpaverage, prepare for an iteration.
for subject in sub001 sub002 sub003 sub004 sub005 sub006 sub009 sub010 sub014 sub015 sub016 sub017 sub018 sub019 sub020
do
    cd $SUBJECTS_DIR/$subject
    mris_register surf/lh.sphere \
        $SUBJECTS_DIR/gumpaverage/lh.reg.template.tif \
        surf/lh.sphere.reg.gumpaverage
    mris_register surf/rh.sphere \
        $SUBJECTS_DIR/gumpaverage/rh.reg.template.tif \
        surf/rh.sphere.reg.gumpaverage
done

# make average subject again, based on projected data, output name is newgumpaverage.
mris_preproc --surfreg sphere.reg.gumpaverage --s sub001 --s sub002 --s sub003 --s sub004 --s sub005 --s sub006 --s sub009 --s sub010 --s sub014 --s sub015 --s sub016 --s sub017 --s sub018 --s sub019 --s sub020

make_average_subject --out newgumpaverage --surf-reg sphere.reg.gumpaverage --subjects sub001 sub002 sub003 sub004 sub005 sub006 sub009 sub010 sub014 sub015 sub016 sub017 sub018 sub019 sub020
