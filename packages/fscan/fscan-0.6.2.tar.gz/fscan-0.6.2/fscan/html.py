# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Evan Goetz (2023)
#
# This file is part of fscan

from gwdetchar.io import html as gwhtml
from MarkupPy import markup
import numpy.ma as ma
from pathlib import Path
import shutil

from .utils.config import CustomConfParser
from .utils.dtutils import (parse_filepath, datetime_to_gps, subfolder_format,
                            snap_to, add_dtlargs, deltastr_to_relativedelta,
                            args_to_intervals, relativedelta_to_tag,
                            )
from .utils.io import read_channel_config
from .plot.static import expected_pngs
from .utils.utils import channels_per_segments, epseg_setup, epoch_info


JS_FILES = [
    'https://code.jquery.com/jquery-3.7.1.min.js',
    'https://code.jquery.com/ui/1.13.2/jquery-ui.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.30.1/moment.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery.lazy/1.7.11/jquery.lazy.min.js',  # noqa
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',  # noqa
    'https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js',  # noqa
    'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js',  # noqa
    'https://cdn.jsdelivr.net/npm/gwbootstrap@1.3.7/lib/gwbootstrap.min.js',
    'https://cdn.jsdelivr.net/npm/gwbootstrap@1.3.7/lib/gwbootstrap-extra.min.js']  # noqa


def navbar(ifo, metadata, ch_list=None):
    """
    Create the navigation bar that contains a title, calendar, and links to
    other pages for this particular Fscan run. A calendar is only created for
    day, week, or month modes. Any other mode does not generate a calendar

    ifo : str
        e.g., 'H1'
    metadata : dict
        metadata obtained from dateTimeLogic.parse_filepath()
    ch_list : list
        strings for the channels to be processed in the navigation bar

    Returns navigation bar object
    """
    if ch_list is None:
        ch_list = []

    # First get brand and class -- I have no idea what this is, but it is
    # needed for something
    (brand, class_) = gwhtml.get_brand(
        ifo, 'Fscan', datetime_to_gps(metadata['epoch']))

    # For the links to other pages, we need to figure out the paths
    html_links = Path(metadata['html-folder'].replace('home/', '~').replace(
        '/public_html/', '/'))

    # First link is the "Summary". It will be the index.html file
    links = [['Summary', f"{str(html_links / 'index.html')}"]]

    # Create the list of links into different subsystems. Note that the PEM
    # subsystem is divided up into various sensors. Anything that is not
    # part of the subsystems in the dictionary below are put into the OTHER
    # category
    subsys_dict = {
        'CAL': ['STRAIN', 'DELTAL', ':CAL'],
        'ASC': [':ASC'],
        'LSC': [':LSC'],
        'SUS': [':SUS'],
        'ACC': ['_ACC_'],
        'MAG': ['_MAG_'],
        'MIC': ['_MIC_'],
        'SEI': ['_SEI_'],
        'OTHER': ['']}
    # Here we use a masked array to track which channels have already gotten
    # linked in a subsystem
    ch_list_ma = ma.masked_array(ch_list, mask=[0]*len(ch_list))
    # loop over the subsystems in the subsys_dict
    for subsys_idx, (subsys, patterns) in enumerate(subsys_dict.items()):
        subsys_links = []
        # loop over the patterns for a given subsystem
        for pattern_idx, pattern in enumerate(patterns):
            # loop over the channels in the channel list masked array
            for ch_idx, ch in enumerate(ch_list_ma):
                if ch_list_ma.mask[ch_idx] is not True and pattern in ch:
                    subsys_links.append(
                        [ch,
                         f"{str(html_links / ch.replace(':', '_'))}.html"])
                    ch_list_ma.mask[ch_idx] = True
        if len(subsys_links) > 0:
            links.append([subsys, subsys_links])
    # Now we have a list of
    # [[<subsystem 1>, [[<channel 1>, <channel 1 link>],
    #                   [<channel 2>, <channel 2 link>]]],
    #  [<subsystem 2>, [[<channel 3>, <channel 3 link>],
    #                   [<channel 4>, <channel 4 link>]]]]

    # If a mode has been selected that we can generate a calendar and date
    # picker, then we add that to the links here
    if ((mode := relativedelta_to_tag(metadata['duration'])) in
            ['day', 'week', 'month']):
        cal = calendar(metadata['epoch'], mode=mode)
        links = list(cal) + links

    return gwhtml.navbar(links, brand=brand, class_=class_)


