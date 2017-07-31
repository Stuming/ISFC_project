import nibabel as nib

avg_ISFC="avg_result/avg_ISFC_S020_group_86217.mgh"
fdata="/s1/data/gumpdata/project/S001/bold/001/fmcpr.up.sm0.fsaverage.lh.mgh"
f=nib.load(fdata)
data=f.get_data()
print(data.argmax(),data.argmin())
print(data.max(),data.min())
print(data.mean())
print(data.var(),data.std())
# f.get_data()  std(), min(), max(), mean(), argmax(), any()

