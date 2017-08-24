"""Use matplot lib plot global mean waveform of raw function data.
In order to check data."""
import matplotlib.pyplot as plt


def plot_waveform(wave_data, meanval=None, x_min=0, x_max=1, sessid=None, runid=None, fig_path=None):
    """Plot waveform and meanval(optional).
    If plot waveform of single run:
        plot_group_waveform(wave_data)
    If you want to save figure into file, input should specify fig_path."""
    # TODO should check wave_data's type.
    plt.plot([num.rstrip("\n") for num in wave_data], hold=True)

    if meanval is not None:
        meanval = [num.rstrip("\n") for num in meanval]
        plt.axhline(meanval, xmin=x_min, xmax=x_max, color='r')

    if sessid is not None:
        if runid is not None:
            plt.title("Global waveform %s %s" % (sessid, runid))
        else:
            plt.title("Global waveform $s" % sessid)
        plt.show()
    else:
        plt.title("Global waveform")
        plt.show()

    if fig_path is not None:
        print("Saving figure: %s" % fig_path)
        plt.savefig(fig_path)
        plt.close()


# This function is used to plot all run into one figure, if plotting one run, should remove r and plt.axvline part.
# And it is not used now.
def plot_waveforms(wave_data, sessid=None, meanval=None, data_length=None,
                        x_min=0, x_max=1, fig_path=None):
    """Plot waveform and meanval(optional).
    If plot waveform of single run:
        plot_group_waveform(wave_data)
    If plot waveform of multiple runs:
        plor_waveform(wave_data, meanval=meanval_data, data_length=data_length)
    If want to save figure into file, should specify sessid(only use to show info) and fig_path."""
    # TODO should check wave_data's type.
    plt.plot([num.rstrip("\n") for num in wave_data], hold=True)

    if meanval is not None:
        meanval = [num.rstrip("\n") for num in meanval]
        if data_length is not None:
            plt.xlim(data_length[0], data_length[8]) # set limitation to x axis, which is needed for axhline/axvline.
            for r in range(1,9):  # FIXME r should not be settled.
                x_min = float(data_length[r - 1]) / data_length[8]
                x_max = float(data_length[r]) / data_length[8]
                plt.axhline(meanval[r], xmin=x_min, xmax=x_max, color='r')
                plt.axvline(data_length[r])
        else:
            plt.axhline(meanval, xmin=x_min, xmax=x_max, color='r')

    if sessid is not None:
        plt.title("Global waveform %s" % sessid)
        plt.show()
        if fig_path is not None:
            print("Saving fig of %s" % sessid)
            plt.savefig(fig_path)
            plt.close()
    else:
        plt.title("Global waveform")
        plt.show()

