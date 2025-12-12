from MuonDataLib.cython_ext.filter import apply_filter
from MuonDataLib.data.utils import NONE
from MuonDataLib.data.hdf5 import (HDF5,
                                   is_list,
                                   is_int,
                                   is_float)
import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


cdef class LogData:
    cdef readonly double[:] x
    cdef readonly double[:] y
    cdef readonly double[:] fx
    cdef readonly double[:] fy
    cdef readonly str _name
    cdef readonly double _min
    cdef readonly double _max

    def __init__(self, double[:] x, double[:] y):
        """
        A class to hold information about sample logs.
        This includes the filters for that specific
        log.
        NONE is a double that is used to signal
        a none value
        :param x: the x values (assume time is seconds)
        :param y: the corresponding y values
        """
        self.x = x
        self.y = y
        self.clear_filters()

    cpdef clear_filters(self):
        """
        Clears the filters applied to the sample log
        """
        self.fx = np.asarray([], dtype=np.double)
        self.fy = np.asarray([], dtype=np.double)
        self._name = ''
        self._max = NONE
        self._min = NONE

    cpdef add_filter(self, str name, double min_value=NONE, double max_value=NONE):
        """
        Adds a filter to a sample log
        :param name: the name of the filter
        :param min_value: the minimum accepted value (i.e. remove data below it)
        :param max_value: the maximum accepted value (i.e. remove data above it)
        """
        self._name = name
        self._min = min_value
        self._max = max_value

    cpdef get_filter(self):
        """
        Gets useful information about the filter
        :returns: name of the filter, original x, original y,
        min value and max value.
        """
        return self._name, self.x, self.y, self._min, self._max

    cpdef set_filter_values(self, double[:] fx, double [:] fy):
        """
        Stores the filtered values
        :param fx: the filtered x values
        :param fy: the filtered y values
        """
        self.fx = fx
        self.fy = fy

    cpdef get_original_values(self):
        """
        :returns: the unfiltered x and y values.
        """
        return (np.asarray(self.x, dtype=np.double),
                np.asarray(self.y, dtype=np.double))

    cpdef get_values(self):
        """
        Gets the x and y values for the sample log.
        If a filtered data is present, then it will
        return filtered data. Otherwise its the
        original values
        :returns: the x and y values for the sample log
        """
        if len(self.fx) > 0:
            return (np.asarray(self.fx, dtype=np.double),
                    np.asarray(self.fy, dtype=np.double))
        else:
            return self.get_original_values()

cdef class BaseSampleLogs:
    """
    A simple class to store the sample log information
    needed for a muon nexus v2 file
    Assume vector data
    """
    cdef readonly dict[str, str] _look_up
    cdef readonly dict[str, LogData] _float_dict
    cdef readonly dict[str, LogData] _int_dict

    def __init__(self):
        """
        Create an empty set of sample logs
        Will store floats, ints etc. seperate
        to make saving easier.
        The look up is to identify which dict
        a given sample log belongs too.
        """
        self._float_dict = {}
        self._int_dict = {}
        self._look_up = {}

    cpdef add_sample_log(self, str name, x_data, y_data):
        """
        Adds a sample log
        :parma name: the name of the sample log
        :param x_data: the x values
        :param y_data: the y values
        """
        if name in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} "
                               "already exists in the sample logs")
        if is_list(y_data):
            y = y_data[0]
            if is_int(y):
                self._int_dict[name] = LogData(x_data, y_data)
                self._look_up[name] = 'int'
                return
            elif is_float(y):
                self._float_dict[name] = LogData(x_data, y_data)
                self._look_up[name] = 'float'
                return
        raise RuntimeError(f"The sample log {name} is "
                           "not currently supported")

    cpdef get_sample_log(self, str name):
        """
        :param name: the sample log requested
        :return: the sample log object requested
        """
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does"
                               "not exist in the sample logs")
        cdef str dtype = self._look_up[name]
        if dtype == 'int':
            return self._int_dict[name]
        elif dtype == 'float':
            return self._float_dict[name]

    cpdef clear(self):
        """
        Removes all sample logs
        """
        self._float_dict.clear()
        self._int_dict.clear()
        self._look_up.clear()

    cpdef get_names(self):
        """
        :return: gets the names of all of the
        sample logs stored.
        """
        return list(self._look_up.keys())

    @cython.boundscheck(False)  # Deactivate bounds checking
    @cython.wraparound(False)   # Deactivate negative indexing.
    cpdef apply_filter(self, double[:, :] times):
        """
        Applies the sane filter to the all of the sample logs.
        :param times: A list of the pairs (as a list) of the
        times to remove from the data.
        """
        cdef double[:] x, y
        cdef str name
        for name in self._look_up.keys():
            dtype = self._look_up[name]
            if dtype == 'int':
                x, y = self._int_dict[name].get_original_values()
            elif dtype == 'float':
                x, y = self._float_dict[name].get_original_values()
                self._float_dict[name].set_filter_values(*apply_filter(x,
                                                                       y,
                                                                       times))

    cpdef add_filter(self, str name, min_value, max_value):
        """
        Adds a filter to a sample log.
        :param name: the name of the sample log
        :param nim_value: the minimum value for the filter in y
        :param max_value: the maximum value for the filter in x
        """
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does not "
                               "exist in the sample logs")
        cdef str dtype = self._look_up[name]
        if dtype == 'int':
            self._int_dict[name].add_filter(name+'_filter',
                                            min_value, max_value)
        elif dtype == 'float':
            self._float_dict[name].add_filter(name+'_filter',
                                              min_value, max_value)

    cpdef get_filter(self, str name):
        """
        Gets useful information about a given filter
        :param name: the name of the filter to get info for.
        :returns: name of the filter, original x, original y,
        min value and max value.
        """
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does "
                               "not exist in the sample logs")
        cdef str dtype = self._look_up[name]
        if dtype == 'int':
            return self._int_dict[name].get_filter()
        elif dtype == 'float':
            return self._float_dict[name].get_filter()

    cpdef clear_filter(self, name):
        self._float_dict[name].clear_filters()

    @cython.boundscheck(False)  # Deactivate bounds checking
    @cython.wraparound(False)   # Deactivate negative indexing.
    cpdef clear_filters(self):
        """
        Clears all of the filters from all of the sample
        logs.
        """
        cdef str name
        for name in self._float_dict.keys():
            self._float_dict[name].clear_filters()
