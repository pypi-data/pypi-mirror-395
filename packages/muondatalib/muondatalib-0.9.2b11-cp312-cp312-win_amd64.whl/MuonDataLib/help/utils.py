from MuonDataLib.help.help_docs import (Doc,
                                        UTILS,
                                        LOG,
                                        MUONDATA)


def get_utils_docs():
    return [Doc('create_data_from_function',
                'data.utils',
                [MUONDATA, UTILS, LOG],
                "A method to create some fake data. "
                "It takes a function, its parameters and the x range "
                "to generate some fake data with noise in both x and y.",
                param={'x1': 'The start x value.',
                       'x2': 'The end x value.',
                       'dx': 'The average step size for the x data.',
                       'params': 'A list of the parameters to use '
                       'in the function',
                       'function': 'The callable function to use when '
                       'creating the data.'},
                optional_param={'seed': ['The seed value for the random '
                                         'number generator',
                                         'None']},
                returns='The fake x and y values.',
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'from MuonDataLib.data.utils import '
                         'create_data_from_function',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'times = data.get_frame_start_times()',
                         'N = 100', '',
                         'def linear(x, m c):',
                         '    return m*x + c', '',
                         'x, y = create_data_from_function(times[0],'
                         ' times[1], '
                         '(times[-1] - times[0])/N, [1.2, -2.1], '
                         'linear, seed=1)',
                         'data.add_sample_log("Fake log", x, y)'])]
