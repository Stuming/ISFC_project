"""Plot head motion parameters in SPM style."""
import os
import matplotlib.pyplot as plt


def plot_headmotion(mcdat, fig_show=True, save_path=None, title_id=None, update=False):
    """fmcpr.mcdat are the motion estimates(mm and degrees).
    mcprextreg is the motion correction parameters after analysis using a PCA.
    fmcpr.mcdat data looks like this:
    In[8]: mcdat
    Out[8]:
    ['   0   0.5607  -1.0781  -0.1929   1.8588   0.4899   0.7560        24.75       12.95   2.066\n',
    '   1   0.5257  -0.9511  -0.1843   1.7889   0.4743   0.7312        24.04       12.97   1.990\n',
    '   2   0.5421  -1.0441  -0.1958   1.8692   0.4812   0.7313        24.56       13.01   2.064\n',

    Parameters:
        mcdat: load file that contains motion estimates. Like: fmcpr.mcdat
        fig_show: default is True, set it to False to skip showing figure.
        save_path: default is None, set a path to it to save figure into this file path.
        title_id: default is None, used to specify the image in figure title.
        update: default is False, means if save_path exists, figure will not be saved.

    Examples:
        plot head motion of single run:
            plot_headmotion("fmcpr.mcdat")
        plot head motion and save it into "results/S001.jpg" without showing figure:
            plot_headmotion("fmcpr.mcdat", fig_show=False, save_path="results/S001.jpg"
    """
    dS = get_para(mcdat, 4)
    dL = get_para(mcdat, 5)
    dP = get_para(mcdat, 6)
    a = get_para(mcdat, 1)
    b = get_para(mcdat, 2)
    c = get_para(mcdat, 3)
    plt.subplot(2,1,1)

    if title_id is not None:
        plt.title("Head motion %s" % title_id)
    else:
        plt.title("Head motion")

    plot_displacement(dS, dL, dP)
    plt.subplot(2,1,2)
    plot_rotation(a, b, c)

    # TODO save figure should be refactored into iofunc
    if save_path is not None:
        if os.path.exists(save_path) and not update:
            print("Not updated: %s exists, figure is not saved." % save_path)
        else:
            plt.savefig(save_path)

    if fig_show:
        plt.show()

    plt.clf()


def get_para(mcdat, index):
    """Get head motion parameter from mcdat.
    fmcpr.mcdat parameters note(index should be number-1):
    1. n      : time point
    2. roll   : rotation about the I-S axis (degrees CCW)
    3. pitch  : rotation about the R-L axis (degrees CCW)
    4. yaw    : rotation about the A-P axis (degrees CCW)
    5. dS     : displacement in the Superior direction (mm)
    6. dL     : displacement in the Left direction (mm)
    7. dP     : displacement in the Posterior direction (mm)
    8. rmsold : RMS difference between input frame and reference frame
    9. rmsnew : RMS difference between output frame and reference frame
    10. trans : translation (mm) = sqrt(dS^2 + dL^2 + dP^2)
    """
    para = []
    for i in range(0,len(mcdat)):
        tp_mcdat = mcdat[i].split()
        para.append(tp_mcdat[index])
    return para


def plot_displacement(x, y, z):
    """dS: displacement in the Superior direction (mm)
    dL: displacement in the Left direction (mm)
    dP: displacement in the Posterior direction (mm)
    """
    plt.plot(x, color="blue", label="dS", hold=True)
    plt.plot(y, color="green", label="dL")
    plt.plot(z, color="red", label="dP")
    # plt.title(""translation)
    # plt.xlabel("image")
    plt.ylabel("translation(mm)")
    plt.legend(loc=0)  # choose legend position automatically


def plot_rotation(a, b, c):
    """roll: rotation about the I-S axis (degrees CCW)
    pitch: rotation about the R-L axis (degrees CCW)
    yaw: rotation about the A-P axis (degrees CCW)
    """
    plt.plot(a, color="blue", label="roll", hold=True)
    plt.plot(b, color="green", label="pitch")
    plt.plot(c, color="red", label="yaw")
    # plt.title("rotation")
    plt.xlabel("image")
    plt.ylabel("rotation(degrees)")
    plt.legend(loc=0)
