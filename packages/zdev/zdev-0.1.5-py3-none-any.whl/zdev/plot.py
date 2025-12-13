"""
Routines for for quick & easy plotting (especially during development)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as mpla
import plotly.graph_objects as go
import plotly.subplots as sp
from functools import partial

from zdev.core import iscomplex
from zdev.colors import *

import pyarrow as pa
import pyarrow.parquet as pq

try:
    from zynamon.zeit import istimeseries, convert_time
    SUPPORTS_TS = True
except:
    SUPPORTS_TS = False
    print("zdev.plot: No support for 'zynamon.zeit.TimeSeries' objects!")


# INTERNAL PARAMETERS & DEFAULTS
_COL_CYCLE = [cDodgerBlue, cSeaGreen, cRed, cGoldenRod, cSteelBlue, cDeepPink, cBlack, cSilver]
_MX_CYCLE = ['.','*','x','p','v','^','<','>','d','o','s','D'] # sorted ~ from small to large
_MX_NUM = 200
_TITLE_SIZE = 10
_YLABEL_SIZE = 9
_TICK_SIZE = 7
_FIG_MARGIN_TOP    = 0.01   # distance to "top" of page
_FIG_MARGIN_BOTTOM = 0.03   # distance to "bottom" of page
_FIG_MARGIN_LEFT   = 0.03   # distance to "left" of page
_FIG_MARGIN_RIGHT  = 0.00   # distance to "right" of page
_SUBPLOT_SCALE = 0.88       # scaling to ensure minimum distance between all axes
_SUBPLOT_BOOST = 0.98       # scaling "boost" for higher number of subplots
_TS_NUM_TICKS = 31            # number of horizontal axis ticks (only for 'TimeSeries' data) 
_TS_FMT = '%Y-%m-%d %H:%M:%S' # format string if 'ISO' display (only for 'TimeSeries' data) 


def unpack_signals(x):
    """ Auto-detects all signals found in 'x' (list | dict | np.ndarray | else) to a flat list. """

    # automatically check on (outer) type & dimensionality of all signals
    all_signals = []

    # (1) LIST
    if (type(x) is list):
        # (1a) "pure, flat list" -> i.e. single signal
        if ((type(x[0]) is not list) and (type(x[0]) is not np.ndarray) and 
            ((not SUPPORTS_TS) or (not istimeseries(x[0])))):
            all_signals.append(x)
        else: # (1b) actual collection of signals
            for s in range(len(x)):
                all_signals.append(x[s])

    # (2) DICT (i.e. named signals)
    elif (type(x) is dict):
        for s, name in enumerate(x.keys()):
            all_signals.append(x[name]) #fixme: what if nested signals (in dict item?)

    # (3) NUMPY ARRAY
    elif (type(x) is np.ndarray):
        # (3a) single signal (1D)
        if (x.ndim == 1):
            all_signals.append(x)
        # (3b) collection of signals
        elif (x.ndim == 2):
            S = min(x.shape)
            idx = x.shape.index(S)
            for s in range(x.shape[idx]):
                all_signals.append(x[s,:])
        # (3c) collection of signals (N-1 layers)
        else:
            D = x.ndim
            S = np.prod(x.shape[:-1]) # num of contained signals (i.e. 'x.shape[-1]' = length)
            # determine all unique index combinations
            idx = [None] * S
            counter = [-1] * (D-1)
            for s in range(S):
                for d in range(D-1):
                    counter[d] += 1
                    if (counter[d] > x.shape[d]-1):
                        counter[d] = 0 # wrap!
                idx[s] = counter.copy()
            idx.sort()
            # copy individual signals (all tensors elements w/ 'd < x.ndim')
            for s in range(S):
                x_reduced = x
                for d in range(D-1):
                    x_reduced = x_reduced[ idx[s][d] ]
                all_signals.append(x_reduced)

    else: # anything else (e.g. 'cbm.TimeSeries' object or plain 'pd.Series'/'pd.DataFrame')
        all_signals.append(x)

    return all_signals


def axxess(fig=None, newplot=False):
    """ Returns handle to axes in existing or new figure (matplotlib framework).

    This is a convenience function to provide an "ease-of-use" feeling for creating (new) axes
    objects in an existing figure. Note that in case of 'newplot=True' this will extend the
    existing layout *auto%matplotlib inlinemagically* (i.e. acc. to internal settings).

    Args:
        fig (:obj:, optional): Existing figure handle. Defaults to 'None' (i.e. create new one).
        newplot (bool, optional): Switch for adding a new subplot/axes at the bottom (if an
            existing figure is used). Defaults to 'False'.

    Returns:
        fh (:obj:): Handle to the figure where axes are located.
        ax (:obj:): Handle to the current axes object on that figure.
    """

    # create new figure...
    if ((fig is None) or (type(fig) is not mpl.figure.Figure)):
        fh = plt.figure()
        ax = fh.subplots(1,1)
    else: # ...use existing figure
        fh = fig

        # insert new axes? (i.e. shift all existing ones by assigning new positions)
        if (newplot):
            all_axes = fh.get_axes()
            M, N = len(all_axes), 1 # Q: don't force single-column layout / how to extend?           
            M += 1 # increase number of tiles

            # compute normalised heigth & width of all layout tiles
            H = (1. - (_FIG_MARGIN_TOP+_FIG_MARGIN_BOTTOM)) / M
            W = (1. - (_FIG_MARGIN_LEFT+_FIG_MARGIN_RIGHT)) / N

            # compute axes sizes & offsets from (outer) tile to (inner) axes)
            h = H * _SUBPLOT_SCALE * _SUBPLOT_BOOST**(M-1)
            w = W * _SUBPLOT_SCALE * _SUBPLOT_BOOST**(N-1)
            osh = H * (1. - _SUBPLOT_SCALE)/2.
            osw = W * (1. - _SUBPLOT_SCALE)/2.

            n = 0 # FIXME: don't force single-column layout / how to extend?
            for m, ax in enumerate(all_axes):
                pos = [ _FIG_MARGIN_LEFT+osw+n*W, _FIG_MARGIN_BOTTOM+osh+(M-1-m)*H, w, h ]
                ax.set_position(pos, which='both')

            # add newest axes (at bottom)
            ax = fh.add_axes([ _FIG_MARGIN_LEFT+osw+n*W, _FIG_MARGIN_BOTTOM+osh+0.0, w, h ])

        # get last axes
        ax = fh.get_axes()[-1]

    return fh, ax


def aniplot(x, t=None, N=1000, L=25, cycle=0.3, accu=False, blit=False, 
            fig=None, newplot=False):
    """ Provides an animated plot of 'x' by advancing 'N' samples at a defined update 'cycle'.

    Args:
        x (np.ndarray): Signal to be visualised.
        t (np.ndarray, optional): Time reference for plotting (if any). Defaults to 'None'.
        N (int, optional): Sliding window size (i.e. number of samples). Defaults to 1000.
        L (int, optional): Frame shift (i.e. number of new samples per step).  Defaults to 25.
        cycle (float, optional): Update rate for animation [s]. Defaults to 0.3 (i.e. 300ms).
        accu (bool, optional): Switch for keep *all* old data, i.e. effective frame size will
            increase by each step. Defaults to 'False'.
        blit (bool, optional): Switch for using a "blitter" mode which does not allow for
            adjustments to the axes (ranges, ticks, labels) but requires less computational
            power & is faster since only "y-values" are drawn anew. Defaults to 'False'.
        fig (:obj:, optional): Existing figure handle. Defaults to 'None' (i.e. create new one).
        newplot (bool, optional): Switch for plotting into a new subplot. Defaults to 'False'.

    Returns:
        ani (:obj:): Animation object associated w/ the underlying timers.
    """

    # get objects & init
    if (fig is None):
        fh, ax = axxess(fig, newplot)
    else:
        fh = fig
        ax = fig.gca()
    mpl.style.use('seaborn-v0_8-darkgrid') #'classic' | 'grascale'

    # check consistency
    if ((L/cycle) > 500):
        print("Warning: High rate of incoming samples > 500/cycle! (actual display may be slower)")
    elif (len(x) < N):
        print(f"Input signal has less than N={N} samples! (aborting)")
        qplot(x, t, fig=fh)
        mpl.style.use('default')
        return fh, ax, -1
    elif (accu and blit):
        print("No accumulation in 'blit' mode! (ignoring)")
        accu = False

    # set data ranges
    if (t is None):
        t = np.arange(len(x))
    V = int( (len(x)-N+1)/L )
    y_limits = [min(x), max(x)]

    # init function (only for 'blit' mode)
    def blitinit():
        ax.set_xlabel("Time [samples]")
        ax.set_ylabel("Measurement")
        ax.set_xlim([0, N])
        ax.set_ylim(y_limits) # Note: This has to be fixed!
        ax.grid(True)
        line, = ax.plot([],[])
        return line,

    # init function (only for 'blit' mode)
    def blitstep(v, x, N, L, ax):
        fixed_t = np.arange(0,N)
        data_x = x[v*L:v*L+N]
        ax.clear()
        line, = ax.plot(fixed_t, data_x)
        return line,

    # step function (for updating)
    def anistep(v, x, t, N, L, ax, accumulate):
        if (accumulate):
            if (v*L+N <= 4000):
                data_t = t[0:v*L+N]
                data_x = x[0:v*L+N]
            else:
                data_t = t[v*L+N-4000:v*L+N]
                data_x = x[v*L+N-4000:v*L+N]
        else: # sliding window
            data_t = t[v*L:v*L+N]
            data_x = x[v*L:v*L+N]
        ax.clear()
        ax.plot(data_t, data_x)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Measurement")
        ax.grid(True)
        return

    # run the animation
    if (blit):
        ani = mpla.FuncAnimation(fh, blitstep, fargs=[x, N, L, ax],
                                 init_func=blitinit, blit=True, frames=V, interval=(cycle*1000))
    else:
        ani = mpla.FuncAnimation(fh, anistep, fargs=[x, t, N, L, ax, accu],
                                 init_func=None, frames=V, interval=(cycle*1000))

    # finalise figure
    fh.tight_layout()
    mpl.style.use('default')

    return fh, ax, ani


def quickplot(sig, ref=None, info=None, color=None, ylabel=None, title=None, fig=None,
              bold=False, legend=True, time_iso=False, newplot=False, drawmode='plot'):
    """ Quickly displays signal 'sig' w/ optional time 'ref' (matplotlib framework).

    This function is provided for a more intuitive use of the "matplotlib" package. It supports
    a default behaviour for a quick & convenient plotting w/ (optional) time reference as well
    as superposition of signals, labeling and/or addition of subplots.

    If 'signal' refers to a list, dict or np.ndarrays, the provided data is plotted in a
    "bundled" way, treating the N-dim layer as containing individual signals, while each may be
    of type 'list', 'np.ndarray' or 'TimeSeries'. If plotting multiple signals in this way, both
    'info' and 'color' parameters have to be given as lists. Moreover for complex-valued data,
    both real and imaginary parts will be plotted alongside.

    Note: For quickest use, simply type 'qplot(sig)'!

    Args:
        sig (np.ndarray): Signal(s) to be visualised. If more signals are containd here, all of
            them will be unbundeled to a flat list.
        ref (np.ndarray, optional): Time reference for plotting (if any). Defaults to 'None'.
        info (str, optional): Text(s) to be used as legend entry (if any). Defaults to 'None'.
        color (str, optional): Line color(s). Defaults to 'None' (i.e. use default color cycle).
        ylabel (str, optional): Vertical axis label (will overwrite). Defaults to 'None'.
        title (str, optional): Subplot heading (will overwrite). Defaults to 'None'.
        fig (:obj:, optional): Existing figure handle. Defaults to 'None' (i.e. create new one).
        bold (bool, optional): Switch for drawing a "bold" line (width 4). Defaults to 'False'.
        legend (bool, optional): Switch for setting a legend. If no 'info' is given, standard
            names, i.e. 's1' ... 'sN', will be applied. Defaults to 'True'.
        time_iso (bool, optional): Switch to enforce a readable time (i.e. ISO 8061 string),
            only applicable for 'TimeSeries' inputs. Defaults to 'False'.
        newplot (bool, optional): Switch for plotting into a new subplot. Defaults to 'False'.
        drawmode (str, optional): General mode of plotting ('plot'|'stem'|'plotmx').
            Defaults to 'plot'.

    Returns:
        fh(:obj:): Handle of created figure.
    """

    # access or init objects
    fh, ax = axxess(fig, newplot)
    num_lines = len(ax.get_lines())

    # auto-detect all individual signals
    all_signals = unpack_signals(sig)

    # ensure consistency of settings
    num_signals = len(all_signals)
    if ((info is not None) and (num_signals == 1)):
        info = [info,]
    if ((color is not None) and (num_signals == 1)):
        color = [color,]

    # draw all signals (one after each other, using same axes/subplot)
    for s, x in enumerate(all_signals):
        num_lines += 1

        # configure basic settings
        if (drawmode == 'plot'):
            plot_type = 'plot'
            kwargs = ''
        elif (drawmode == 'stem'):
            plot_type = 'stem'
            kwargs = '' # ", use_line_collection=True" -> removed of matplotlib 3.8!
        else: # drawmode == 'plotmx'
            plot_type = 'plot'
            if (len(x) > (2*_MX_NUM)):
                ds = int(len(x)/_MX_NUM)
            else:
                ds = 1
            kwargs = f", marker='{_MX_CYCLE[(num_lines-1)%len(_MX_CYCLE)]}', markevery={ds}"

        # configure labels
        if (info is not None):
            kwargs += f", label='{info[s]}'"
        else:
            if (SUPPORTS_TS and istimeseries(x)):
                kwargs += f", label='{x.name}'"
            else:
                kwargs += f", label='s{num_lines}'" # default: 's1', 's2', ... 'sN'
        # Note: Placing the 'info' check first enables an override for 'TimeSeries' objects!

        # configure line settings
        if (drawmode != 'stem'): # Note: Options not available for 'stem' plots!
            if (color is not None):
                kwargs += f", color='{mpl.colors.rgb2hex(color[s])}'"
            else:
                color_now = mpl.colors.rgb2hex( _COL_CYCLE[(num_lines-1)%len(_COL_CYCLE)] )
                kwargs += f", color='{color_now}'"
            if (bold):
                kwargs += ", linewidth=3"
            else:
                kwargs += ", linewidth=1"

        # actual plotting
        if (SUPPORTS_TS and istimeseries(x)):
            x.time_convert('stamp')
            eval(f"ax.{plot_type}(x.df.t, x.df.x {kwargs})")
            if (time_iso):
                ticks = []
                for n in range(_TS_NUM_TICKS-1):
                    ticks.append(x.df.t.iloc[int(n*len(x)/_TS_NUM_TICKS)])
                ticks.append(x.df.t.iloc[len(x)-1])
                labels = convert_time(ticks, _TS_FMT)
                ax.tick_params(axis='x', labelrotation=15)
                ax.set_xticks(ticks)
                ax.set_xticklabels(labels)
                # Note: To avoid cluttering & slow-down of display for strings, the amount of
                # 'xticks' should be limited to a small subset of the time stamps!
        elif (iscomplex(x)):
            if (ref is None):
                eval(f"ax.{plot_type}(np.real(x) {kwargs})")
                eval(f"ax.{plot_type}(np.imag(x) {kwargs})")
            else:
                eval(f"ax.{plot_type}(ref, np.real(x) {kwargs})")
                eval(f"ax.{plot_type}(ref, np.imag(x) {kwargs})")
        else:
            if (ref is None):
                eval(f"ax.{plot_type}(x {kwargs})")
            else:
                eval(f"ax.{plot_type}(ref, x {kwargs})")

    # finalise plot
    if (legend):
        ax.legend(loc='best')
    if (ylabel is not None):
        ax.set_ylabel(ylabel, fontsize=_YLABEL_SIZE)
    elif (ax.get_ylabel() == ''): # default, but only if no ylabel yet!
        ax.set_ylabel(f"[{num_lines} signals]")
    else:
        pass # don't change existing label!
    if (title is not None):
        ax.set_title(title, fontsize=_TITLE_SIZE)
    elif (ax.get_title() == ''): # default, but only if no title yet!
        ax.set_title("", fontsize=_TITLE_SIZE)
    ax.tick_params(axis='both', labelsize=_TICK_SIZE)
    ax.xaxis.get_offset_text().set_fontsize(_TICK_SIZE)

    ax.grid(True)
    # try:
    #     fh.show()
    # except:
    #     pass # Note: This may mean that 'quickplot()' has been called form a higher-level
    #          #       routine, e.g. from a GUI?
    return fh

qplot = partial(quickplot, drawmode='plot')
qstem = partial(quickplot, drawmode='stem')
qplotmx = partial(quickplot, drawmode='plotmarks')


def quickplotly(sig, ref=None, info=None, color=None, ylabel=None, title=None, fig=None,
                bold=False, legend=True, time_iso=False, slider=True, drawtools=False,
                drawmode='plot', renderer='browser', num_ticks=_TS_NUM_TICKS, size=[1600,900]):
    """ Quickly displays signal 'sig' w/ optional time 'ref' (plotly framework).

    This function is provided for a more intuitive & unified use of the "plotly" package. It
    supports a much faster plotting, as preparations for all settings are hidden inside.

    Note: For quickest use, simply type 'qplotly(x)'!

    Args:
        sig (np.ndarray): Signal(s) to be visualised. If more signals are containd here, all of
            them will be unbundeled to a flat list.
        ref (np.ndarray, optional): Time reference for plotting (if any). Defaults to 'None'.
        info (str, optional): Signal name used as legend entry (if any). Defaults to 'None'.
        color (str, optional): Line color(s). Defaults to 'None' (i.e. use default color cycle).

        ylabel (str, optional): Vertical axis label (will overwrite). Defaults to 'None'.
        title (str, optional): Subplot heading (will overwrite). Defaults to 'None'.

        fig (:obj:, optional): Existing figure handle. Defaults to 'None' (i.e. create new one).
        bold (bool, optional): Switch for drawing a "bold" line (width 4). Defaults to 'False'.
        legend (bool, optional): Switch for setting a legend *on top* of the plot. If no 'info'
            is given, standard names, i.e. 's1' ... 'sN', will be applied. Defaults to 'True'.
        
        time_iso (bool, optional): Switch to enforce a readable time (i.e. ISO 8061 string), 
            only applicable for 'TimeSeries' inputs. Defaults to 'False'.                
        slider (bool, optional): Switch for placing a time-slider at the bottom. With this,
            the range of display on the horizontal axes can be adjusted. Defaults to 'False'.
        drawtools (bool, optional): Switch for enabling interactive tools. Defaults to 'False'.
        drawmode (str, optional): General mode of plotting ('plot'|'bar'). Defaults to 'plot'.
        num_ticks (int, optional): Number of ticks on the horizontal axis to avoid hard-to-read
            labeling, only applicable for 'TimeSeries'. Defaults to '_TS_NUM_TICKS'.
        renderer (str, optional): Desired renderer for output image. Defaults to 'browser'.
            Options: (static)       --> 'png'|'jpg'|'svg'
                     (interactive)  --> 'browser'|'chrome'|'firefox'|'notebook'|'iframe'|
                                        'notebook_connected'|'iframe_connected'
        size (2-tuple. optional): Two-tuple indicating the size as [width,height] for the
            renderer. Defaults to [1600,900].

    Returns:
        fh(:obj:): Handle of created figure.
    """

    # create new figure?
    if (fig is None):
        fh = sp.make_subplots(rows=1, cols=1)
    else:
        fh = fig
    num_lines = len(fh.data)

    # auto-detect all individual signals
    all_signals = unpack_signals(sig)

    # ensure consistency of settings
    num_signals = len(all_signals)
    if ((info is not None) and (num_signals == 1)):
        info = [info,]
    if ((color is not None) and (num_signals == 1)):
        color = [color,]

    # draw all signals (one after each other, using same axes/subplot)
    for s, x in enumerate(all_signals):
        num_lines += 1
        kwargs = ''

        # configure labels
        if (info is not None):
            kwargs += f", name='{info[s]}'"
        else:
            if (SUPPORTS_TS and istimeseries(x)):
                kwargs += f", name='{x.name}'"
            else:
                kwargs += f", name='s{num_lines}'" # default: 's1', 's2', ... 'sN'
        # Note: Placing the 'info' check first enables an override for 'TimeSeries' objects!

        # configure line settings
        line_dict = {}
        if (color is not None):
            line_dict['color'] = color[s] # TODO: how to check if already used?
        else:
            color_now = mpl.colors.rgb2hex( _COL_CYCLE[(num_lines-1)%len(_COL_CYCLE)] )
            line_dict['color'] = color_now
        if (bold):
            line_dict['width'] = 3
        else:
            pass # line_dict['width'] = 2
        if (line_dict is not {}):
            kwargs += f", line={line_dict}"

        # configure legend settings
        kwargs += f", showlegend={legend}"

        # actual plotting acc. to proper "graph object"
        if (drawmode == 'plot'):
            if (SUPPORTS_TS and istimeseries(x)):
                x.time_convert('stamp')
                eval(f"fh.add_trace( go.Scatter(x=x.df.t, y=x.df.x {kwargs}) )")
                if (time_iso):
                    ticks = []
                    for n in range(num_ticks-1):
                        ticks.append(x.df.t.iloc[int(n*len(x)/num_ticks)])
                    ticks.append(x.df.t.iloc[len(x)-1])
                    labels = convert_time(ticks, _TS_FMT)
                    fh.update_layout(xaxis={'tickmode': 'array', 'tickvals': ticks, 'ticktext': labels})
                    # Note: To avoid cluttering & slow-down of display for strings, the amount of
                    # 'xticks' should be limited to a small subset of the time stamps!

                # if (num_ticks):
                #     ticks = []
                #     for n in range(num_ticks-1):
                #         ticks.append(x.df.t.iloc[int(n*len(x)/num_ticks)])                        
                #     ticks.append(x.df.t.iloc[len(x)-1])
                #     if (time_iso):
                #         labels = convert_time(ticks, _TS_FMT)
                #     fh.update_layout(xaxis={'tickmode': 'array', 'tickvals': ticks, 'ticktext': labels})
                
            else:
                eval(f"fh.add_trace( go.Scatter(x=ref, y=x {kwargs}) )")
        # elif (drawmode == 'bar'):
        #     obj = go.Bar(x=t, y=signal)
        else:
            pass

    # configure menubar
    menubar_cfg = {
        'displayModeBar': True, # show mode bar at all?
        'displaylogo': True,    # show plotly logo?
        'responsive': True,     # adjust figure size/resolution when window changes?
        'scrollZoom': True,     # use mouse-wheel to scroll in/out of figures?

        # remove standard buttons? (zoom|pan|select|zoomIn|zoomOut|autoScale|resetScale)
        'modeBarButtonsToRemove': [],

        # customize download button
        'toImageButtonOptions': {
            'format': 'jpeg', # options: jpeg | png | svg | webp
              'filename': 'qplotly_image',
              'width': 1600,
              'height': 900,
              'scale': 1 # Note: will multiply title/legend/axis/canvas sizes by this
              },
        }

    # add interactive drawing tools?
    if (drawtools):
        menubar_cfg['modeBarButtonsToAdd'] = ['drawline', 'drawcircle', 'drawrect',
                                              'drawopenpath', 'drawclosedpath', 'eraseshape']

    # add time slider?
    if (slider and (renderer in ('browser','chrome','firefox','notebook','iframe'))):
        fh.update_layout(xaxis={'type': 'linear',
                                'rangeslider': {'visible': True, 'bgcolor': 'white'}})
        fh.update_xaxes(rangeslider_thickness=0.08)

    # finalise
    if (legend):
        fh.update_layout(legend={'orientation': 'h',
                                 'yanchor': 'bottom', 'y': 1.02,
                                 'xanchor': 'right', 'x': 1})
    if (renderer is None):
        return fh
    else:
        fh.show(renderer, width=size[0], height=size[1], config=menubar_cfg)
        return fh

qplotly = partial(quickplotly, drawmode='plot')
qplotly_bar = partial(quickplotly, drawmode='bar')



# def quickviewer(sig, ref=None, size=[1600,900]):
#     """ Quickly shows 'sig' w/ optional 'ref' in system's default viewer (blocks until closed!).

