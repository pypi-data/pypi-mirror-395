from MuonDataLib.cython_ext.event_data import Events

import h5py
import numpy as np
import time
cimport numpy as cnp
import cython
cnp.import_array()


def _load_data(file_name):
        """
        Loads event data from the event nxs file.
        This should make it easier to swap out later.
        :param file_name: the name of the file to load.
        :return: IDs, first index for frame, time stamps,
        amplitudes, time at the start of the frame,
        list of the period each frame belongs to
        """

        with h5py.File(file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1_events')

            N = tmp['event_id'].len()

            IDs = np.zeros(N, dtype=np.int32)
            times = np.zeros(N, dtype=np.double)
            amps = np.zeros(N, dtype=np.double)

            M = tmp['event_index'].len()
            start_j = np.zeros(M, dtype=np.int32)
            start_t = np.zeros(M, dtype=np.double)
            periods = np.zeros(M, dtype=np.int32)

            tmp['event_id'].read_direct(IDs)
            tmp['event_time_offset'].read_direct(times)
            tmp['pulse_height'].read_direct(amps)
            tmp['event_index'].read_direct(start_j)
            tmp['event_time_zero'].read_direct(start_t)

            if 'period_number' in tmp.keys():
                tmp['period_number'].read_direct(periods)
        return IDs, start_j, times, amps, start_t, periods

def load_data(file_name, N_det):
        """
        Loads the data from an event nxs file
        :param file_name: the name of the event nxs file to load
        :param N_det: the number of detectors
        :return: the time to run this method, the total number of events
        """
        start = time.time()
        IDs, frames, times, amps, frame_times, periods = _load_data(file_name)
        events = Events(IDs, times, frames, frame_times, N_det, periods, amps)
        return time.time() - start, events


