from MuonDataLib.data.utils import NONE
from MuonDataLib.cython_ext.stats import make_histogram
from MuonDataLib.cython_ext.filter import (
                                           get_indices,
                                           rm_overlaps,
                                           good_periods,
                                           good_values_ints,
                                           good_values_double)
import numpy as np
import time
cimport numpy as cnp
import cython
cnp.import_array()


cdef double ns_to_s = 1.e-9


"""
These need to be classes to pass function argument
in Cython
The below are not tested directly, in the interest
of run time speed (the function classes are
not exposed to Python).

Need to be in the
same file as they used in order to use type defs.
Need to use
https://docs.cython.org/en/latest/src/userguide/sharing_declarations.html
to split into multiple files (not got time)
"""
cdef class cf:
    """
    Simple class for comparing values
    """
    cdef cf(self, min_filter, max_filter, status, y, greater, less):
        raise NotImplementedError()

cdef class cf_band(cf):
    cdef cf(self, min_filter, max_filter, status, y, greater, less):
        """
        For checking if a data point is within a band of accepted values
        :param min_filter: the min accepted y value
        :param max_filter: the max accepted y value
        :param status: if the data is being removed
        :param y: the y value being considered
        :param greater: the comparison method
        :param less: the comparion method
        """
        return (keep_data(min_filter, status, y, greater) and
                keep_data(max_filter, status, y, less))

cdef class cf_max(cf):
    cdef cf(self, min_filter, max_filter, status, y, greater, less):
        """
        For checking if a data point is below a max accepted value
        :param min_filter: the min accepted y value - not used
        :param max_filter: the max accepted y value
        :param status: if the data is being removed
        :param y: the y value being considered
        :param greater: the comparison method - not used
        :param less: the comparion method
        """
        return keep_data(max_filter, status, y, less)

cdef class cf_min(cf):
    cdef cf(self, min_filter, max_filter, status, y, greater, less):
        """
        For checking if a data point is below an accepted value
        :param min_filter: the min accepted y value
        :param max_filter: the max accepted y value - not used
        :param status: if the data is being removed
        :param y: the y value being considered
        :param greater: the comparison method
        :param less: the comparion method - not used
        """
        return keep_data(min_filter, status, y, greater)


cdef class Func:
    """
    compares a pair of values
    Need this as sometimes the comparison are flipped
    when doing the checks. So want a unified interface
    """
    cdef compare(self, double threshold, double y):
        raise NotImplementedError()

cdef class cf_less(Func):
    cdef compare(self, double threshold, double y):
        """
        Is y < threshold
        :param threshold: the threshold value
        :param y: the y value
        :return: a bool of is y < threshold
        """
        return y < threshold

cdef class cf_greater(Func):
    cdef compare(self, double threshold, double y):
        """
        Is y > threshold
        :param threshold: the threshold value
        :param y: the y value
        :return: a bool of is y > threshold
        """
        return y > threshold

cdef remove_data(double threshold, status, double y, Func cf):
    """
    Checks if the data should be removed
    :param threshold: the threshold value
    :param status: it data is currently being removed
    :param y: the y value being considered
    :param cf: the comparison function to use
    :return: a bool of if the y data point is to be removed
    """
    return threshold != NONE and not status and cf.compare(threshold, y)

cdef keep_data(double threshold, status, double y, Func cf):
    """
    Checks if the data should be kept
    :param threshold: the threshold value
    :param status: it data is currently being removed
    :param y: the y value being considered
    :param cf: the comparison function to use
    :return: a bool of if the y data point is to be kept
    """
    return threshold != NONE and status and cf.compare(threshold, y)