#     Args:
#         sig (np.ndarray): Signal(s) to be visualised. If more signals are containd here, all of
#             them will be unbundeled to a flat list.
#         ref (np.ndarray, optional): Time reference for plotting (if any). Defaults to 'None'.
#         size (2-tuple. optional): Two-tuple indicating the size as [width,height] for the
#             renderer. Defaults to [1600,900].

#     Returns:
#         --
#     """ 
#     import io
#     import plotly.io as pio
#     from PIL import Image   

#     # create "normal" plotly object
#     fh = qplotly(sig, ref, size, slider=False, renderer=None)

#     # transform into bytes object
#     buf = io.BytesIO()
#     pio.write_image(fh, buf, width=size[0], height=size[1])

#     # show in default system viewer
#     img = Image.open(buf)
#     img.show() # Note: Blocks Python processing until viewer is closed!

#     return



#===============================================================================================
# Plotly
#
# When manipulating a plotly.graph_objects.Figure object, attributes can be set either directly
# using Python object attributes e.g.
#
#   > fig.layout.title.font.family="Open Sans"
#
# or using update methods and "magic underscores" (to directly adress a nested attribute) e.g.
#
#   > fig.update_layout(title_font_family="Open Sans")
#
# Available options:
#
#   layout_title_text:  [str]
#   layout_xaxis:       {'range': [xa,xb]}
#   layout_yaxisN:      {'range': [ya,yb], 'title': 'MyTitle_on_y_axis'}
#   layout_legend:      {'yanchor': 'top', 'y': 0.99, 'xanchor': 'left', 'x': 0.95}
#
#   fh.update_layout:   legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.95)
#
#===============================================================================================



