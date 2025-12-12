from MuonDataLib.data.sample import Sample
from MuonDataLib.data.raw_data import (EventsRawData,
                                       read_raw_data_from_events)
from MuonDataLib.data.source import Source
from MuonDataLib.data.user import User
from MuonDataLib.data.periods import EventsPeriods
from MuonDataLib.data.detector1 import EventsDetector_1 as Det1
from MuonDataLib.data.muon_data import MuonEventData
from MuonDataLib.cython_ext.load_events import load_data
from MuonDataLib.cython_ext.events_cache import EventsCache

import h5py
import numpy as np


def load_log_data(log, key, data):
    """
    A method to loop over the sample logs and save them.
    This exists to check that the sample log data is a
    vector of doubles. Otherwise the rest of the algorithms
    will fail at present.
    :param log: the file object, pointing at the specific sample log data
    param key: the name of the specific sample log
    :param data: the muon data object
    """
    x = log['value_log']['time'][:]
    if isinstance(x[0], np.float32):
        y = log['value_log']['value'][:]
        data.add_sample_log(key,
                            np.asarray(x, dtype=np.double),
                            np.asarray(y, dtype=np.double))


def load_logs(log, data):
    """
    A method to loop over the sample logs and save them
    :param log: the file object, pointing at the sample log data
    :param data: the muon data object
    """
    for key in log.keys():
        tmp = log[key]
        load_log_data(tmp, key, data)


def load_events(file_name, N):
    """
    Load muon event nxs file (ISIS)
    with error handling
    :param file_name: the name of the file to load
    :param N: the number of detectors
    :return: a MuonEventData object
    """
    try:
        return _load_events(file_name, N)
    except Exception:
        msg = f"The file {file_name} cannot be read"
        raise RuntimeError(msg)


def _load_events(file_name, N):
    """
    Load muon event nxs file (ISIS)
    :param file_name: the name of the file to load
    :param N: the number of detectors
    :return: a MuonEventData object
    """
    with h5py.File(file_name, 'r') as file:
        raw_args, start_time = read_raw_data_from_events(file)
        tmp = file.require_group('raw_data_1')
        p_group = tmp.require_group('periods')
        p_type = p_group['type'][:]

        # store data in objects
        _, events = load_data(file_name, N)
        cache = EventsCache(start_time,
                            events.get_total_frames)

        raw_data = EventsRawData(cache,
                                 *raw_args)

        sample = Sample('sample ID: test',
                        1.1,
                        2.2,
                        3.3,
                        4.4,
                        5.5,
                        'sample name: test')

        source = Source('ISIS',
                        'Probe',
                        'Pulsed')

        user = User('user name: RAL',
                    'affiliation: test')

        periods = EventsPeriods(cache,
                                1,
                                'label test',
                                p_type,
                                [0])

        detector1 = Det1(cache,
                         0.016,
                         np.arange(1, N + 1, dtype=np.int32),
                         'HIFI test',
                         0.0,
                         0.0,
                         32.0)

        data = MuonEventData(events,
                             cache,
                             sample=sample,
                             raw_data=raw_data,
                             source=source,
                             user=user,
                             periods=periods,
                             detector1=detector1)

        if 'selog' in tmp.keys():
            log = tmp['selog']
            load_logs(log, data)

    return data
