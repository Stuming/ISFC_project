"""Use matplot lib plot global mean waveform of raw function data.
In order to check data."""
import matplotlib.pyplot as plt
import os


def plot_waveform(wave_data, meanval=None, fig_show=True, x_min=0, x_max=1, save_path=None,
                  title_id=None, update=False):
    """Plot waveform and meanval(optional).
    Parameters:
        wave_data: load file that contains waveform.
        meanval: load file that contains meanval.
        fig_show: default is True, set it to False to skip showing figure.
        x_min: set start(%) for displaying meanval.
        x_max: set end(%) for displaying meanval.
        save_path: default is None, set a path to it to save figure into this file path.
        title_id: default is None, used to specify the image in figure title.
        update: default is False, means if save_path exists, figure will not be saved.

    Examples:
        If plot waveform of single run:
            plot_waveform(wave_data)
        If you want to save figure into file, input should specify fig_path.
            plot_waveform(wave_data, meanval=meanval, save_path=filepath, update=True)"""
    # TODO should check wave_data's type.
    plt.plot([num.rstrip("\n") for num in wave_data], hold=True)

    if meanval is not None:
        meanval = [num.rstrip("\n") for num in meanval]
        plt.axhline(meanval, xmin=x_min, xmax=x_max, color='r')

    if title_id is not None:
        plt.title("Waveform $s" % title_id)
    else:
        plt.title("Waveform")

    if fig_show:
        plt.show()

    # TODO save figure should be refactored into iofunc
    if save_path is not None:
        if os.path.exists(save_path) and not update:
            print("Not updated: %s exists, figure is not saved." % save_path)
        else:
            plt.savefig(save_path)

    plt.clf()


# TODO plot waveforms, plot multi waveforms into one figure.