import h5py
from MuonDataLib.data.sample_logs import SampleLogs
from MuonDataLib.data.utils import NONE
import numpy as np
import json


class MuonData(object):
    """
    A class to store all of the information needed for muon data
    """
    def __init__(self, sample, raw_data, source, user, periods, detector1):
        """
        Creates a store for relevant muon data (defined by nxs v2)
        :param sample: the Sample data needed for nexus v2 file
        :param raw_data: the RawData data needed for nexus v2 file
        :param source: the Source data needed for nexus v2 file
        :param user: the User data needed for nexus v2 file
        :param periods: the Periods data needed for nexus v2 file
        :param detector1: the Detector1 data needed for nexus v2 file
        """
        self._dict = {}
        self._dict['raw_data'] = raw_data
        self._dict['sample'] = sample
        self._dict['source'] = source
        self._dict['user'] = user
        self._dict['periods'] = periods
        self._dict['detector_1'] = detector1

    def save_histograms(self, file_name):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        """
        file = h5py.File(file_name, 'w')
        for key in self._dict.keys():
            self._dict[key].save_nxs2(file)
        file.close()
        return


ns_to_s = 1.e-9


class MuonEventData(MuonData):
    def __init__(self, events, cache, sample, raw_data, source, user,
                 periods, detector1):
        """
        Creates a store for relevant muon data (defined by nxs v2)
        :param events: the event data
        :param cache: the cache for the event data
        :param sample: the Sample data needed for nexus v2 file
        :param raw_data: the RawData data needed for nexus v2 file
        :param source: the Source data needed for nexus v2 file
        :param user: the User data needed for nexus v2 file
        :param periods: the Periods data needed for nexus v2 file
        :param detector1: the Detector1 data needed for nexus v2 file
        """
        self._events = events
        self._cache = cache
        self._time_filter = {}
        self._keep_times = {}
        super().__init__(sample, raw_data, source, user, periods, detector1)
        self._dict['logs'] = SampleLogs()

    def _clear(self):
        """
        A method to make sure that the filters are removed.
        This is a little heavy handed, but we recalculate
        all of the filters anyway. So it makes no difference
        to the compute time. However, it does make sure that
        the filters behave as expected.
        """
        self._cache.clear()
        self._events.clear_filters()

    def _filter_remove_times(self):
        """
        A method for getting getting time filter values
        from the remove_data_time_between method
        """
        for name in self._time_filter.keys():
            start, end = self._time_filter[name]
            self._events.add_filter(name, start/ns_to_s, end/ns_to_s)

    def _filter_keep_times(self):
        """
        A method for getting the time filter values
        from the keep_data_time_between method.
        """

        start_times = []
        end_times = []
        for key in self._keep_times.keys():
            tmp = self._keep_times[key]
            start_times.append(tmp[0])
            end_times.append(tmp[1])

        start_times = np.sort(np.asarray(start_times), kind='quicksort')
        end_times = np.sort(np.asarray(end_times), kind='quicksort')

        N = len(start_times)
        if N > 0:
            data_end = self.get_frame_start_times()[-1] + 1.
            # remove from start (assume 0) to first window
            self._events.add_filter('keep_0', 0.0,
                                    start_times[0]/ns_to_s)
            for j in range(1, len(self._keep_times)):
                self._events.add_filter(f'keep_{j}',
                                        end_times[j-1]/ns_to_s,
                                        start_times[j]/ns_to_s)
            # dont use the real name as we have changed the order and
            # its only used internally
            self._events.add_filter(f'keep_{N}',
                                    end_times[-1]/ns_to_s,
                                    data_end/ns_to_s)

    def _filter_logs(self):
        """
        A method for getting the time filter values
        from the sample logs:
        - keep_data_sample_log_between
        - keep_data_sample_log_below
        - keep_data_sample_log_above
        """
        log_names = self._dict['logs'].get_names()
        for name in log_names:
            result = self._dict['logs'].get_filter(name)
            self._events.apply_log_filter(*result)

        # apply the filters from the logs
        filters = self._report_raw_filters().values()
        if not filters:
            return
        filter_times = list(filters)
        filter_times = np.asarray([np.asarray(filter_times[k],
                                              dtype=np.double)
                                   for k in range(len(filter_times))],
                                  dtype=np.double)
        self._dict['logs'].apply_filter(filter_times)

    def _filters(self):
        """
        A simple wrapper method for getting
        all of the possible time filters
        """
        self._filter_remove_times()
        self._filter_keep_times()
        self._filter_logs()

    def histogram(self, resolution=0.016):
        """
        A method for constructing a histogram.
        This will skip calculating the filters
        if the cache is occupied.
        If just the resolution has changed it will
        not alter the filtered values.
        :param resolution: the resolution of the
        histogram
        :return: the histograms and bins
        """
        is_cache_empty = self._cache.empty()

        if is_cache_empty:
            self._filters()

        if is_cache_empty or self._cache.get_resolution() != resolution:
            return self._events.histogram(width=resolution,
                                          cache=self._cache)
        return self._cache.get_histograms()

    def save_histograms(self, file_name, resolution=0.016):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        :param resolution: the resolution for the histogram
        """
        hist, _ = self.histogram(resolution)
        super().save_histograms(file_name)

    def clear_filters(self):
        """
        A method to remove all of the filters (including
        those for peak parameters)
        """
        self._clear()
        self._dict['logs'].clear_filters()
        self._time_filter.clear()
        self._keep_times = {}
        self._events.clear_thresholds()

    def add_sample_log(self, name, x_data, y_data):
        """
        A method to add a sample log
        :param name: the name of the sample log
        :param x_data: the x values (assumed to be time in seconds)
        :param y_data: the y values
        """
        self._clear()
        self._dict['logs'].add_sample_log(name, x_data, y_data)

    def _get_sample_log(self, name):
        """
        :param name: the name of the sample log
        :return: the requested sample log object
        """
        return self._dict['logs'].get_sample_log(name)

    def get_peak_property_histogram(self, name):
        """
        A method to get a histogram that shows the
        distribution for the values of a peak
        property.
        :param name: the name of the peak property
        :returns: histogram values (counts), bins
        """
        return self._events.get_peak_property_histogram(name)

    def keep_data_peak_property_above(self, name, value):
        """
        A method to add a filter on a peak property
        (e.g. Amplitudes)
        :param name: the name of the peak property
        :param value: the value for the filter
        """
        self._cache.clear()
        self._events.set_threshold(name, value)

    def delete_data_peak_property_above(self, name):
        """
        A method to remove a filter on a peak property.
        :param name: the name of the peak property.
        """
        self._cache.clear()
        self._events.set_threshold(name, 0)

    def keep_data_sample_log_below(self, log_name, max_value):
        """
        Sets a filter to remove data above a value
        :param log_name: the name of the log
        :param max_value: the value to remove data if its above it
        """
        self._clear()
        self._dict['logs'].add_filter(log_name, NONE, max_value)

    def keep_data_sample_log_above(self, log_name, min_value):
        """
        Sets a filter to remove data below a value
        :param log_name: the name of the log
        :param max_value: the value to remove data if its below it
        """
        self._clear()
        self._dict['logs'].add_filter(log_name, min_value, NONE)

    def keep_data_sample_log_between(self, log_name, min_value, max_value):
        """
        Sets a filter to remove data if its outside of the range
        :param log_name: the name of the log
        :param min_value: the kept data will be above this
        :param max_value: the kept data will be below this
        """
        if max_value <= min_value:
            raise RuntimeError("The max filter value is smaller "
                               "than the min value")
        self._clear()
        self._dict['logs'].add_filter(log_name, min_value, max_value)

    def only_keep_data_time_between(self, name, start, end):
        """
        Adds a filter that keeps data between given times
        :param times: a list of the start, end times (as a list)
        """
        if name in self._keep_times.keys():
            raise RuntimeError(f'The name {name} is already in use')
        elif start > end:
            error = (f'the start time {start} is after '
                     f'the end time {end}')
            raise RuntimeError(error)
        self._clear()
        self._keep_times[name] = [start, end]

    def remove_data_time_between(self, name, start, end):
        """
        A method to remove events between 2 time stamps.
        :param name: the name for the filter
        :param start: the time to start removing data from
        """
        if name in self._time_filter.keys():
            raise RuntimeError(f'The name {name} already exists')
        if start > end:
            raise RuntimeError('The start time is after the end time')
        self._clear()
        self._time_filter[name] = (start, end)

    def delete_sample_log_filter(self, name):
        """
        A method to remove a sample log filter,
        but not the sample log itself.
        :param name: the name of the sample log
        to remove the filter from
        """
        self._clear()
        self._dict['logs'].clear_filter(name)

    def delete_only_keep_data_time_between(self, name):
        """
        A method to remove the filters that
        define time bands to keep date within
        """
        if name not in self._keep_times.keys():
            raise RuntimeError(f'The name {name} is not present')
        self._clear()
        del self._keep_times[name]

    def delete_remove_data_time_between(self, name):
        """
        A method to remove a filter that defines a band
        of data to discard events from
        :param name: the name of the filter to remove
        """
        self._clear()
        del self._time_filter[name]

    def get_frame_start_times(self):
        """
        A method to get the frame start times
        :returns: the frame start times
        """
        return self._events.get_start_times()*ns_to_s

    def _report_raw_filters(self):
        """
        Gets the filters from the events
        :return: dict of filters in time
        """
        data = self._events.report_filters()
        for key in data.keys():
            data[key] = [x*ns_to_s for x in data[key]]
        return data

    def report_filters(self):
        """
        :returns: the applied filters as a structured dict
        """
        data = {}

        # peak filter
        data['peak_property'] = {'Amplitudes':
                                 self._events.get_threshold('Amplitudes')}

        # add sample logs
        tmp = {}
        for name in self._dict['logs'].get_names():
            result = self._dict['logs'].get_filter(name)
            if result[3] != NONE or result[4] != NONE:
                tmp[name] = [result[3], result[4]]
        data['sample_log_filters'] = tmp

        # add time filters
        data['time_filters'] = {'keep_filters': self._keep_times,
                                'remove_filters': self._time_filter}
        return data

    def load_filters(self, file_name):
        """
        A method to get filters from a json file.
        This will apply all of the filters from the file.
        :param file_name: the name of the json file
        """
        self._clear()
        with open(file_name, 'r') as file:
            data = json.load(file)
        tmp = data['time_filters']
        self._time_filter = tmp['remove_filters']

        tmp = tmp['keep_filters']
        self._keep_times = {}
        for key in tmp.keys():
            self._keep_times[key] = tmp[key]

        tmp = data['sample_log_filters']
        for name in tmp.keys():
            self._dict['logs'].add_filter(name, *tmp[name])

        tmp = data['peak_property']
        for name in tmp.keys():
            self._events.set_threshold(name, tmp[name])

    def save_filters(self, file_name):
        """
        A method to save the current filters to a file.
        :param file_name: the name of the json file to save to.
        """
        data = self.report_filters()
        with open(file_name, 'w') as file:
            json.dump(data, file, ensure_ascii=False,
                      sort_keys=True, indent=4)
