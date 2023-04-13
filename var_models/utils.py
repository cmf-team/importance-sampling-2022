import matplotlib.pyplot as plt
import numpy as np


def plot_var(var, target):
    """
    Plots returns of a portfolio and calculated VaR in a single figure.

    Parameters
    ----------
    var
        Predicted VaRs.
    target
        Corresponded returns.
    """
    plt.figure(figsize=(12, 3))
    plt.plot(target, label='target')
    plt.plot(var, label='var')
    ymin = min(target.min(), var.min())
    ymax = max(target.max(), var.max())
    plt.vlines(
        np.arange(len(target))[target < var], 
        ymin, 
        ymax,
        label='exceptions',
        zorder=3)
    plt.ylim(ymin, ymax)
    plt.legend()
    plt.show()
