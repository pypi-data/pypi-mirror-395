from MuonDataLib.data.utils import (INT32, UINT32,
                                    FLOAT32,
                                    stype)

import numpy as np


def is_list(values):
    return isinstance(values, np.ndarray) or isinstance(values, list)


def is_int(value):
    return (isinstance(value, int) or
            isinstance(value, INT32) or
            isinstance(value, UINT32))


def is_float(value):
    return isinstance(value, float) or isinstance(value, FLOAT32)


def is_string(value):
    return isinstance(value, str)


class HDF5(object):
    """
    A wrapper object to make it easier to write
    muon nexus v2 files
    """
    def __init__(self):
        """
        Create an empty dict of values
        """
        self._dict = {}

    def save_str(self, name, string, group):
        """
        Save a string to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param string: the string to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if isinstance(string, str):
            dtype = stype(string)
            return group.require_dataset(name=name,
                                         shape=(1),
                                         data=np.array([string.encode()],
                                                       dtype=dtype),
                                         dtype=dtype)
        else:
            raise ValueError(f'{string} is not a string')

    def save_float(self, name, value, group):
        """
        Save a float value to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param value: the float value to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if is_float(value):
            return group.require_dataset(name=name,
                                         shape=(1),
                                         data=[value],
                                         dtype=FLOAT32)
        else:
            raise ValueError(f'{value} is a {type(value)}, not a float')

    def save_int(self, name, value, group):
        """
        Save an int value to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param value: the int to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if is_int(value):
            return group.require_dataset(name=name,
                                         shape=(1),
                                         data=[value],
                                         dtype=INT32)
        else:
            raise ValueError(f'{value} is a {type(value)}, not an integer')

    def save_int_array(self, name, values, group):
        """
        Save an array of ints to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param values: the int values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if is_list(values) and is_int(values[0]):
            return group.require_dataset(name=name,
                                         shape=len(values),
                                         data=values,
                                         dtype=INT32)
        else:
            raise ValueError(f'{values} is a {type(values)}, '
                             'not a list of ints')

    def save_float_array(self, name, values, group):
        """
        Save an array of float values to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param values: the float values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if is_list(values) and is_float(values[0]):
            return group.require_dataset(name=name,
                                         shape=len(values),
                                         data=values,
                                         dtype=FLOAT32)
        else:
            raise ValueError(f'{values} is a {type(values)}, '
                             'not a list of floats')

    def save_counts_array(self, name, N_periods, N_hist, N_x, values, group):
        """
        Save the counts array to the relevant part of the nexus file
        The counts are (period #, spec #, time values)
        It is not practical to test every value, so just do the first.
        :param name: the name used to reference the value in the file
        :param N_periods: the number of periods
        :param N_hist: the number of histograms
        :param N_x: the number of x (time) values
        :param values: the count values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        if len(values) != N_periods:
            raise ValueError(f'The length of counts is {len(values)} '
                             'and should be of length {N_periods}')

        elif len(values[0]) != N_hist:
            raise ValueError(f'The number of spectra is {len(values[0])} '
                             'and should be {N_hist}')

        elif len(values[0][0]) != N_x:
            raise ValueError(f'The length of x data is {len(values[0][0])} '
                             'and should be of length {N_x}')

        elif is_int(values[0][0][0]):
            return group.require_dataset(name=name,
                                         shape=(N_periods, N_hist, N_x),
                                         data=values,
                                         dtype=INT32)
        else:
            raise ValueError('Should contain integers in count data, '
                             f'not {type(values[0][0][0])}')
