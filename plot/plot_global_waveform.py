# Use matplot lib plot global mean waveform of raw function data.
# In order to check data.
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import os
from ISFC_tools import match_datashape, load_file

datadir="/s1/data/gumpdata/project"
sessidlist=["S001", "S002", "S003", "S004", "S005", "S006", "S009", "S010", "S014", "S015", "S016", "S017", "S018", "S019", "S020"]
funcname="bold"

mcpr="fmcpr"
stc="up"
sm="sm0"
surf="fsaverage"
side="lh"
outfmt="nii.gz"

prefix=mcpr+"."+stc # In order to change different file

# waveform_filename="global.waveform.dat" # waveform of f.nii.gz
# meanval_filename="global.meanval.dat" # meanval of f.nii.gz
waveform_filename="global.waveform."+prefix+".dat" # waveform of {$prefix}.nii.gz
meanval_filename="global.meanval."+prefix+".dat"


def get_global_waveform(sessid):
    wave_data=[]
    meanval_data=[0]
    length_data=[0] # record data length of every run to plot meanval.
    for r in range(1,9):
        runid=str(r)
        while len(runid)<3:
            runid="0"+runid
        waveform_filepath=os.path.join(datadir,sessid,funcname,runid,waveform_filename)
        meanval_filepath=os.path.join(datadir,sessid,funcname,runid,meanval_filename)

        f_wave=open(waveform_filepath,"r")
        f_mean=open(meanval_filepath,"r")
        wave_rundata=f_wave.readlines()
        wave_data.append(wave_rundata)
        meanval_data.append(f_mean.readlines())
        length_data.append(len(wave_rundata)+length_data[r-1])

        f_wave.close()
        f_mean.close()
    return(wave_data,meanval_data,length_data)

def plot_global_waveform(wave_data,meanval_data,length_data,sessid,fig_name):
    plt.plot([num for elem in wave_data for num in elem],hold=True) # pay attention to how to get data
    plt.xlim(length_data[0],length_data[8]) # set limitation to x axis, which is needed for axhline/axvline.

    for r in range(1,9): # plot meanval and the split lines
        x_min=float(length_data[r-1])/length_data[8]
        x_max=float(length_data[r])/length_data[8]
        plt.axhline(meanval_data[r],xmin=x_min,xmax=x_max,color='r')
        plt.axvline(length_data[r])

    plt.title("Global waveform of "+sessid)
    #fig_name="fig_waveform/Globalwaveform_"+sessid+"_run_"+runid+"_rescaling.jpg" # save fig into folder fig_waveform
    
    print("Saving fig of "+sessid)
    plt.plot()
    plt.savefig(fig_name)
    plt.close()


for sessid in sessidlist:
#sessid="S001"
#if 1==1:
    task="global"
    if task=="global":
        # plot global waveform
        (wave_data,meanval_data,length_data)=get_global_waveform(sessid)
        fig_name="fig_waveform/Globalwaveform_all_"+sessid+"."+prefix+".jpg" # save fig into folder fig_waveform
        #fig_name="fig_waveform/Globalwaveform_all_"+sessid+".jpg" # save fig into folder fig_waveform
        plot_global_waveform(wave_data,meanval_data,length_data,sessid,fig_name)
