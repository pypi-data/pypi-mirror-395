from MuonDataLib.help.help_docs import (Doc,
                                        NXS,
                                        LOAD,
                                        MUONDATA)


def get_load_docs():
    return [Doc('load_events',
                'data.loader.load_events',
                [LOAD, MUONDATA, NXS],
                "A method to load a muon event NeXus file "
                "into a MuonData object",
                param={'file_name': "The name of the event NeXus "
                       "file to read.",
                       "N": "The number of expected spectra for the file."},
                returns='A MuonData object, containing the data from '
                        'the NeXus file',
                example=['from MuonDataLib.data.loader.load_events import '
                         'load_events',
                         'data = load_events("HIFI00001.nxs", 64)'])]
