from MuonDataLib.help.help_docs import (Doc,
                                        HIST,
                                        LOG,
                                        PEAK,
                                        FIGURE,
                                        MUONDATA)


def get_figure_docs():
    return [Doc('Figure',
                'plot.basic',
                [FIGURE],
                "An object to handle making Plotly plots.",
                optional_param={'title': ["The title for the plot.", "''"],
                                'x_label': ['The label for the x axis.',
                                            'time (micro seconds)'],
                                'y_label': ['The label for the y axis.',
                                            'Counts']},
                example=['from MuonDataLib.plot.basic import Figure',
                         'fig = Figure("Example plot", '
                         'y_label="Temp (Kelvin)")']),

            Doc('plot',
                'plot.basic.Figure',
                [FIGURE],
                "A method to create a simple plot in the "
                "Figure object.",
                param={'bin_centres': 'The list of bin centres '
                       '(i.e. point data).',
                       'y_values': "The y values to plot.",
                       'label': 'The label to give the data '
                       'set in the legend'},
                example=['from MuonDataLib.plot.basic import Figure',
                         'import numpy as np',
                         'fig = Figure("Example plot")',
                         'x = np.arange(0, 10)',
                         'y = np.sin(2.1*x)',
                         'fig.plot(x, y, "sin(2.1 x)")']),

            Doc('show',
                'plot.basic.Figure',
                [FIGURE],
                "A method to generate and present the plot "
                "from the Figure object.",
                example=['from MuonDataLib.plot.basic import Figure',
                         'import numpy as np',
                         'fig = Figure("Example plot")',
                         'x = np.arange(0, 10)',
                         'y = np.sin(2.1*x)',
                         'fig.plot(x, y, "sin(2.1 x)")',
                         'fig.show()']),

            Doc('plot_peak_property_histogram',
                'plot.basic.Figure',
                [FIGURE, HIST, MUONDATA, PEAK],
                "A method to create a plot "
                "of histogram data from a peak property.",
                param={'hist': 'The histogram matrix (as from np.histogram) ',
                       'bins': 'The bin edges for the histogram.'},
                optional_param={'label': ['The base label to use '
                                          'in the legend.', '""']},
                example=['from MuonDataLib.plot.basic import Figure',
                         'from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'hist, bins = data.get_peak_property_histogram'
                         '("Amplitudes")',
                         'fig = Figure("Example plot")',
                         'fig.plot_peak_property_histogram(hist, bins'
                         'label="HIFI00001")',
                         'fig.show()']),

            Doc('plot_from_histogram',
                'plot.basic.Figure',
                [FIGURE, HIST, MUONDATA],
                "A method to store that data needed "
                "to make a plot of histogram data.",
                param={'bins': 'The bin edges for the histogram.',
                       'hist': 'The histogram matrix (period, '
                       'spectrum number, bins).',
                       'det_list': 'The list of spectrum numbers to plot.'},
                optional_param={'label': ['The base label to use '
                                          'in the legend.', '""'],
                                'period': ['The period to plot.', '1']},
                example=['from MuonDataLib.plot.basic import Figure',
                         'from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'hist, bins = data.histogram()',
                         'fig = Figure("Example plot")',
                         'fig.plot_from_histogram(bins, hist, [1, 3, 5], '
                         'label="HIFI00001")',
                         'fig.show()']),

            Doc('plot_sample_log',
                'plot.basic.Figure',
                [FIGURE, MUONDATA, LOG, HIST],
                "A method to add the data to plot "
                "the current (filtered) sample logs "
                "and their original values.",
                param={'muon_data': 'The MuonData object that contains '
                       'the log that we want to plot.',
                       'log_name': "The name of the sample log to plot"},
                example=['from MuonDataLib.plot.basic import Figure',
                         'from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'fig = Figure("Example plot")',
                         'fig.plot_sample_log(data, "HIFI_field")',
                         'fig.show()'])]