# Copied from gwsumm/gwsumm/html/bootstrap.py
# We need to be able to set the mode ourselves
def calendar(date, class_='nav-link dropdown-toggle',
             id_='calendar', dateformat=None, mode='day'):
    """
    Construct a bootstrap-datepicker calendar

    Parameters
    ----------
    date : :class:`datetime.datetime`, :class:`datetime.date`
        active date for the calendar
    class_ : str
    id_ : str
        id of the calendar
    dateformat : str
        date format to use
    mode : str
        If dateformat not given then derive it from 'day', 'week', 'month',
        or 'year'

    Returns
    -------
    calendar : list
        a list of three oneliner strings of HTML containing the calendar
        text and a triggering dropdown
    """
    if dateformat is None:
        if mode == 'day':
            dateformat = '%B %d %Y'
        elif mode == 'week':
            dateformat = 'Week of %B %d %Y'
        elif mode == 'month':
            dateformat = '%B %Y'
        elif mode == 'year':
            dateformat = '%Y'
        else:
            raise ValueError(f"Cannot generate calendar for Mode {mode}")
    datestring = date.strftime(dateformat).replace(' 0', ' ')
    data_date = date.strftime('%d-%m-%Y')
    # get navigation objects
    backward = markup.oneliner.a(
        '&laquo;', class_='nav-link step-back', title='Step backward')
    cal = markup.oneliner.a(
        datestring, id_=id_, class_=class_, title='Show/hide calendar',
        **{'data-date': data_date, 'data-date-format': 'dd-mm-yyyy',
           'data-viewmode': '%ss' % mode})
    forward = markup.oneliner.a(
        '&raquo;', class_='nav-link step-forward', title='Step forward')
    return [backward, cal, forward]


def banner(channel):
    """
    Initialise a new markup banner

    Parameters
    ----------
    channel : str
        channel name
    Returns
    -------
    page : :class:`markup.page`
        the structured markup to open an HTML document
    """
    # create page
    page = markup.page()
    # write banner
    page.div(class_='page-header', role='banner')
    page.h1(f"Fscan: {channel}", class_='pb-2 mt-3 mb-2 border-bottom')
    page.div.close()
    return page()


def button_links(html_path, full_path, extra=None):
    """
    Add the button links to other pages

    Parameters
    ----------
    html_path : str
        full path to Fscan summary page index.html file
    full_path : str
        full path to channel directory with data files
    extra : list of tuples, optional
        Extra button path tuples of the form (<name>, <path>)
    Returns
    -------
    page : :class:`markup.page`
        the structured markup to open an HTML document
    """
    if extra is None:
        extra = []

    # derive the username
    pub_dir_idx = -1
    for idx, part in enumerate(Path(full_path).parts):
        if part == 'public_html':
            pub_dir_idx = idx
            break
    pub_dir_user = Path(full_path).parts[pub_dir_idx - 1]

    # Now make the page for the buttons
    page = markup.page()
    page.div(class_="button-group border-bottom pb-2")
    page.a('Full Fscan navigation',
           href=html_path.replace(
               f'home/{pub_dir_user}/public_html', f'~{pub_dir_user}'),
           rel='external',
           target='_blank',
           class_='btn btn-primary btn-xl')
    page.a('Fscan data files',
           href=full_path.replace(
               f'home/{pub_dir_user}/public_html', f'~{pub_dir_user}'),
           rel='external',
           target='_blank',
           class_='btn btn-info btn-xl')
    for idx, (name, path) in enumerate(extra):
        page.a(name,
               href=path.replace(
                   f'home/{pub_dir_user}/public_html', f'~{pub_dir_user}'),
               rel='external',
               target='_blank',
               class_='btn btn-info btn-xl')
    page.div.close()
    return page()


def navigation_text():
    """This is a super simple function to print a special text string
    to the index.html page to help navigate.
    """
    page = markup.page()
    page.p('No STRAIN channel was part of this segment type, but other data '
           'may be available. Please use the Fscan subsystem navigation bar '
           'above.', class_="text-info")
    return page()


def no_data_text():
    """This is a super simple function to print a special text string
    to the <channel>.html page to understand that no data was available.
    """
    page = markup.page()
    page.p('No SFT data was available for this segment type, epoch, and '
           'duration, but other data may be available for different segment '
           'types. When available, please select another segment type from '
           'the buttons above.', class_="text-info")
    return page()