# def axxess_GOOD_OLD(fig=None, newplot=False, direction='bottom', fillup=True):
#     """ Returns handle to last axes in given figure or create new one (figure or subplot).

#     This is a convenience function to provide an "ease-of-use" feeling for creating (new) axes
#     objects in an existing figure. Note that in case of 'newplot=True' this might also
#     automagically extend the existing layout acc. to the specified settings if required.

#     Args:
#         fig (:obj:, optional): Existing figure handle. Defaults to 'None' (i.e. create new one).
#         newplot (bool, optional): Switch for adding a new subplot/axes at the bottom (if an
#             existing figure is used). Defaults to 'False'.
#         direction (str, optional): Direction in which to create the new plot (if desired).
#             Options are 'bottom' or 'right' (i.e. new row/column). Defaults to 'bottom'.
#         fillup (bool, optional): Switch to fill-up "empty subplots" if existing before actually
#             adding new rows/columns to the layout. Defaults to 'True'.

#     Returns:
#         fh (:obj:): Handle to the figure where axes are located.
#         ax (:obj:): Handle to the current axes object on that figure.
#     """

#     def idx2coord(geometry):
#         """ Computes (0-based) coordinates 'm,n' from axes 'geometry' (sizes & index). """
#         M, N, idx = geometry[:]
#         m = int((idx-1)/N) # row index
#         n = (idx-1) - m*N  # col index
#         return (m,n)