cdef class Events:
    """
    Class for storing event information
    """
    cdef public int [:] IDs
    cdef public int [:] periods
    cdef public double[:] times
    cdef readonly int N_spec
    cdef public int[:] start_index_list
    cdef public int[:] end_index_list
    cdef readonly dict[str, double] filter_start
    cdef readonly dict[str, double] filter_end
    cdef readonly double[:] frame_start_time
    cdef readonly dict[str, double] peak_prop
    cdef readonly dict[str, double] threshold


    def __init__(self,
                 cnp.ndarray[int] IDs,
                 cnp.ndarray[double] times,
                 cnp.ndarray[int] start_i,
                 cnp.ndarray[double] frame_start,
                 int N_det,
                 cnp.ndarray[int] periods,
                 cnp.ndarray[double] amps,
                 ):
        """
        Creates an event object.
        This knows everything needed for the events to create a histogram.
        :param IDs: the detector ID's for the events
        :param times: the time stamps for the events, relative to the start of their frame
        :param start_i: the first event index for each frame
        :param frame_start: the start time for the frames
        :param N_det: the number of detectors
        :param periods: a vector of the periods for each frame
        :param amps: a vector of the amplitudes for each event
        """
        self.IDs = IDs
        self.N_spec = N_det
        self.times = times
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:], np.int32(len(IDs)))
        self.frame_start_time = frame_start
        self.filter_start = {}
        self.filter_end = {}
        self.periods = periods
        self.peak_prop = {'Amplitudes': amps}
        self.clear_thresholds()

    def get_peak_property_histogram(self, str name):
        """
        A method to inspect the data (e.g. Ampltiudes),
        which describes the properties of the event
        peaks. 
        :param name: the name of the property
        :returns: the histogram of the requested property,
        and the bin edges.
        """
        return np.histogram(self.peak_prop[name])

    def clear_thresholds(self):
        """
        A method to reset all of the filters 
        on the peak properties.
        """
        self.threshold = {"Amplitudes": 0.0}


    def set_threshold(self, str name, double value):
        """
        A method to set the filter/threshold for 
        a peak property. 
        :param name: the name of the property
        :param value: the value for the threshold/filter.
        """
        self.threshold[name] = value

    def get_threshold(self, str name):
        """
        A method to get the value of the threshold/filter
        for a peak property.
        :param name: the name of the property
        :returns: the value of the filter/threshold.
        """
        return self.threshold[name]

    def get_start_times(self):
        """
        Get the frame start times (stored in ns)
        :returns: the frame start times in seconds
        """
        return np.asarray(self.frame_start_time)

    def _get_filters(self):
        """
        A method to get the filters for testing
        :returns: the filter dicts
        """
        return self.filter_start, self.filter_end

    @cython.boundscheck(False)  # Deactivate bounds checking
    @cython.wraparound(False)   # Deactivate negative indexing.
    cpdef apply_log_filter(self, str name, double[:] x, double[:] y, double min_filter, double max_filter):
        """
        A method for extracting the filters from the logs.
        :param name: the name of the log to filter against
        :param x: the x values for the log
        :param y: the y values for the log
        :param min_filter: the min accepted y value
        :param max_filter: the max accepted y value
        """

        cdef cf compare
        if min_filter == NONE and max_filter == NONE:
            return [], [], [], []
        elif min_filter == NONE:
            compare = cf_max()
        elif max_filter == NONE:
            compare = cf_min()
        else:
            compare = cf_band()
        status = False

        cdef Py_ssize_t j, N
        N = 0
        cdef cnp.ndarray[int] start = np.zeros(len(x), dtype=np.int32)
        cdef cnp.ndarray[int] stop = np.zeros(len(x), dtype=np.int32)

        if (min_filter is not NONE and y[0] < min_filter or
            max_filter is not NONE and y[0] > max_filter):
            status = True
            start[0] = 0

        cdef cf_less less = cf_less()
        cdef cf_greater greater = cf_greater()

        for j in range(1, len(y)):
            if (remove_data(min_filter, status, y[j], less) or
                remove_data(max_filter, status, y[j], greater)):
                status = True
                # since it crosses before the current value
                start[N] = j-1
            elif compare.cf(min_filter, max_filter, status, y[j], greater, less):
                status = False
                stop[N] = j
                N += 1

        # if its on, turn it off
        if status:
            stop[N] = len(y) - 1
            N += 1

        if start[0] == 0:
            """
            This does cause a warning, but makes sure that the
            first event is excluded.
            """
            self.add_filter(f'{name}_0', 0,
                            x[stop[0]]/ns_to_s)
        else:
            self.add_filter(f'{name}_0', x[start[0]]/ns_to_s,
                            x[stop[0]]/ns_to_s)

        for j in range(1, N):
            self.add_filter(f'{name}_{j}', x[start[j]]/ns_to_s,
                            x[stop[j]]/ns_to_s)

    def add_filter(self, str name, double start, double end):
        """
        Adds a time filter to the events
        The times are in the same units as the stored events
        :param name: the name of the filter
        :param start: the start time for the filter
        :param end: the end time for the filter
        """
        if name in self.filter_start.keys():
            raise RuntimeError(f'The filter {name} already exists')
        self.filter_start[name] = start
        self.filter_end[name] = end

    def remove_filter(self, str name):
        """
        Remove a time filter from the events
        :param name: the name of the filter to remove
        """
        if name not in self.filter_start.keys():
            raise RuntimeError(f'The filter {name} does not exist')
        del self.filter_start[name]
        del self.filter_end[name]

    def clear_filters(self):
        """
        A method to clear all of the time filters
        """
        self.filter_start.clear()
        self.filter_end.clear()

    def report_filters(self):
        """
        A simple method to create a more readable form for the
        user to inspect.
        :return: a dict of the filters, with start and end values.
        """
        data = {}
        for key in self.filter_start.keys():
            data[key] = (self.filter_start[key], self.filter_end[key])
        return data

    @property
    def get_total_frames(self):
        """
        :return: The original number of frames in each period
        """
        _, frames = np.unique(self.periods, return_counts=True)
        return np.asarray(frames, dtype=np.int32)

    def _get_filtered_data(self, frame_times):
        """
        A method to get the information about the applied filters.
        This includes the list of events after the filter has been applied,
        the number of removed frames and the indices for the filters.
        :param frame_times: the times for the start of each frame (in seconds).
        The number of removed frames. The list of filtered detector IDs and
        event time stamps. The list of periods for the kept events and
        the amplitudes of the kept events.
        """

        cdef int[:] IDs, f_i_start, f_i_end
        cdef int[:] periods
        cdef int[:] rm_frames = np.zeros(np.max(self.periods) + 1, dtype=np.int32)
        cdef double[:] times, f_start, f_end, amps

        if len(self.filter_start.keys())>0:
            # sort the filter data
            f_start = np.sort(np.asarray(list(self.filter_start.values()), dtype=np.double), kind='quicksort')
            f_end = np.sort(np.asarray(list(self.filter_end.values()), dtype=np.double), kind='quicksort')

            # calculate the frames that are excluded by the filter
            f_i_start, f_i_end = get_indices(frame_times,
                                             ns_to_s*np.asarray(f_start),
                                             ns_to_s*np.asarray(f_end),
                                             'frame start time',
                                             'seconds')
            f_i_start, f_i_end, rm_frames = rm_overlaps(f_i_start, f_i_end, self.periods)
            # remove the filtered data from the event lists
            IDs = good_values_ints(f_i_start, f_i_end, self.start_index_list, self.IDs)
            times = good_values_double(f_i_start, f_i_end, self.start_index_list, self.times)
            amps = good_values_double(f_i_start, f_i_end, self.start_index_list,
                                      self.peak_prop['Amplitudes'])

            if len(times) == 0:
                raise ValueError("The current filter selection results in zero data "
                                 "for the histograms. Aborting histogram generation.")
        else:
            # no filters
            IDs = self.IDs
            times = self.times
            amps = self.peak_prop['Amplitudes']
            f_i_start = np.asarray([], dtype=np.int32)
            f_i_end = np.asarray([], dtype=np.int32)
        # get the periods for each event
        periods = good_periods(f_i_start, f_i_end, self.start_index_list, self.periods, len(self.times))
        return f_i_start, f_i_end, rm_frames, IDs, times, periods, amps

    def histogram(self,
                  double min_time=0.,
                  double max_time=32.768,
                  double width=0.016,
                  cache=None,
                  ):
        """
        Create a matrix of histograms from the event data
        and apply any filters that might be present (including
        those from peak properties).
        :param min_time: the start time for the histogram
        :param max_time: the end time for the histogram
        :param width: the bin width for the histogram
        :param cache: the cache of event data histograms
        :returns: a matrix of histograms, bin edges
        """
        cdef int[:] IDs, f_i_start, f_i_end, periods
        cdef int[:] rm_frames
        cdef double[:] times

        cdef double[:] frame_times = ns_to_s*np.asarray(self.get_start_times())

        f_i_start, f_i_end, rm_frames, IDs, times, periods, amps = self._get_filtered_data(frame_times)

        cdef int[:] weight = np.array(np.where(amps > np.double(self.threshold['Amplitudes']), 1., 0.),
                                      dtype=np.int32)

        hist, bins, N = make_histogram(times=times,
                                       spec=IDs,
                                       N_spec=self.N_spec,
                                       periods=periods,
                                       min_time=min_time,
                                       max_time=max_time,
                                       width=width,
                                       weight=weight)
        if cache is not None:

            first_time, last_time = self._start_and_end_times(frame_times,
                                                              f_i_start,
                                                              f_i_end)
            cache.save(hist, bins,
                       rm_frames,
                       veto_frames=np.zeros(len(rm_frames), dtype=np.int32),
                       first_time=first_time,
                       last_time=last_time,
                       resolution=width,
                       N_events=N)

        return hist, bins

    @staticmethod
    def _start_and_end_times(double[:] frame_times,
                             int[:] f_i_start,
                             int[:] f_i_end):
        """
        A method to get the start and end time for the filtered
        data. Each frame at best contains about 20ms of events
        and these will always be at the start of the frame.
        So if the beam goes down, the next frame could be an hour
        later but the events will all be within the
        first 20ms of the frame. Therefore,
        we can estimate the end time by using the time passed
        between the start time and the time stamp for the start
        of the last frame. Since the 20ms will make little
        difference to the end tiime as a first order approximation
        (we only record to an accuracy of seconds). The start time
        is from the first frame that is included in the filtered
        data.
        :param frame_times: the timestamps for the start of the
        frames.
        :param f_i_start: the list of indices for the start
        of the filters.
        :param f_i_end: the list of indices for the end
        of the filters
        :returns: the start and end times for the filtered data
        """
        cdef double first_time, last_time
        # no filters
        if len(f_i_start) == 0:
            return frame_times[0], frame_times[-1]

        if f_i_start[0] > 0:
            # if first filter is after first frame
            first_time = frame_times[0]
        else:
            # the first filter includes first frame
            first_time = frame_times[f_i_end[0] + 1]

        if f_i_end[-1] < len(frame_times)-1:
            # if the last filter is before the last frame
            last_time = frame_times[-1]
        else:
            """
            If the last filter includes the last frame.
            Want to get the time of the frame just
            before the last filter starts.
            Hence, f_i_start[-1] - 1.
            """
            last_time = frame_times[f_i_start[-1] - 1]
        return first_time, last_time

    @property
    def get_N_spec(self):
        """
        :return: the number of spectra/detectors
        """
        return self.N_spec

    @property
    def get_N_events(self):
        """
        :return: the number of spectra/detectors
        """
        return len(self.IDs)

