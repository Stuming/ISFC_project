"""Use matplot lib plot global mean waveform of raw function data.
In order to check data."""
import matplotlib.pyplot as plt


# TODO this function is used to plot all run into one figure, if plotting one run, should remove r and plt.axvline part.
def plot_global_waveform(wave_data, meanval_data, length_data, sessid, fig_name):
    plt.plot([num for elem in wave_data for num in elem],hold=True) # pay attention to how to get data
    plt.xlim(length_data[0],length_data[8]) # set limitation to x axis, which is needed for axhline/axvline.

    for r in range(1,9):  # FIXME r should not be settled.
        x_min = float(length_data[r-1])/length_data[8]
        x_max = float(length_data[r])/length_data[8]
        plt.axhline(meanval_data[r],xmin=x_min,xmax=x_max,color='r')
        plt.axvline(length_data[r])

    plt.title("Global waveform of "+sessid)
    #fig_name="fig_waveform/Globalwaveform_"+sessid+"_run_"+runid+"_rescaling.jpg" # save fig into folder fig_waveform
    
    print("Saving fig of "+sessid)
    plt.plot()
    plt.savefig(fig_name)
    plt.close()




