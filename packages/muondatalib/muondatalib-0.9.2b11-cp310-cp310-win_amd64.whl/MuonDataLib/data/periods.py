from MuonDataLib.data.hdf5 import HDF5
import numpy as np


class _Periods(HDF5):
    """
    A base class to store the period informtaion for muon data
    """
    def __init__(self, number, labels, p_type,
                 output):
        """
        A class to store the period data needed for a muon nexus v2 file
        :param number: the number of periods
        :param labels: a string of the period labels
        :param p_type: an int array representing the type of period
        :param output: an int array of the outputs
        """
        super().__init__()
        self._dict['number'] = number
        self._dict['labels'] = labels
        self._dict['type'] = p_type
        self._dict['output'] = output

    def save_nxs2(self, file, requested, raw, counts, sequences):
        """
        A method to save the periods information as a muon
        nexus v2 file
        :param file: the open file to write to
        :param requested: the number of requested frames
        :param raw: the number of raw frames
        :param counts: a float array of the total counts
        :param sequences: an int array of the sequences
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('periods')

        tmp.attrs['NX_class'] = 'NXperiod'
        self.save_int('number', self._dict['number'], tmp)
        self.save_int_array('sequences', sequences, tmp)
        self.save_str('labels', self._dict['labels'], tmp)
        self.save_int_array('type', self._dict['type'], tmp)
        self.save_int_array('frames_requested', requested, tmp)
        self.save_int_array('raw_frames', raw, tmp)
        self.save_int_array('output', self._dict['output'], tmp)
        self.save_float_array('total_counts', counts, tmp)


class Periods(_Periods):
    """
    A class to store the period informtaion for muon data
    """
    def __init__(self, number, labels, p_type, requested,
                 raw, output, counts, sequences):
        """
        A class to store the period data needed for a muon nexus v2 file
        :param number: the number of periods
        :param labels: a string of the period labels
        :param p_type: an int array representing the type of period
        :param requested: the number of requested frames
        :param raw: the number of raw frames
        :param output: an int array of the outputs
        :param counts: a float array of the total counts
        :param sequences: an int array of the sequences
        """
        super().__init__(number, labels, p_type, output)
        self._dict['requested'] = requested
        self._dict['raw'] = raw
        self._dict['total_counts'] = counts
        self._dict['sequences'] = sequences

    def save_nxs2(self, file):
        """
        A method to save the periods information as a muon
        nexus v2 file
        :param file: the open file to write to
        """
        super().save_nxs2(file,
                          self._dict['requested'],
                          self._dict['raw'],
                          self._dict['total_counts'],
                          self._dict['sequences'])


class EventsPeriods(_Periods):
    """
    A class to store the period informtaion for muon data
    """
    def __init__(self, cache, _number, _labels, p_type,
                 _output):
        """
        A class to store the period data needed for a muon nexus v2 file
        Most of the values are currently overwritten as they are not
        present in the event file
        :param cache: the events cache
        :param number: the number of periods
        :param labels: a string of the period labels
        :param p_type: an int array representing the type of period
        :param output: an int array of the outputs
        """
        N = len(p_type)

        label = ''
        for k in range(N):
            label += f'period {k + 1};'
        label = label[:-1]
        output = np.zeros(N, dtype=np.int32)

        super().__init__(N, label, p_type, output)
        self._cache = cache

    def save_nxs2(self, file):
        """
        A method to save the periods information as a muon
        nexus v2 file
        :param file: the open file to write to
        """
        # in the examples the counts always seems to be zero
        # but will set it to be the sum for the period

        hist, _ = self._cache.get_histograms()
        counts = np.zeros(self._dict['number'], dtype=np.double)
        for k in range(self._dict['number']):
            # store MeV
            counts[k] = float(np.sum(hist[k]))/1.e6

        good = np.asarray(self._cache.get_good_frames)
        super().save_nxs2(file,
                          good,
                          np.asarray(self._cache.get_raw_frames),
                          counts,
                          good)


def read_periods_from_histogram(file):
    """
    A method for reading the period information
    a nexus v2 histogram file
    :param file: the open file to read from
    :return: the Periods object
    """
    tmp = file['raw_data_1']['periods']

    return Periods(number=tmp['number'][:][0],
                   labels=tmp['labels'][:][0].decode(),
                   p_type=tmp['type'][:],
                   requested=tmp['frames_requested'][:],
                   raw=tmp['raw_frames'][:],
                   output=tmp['output'][:],
                   counts=tmp['total_counts'][:],
                   sequences=tmp['sequences'][:])
