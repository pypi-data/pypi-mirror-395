import numpy as np
cimport numpy as cnp
import cython
cimport cpython.datetime as dt
cnp.import_array()


cdef class EventsCache:
    """
    A simple class for caching the event data into histograms

    *********************************************************
    WARNING:

    This class may not take multi period data into account
    beyond allowing unit tests to pass
    *********************************************************

    """
    cdef readonly int[:, :, :] histograms
    cdef readonly double[:] bins
    cdef readonly int[:] N_event_frames
    cdef readonly int[:] N_filter_frames
    cdef readonly int[:] N_veto_frames
    cdef readonly dt.datetime start_time
    cdef readonly dt.datetime first_good_time
    cdef readonly dt.datetime last_good_time
    cdef readonly double resolution
    cdef readonly int N_events

    def __init__(self, dt.datetime start_time, int[:] event_frames):
        """
        Create an empty cache
        """
        self.N_event_frames = event_frames
        self.start_time = start_time
        self.clear()

    def clear(self):
        """
        Clear all data from the cache
        """
        self.histograms = None
        self.bins = None
        self.N_events = 0
        self.resolution = 0.016
        self.N_filter_frames = np.asarray([], dtype=np.int32)
        self.N_veto_frames = np.asarray([], dtype=np.int32)
        self.first_good_time = dt.datetime(2000, 1, 1, 1, 1, 1)
        self.last_good_time = dt.datetime(2000, 1, 1, 1, 1, 1)

    def save(self,
            int[:, :, :] histograms,
            double[:] bins,
            int[:] filter_frames,
            int[:] veto_frames,
            double first_time,
            double last_time,
            double resolution,
            int N_events):
        """
        Store data in the cache
        :param histograms: the histogram data (periods, N_det, bin)
        :param bins: the histogram bins
        :param filter_frames: the number of frames removed by filter
        (at present doesnt account for multiperiod data)
        :param veto_frames: the number of frames removed by veto
        (at present doesnt account for multiperiod data)
        :param fist_time: the time (s) for the first good frame
        :param last_time: the last frame start time
        :param resolution: the resolution of the histogram (bin width)
        :param N_events: the number of events in the histogram
        """
        N = len(self.N_event_frames)
        if len(filter_frames) != N or len(veto_frames) != N:
            raise RuntimeError("The list of frames does not match")
        self.histograms = histograms
        self.bins = bins
        self.N_filter_frames = filter_frames
        self.N_veto_frames = veto_frames
        self.N_events = N_events
        self.first_good_time = self.start_time + dt.timedelta(seconds=first_time)
        self.last_good_time = self.start_time + dt.timedelta(seconds=last_time)

        self.resolution = resolution

    @property
    def get_N_events(self):
        """
        :return: the number of events in the histogram
        """
        return int(self.N_events)

    def get_histograms(self):
        """
        :return: the stored histograms and bins
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get histograms")
        return np.asarray(self.histograms), np.asarray(self.bins)

    def frame_check(self):
        """
        Check that the cache has data, if not return error
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get frames")

    def get_resolution(self):
        """
        :return: the resolution of the histogram
        """
        return self.resolution

    @property
    def _discarded_good_frames(self):
        """
        :return: the number of discarded good frames (filtered + veto)
        """
        return np.asarray(self.N_filter_frames) + np.asarray(self.N_veto_frames)

    @property
    def get_discarded_raw_frames(self):
        """
        :return: the number of discarded raw frames (filtered)
        """
        self.frame_check()
        return np.asarray(self.N_filter_frames)

    @property
    def get_good_frames(self):
        """
        :return: the number of good frames
        """
        self.frame_check()
        return np.asarray(self.N_event_frames) - self._discarded_good_frames

    @property
    def get_raw_frames(self):
        """
        :return: the number of raw frames
        """
        self.frame_check()
        return np.asarray(self.N_event_frames) - self.get_discarded_raw_frames

    def empty(self):
        """
        Check if the cache is empty
        :return: if the cache is empty as a bool
        """
        if len(self.N_filter_frames)==0:
            return True
        return False

    @property
    def get_start_time(self):
        """
        :return: the date time for the first good frame
        """
        return self.first_good_time

    @property
    def get_end_time(self):
        """
        :return: the date time for the last good frame start (approx)
        """
        return self.last_good_time

    @property
    def get_duration(self):
        """
        :return: the total amount of time between the first and last good frame
        including down time from the beam
        """
        duration = self.last_good_time - self.first_good_time
        return duration.total_seconds()

    @property
    def get_count_duration(self):
        """
        Time we expect the experiment to have run given the filters and vetos.
        At ISIS expect 4 pulses over 100 ms.
        good frames * (100 ms)/4 then convert to seconds

        :return: the duration of the experiment, while on, in seconds
        """
        self.frame_check()
        return self.get_good_frames*0.025
