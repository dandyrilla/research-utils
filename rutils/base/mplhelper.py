import matplotlib.pyplot as plt
from matplotlib.font_manager import findSystemFonts, fontManager

from rutils.base.fileio import make_parent_dir
from rutils.base.stats import neglog10


def update_mpl_style(fontpaths='fonts'):

    for fontfile in findSystemFonts(fontpaths=fontpaths):
        fontManager.addfont(fontfile)

    # Update matplotlib rcParams
    plt.rcParams.update({
        'savefig.facecolor': 'none',
        'figure.facecolor': 'white',
        'font.family': 'Arial',
        'pdf.fonttype': 42,

        'axes.axisbelow': True,
        'axes.grid': True,
        'axes.facecolor': 'e9e9e9',
        'axes.edgecolor': 'none',
        'axes.linewidth': 0,

        'errorbar.capsize': 5,
        'legend.frameon': False,

        'xtick.major.size': 0,
        'ytick.major.size': 0,
        'xtick.minor.size': 0,
        'ytick.minor.size': 0,

        'grid.color': 'white',
        'lines.solid_capstyle': 'round',
        'image.cmap': 'Greys',
    })


def ax_axhlines_alpha(a=0.05, ax=None, **kwargs):
    """
    Draw horizontal lines of the significance level, alpha.
    Positive and negative log10-scaled alpha values are plotted at y-axis.

    :cell float a: The significance level, alpha. (0.05)
    :cell Axes ax: The axes to draw horizontal lines. (Current axes)
    :cell kwargs: Keyword arguments to pass the ``ax.axhline()`` method.

    Example:

    .. code-block:: python

        from baeklab.base import *

        plt.figure(1, figsize=(4, 3))

        params = [1, 2, 3, 4, 5]
        phreds = [-1, 4, -5, 3, -2]
        plt.bar(params, phreds)
        plt.ylabel('(signed) Phred score')

        ax_axhlines_alpha(0.05, color='red', ls='dashed')

        plt.savefig('axhlines_alpha.png')

    .. image:: _static/axhlines_alpha.png
    """
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()
    log10a = neglog10(a)
    pos, neg = (log10a, -log10a)
    ax.axhline(y=pos, **kwargs)
    ax.axhline(y=neg, **kwargs)


def autotext(x, y, s, ax=None, **kwargs):
    """
    Add text based on zero-to-one transformed axes. You don't worry about the real x and y scalars to every axes.
    The function automatically aligns the text depending on the positions.

    :cell float x: The position to place the text on the x axis: 0.0 (left) to 1.0 (right)
    :cell float y: The position to place the text on the y axis: 0.0 (bottom) to 1.0 (top)
    :cell str s: The text.
    :cell Axes ax: The axes to place the text. (Current axes)
    :cell kwargs: Keyword arguments to pass the ``ax.text()`` method.

    Example:

    .. code-block:: python

        import numpy as np
        from baeklab.base import *

        t = np.arange(0, 2, 0.01)
        s = np.sin(2 * np.pi * t)

        fig, ax = plt.subplots()
        ax.plot(t, s, color='lightgray')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (mV)')
        ax.set_title('autotext(): Convenient way to plot text')

        kwargs = dict(fontsize='x-large', color='red')
        autotext(0.0, 0.0, 'Left\\nbottom',  **kwargs)
        autotext(0.0, 0.5, 'Left\\ncenter',  **kwargs)
        autotext(0.0, 1.0, 'Left\\ntop',     **kwargs)
        autotext(0.5, 0.0, 'Bottom',        **kwargs)
        autotext(0.5, 0.5, 'Center',        **kwargs)
        autotext(0.5, 1.0, 'Top',           **kwargs)
        autotext(1.0, 0.0, 'Right\\nbottom', **kwargs)
        autotext(1.0, 0.5, 'Right\\ncenter', **kwargs)
        autotext(1.0, 1.0, 'Right\\ntop',    **kwargs)
        autotext(0.25, 0.25, '0.25, 0.25',  **kwargs)
        autotext(0.75, 0.75, '0.75, 0.75',  **kwargs)

        plt.savefig("autotext.png")

    .. image:: _static/autotext.png
    """
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()
    ha = 'center' if x == 0.5 else ('left' if x < 0.5 else 'right')
    va = 'center' if y == 0.5 else ('bottom' if y < 0.5 else 'top')
    text_kw = dict(xycoords='axes fraction', ha=ha, va=va)
    text_kw.update(kwargs)
    ax.annotate(s, xy=(x, y), **text_kw)


def autolabel(rects, xpos='center', formatstr='{}', ax=None, ylim=None, **kwargs):
    """
    Attach a text label above each bar in ``rects``, displaying its height.
    (Inspired by `autolabel() <https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html>`_)

    :cell list rects: List of bar rectangle objects.
    :cell str xpos: indicates which side to place the text w.r.t. the center of the bar.
                      It can be one of the following ('center', 'right', 'left').
    :cell str formatstr: The string for formatting label. ('{}')
    :cell Axes ax: The axes to place the text. (Current axes)
    :cell kwargs: Keyword arguments to pass the ``ax.text()`` method.

    Example:

    .. code-block:: python

        import numpy as np
        from baeklab.base import *

        men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
        women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)

        ind = np.arange(len(men_means))  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2,   men_means, width, yerr=men_std,   color='skyblue',   label='Men')
        rects2 = ax.bar(ind + width / 2, women_means, width, yerr=women_std, color='indianred', label='Women')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(ind)
        ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
        ax.legend()

        autolabel(rects1, 'left', ax=ax, color='skyblue')
        autolabel(rects2, 'right', ax=ax, color='indianred')

        plt.savefig('autolabel.png')

    .. image:: _static/autolabel.png
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    for rect in rects:
        height = rect.get_height()
        va = 'bottom' if height >= 0.0 else 'top'
        if ylim and height < ylim[0]:
            height = ylim[0]
            va = 'bottom'
        if ylim and ylim[1] < height:
            height = ylim[1]
            va = 'top'
        x = rect.get_x() + rect.get_width() * offset[xpos]
        y = height
        ax.text(x, y, formatstr.format(height), ha=ha[xpos], va=va, **kwargs)


def set_xtlab(ax, x, xtlab, **kwargs):
    """
    Set xticklabels.
    """
    ax.set_xticks(x)
    ax.set_xticklabels(xtlab, **kwargs)


def set_ylim_symm(ax):
    """
    Set y-axis symmetrical based on 0.0.
    """
    yb, yt = ax.get_ylim()
    yabsmax = max(abs(yb), abs(yt))
    ax.set_ylim(-yabsmax, yabsmax)


def set_sharey_symm(axs):
    """
    Make y-axes symmetrical.
    """
    yabsmax = 0
    for ax in axs:
        yb, yt = ax.get_ylim()
        yabsmax = max(abs(yb), abs(yt), yabsmax)
    for ax in axs:
        ax.set_ylim(-yabsmax, yabsmax)


def savefig(filename, **kwargs):
    make_parent_dir(filename)
    tight_layout = kwargs.pop('tight_layout', False)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(filename, **kwargs)
    plt.close()
