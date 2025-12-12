# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

from pathlib import Path
import numpy as np
import argparse
import itertools
import collections
from ..process import spectlinetools as slt
from ..process import linefinder
from ..utils import io
from ..utils.utils import str_to_bool
import bokeh.plotting as bp
import bokeh.models as bm
import bokeh.layouts as bl
import bokeh.events as be


def get_args():
    """ Create an argument parser and parse the arguments

    Returns
    -------
    namespace: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="FineTooth plotting tool"
    )

    parser.register('type', 'bool', str_to_bool)

    parser.add_argument(
        "--outfile",
        type=Path,
        required=True,
        help="Path to output file (must end in .html)"
    )

    group_input = parser.add_argument_group('Input data arguments')
    group_input.add_argument(
        "--spectfile", type=Path, required=True,
        help="Path to spectrum file. Supports ASCII txt or fscan-style npz."
    )
    group_input.add_argument(
        "--freqcolname", type=str, default='f',
        help=(
            "The name/key of the array from which to load frequencies.")
    )
    group_input.add_argument(
        "--datacolname", type=str,
        help=(
            "The name/key of the array from which to load values")
    )
    group_input.add_argument(
        "--spectfile-ref", type=Path, default=None,
        help=(
            "Path to a spectral file for comparison. Will create a ratio plot."
            )
    )
    group_input.add_argument(
        "--freqcolname-ref", type=str, default=None,
        help=(
            "If loading a reference spectrum, this is the name/key"
            " of the array from which to load frequencies.")
    )
    group_input.add_argument(
        "--datacolname-ref", type=str, default=None,
        help=(
            "If loading a reference spectrum, this is the name/key of the"
            " array from which to load values")
    )

    group_plot_options = parser.add_argument_group('Plotting options')
    group_plot_options.add_argument(
        "--fmin",
        type=float, required=True,
        help="Minimum frequency to display"
    )
    group_plot_options.add_argument(
        "--fmax",
        type=float, required=True,
        help="Maximum frequency to display"
    )
    group_plot_options.add_argument(
        "--desc", type=str, default="Spectrum",
        help="Legend description for main spectrum (if plotting multiple)"
    )
    group_plot_options.add_argument(
        "--desc-ref", type=str, default=None,
        help="Legend description for reference spectrum"
    )
    group_plot_options.add_argument(
        "--comparison", type=str, default=None,
        choices=["ratio", "fraction"],
        help="Y-axis for comparison plot (requires reference spectrum)"
    )
    group_plot_options.add_argument(
        "--annotate", type='bool', default=True,
        help=(
            "Allow annotation of plot (default: True). Turn off annotation to"
            " make the plot more lightweight in the browser.")
    )
    group_plot_options.add_argument(
        "--ylog", type='bool', default=True,
        help=("Whether to have the y-axis on a log scale")
    )
    group_plot_options.add_argument(
        "--title",
        type=str, default=None,
        help="Title for plot"
    )
    group_plot_options.add_argument(
        "--yaxlabel",
        type=str, default="",
        help="Y-axis label"
    )
    group_plot_options.add_argument(
        "--legend",
        type='bool', default=False,
        help="Whether a legend should be added to the figure"
    )

    group_tagging = parser.add_argument_group('Tagging options')
    group_tagging.add_argument(
        "--linesfile", type=Path,
        help="Path to lines file", nargs="*"
    )
    group_tagging.add_argument(
        "--linesfile-label", type=str, nargs="*",
        help="Labels for linesfile to use on legend (if colorcode=fromfile)"
    )
    group_tagging.add_argument(
        "--colorcode", type=str,
        choices=[
            'autocolor',
            'highlight',
            'highlight-only',
            'fromfile',
            'none'],
        default='autocolor',
        help=(
            "Autocolor will assign the N most common line descriptions to a"
            " unique dot color (ignores notes in parentheses). Highlight will"
            " assign the N most common tags, indicated by \"!tag\" at the end"
            " of the description, to a unique dot color.")
    )
    group_tagging.add_argument(
        "--colorcode-group-min",
        type=int, default=0,
        help="Minimum number of items in a color-coded group"
    )
    group_tagging.add_argument(
        "--plotcombs",
        nargs="+",
        type=str,
        default=None,
        help=(
            "Combs to plot on top of other annotations. Must be specified as"
            " \"spacing,offset\". Any line file color coding options will be"
            " overriden so that (up to 8) combs can be color coded.")
    )
    group_tagging.add_argument(
        "--intersect-linefinder",
        type='bool',
        default=False,
        help=(
            "Whether or not to require that input lines also pass linefinder"
            " thresholds to be plotted")
    )
    group_tagging.add_argument(
        "--peaksensitivity",
        type=float, default=.001,
        help="(Very approximate) false alarm rate for peak finding"
    )
    group_tagging.add_argument(
        "--peakmedwindow",
        type=float, default=0.05,
        help="spectrum chunk length for calculating running statistics (Hz)"
    )

    args = parser.parse_args()

    # argument checks
    if args.comparison and not args.spectfile_ref:
        raise parser.error("Must provide --spectfile-ref with --comparison")

    if args.linesfile is None:
        args.linesfile = []
    if args.linesfile_label is None:
        args.linesfile_label = []

    if args.title is None and args.spectfile_ref is None:
        args.title = args.desc

    if args.spectfile_ref and args.desc_ref is None:
        args.desc_ref = "Reference spectrum"

    return args


def plot_spect(outfile, freq, val, title, yaxlabel, ylog):
    """ Create a basic spectrum plot.

    Parameters
    ----------
    outfile : str
        The output file.
    freq : 1d numpy array
        Frequencies for the spectrum
    val : 1d numpy array
        Values (e.g. ASD, PSD...) for the spectrum
    title : str
        Title for plot
    yaxlabel : str
        y-axis label for plot

    Returns
    -------
    fig : bokeh figure
        The figure on which the spectrum is plotted.
    spectsource : bokeh column data source
        Contains freq, val in a data source.
    spinners : list of bokeh.models Spinner objects
        Used to adjust fmin, fmax, visual reference line, ymin, and ymax.
    """

    # Set the output file
    bp.output_file(outfile)

    # Spectrum data source
    spectsource = bp.ColumnDataSource({
        'freq': freq,
        'val': val
    })

    if ylog:
        yscale = 'log'
    else:
        yscale = 'linear'
    # Figure for plotting the spectrum
    fig = bp.figure(
        title="",  # Default plot title
        x_axis_label="Frequency (Hz)",
        y_axis_label=yaxlabel,
        y_axis_type=yscale,
        tools='pan,box_zoom,undo,redo,reset,zoom_in,zoom_out,save',
        active_drag=None,
        active_multi='box_zoom',
        min_width=1500,
    )
    # Add spinners for detailed adjustment of frequency range
    spinner_fmin = bm.Spinner(
        title="Plot min frequency",
        format='0.00000'
    )

    spinner_fmax = bm.Spinner(
        title="Plot max frequency",
        format='0.00000'
    )

    spinner_fmin.js_link('value', fig.x_range, 'start')
    spinner_fmax.js_link('value', fig.x_range, 'end')
    fig.x_range.js_link('start', spinner_fmin, 'value')
    fig.x_range.js_link('end', spinner_fmax, 'value')

    # Add spinner for detailed adjustment of vertical range
    valsformat = bm.formatters.PrintfTickFormatter(format='%.3e')
    spinner_ymin = bm.Spinner(
        title="Plot min vertical",
        format=valsformat
    )

    spinner_ymax = bm.Spinner(
        title="Plot max vertical",
        format=valsformat
    )

    spinner_ymin.js_link('value', fig.y_range, 'start')
    spinner_ymax.js_link('value', fig.y_range, 'end')
    fig.y_range.js_link('start', spinner_ymin, 'value')
    fig.y_range.js_link('end', spinner_ymax, 'value')

    # Add spinner and span for vertical line reference
    ref = bm.Span(
        location=0,
        dimension='height',
        line_color='deeppink',
        line_width=2.0
    )

    spinner_ref = bm.Spinner(
        title="Visual reference frequency",
        format="0.00000",
        value=0,
    )

    fig.add_layout(ref)

    spinner_ref.js_link('value', ref, 'location')
    ref.js_link('location', spinner_ref, 'value')

    # package up all the spinners
    spinners = [
        spinner_fmin,
        spinner_fmax,
        spinner_ref,
        spinner_ymin,
        spinner_ymax,
    ]

    # Update plot title if one was supplied
    if isinstance(title, str):
        fig.title.text = title

    # Spectrum plotted as a line
    spectline = fig.line(
        'freq', 'val',
        source=spectsource,
        color='black',
        )

    # Tooltips for the spectrum itself
    specttips = [
        ("Frequency", "@freq{0.00000}"),
    ]

    # Add a hover tool for the spectrum
    spect_hover = bm.HoverTool(tooltips=specttips, renderers=[spectline])
    fig.add_tools(spect_hover)

    return fig, spectsource, spinners, spectline


def plot_reference_spect(
        fig, freq, reffreq, refval, make_legend=True,
        spectline_renderer=None, spect_desc=None,
        refspect_desc=None):
    """
    Make a reference spectra

    Parameters
    ----------
    fig : bokeh figure
    freq : 1d numpy array (dtype=float)
    reffreq : 1d numpy array (dtype=float)
    refval : 1d numpy array (dtype=float)
    make_legend : bool (default=True)
    spectline_renderer : bokeh renderer (default=None)
    spect_desc : str (default=None)
    refspect_desc : str (default=None)

    Returns
    -------
    fig : bokeh figure
    refval : 1d numpy array (dtype=float)
    """

    # Decrease resolution of the reference spectrum to match
    # the main spectrum if necessary
    n_ref_pts = len(reffreq)
    n_pts = len(freq)
    if n_pts < n_ref_pts:
        ix = slt.match_bins(freq, reffreq)
        _, cts = np.unique(ix, return_counts=True)
        refval = np.bincount(ix, refval)/cts
        reffreq = freq
    # Don't allow the reverse
    if n_pts > n_ref_pts:
        raise Exception(
            "Reference spectrum can't be lower resolution than spectrum.")

    # Plot the reference spectrum
    refspectsource = bp.ColumnDataSource({
        'reffreq': reffreq,
        'refval': refval,
        })

    refspectline = fig.line(
        'reffreq',
        'refval',
        source=refspectsource,
        color='orange',
        level='underlay',
        line_width=5)

    # Tooltips for the reference spectrum
    refspecttips = [("Frequency", "@reffreq{0.00000}")]

    refspectline_hover = bm.HoverTool(
        tooltips=refspecttips,
        renderers=[refspectline])
    fig.add_tools(refspectline_hover)

    # Add legend
    if make_legend:
        fig.add_layout(bm.Legend(), 'right')

    if spect_desc:
        fig.legend.items.extend(
            [bm.LegendItem(
                label=spect_desc,
                renderers=[spectline_renderer])])
    if refspect_desc:
        fig.legend.items.extend(
            [bm.LegendItem(
                label=refspect_desc,
                renderers=[refspectline])])

    return fig, refval


def plot_comparison_figure(fig, freq, val, refval, comptype):
    """
    Create a plot of the spectral ratio or fractional difference between the
    main and reference spectra.

    Parameters
    ----------
    fig : bokeh figure
        The already-existing main figure, to which the comparison x-axis will
        range will be linked.
    freq : 1d numpy array (dtype: float)
        Frequency axis
    val : 1d numpy array (dtype: float)
        Y-axis values for the main spectrum
    refval : 1d numpy array (dtype: float)
        Y-axis values for the reference spectrum. Must be the same length
        as `val`.
    comptype : str
        Comparison quantity to plot. Must be one of: "fraction", "ratio".

    Returns
    -------
    compfig : bokeh figure
        Figure showing the comparison quantity vs frequency.
    """

    if comptype == "fraction":
        comp = (val-refval)/np.max([val, refval], axis=0)
        title = "Fractional difference between spectra, calculated as:\n" \
                "(spectrum [black] - reference spectrum [orange]) " \
                "/ maximum(either spectrum)"
        yscale = 'linear'

    if comptype == "ratio":
        comp = val/refval
        title = "Ratio between spectra, calculated as:\n" \
                "spectrum [black] / reference spectrum [orange]"
        yscale = "log"

    compspectsource = bp.ColumnDataSource({
        'freq': freq,
        'comp': comp,
        })

    # Now set up the ratio figure
    compfig = bp.figure(
        title=title,
        min_width=1500,
        height=300,
        y_axis_type=yscale,
        x_range=fig.x_range,
        active_drag=None,
        active_multi=None,
        active_inspect=None,
        toolbar_location=None)
    compfig.title.text_font_style = "italic"

    # And plot the ratio
    compfig.line(
        'freq',
        'comp',
        source=compspectsource,
        color='turquoise')

    return compfig


def overlay(fig, spectsource, xinds, names, lfreq, colors, markers, sizes,
            tags, left=[], right=[], boxmids=[], boxnames=[], legend=None):
    """ Create a basic spectrum plot.

    Parameters
    ----------
    fig : bokeh figure
        The fig on which to add the overlay
    spectsource : bokeh column data source
        contains: freq, val in a data source
    xinds : 1d numpy array (dtype: int)
        Frequency bin indices where overlay points are located
    names : 1d numpy array (dtype: str)
        Labels from the line list for each overlay point
    lfreq : 1d numpy array (dtype: float)
        Listed frequencies in the line list for each overlay point
    colors : list of strings
        Color for each overlay point
    markers : list of strings
        Marker type for each overlay point (square, circle, triangle..)
    sizes : list of ints
        Marker size for each overlay point
    legend : bool
        Whether or not to add a legend
    tags : list of strings
        Category names for each point (corresponds to color/marker-coding
        and legend)

    Returns
    -------
    fig : bokeh figure
        The now-annotated figure
    """

    # Wrap text on names
    names = [x.replace("; ", "<br>") for x in names]

    if legend is None:
        if len(set(colors)) == 1:
            legend = False
        else:
            legend = True

    # Alpha currently set to 0.7 for all points; leaving
    # this array here in case we want to amend it
    alphas = np.ones(len(names))*.7

    # Create data source and tooltips
    overlaySource = bp.ColumnDataSource(data={
        'x': spectsource.data['freq'][xinds],
        'y': spectsource.data['val'][xinds],
        'name': names,
        'lfreq': lfreq,
        'color': colors,
        'alpha': alphas,
        'marker': markers,
        'size': sizes,
        'tag': tags,
    })

    overlaytips = [
        ("Description", "@name{safe}"),
        ("Frequency bin", "@x{0.00000}"),
        ("Frequency in list", "@lfreq{0.00000}"),
    ]

    # Set up kwargs for the overlay glyphs
    # (Not passing them directly because we want to
    # conditionally pass the legend argument)
    scatter_kwargs = {
        'x': 'x',
        'y': 'y',
        'source': overlaySource,
        'fill_color': 'color',
        'line_color': 'black',
        'fill_alpha': 'alpha',
        'marker': 'marker',
        'size': 'size',
    }

    if legend:
        # Add the legend group
        scatter_kwargs['legend_group'] = 'tag'
        # The legend ought to be outside the plot area. This achievable with
        # fig.add_layout(bm.Legend(), 'right')
        # Unfortunately, bokeh 3.7.2 has a legend placement bug that causes an
        # overlap with the toolbar for legends outside the plot.
        # This will be fixed in 3.7.3, according to
        # https://github.com/bokeh/bokeh/pull/14457
        # In the meantime, put the legend inside the plot.
        fig.add_layout(bm.Legend(location='top_right'))

    # Create the actual glyphs
    overlaydots = fig.scatter(**scatter_kwargs)

    # Add a hover tool for the overlay
    overlay_hover = bm.HoverTool(tooltips=overlaytips, renderers=[overlaydots])
    fig.add_tools(overlay_hover)

    # Set up the band boxes
    base = []
    width = []
    height = []

    # for each set of left & right bounds
    for lbound, rbound, mid in zip(left, right, boxmids):

        # Readjust the box and notify the user if the left bound is
        # above the frequency of the entry
        if lbound > mid:
            lbound = mid
            print(f"Left bound for {mid}Hz is too high, adjusting.")
        # If the left bound simply goes off the plot, truncate it.
        if lbound < spectsource.data['freq'][0]:
            lbound = spectsource.data['freq'][0]

        # Readjust the box and notify the user if the right bound is
        # below the frequency of the entry
        if rbound < mid:
            rbound = mid
            print(f"Right bound for {mid}Hz is too low, adjusting.")
        # If the right bound simply goes off the plot, truncate it.
        if rbound > spectsource.data['freq'][-1]:
            rbound = spectsource.data['freq'][-1]

        # select the data that lies between the left bound and right bound
        select = spectsource.data['val'][
                (spectsource.data['freq'] <= rbound) &
                (spectsource.data['freq'] >= lbound)]

        # If there are no data points in the selection region, we'll just
        # set the top and bottom to the same value: that of the nearest data pt
        # to the right of the region. (This will show no box on the plot.)
        if len(select) == 0:
            top = spectsource.data['val'][
                spectsource.data['freq'] >= lbound][0]
            bottom = top
        # If there is data in the selection box, the box's vertical extent will
        # be defined by its min and max values.
        else:
            top = max(select)
            bottom = min(select)

        # Add onto the lists defining all boxes to be plotted
        base.extend([bottom])
        width.extend([(rbound-lbound)])
        height.extend([(top-bottom)])

    boxsource = bp.ColumnDataSource(data={
                'x': left,
                'y': base,
                'width': width,
                'height': height,
                'names': boxnames,
                'fill_color': ['#D55E00']*len(left),
                'fill_alpha': [0.1]*len(left),
                'line_width': [0]*len(left)
                })
    box_glyph = bm.Block(
                            x='x',
                            y='y',
                            width='width',
                            height='height',
                            fill_color='fill_color',
                            fill_alpha='fill_alpha',
                            line_width='line_width'
                            )
    boxes = fig.add_glyph(boxsource, box_glyph)

    # Add a hover tool for the boxes
    boxtips = [
        ("Shaded region", "@names{safe}")]
    box_hover = bm.HoverTool(tooltips=boxtips, renderers=[boxes])
    fig.add_tools(box_hover)

    return fig


def make_clickable(fig, spectsource):
    """
    This function adds the ability to click on a spectrum point to annotate it.
    The annotated point is marked with a red dot, and the relevant data is
    logged in a data table.
    """

    # Create a new copy of the data source to work around a bug.
    ''' Odd as it may seem, there is a bokeh bug which causes segments of the
    line glyph to go invisible when a circle glyph sharing the same source is
    selected. (Confirmed elsewhere.) Creating an independent copy fixes the
    bug.
    '''
    spectsource = bp.ColumnDataSource(spectsource.data.copy())

    # Create invisible dots at each data point on the spectrum.
    '''These dots are a kludgey way to make sure that there is a
    clickable glyph at each point, on which the TapTool can trigger.
    They are mostly just confusing if made visible, although I might
    try showing them on hover later.'''

    spectdots = fig.scatter(
        'freq', 'val',
        size=15,
        fill_alpha=0,
        nonselection_fill_alpha=0,
        line_alpha=0,
        nonselection_line_alpha=0,
        source=spectsource)

    # Empty data source for the drawn points.
    drawnsource = bp.ColumnDataSource({
        'x': [],
        'y': [],
        'label': [],
    })

    # Renderer for the drawn points.
    drawndots = fig.scatter(
        x='x',
        y='y',
        size=10,
        fill_color='red',
        nonselection_fill_color='red',
        alpha=1,
        nonselection_fill_alpha=1,
        line_color='black',
        line_width=2,
        nonselection_line_color=None,
        nonselection_line_width=0,
        source=drawnsource,
    )

    # Create a template for the data table values (num. decimal places)
    template = """
    <%= (value).toFixed(5) %>
    """
    fmat = bm.HTMLTemplateFormatter(template=template)

    # Columns for the data table of drawn points.
    drawncolumns = [
        bm.TableColumn(field='x',
                       title="Frequency",
                       formatter=fmat,
                       editor=bm.widgets.tables.NumberEditor()),
        bm.TableColumn(field='label',
                       title="Label",
                       editor=bm.widgets.tables.StringEditor())
    ]

    # Data table for the drawn points.
    drawntable = bm.DataTable(
        source=drawnsource,
        columns=drawncolumns,
        editable=True,
        height=30)

    # Div to contain the drawn points in CSV format
    div = bm.Div(text="", visible=False)

    # Custom JS code to update the list of drawn points.
    markClick = """

    /* pts are the coordinates and labels of tagged points */
    const pts = drawnsource.data

    /* index is the spectral location of the most recetly selected point */
    var index = spectsource.selected.indices[0]

    /* indexindrawn will be -1 if the most recently selected point is new
    (not already annotated). If it's already annotated, indexindrawn will
    be its index in the list of already-annotated points. */
    var indexindrawn = pts['x'].indexOf(spectsource.data.freq[index])

    /* If the clicked point is new, append it to the list of annotated pts. */
    if (indexindrawn == -1){
        pts['x'].push(spectsource.data.freq[index])
        pts['y'].push(spectsource.data.val[index])
        pts['label'].push("")
        }

    /* If the clicked point was already annotated, remove it from the list. */
    else {
        pts['x'].splice(indexindrawn,1)
        pts['y'].splice(indexindrawn,1)
        pts['label'].splice(indexindrawn,1)
        }

    /* Update the plot with the new values */
    drawnsource.data = pts
    drawnsource.change.emit()

    /* Update the table height */
    drawntable.height = drawntable.row_height*(drawnsource.data.x.length + 1)
    """

    csvUpdate = """
    var i
    var text = ""
    for (i=0; i<drawnsource.data.x.length; i++) {
        text+=drawnsource.data.x[i].toFixed(5)+","
        text+=drawnsource.data.label[i]+"<br>"
        }
    div.text = text

    """

    # Callback to update the list of drawn points
    callbackMarkClick = bm.CustomJS(args={
        'spectsource': spectsource,
        'drawnsource': drawndots.data_source,
        'drawntable': drawntable,
        'div': div}, code=markClick+csvUpdate)

    # Tap tool which triggers the custom JS callback when an invisible circle
    # is clicked.
    tap_tool = bm.TapTool(renderers=[spectdots], callback=callbackMarkClick)
    fig.add_tools(tap_tool)
    fig.toolbar.active_tap = tap_tool

    # Button to show/hide spectral data in CSV format
    csvbut = bm.Button(label="Show/hide CSV data table", button_type="default")

    # Custom JS for CSV show/hide
    showCSV = """
    if (div.visible == false) {
        div.visible = true
        }
    else {
        div.visible = false}
    """

    # Callback for CSV show/hide
    callbackShowCSV = bm.CustomJS(args={
        'drawnsource': drawnsource,
        'div': div}, code=csvUpdate+showCSV)

    # Add the callback to the button for CSV show/hide
    csvbut.js_on_event(be.ButtonClick, callbackShowCSV)

    # Return the modified figure and the data table of drawn points
    return fig, drawntable, csvbut, div


def linenames_to_visualtags(names, tagtype='autocolor', groupmin=2):
    """
    From a list of names, make the visual tags

    Parameters
    ----------
    names : list of str
        Labels or names of lines from a lines file
    tagtype : str
        one of `tagtypes` given below. Sets the mode for color-coding points.
    groupmin : int
        minimum number in a group

    Returns
    -------
    colors : list of strings
        Color for each overlay point
    markers : list of strings
        Marker type for each overlay point (square, circle, triangle..)
    sizes : list of ints
        Marker size for each overlay point
    legend : bool
        Whether or not to add a legend
    tags : list of strings
        Category names for each point (corresponds to color/marker-coding
            and legend)
    """

    # Set up color options
    color_range = [
        "#009bffff",
        "#fff800ff",
        "#ff57d9ff",
        "#9fff48ff",
        "#ff5b5dff",
        "#baa2fbff",
        "#00e8ffff",
        "#8ac14bff",
        "#ffc96aff",
        "#ff8e8fff",
        "#bd43d9ff",
        "#3eaa21ff",
        "#e09b24ff",
        "#9ec7ffff",
        "#9524ffff",
        "#ff96e7ff",
        "#00ffb5ff",
        "#b86958ff",
        "#facbefff",
        "#0cbfa1ff",
        "#2f54fdff",
        "#9d79ffff"
    ]

    # set up marker options
    # note to future: do NOT use inverted_triangle;
    # it causes a silent error
    marker_range = [
        "square",
        "triangle",
        "diamond",
        "plus",
        "star",
        "circle_cross",
        "square_x",
        "triangle_dot",
        "diamond_cross",
        "star_dot",
        "circle_x",
        "square_pin",
        "triangle_pin",
        "diamond_dot",
        "circle_dot",
        "hex",
        "circle_y",
        "square_cross",
        "hex_dot",
        "square_dot",
        "asterisk",
        "x"
    ]

    # some gymnastics to generate color-marker pairs more elegantly
    marker_range_deque = collections.deque(marker_range)
    glyphlooks = []
    for i in range(len(color_range)):
        glyphlooks += list(zip(color_range, marker_range_deque))
        marker_range_deque.rotate(-1)

    # Below: need to turn the line names into a set of "tags" that will define
    # groups of lines for color-coding.

    tagdefault = "all other entries"
    if tagtype == "autocolor":
        # If we are auto-coloring, ignore parenthetical notes
        # and strip off whitespace
        notechar = "("
        tags = []
        for n in names:
            if notechar in n:
                tag, othernote = n.split(notechar, 1)
                tag = tag.strip()
            else:
                tag = n.strip()
            tags += [tag]

    elif tagtype in ["highlight", "highlight-only"]:
        # If we are in highlight mode, pay attention to things
        # after the exclamation point.
        # Also strip off whitespace.
        tagchar = "!"
        tags = []
        for n in names:
            if tagchar in n:
                othernote, tag = n.split(tagchar)
                tag = f'{tagchar}{tag.strip()}'
            else:
                # Group everything without a ! into the default category
                if tagtype == "highlight-only":
                    tag = tagdefault
                else:
                    tag = n
            tags += [tag]
    else:
        # If we aren't in a highlight or autocolor mode, everything
        # gets the default tag
        tags = [tagdefault]*len(names)

    # Compute the unique tags and their counts.
    # Order by counts in descending order.
    tags = np.array(tags)
    utags, taginds, counts = np.unique(
        tags, return_inverse=True, return_counts=True)
    # If a group min size was set, reset everything under that group
    # size to the default tag
    if len(tags) > 0 and groupmin > 1:
        tags[counts[taginds] < groupmin] = tagdefault
    utags, counts = np.unique(tags, return_counts=True)

    # Create the colors and markers arrays, which are currently empty
    colors = np.array([""]*len(names), dtype='<U16')
    markers = np.array([""]*len(names), dtype='<U16')
    sizes = np.ones(len(names))*11

    # Determine if any tags in highlight mode are forcing a color/marker code
    # If so, reserve them and remove them from rotation
    reserved_gl_dict = {}
    pretty_utags = []
    if tagtype in ['highlight', 'highlight-only']:
        for iutag, utag in enumerate(utags):
            # if we have a tag...
            if utag[0] == tagchar:
                # see if it has a numeric code right after the tagchar
                ccode_field = utag.strip(tagchar).split(" ")[0]
                if ccode_field.isnumeric():
                    # reserve the glyph corresponding to the numeric code
                    reserved_gl = glyphlooks[int(ccode_field)]
                    reserved_gl_dict[utags[iutag]] = reserved_gl
                    # make a "pretty" version of the tag (minus numeric code)
                    pretty_utag = utag.strip(
                        tagchar).strip(ccode_field).strip()
                    # check for and resolve collisions with non-numeric tags
                    if f'{tagchar}{pretty_utag}' in utags:
                        pretty_utag = f"{pretty_utag} group 2"
                    pretty_utags.extend([pretty_utag])
                else:
                    pretty_utags.extend([utag.strip(tagchar)])
            else:
                pretty_utags.extend([utag])
        # remove any reserved glyphs from the cycle
        for r in reserved_gl_dict.values():
            glyphlooks.remove(r)

        # deal with cases of pretty tag duplication
        # (for example, same descriptor, different numeric codes)
        # that have not already been dealt with above
        pretty_utag_dups = (
            collections.Counter(pretty_utags) -
            collections.Counter(set(pretty_utags)))
        pretty_utag_dups = list(pretty_utag_dups.keys())
        for iutag, utag in enumerate(utags):
            # also deals with "empty" numeric tags (used to force the
            # color coding but not otherwise named)
            if len(pretty_utags[iutag]) == 0:
                pretty_utags[iutag] = "Unlabeled group"
            if utag in pretty_utag_dups:
                pretty_utags[iutag] = f'{pretty_utags[iutag]} group 2'
        pretty_utags = np.array(pretty_utags)

    else:
        pretty_utags = utags

    glyph_cycle = itertools.cycle(glyphlooks)
    # Loop through the unique tags and set all corresponding color
    # array entries to the corresponding color.
    tags_pretty = tags.tolist()
    for iutag, utag in enumerate(utags):
        # special case: tag defaults
        if utag == tagdefault:
            color = "lightgray"
            marker = "circle"
        # special case: hints
        elif utag.lower() in ['!hint', '!hints']:
            color = 'black'
            marker = 'x'
        # assign any colors as specifically requested in numeric tags
        elif utag in reserved_gl_dict.keys():
            glyphlook = reserved_gl_dict[utag]
            color, marker = glyphlook
        # otherwise, just cycle to the next glyph
        else:
            glyphlook = next(glyph_cycle)
            color, marker = glyphlook
        tagplaces = np.where(tags == utag)[0]
        # certain markers are really small for some reason... fix that
        for pattern in ["triangle", "diamond", "star", "hex"]:
            if pattern in marker:
                sizes[tagplaces] = 16
        colors[tagplaces] = color
        markers[tagplaces] = marker
        for t in tagplaces:
            tags_pretty[t] = pretty_utags[iutag]

    return colors, markers, sizes, tags_pretty


def make_interactive_plot(spectfile, fmin, fmax, outfile,
                          freqcolname=None, datacolname=None,
                          linesfile=None, colorcode='autocolor',
                          colorcode_group_min=0, linesfile_label=None,
                          plotcombs=None, intersect_linefinder=False,
                          peaksensitivity=0.001, peakmedwindow=0.05,
                          title=None, yaxlabel="", ylog=True, legend=False,
                          desc="", spectfile_ref=None, freqcolname_ref=None,
                          datacolname_ref=None, desc_ref=None, comparison=None,
                          annotate=True,):
    """
    Make an interactive plot

    Parameters
    ----------
    spectfile : Path
    fmin : float
    fmax : float
    outfile : Path
    freqcolname : str
        Name of the frequency column in the npz file
    datacolname : str
        Name of the data column in the npz file
    linesfile : Path
    colorcode : str
    colorcode_group_min: int
    linesfile_label: str
    plotcombs : list of str
    intersect_linefinder : bool
    peaksensitivity : float
    peakmedwindow : float
    title : str
    yaxlabel : str
    ylog : bool
    legend : bool
    desc : str
    spectfile_ref : Path
    freqcolname_ref : str
    datacolname_ref : str
    desc_ref : str
    comparison : str
        Method for comparison calculation "ratio" or "fraction"
    annotate : bool
    """

    # Load spectral data and clip to user-specified bounds
    freq, val, mdata = io.load_spect_data(spectfile,
                                          freqname=freqcolname,
                                          dataname=datacolname,
                                          fmin=fmin,
                                          fmax=fmax)

    # Assign default labels
    if yaxlabel is None or yaxlabel == '':
        if mdata['dtype'] == 'normpow':
            yaxlabel = 'Normalized average power'
        elif mdata['dtype'] in ['psd', 'psdwt']:
            yaxlabel = 'Power / Hz'
        elif mdata['dtype'] in ['amppsd', 'amppsdwt']:
            yaxlabel = 'Amplitude / sqrt(Hz)'
        elif mdata['dtype'] == 'persist':
            yaxlabel = 'Persistency'
        elif mdata['dtype'] == 'coherence':
            yaxlabel = 'Coherence'

    # Load lines data, if any, and clip to bounds matching spectrum
    linds, lnames, lfreq = [], [], []
    for i, linesfile in enumerate(linesfile):
        lfreq_i, lnames_i = io.load_lines_from_linesfile(linesfile)
        if colorcode == "fromfile":
            try:
                nickname = linesfile_label[i]
            except IndexError:
                nickname = Path(linesfile).name
            new_lnames = []
            for j, x in enumerate(lnames_i):
                if "!" in x:
                    existing_name, existing_tag = x.split("!")
                    if existing_tag in ["hint", "hints"]:
                        new_lnames.extend([x])
                    else:
                        new_lnames.extend(
                            [f"{existing_name} !entries from {nickname}"])
                else:
                    new_lnames.extend([f"{x} !entries from {nickname}"])
            lnames_i = new_lnames
        if len(lfreq_i) > 0:
            lfreq_i, lnames_i = slt.clip_spect(
                lfreq_i, lnames_i, freq[0], freq[-1], islinefile=True)
            linds_i = slt.match_bins(freq, lfreq_i)
            linds = np.append(linds, linds_i)
            lnames = np.append(lnames, lnames_i)
            lfreq = np.append(lfreq, lfreq_i)
    if colorcode == "fromfile":
        colorcode = "highlight"

    # If the user didn't specify color coding, try to guess based on
    # the contents of the lines file. Default to auto-coloring.
    if colorcode == 'autocolor' and linesfile and "!" in "".join(lnames):
        colorcode = 'highlight'

    # Get ready to load comb data, if any, by setting up arrays
    combinds = np.zeros(0)  # spectral indices of teeth
    combnames = np.zeros(0)  # labels of teeth
    combfreq = np.zeros(0)  # frequencies of teeth

    if plotcombs:
        # loop over specified combs
        for combarg in plotcombs:
            sp, off = io.combarg_to_combparams(combarg)
            jcombfreq, jcombinds, jcombnames = slt.combparams_to_labeled_teeth(
                sp, off, freq, np.arange(0, len(freq), 1))

            # If we have *also* got highlights specified, then each comb
            # needs its own highlight tag as well.
            if colorcode == 'highlight':
                jcombnames = [
                    f"{x} !comb {sp:.5};{off:.5} Hz"
                    for x in jcombnames]

            # Append to the waiting arrays
            combinds = np.append(combinds, jcombinds)
            combnames = np.append(combnames, jcombnames)
            combfreq = np.append(combfreq, jcombfreq)

    # Concatenate the line and comb data
    inds = np.append(linds, combinds).astype(int)
    names = np.append(lnames, combnames)
    tagfreq = np.append(lfreq, combfreq)

    # If asked to intersect with linefinder results
    if intersect_linefinder:
        # convert the running median window to bins
        medwindow_bins = int(peakmedwindow /
                             (freq[-1] - freq[0]) * len(freq))
        # get indices of peaks that pass the cuts
        peaks = linefinder.peaks(val, peaksensitivity, medwindow_bins)
        # filter line data based on whether it's in the peak data
        filt = np.isin(inds, peaks)
        inds = inds[filt]
        names = names[filt]
        tagfreq = tagfreq[filt]

    # Collect any left and right tags
    left = []
    right = []
    boxnames = []
    boxmids = []
    for i, name in enumerate(names):
        if "left@" in names[i] and "right@" in names[i]:
            lbound = float(name.split("left@")[1].split()[0])
            rbound = float(name.split("right@")[1].split()[0])
            left.extend([lbound])
            right.extend([rbound])
            boxnames.extend([f"extent of {tagfreq[i]} Hz peak: {name}"])
            boxmids.extend([tagfreq[i]])

    # Convert the lines to visual tags (markers, colors, etc for glyphs)
    colors, markers, sizes, tags = linenames_to_visualtags(
        names,
        tagtype=colorcode,
        groupmin=colorcode_group_min)

    # Plot the spectrum
    fig, spectsource, spinners, spectline = plot_spect(
        outfile=outfile,
        freq=freq,
        val=val,
        title=title,
        yaxlabel=yaxlabel,
        ylog=ylog
    )

    # Overlay the line and comb data
    fig = overlay(fig,
                  spectsource,
                  inds,
                  names,
                  tagfreq,
                  colors,
                  markers,
                  sizes,
                  tags,
                  left=left,
                  right=right,
                  boxnames=boxnames,
                  boxmids=boxmids,
                  legend=legend
                  )

    gplots = [fig]

    # Plot the reference spect if requested
    if spectfile_ref:

        reffreq, refval, _ = io.load_spect_data(
            spectfile_ref,
            freqname=freqcolname_ref,
            dataname=datacolname_ref,
            fmin=fmin,
            fmax=fmax,
        )

        fig, refval = plot_reference_spect(
            fig, freq, reffreq, refval,
            make_legend=(not legend),
            spectline_renderer=spectline,
            spect_desc=desc,
            refspect_desc=desc_ref,
        )

        if comparison:
            compfig = plot_comparison_figure(
                fig, freq, val, refval, comparison)
            gplots = [compfig, fig]

    # If the user requested an annotatable plot
    # add the clickable features and save
    if annotate:
        fig, drawntable, csvbut, div = make_clickable(fig, spectsource)
        bp.save(bl.column(
            *gplots,
            bl.row(spinners),
            drawntable,
            csvbut,
            div,
            sizing_mode='stretch_width'
        ))

    # Otherwise, just save as-is
    else:
        bp.save(bl.column(
            *gplots,
            bl.row(spinners),
            sizing_mode='stretch_width'
        ))


def main():
    args = get_args()

    kwargs = dict(args._get_kwargs())
    _ = kwargs.pop('spectfile', None)
    _ = kwargs.pop('fmin', None)
    _ = kwargs.pop('fmax', None)
    _ = kwargs.pop('outfile', None)

    make_interactive_plot(
        args.spectfile,
        args.fmin,
        args.fmax,
        args.outfile,
        **kwargs,
    )


if __name__ == "__main__":
    main()