#     def coord2idx(coord,M,N):
#         """ Computes (1-based) index from (0-based) 'coordinates' (m,n) and geometry sizes. """
#         (m,n) = coord
#         idx = 1 + m*N + n
#         return idx

#     # create new figure...
#     if (type(fig) is not mpl.figure.Figure):
#         if (fig is None):
#             fh = plt.figure()
#         else:
#             fh = plt.figure(num=fig)
#         ax = fh.subplots(1,1) # start w/ single subplot

#     else: # ...or use existing figure?
#         fh = fig

#         # use existing axes...
#         if (not newplot):
#             ax = fh.get_axes()[-1]
#         else: # ...or insert new axes?
#             all_axes = fh.get_axes()
#             M,N = all_axes[-1].get_subplotspec().get_geometry()[0:2]

#             # check consistency
#             if (direction not in ('bottom','right')):
#                 print(f"Unknown direction '{direction}' specified! (aborting)")
#                 return fh, None

#             # analyse coverage of layout (i.e. any "free subplots"?)
#             ax_map = np.zeros((M,N), dtype=np.int32)
#             for sp, ax in enumerate(all_axes, start=1):
#                 (m,n) = idx2coord(ax.get_geometry())
#                 ax_map[m,n] = sp
#             if (not ax_map.all()):
#                 space_left = True
#             else:
#                 space_left = False