def invalid_ch_text():
    """This is a super simple function to print a special text string
    to the <channel>.html page to understand that the channel is not valid.
    """
    page = markup.page()
    page.p('No SFT data was available for this channel, either because the '
           'channel was not in frames or the sampling rate is to low for the '
           'requested frequency band. Other channels may be available by '
           'using the buttons above.', class_="text-info")
    return page()


def zero_ch_text():
    """This is a super simple function to print a special text string
    to the <channel>.html page to understand that the channel is zeros.
    """
    page = markup.page()
    page.p('SFT data is entirely zeros for this channel; no plots are '
           'created in this case. Other channels may be available by '
           'using the buttons above.', class_="text-info")
    return page()


# Copied from gwdetchar/gwdetchar/html/io/html.py
# The original had some hardcoded values for substrings that wasn't very
# flexible
def fancybox_img(img, linkparams=None, lazy=False, **params):
    """
    Return the markup to embed an <img> in HTML

    Parameters
    ----------
    img : :class:`FancyPlot`
        a `FancyPlot` object containing the path of the image to embed
        and its caption to be displayed
    linkparams : dict, optional
        the HTML attributes for the ``<a>`` tag
    lazy : bool, optional
        whether to lazy-load the image, default: False
    **params
        the HTML attributes for the ``<img>`` tag

    Returns
    -------
    page : `~MarkupPy.markup.page`
        the markup object containing fancyplot HTML
    """
    if linkparams is None:
        linkparams = {}

    page = markup.page()
    aparams = {
        'title': img.caption,
        'class_': 'fancybox',
        'target': '_blank',
        'data-caption': img.caption,
        'data-fancybox': 'gallery',
        'data-fancybox-group': 'images',
    }
    aparams.update(linkparams)
    img = str(img)
    img_path = Path(img)
    substrings = img_path.name.split('_')
    if len(substrings) >= 3:
        plt = substrings[0]
        fmin = substrings[1]
        fmax = substrings[2]
        id_str = f'{plt}_{fmin}_{fmax}'
    elif len(substrings) == 1:
        id_str = substrings[0]
    else:
        raise ValueError('Image filename must be either <name> with no '
                         'underscores in <name> or <name> must have two '
                         'underscores where <name> = <plot>_<fmin>_<fmax>')
    page.a(href=img, id_=id_str, **aparams)
    src_attr = lazy and 'data-src' or 'src'
    imgparams = {
        'alt': img_path.name,
        'class_': lazy and 'img-fluid w-100 lazy' or 'img-fluid w-100',
        src_attr: img.replace('.svg', '.png'),
    }
    imgparams.update(params)
    page.img(id_=id_str, **imgparams)
    page.a.close()
    return page()


