from MuonDataLib.data.utils import (INT32,
                                    stype)
from MuonDataLib.data.hdf5 import HDF5
import numpy as np


class _Detector_1(HDF5):
    """
    A base class for storing the data associated with the detector 1 group
    in a muon NXS v2 file.
    """
    def __init__(self, resolution, spec_i,
                 inst, t0, first, last):
        """
        Stores the data for the detector 1 group
        :param resolution: the time resolution (micro s)
        :param spec_i: the spectrum indices
        :param inst: the instrument name
        :param t0: the time zero value
        :param first: the first good bin
        :param last: the last good bin
        """
        super().__init__()
        self._dict['resolution'] = resolution
        self._dict['spectrum_index'] = spec_i
        self._dict['inst'] = inst
        self._dict['time_zero'] = t0
        self._dict['first_good'] = first
        self._dict['last_good'] = last

    @property
    def resolution(self):
        """
        Get the resolution in pico seconds
        :return the resolution in pico seconds
        """
        return int(self._dict['resolution']*1e6)

    def get_bin(self, value, offset=1,
                offset_bin_start=0):
        """
        A method to get the bin value from a time stamp.
        This can apply offsets for when the time stamp
        is part way into the bin or at the start of a bin.
        It is also used for t0 bin.
        :param value: the time stamp
        :param offset: if to use the next or previous bin, if the
        time stamp is in the middle of the bin
        :param offset_bin_start: the offset to use if the time
        stamp is on the left hand bin edge
        :returns: the bin value for the time stamp,
        such that it is complete good bin
        """
        # convert resolution to micro seconds
        res = self.resolution/1e6
        exact = value/res
        bin_value = int(value/res)
        if abs(exact - bin_value) > 1e-6:
            bin_value += offset
        else:
            bin_value += offset_bin_start
        return bin_value

    def get_time_zero_bin(self, value):
        """
        Gets the bin for the time zero.
        This just returns the bin that contains
        the time zero time stamp.
        :param value: the time stamp for time zero
        :returns: the bin for time zero
        """
        return self.get_bin(value,
                            offset=0,
                            offset_bin_start=0)

    def get_first_good_bin(self, value):
        """
        Gets the bin for first good.
        The first good bin is the first complete
        bin after the time stamp (value).
        :param value: the time stamp for first
        good.
        :returns: the first good bin
        """
        return self.get_bin(value,
                            offset=1,
                            offset_bin_start=0)

    def get_last_good_bin(self, value):
        """
        Gets the bin for last good.
        The last good bin is the last complete
        bin before the time stamp (value).
        Hence, if the time stamp is on the left
        hand bin edge, the previous bin is the last
        good bin.
        :param value: the time stamp for last
        good.
        :returns: the last good bin
        """
        return self.get_bin(value,
                            offset=-1,
                            offset_bin_start=-1)

    def save_nxs2(self, file,
                  raw_time,
                  counts,
                  N_x,
                  N_hist,
                  N_periods):
        """
        Save the detector 1 values for a muon NXS v2 file
        :param file: the open file to write the data to
        :param raw_time: the uncorrected time
        :param counts: the counts for the data (period, spec, time)
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('instrument')
        tmp.attrs['NX_class'] = 'NXinstrument'
        tmp = tmp.require_group('detector_1')
        tmp.attrs['NX_class'] = 'NXdetector'

        resolution = self.save_int('resolution', self.resolution, tmp)
        resolution.attrs.create('units', 'picoseconds'.encode(), dtype='S11')

        raw = self.save_float_array('raw_time', raw_time, tmp)
        raw.attrs.create('units', 'microseconds'.encode(), dtype='S12')
        raw.attrs.create('long_name', 'time'.encode(), dtype='S4')

        self.save_int_array('spectrum_index',
                            self._dict['spectrum_index'],
                            tmp)

        counts = self.save_counts_array('counts', N_periods,
                                        N_hist, N_x,
                                        counts, tmp)
        counts.attrs.create('axes',
                            ('[period index, '
                             'spectrum index, '
                             'raw time bin]').encode(),
                            dtype='S45')
        counts.attrs.create('long_name', self._dict['inst'].encode(),
                            dtype=stype(self._dict['inst']))

        t0_bin = self.get_time_zero_bin(self._dict['time_zero'])
        counts.attrs.create('t0_bin', t0_bin, dtype=INT32)

        first_bin = self.get_first_good_bin(self._dict['first_good'])
        counts.attrs.create('first_good_bin',
                            first_bin,
                            dtype=INT32)

        last_bin = self.get_last_good_bin(self._dict['last_good'])
        counts.attrs.create('last_good_bin',
                            last_bin,
                            dtype=INT32)


class Detector_1(_Detector_1):
    """
    A class for storing the data associated with the detector 1 group
    in a muon NXS v2 file.
    """
    def __init__(self, resolution, raw_time, spec_i,
                 counts, inst, t0, first, last):
        """
        Stores the data for the detector 1 group
        :param resolution: the time resolution (micro s)
        :param raw_time: the uncorrected time
        :param spec_i: the spectrum indices
        :param counts: the counts for the data (period, spec, time)
        :param inst: the instrument name
        :param t0: the time zero value
        :param first: the first good bin
        :param last: the last good bin
        """
        super().__init__(resolution, spec_i,
                         inst, t0, first, last)
        self._dict['raw_time'] = raw_time
        self._dict['counts'] = counts
        self.N_x = len(counts[0][0])
        self.N_hist = len(counts[0])
        self.N_periods = len(counts)

    def save_nxs2(self, file):
        """
        Save the detector 1 values for a muon NXS v2 file
        :param file: the open file to write the data to
        """
        super().save_nxs2(file,
                          self._dict['raw_time'],
                          self._dict['counts'],
                          self.N_x,
                          self.N_hist,
                          self.N_periods)


class EventsDetector_1(_Detector_1):
    """
    A class for storing the data associated with the detector 1 group
    in a muon NXS v2 file.
    """
    def __init__(self, events_cache, resolution, spec_i,
                 inst, t0, first, last):
        """
        Stores the data for the detector 1 group
        :param resolution: the time resolution (micro s)
        :param raw_time: the uncorrected time
        :param spec_i: the spectrum indices
        :param counts: the counts for the data (period, spec, time)
        :param inst: the instrument name
        :param t0: the time zero value
        :param first: the first good bin
        :param last: the last good bin
        """
        super().__init__(resolution, spec_i,
                         inst, t0, first, last)
        self._cache = events_cache

    @property
    def resolution(self):
        """
        Get the resolution in pico seconds
        :return the resolution in pico seconds
        """
        return np.int32(1e6*self._cache.get_resolution())

    def save_nxs2(self, file):
        """
        Save the detector 1 values for a muon NXS v2 file
        :param file: the open file to write the data to
        """
        counts, bins = self._cache.get_histograms()
        super().save_nxs2(file,
                          bins,
                          counts,
                          len(counts[0][0]),
                          len(counts[0]),
                          len(counts))


def read_detector1_from_histogram(file):
    """
    A method to read the detector 1 values from a
    muon NXS v2 file.
    :param: the open file to read the values from
    :return: a Detector_1 object with the values loaded
    """
    tmp = file['raw_data_1']['instrument']['detector_1']

    # convert to micro seconds
    resolution = tmp['resolution'][0] / 1.e6

    raw_time = tmp['raw_time'][:]
    spec = tmp['spectrum_index'][:]

    tmp = tmp['counts']
    inst = tmp.attrs['long_name'].decode()
    first_good = tmp.attrs['first_good_bin'] * resolution
    """
    Need to add 1 to the last good, so that the
    correct bin is a complete bin of good data.
    """
    last_good = (tmp.attrs['last_good_bin'] + 1) * resolution
    t0 = tmp.attrs['t0_bin'] * resolution
    counts = tmp[:]

    # not used...
    # direction =  tmp['orientation'][0].decode()
    # tmp = file['raw_data_1']['detector_1']
    # needed for mantid ?
    # dead_time = tmp['dead_time'][:]
    # grouping = tmp['grouping'][:]
    # time_zero = tmp['time_zero'][:]

    return Detector_1(resolution,
                      raw_time,
                      spec,
                      counts,
                      inst, t0,
                      first_good,
                      last_good)