#             # get first "free subplot" acc. to desired direction
#             if (space_left and fillup):
#                 free_pos_found = False
#                 if (direction == 'bottom'):
#                     for n in range(N): # find first col w/ free row position
#                         for m in range(M):
#                             if (not ax_map[m,n]):
#                                 free_pos_found = True
#                                 break
#                         if (free_pos_found):
#                             break
#                 else: # (direction == 'right'):
#                     for m in range(M): # find first row w/ free col position
#                         for n in range(N):
#                             if (not ax_map[m,n]):
#                                 free_pos_found = True
#                                 break
#                         if (free_pos_found):
#                             break

#                 # add new axes @ "free subplot" position
#                 idx = coord2idx((m,n),M,N)
#                 fh.add_subplot(M,N,idx)
#                 ax = fh.get_axes()[-1]

#             else: # extend layout first (i.e. no empty subplots left or filling is not desired)
#                 if (direction == 'bottom'):
#                     Mx, Nx = M+1, N
#                 else: # (direction == 'right'):
#                     Mx, Nx = M, N+1

#                 # re-assign geometry for all existing subplots
#                 for sp, ax in enumerate(all_axes, start=1):
#                     (m,n) = idx2coord(ax.get_geometry())
#                     idx = coord2idx((m,n),Mx,Nx)
#                     ax.change_geometry(Mx,Nx,idx)

#                 # add new subplot (in recursive call, enforcing "fillup")
#                 fh, ax = axxess(fig=fh, newplot=True, direction=direction, fillup=True)

#     return fh, ax