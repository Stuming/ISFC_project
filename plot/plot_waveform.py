"""Use matplot lib plot global mean waveform of raw function data.
In order to check data."""
import os
import numpy as np
import matplotlib.pyplot as plt
from utils.utils import check_list


def plot_waveform(wave_data, meanval=True, fig_show=True, color='b', x_min=0, x_max=1, save_path=None,
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
    wave_data = check_list(wave_data)
    plt.plot(wave_data, hold=True, color=color)

    if meanval:
        meanval = np.mean(wave_data)
        plt.axhline(meanval, xmin=x_min, xmax=x_max, color=color)

    if title_id is not None:
        plt.title(title_id)
    else:
        plt.title("Waveform")

    # TODO save figure should be refactored into iofunc
    if save_path is not None:
        if os.path.exists(save_path) and not update:
            print("Not updated: %s exists, figure is not saved." % save_path)
        else:
            plt.savefig(save_path)
            print("Save fig: %s" % save_path)

    if fig_show:
        plt.show()

    plt.clf()


def plot_multi_waveforms(data, vertex_list, meanval=True, color='b', x_min=0, x_max=1, norm=False, fig_show=True, save_path=None,
                  title_id=None, update=False):
    """Plot multi waveforms in vertex_list into one figure.
    data
    vertex_list is list, line color would be parameter 'color'.
    if vertex_list is dict(eg. {1:'r'}), parameter 'color' will be omitted, and line color would be its value in dict.
    """
    # TODO maybe call plot_waveform() to finish plotting.
    plt.figure(figsize=(20, 10))
    custom_color = False
    if not isinstance(vertex_list, (list, dict)):
        raise Exception("Wrong type of vertex_list: %s" % type(vertex_list))
    if isinstance(vertex_list, dict):
        custom_color = True

    for vertex_num in vertex_list:
        waveform = data[vertex_num]
        if custom_color:
            color = vertex_list[vertex_num]
        if norm:
            waveform = waveform - np.mean(waveform)
            waveform = waveform / (np.max(waveform) - np.min(waveform))
            plt.ylim((-1, 1))
        if meanval:
            plt.axhline(meanval, xmin=x_min, xmax=x_max, color=color)
        plt.plot(waveform[0, 0, :], color=color, label=str(vertex_num), hold=True)

    plt.title(title_id)
    plt.legend(loc=2, bbox_to_anchor=(1, 1))

    if title_id is not None:
        plt.title(title_id)
    else:
        plt.title("Waveform")

    # TODO save figure should be refactored into iofunc
    if save_path is not None:
        if os.path.exists(save_path) and not update:
            print("Not updated: %s exists, figure is not saved." % save_path)
        else:
            plt.savefig(save_path)
            print("Save fig: %s" % save_path)

    if fig_show:
        plt.show()

    plt.clf()