# Copied from gwdetchar/gwdetchar/io/html.py because I wanted to be sure that
# this function used the fancybox_img() function from this file
def scaffold_plots(plots, nperrow=3, lazy=True):
    """
    Embed a `list` of images in a bootstrap scaffold

    Parameters
    ----------
    plots : `list` of `FancyPlot`
        the list of image paths to embed
    nperrow : `int`
        the number of images to place in a row (on a desktop screen)
    lazy : `bool`, optional
        whether to lazy-load images, default: True

    Returns
    -------
    page : `~MarkupPy.markup.page`
        the markup object containing the scaffolded HTML
    """
    page = markup.page()
    x = int(12//nperrow)
    # scaffold plots
    for i, p in enumerate(plots):
        if i % nperrow == 0:
            page.div(class_='row scaffold')
        page.div(class_='col-sm-%d' % x)
        page.add(fancybox_img(p, lazy=lazy))
        page.div.close()  # col
        if i % nperrow == nperrow - 1:
            page.div.close()  # row
    if i % nperrow < nperrow-1:
        page.div.close()  # row
    return page()


def write_channel_page(epseg_info, metadata, navbar, fband,
                       ptypes=None):
    """
    Write a single html page for a specific channel

    Parameters
    ----------
    epseg_info : dict
        dict of epoch and segment info obtained from FscanDriver.epseg_setup()
    metadata : dict
        dict of metadata obtained from dateTimeLogic.parse_filepath()
    navbar : navbar object
        use the return value of FscanHTML.navbar() to prior to calling this
        method
    fband : float
        plot sub bands, from the channel configuration yaml file plot_sub_band
        variable
    ptypes : list, optional
        Plot types: spectrogram, timeaverage, persist, and coherence. Default:
        ['spectrogram', 'timeaverage', 'persist']

    Returns
    -------
    page : `~MarkupPy.markup.page`
        the markup object containing the HTML
    """
    if ptypes is None:
        ptypes = ['spectrogram', 'timeaverage', 'persist']

    # Create the HTML output directory if needed
    Path(metadata['html-folder']).mkdir(parents=True, exist_ok=True)

    # Create page
    page = gwhtml.new_bootstrap_page(
        navbar=navbar, topbtn=False, script=JS_FILES,
        title=f"Fscan | {metadata['channel']} | {metadata['epoch']}")
    page.add(banner(metadata['channel']))

    # Button links
    extra = []
    if ('coherence' not in ptypes and
            ('STRAIN' in metadata['channel'] or
             'DELTAL' in metadata['channel'])):
        extra.append(('Interactive spectrum',
                      str(Path(metadata['channel-path'],
                               'visual_overview_speclong_0000to0300Hz.html'))))
        extra.append(('Interactive persistency',
                      str(Path(metadata['channel-path'],
                               'visual_overview_persist.html'))))
    elif 'coherence' in ptypes:
        extra = [('Interactive coherence',
                  str(Path(metadata['channel-path'],
                           'visual_overview_coherence_0000to0300Hz.html')))]
    # Last week and last month buttons
    week_subfolder = subfolder_format(
        'week',
        snap_to(metadata['epoch'], 'midnight wednesday') -
        deltastr_to_relativedelta('1week')
    )
    month_subfolder = subfolder_format(
        'month',
        snap_to(metadata['epoch'], 'midnight month') -
        deltastr_to_relativedelta('1month')
    )
    extra.append(
        ('Last week',
         str(Path(metadata['segtype-folder'],
                  'summary',
                  'week',
                  week_subfolder,
                  f"{metadata['channel-label']}.html")))
    )
    extra.append(
        ('Last month',
         str(Path(metadata['segtype-folder'],
                  'summary',
                  'month',
                  month_subfolder,
                  f"{metadata['channel-label']}.html")))
    )
    page.add(button_links(
        str(Path(metadata['html-folder'], 'index.html')),
        metadata['channel-path'],
        extra=extra
    ))

    # Create a sorted list of different plot types
    # TODO: a better way to make list variables based on plt_types??
    plt_type_lists = {}
    for plt_type in ptypes:
        try:
            file_list, _, _ = expected_pngs(
                metadata['channel-path'],
                metadata['fmin'],
                metadata['fmax'],
                fband,
                epseg_info['SFTGPSstart'],
                epseg_info['SFTGPSend'],
                metadata['Tsft'],
                plt_type)
        except KeyError:
            # This might happen because there was no SUPERDAG.dag file
            gwhtml.close_page(page, f"{str(Path(metadata['html-folder'], metadata['channel-label']))}.html")  # noqa E501
            return page

        plt_type_lists[plt_type] = sorted(
            file_list, key=lambda p: float(Path(p).name.split('_')[1]))

    # Begin populating the page in a container
    page.div(class_="container")

    # need "home/<username>/public_html" to get the proper links
    public_html_folder_nobase = str(
        Path(*Path(metadata['public-html-folder']).parts[1:])
    )

    # If this is a STRAIN or DELTAL channel then we have run the
    # forestOfLines() from postProcess.py
    if 'STRAIN' in metadata['channel'] or 'DELTAL' in metadata['channel']:
        headline_plots = [
            gwhtml.FancyPlot(
                str(plt_type_lists['timeaverage'][0]).replace(
                    public_html_folder_nobase,
                    f"~{metadata['username']}")),
            gwhtml.FancyPlot(str(Path(
                metadata['channel-path'].replace(
                    public_html_folder_nobase, f"~{metadata['username']}"),
                'linecount.png'))),
            gwhtml.FancyPlot(str(Path(
                metadata['channel-path'].replace(
                    public_html_folder_nobase, f"~{metadata['username']}"),
                'heatmap.png'))),
        ]
        page.add(scaffold_plots(headline_plots))

    # Add a list of FancyPlot objects that use links
    fancy_plots = []
    for idx in range(len(plt_type_lists[ptypes[0]])):
        for plt_type in ptypes:
            plt = str(plt_type_lists[plt_type][idx])
            plt = plt.replace(
                public_html_folder_nobase, f"~{metadata['username']}")
            fancy_plots.append(gwhtml.FancyPlot(plt))
    page.add(scaffold_plots(fancy_plots, nperrow=len(ptypes)))

    # Done filling the page, so we can close the container
    page.div.close()

    # Save to the output path
    gwhtml.close_page(page, f"{str(Path(metadata['html-folder'], metadata['channel-label']))}.html")  # noqa E501

    return page


def write_no_data_page(metadata, navbar, ch_problem=None):
    """
    Write a single html page for a specific channel when no data exists

    Parameters
    ----------
    metadata : dict
        metadata obtained from dateTimeLogic.parse_filepath()
    navbar : navbar object
        use the return value of FscanHTML.navbar() to prior to calling this
        method
    ch_problem : `str`, optional
        The channel is "invalid" if no SFTs were produced because the channel
        is not in frames or has too low a sampling frequency. The channel
        could be "zeros" if there is a digital setting that has zeroed the
        channel

    Returns
    -------
    page : `~MarkupPy.markup.page`
        the markup object containing the HTML

    Raises
    ------
    Exception
        if the value of ch_problem is not "invalid" or "zeros"
    """

    # Create the HTML output directory if needed
    Path(metadata['html-folder']).mkdir(parents=True, exist_ok=True)

    # Create page
    page = gwhtml.new_bootstrap_page(
        navbar=navbar, topbtn=False, script=JS_FILES,
        title=f"Fscan | {metadata['channel']} | {metadata['epoch']}")
    page.add(banner(metadata['channel']))
    page.add(button_links(
        str(Path(metadata['html-folder'], 'index.html')),
        metadata['channel-path']))
    if not ch_problem:
        page.add(no_data_text())
    elif ch_problem == 'invalid':
        page.add(invalid_ch_text())
    elif ch_problem == 'zeros':
        page.add(zero_ch_text())
    else:
        raise Exception(f'ch_problem={ch_problem} not recognized')

    # Save to the output path
    gwhtml.close_page(page, f"{str(Path(metadata['html-folder'], metadata['channel-label']))}.html")  # noqa E501

    return page


def write_special_index_page(metadata, navbar, no_data=False,
                             ch_problem=None):
    """
    Write an index.html page for when no index.html was created

    Parameters
    ----------
    metadata : dict
        dict of metadata obtained from dateTimeLogic.parse_filepath()
    navbar : navbar object
        use the return value of FscanHTML.navbar() to prior to calling this
        method
    no_data : bool, optional
        If no SFTs are available for this segment type and epoch, then set
        this to True so that a message can be printed to the summary pages
    ch_problem : `str`, optional
        The channel is "invalid" if no SFTs were produced because the channel
        is not in frames or has too low a sampling frequency. The channel
        could be "zeros" if there is a digital setting that has zeroed the
        channel

    Returns
    -------
    page : `~MarkupPy.markup.page`
        the markup object containing the HTML

    Raises
    ------
    Exception
    """

    # Create the HTML output directory if needed
    Path(metadata['html-folder']).mkdir(parents=True, exist_ok=True)

    # Create page
    page = gwhtml.new_bootstrap_page(
        navbar=navbar, topbtn=False, script=JS_FILES,
        title=f"Fscan | {metadata['epoch']}")
    page.add(banner('Summary'))
    page.add(button_links(
        str(Path(metadata['html-folder'], 'index.html')),
        metadata['channel-path']))
    if no_data:
        page.add(no_data_text())
    elif ch_problem == 'invalid':
        page.add(invalid_ch_text())
    elif ch_problem == 'zeros':
        page.add(zero_ch_text())
    elif ch_problem:
        raise Exception(f'ch_problem={ch_problem} not recognized')
    else:
        page.add(navigation_text())

    # Save to the output path
    gwhtml.close_page(page, f"{str(Path(metadata['html-folder'], 'index.html'))}")  # noqa E501

    return page


def check_post_success(ch_path):
    """Check status of the post process workflow

    Parameters
    ----------
    ch_path : Path, str
        Path to the channel

    Returns
    -------
    success : bool
        True if the post process was successful

    Raises
    ------
    Exception
        if post output file does not end with success
    """
    # Check that postProcess succeeded to the end
    post_process_path = Path(
        ch_path,
        'postProcess_success'
    )
    # for older workflows, we didn't have a file output so check the
    # standard output file from the job
    if not (postprocess_succeeded := post_process_path.exists()):
        if (filename := (post_process_path.parent /
                         'logs' /
                         'postProcess.out')).exists():
            pass
        elif (filename := (post_process_path.parent /
                           'logs' /
                           'postProcess_0.out')).exists():
            pass
        else:
            raise Exception('Post process failed without explanation')

        with open(filename) as f:
            lines = f.readlines()
        if lines[-1].strip() == 'Completed postProcess successfully':
            postprocess_succeeded = True

    return postprocess_succeeded


def write_fscan_page(ifo, epseg_info, channel_tup, no_data=False,
                     ptypes=None):
    """
    This should write out all the summary pages to
    <T_sft>/<seg type>/summary/<average dur>/<epoch>/<channel>.html
    where the data/plots are stored under
    <T_sft>/<seg type>/<average dur>/<epoch>/<channel>

    Parameters
    ----------
    ifo : `str`
        Interferometer string, ex. "H1"
    epseg_info : dict
        dictionary of info that is specific to each *combination* of an
        epoch and a segment type (generated by FscanDriver.epseg_setup())
    channel_tup : list
        List of tuples: (channel, plot sub band)
    no_data : bool, optional
        If no SFTs are available for this segment type and epoch, then set
        this to True so that a message can be printed to the summary pages
    ptypes : list, optional
        Plot types: spectrogram, timeaverage, persist, and coherence. Default:
        ['spectrogram', 'timeaverage', 'persist']

    Raises
    ------
    Exception
    """
    if ptypes is None:
        ptypes = ['spectrogram', 'timeaverage', 'persist']

    mdata = parse_filepath(epseg_info['epoch_path'])

    channel_list = [ch[0] for ch in channel_tup]

    # Create a navigation bar for all of the pages
    nav = navbar(ifo, mdata, channel_list)

    index_html_made = False

    # Loop through the channels, creating summary pages for each channel
    for idx, (ch, plot_sub_band) in enumerate(channel_tup):
        mdata['channel'] = ch
        mdata['channel-label'] = ch.replace(':', '_')
        mdata['channel-path'] = str(Path(epseg_info['epoch_path'],
                                         mdata['channel-label']))
        mdata['sfts-path'] = str(Path(mdata['channel-path'], 'sfts'))

        # Write a page for the channel
        if no_data:
            _ = write_no_data_page(mdata, nav, ch_problem=None)
        elif not (post_succeeded := check_post_success(mdata['channel-path'])):
            if Path(mdata['sfts-path'], 'nosfts').exists():
                ch_problem = 'invalid'
            elif Path(mdata['sfts-path'], 'zerosfts').exists():
                ch_problem = 'zeros'
            else:
                raise Exception('Post process failed without explanation')
            _ = write_no_data_page(mdata, nav, ch_problem=ch_problem)
        elif post_succeeded:
            mdata = parse_filepath(mdata['channel-path'])

            # Update plot types for coherence
            if ('coherence-ref-channel' in mdata.keys() and
                    mdata['coherence-ref-channel'] is not None and
                    'coherence' not in ptypes):
                ptypes.append('coherence')
            elif ('coherence' in ptypes and
                  ('coherence-ref-channel' not in mdata.keys() or
                   mdata['coherence-ref-channel'] is None)):
                ptypes.remove('coherence')

            _ = write_channel_page(epseg_info, mdata, nav, plot_sub_band,
                                   ptypes=ptypes)
        else:
            raise Exception('Something has gone wrong, we should have written '
                            f'a summary page for {ch}')

        # If an index.html page has not been created, and we have a STRAIN
        # channel then copy that channel page to index.html
        if not index_html_made and ('STRAIN' in ch or 'DELTAL' in ch):
            shutil.copy(
                Path(mdata['html-folder'], f"{mdata['channel-label']}.html"),
                Path(mdata['html-folder'], "index.html")
            )
            index_html_made = True

    # If no index.html page was made, then create a special index.html page.
    # The first channel in the segment type is the "landing page" channel
    if not index_html_made:
        (ch, plot_sub_band) = channel_tup[0]
        full_path = Path(epseg_info['epoch_path'], ch.replace(':', '_'))
        mdata = parse_filepath(str(full_path))

        # Write special index page
        if no_data or check_post_success(full_path):
            ch_problem = None
        elif Path(full_path, 'sfts', 'nosfts').exists():
            ch_problem = 'invalid'
        elif Path(full_path, 'sfts', 'zerosfs').exists():
            ch_problem = 'zeros'
        else:
            raise Exception('Post process failed without explanation')
        _ = write_special_index_page(
            mdata, nav, no_data=no_data, ch_problem=ch_problem)


class SummaryPage(object):

    def __init__(self, ch_info, epseg_info):
        self.epseg_info = epseg_info  # epoch+segtype dict
        # channels is a tuple of:
        #   channels using this segment type
        #   index values of those channels + segment type in ch_info yaml file
        # we want a new tuple of (channel name, plot sub band)
        channel_list = [
            ch['channel'] for ch in ch_info
            if ch['segment_type'] in epseg_info['segtype']]
        self.channels_tup = [
            (ch['channel'], ch['plot_sub_band'])
            for ch in ch_info if ch['segment_type'] in epseg_info['segtype']]

        # determine if this is a single IFO run or multi IFO run (this is
        # needed for generating the navigation bar for the summary page)
        self.ifo_try = channel_list[0][0:2]
        for idx, ch in enumerate(channel_list):
            if self.ifo_try != ch[0:2]:
                self.ifo_try = 'Network'
                break

    def build_summary_pages(self, no_data=False):
        write_fscan_page(self.ifo_try,
                         self.epseg_info,
                         self.channels_tup,
                         no_data=no_data)


def main():

    parser = CustomConfParser()
    parser.add_argument('--fscan-output-path', required=True, type=Path)
    parser = add_dtlargs(parser)
    parser.add_argument('-T', '--Tsft', type=int, default=1800,
                        help='SFT coherence length')
    parser.add_argument('--overlap-fraction', type=float, default=0.5,
                        help='overlap fraction (for use with windows; e.g., '
                             'use --overlap-fraction=0.5 with -w "hann")')
    parser.add_argument('-y', '--chan-opts', required=True, type=Path,
                        help='yml file containing list of channels, frametype,'
                             ' etc. to run over multiple channels')
    parser.add_argument('-s', '--segment-type', nargs='+', type=str,
                        required=True,
                        help='segment type of summary page(s) to generate '
                             'from the --chan-opts file')
    parser.add_argument('-I', '--intersect-data', type='bool', default=False,
                        help='Run gw_data_find with the --show-times option to'
                             ' find times data exist, and use LIGOtools '
                             ' segexpr to intersect this with the segments.')
    args = parser.parse_args()

    # parse the yaml file with channel specific information
    all_ch_info = read_channel_config(args.chan_opts)

    # Here's the sorted dictionary of segment types and channels
    segtype_info = channels_per_segments(all_ch_info)

    # Here's the dictionary of useful values for each epoch
    gps_intervals, duration_tags, epoch_tags = args_to_intervals(
        analysisStart=args.analysisStart,
        analysisEnd=args.analysisEnd,
        analysisDuration=args.analysisDuration,
        averageDuration=args.averageDuration,
        snapToLast=args.snapToLast,
        greedy=args.greedy,
    )
    epochs_info = epoch_info(gps_intervals, duration_tags, epoch_tags,
                             args.Tsft, args.overlap_fraction)

    # loop over segment types
    for segtype_idx, (segtype, channels) in enumerate(segtype_info.items()):
        if (','.join(sorted(segtype.split(','))) in
                ','.join(sorted(args.segment_type))):
            # loop over epochs
            for ep_idx, ep in enumerate(epochs_info):
                epseg_info = epseg_setup(
                    args.fscan_output_path, ep, segtype, channels,
                    intersect_data=args.intersect_data)

                # set no_data variable to True if the epseg_setup returned no
                # start and end GPS times for the SFTs
                if (epseg_info['SFTGPSstart'] is None and
                        epseg_info['SFTGPSend'] is None):
                    no_data = True
                else:
                    no_data = False

                # create summary pages
                summ_page = SummaryPage(all_ch_info, epseg_info)
                summ_page.build_summary_pages(no_data)


if __name__ == "__main__":
    main()
