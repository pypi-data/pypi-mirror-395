from MuonDataLib.data.utils import (convert_date_for_NXS,
                                    convert_date)
from MuonDataLib.data.hdf5 import HDF5
import re
import numpy as np


class _RawData(HDF5):
    """
    A base class for storing the "raw data" information for a
    muon nexus v2 file
    """
    def __init__(self, IDF, definition, inst, title, notes,
                 run_number, ID):
        """
        Creates the raw data object, which holds all of the information
        for the raw data section of a muon nexus v2 file
        :param IDF: the version of the Instrument Definition File (IDF)
        :param definition: the definition (e.g. pulsedTD)
        :param inst: the instrument name
        :param title: the title of the experiment
        :param notes: the additional notes/comments
        :param run_number: the run number
        :param duration: the duration of the experiment
        :param ID: a string identifier for the experiment
        """
        super().__init__()
        self._dict['IDF'] = IDF
        self._dict['def'] = definition
        self._dict['inst'] = inst
        self._dict['title'] = title
        self._dict['notes'] = notes
        self._dict['run_number'] = run_number
        self._dict['ID'] = ID

    def save_nxs2(self, file, good_frames, raw_frames,
                  start_time, end_time, duration):
        """
        A method to save the information into a muon nexus v2 file
        :param file: the open file to write to.
        :param good_frames: the number of good frames
        :param raw_frames: the number of raw frames
        :param start_time: the start date time
        :param end_time: the end date time
        """
        tmp = file.require_group('raw_data_1')
        tmp.attrs['NX_class'] = 'NXentry'

        self.save_int('good_frames', good_frames, tmp)
        self.save_int('IDF_version', self._dict['IDF'], tmp)
        self.save_str('definition', self._dict['def'], tmp)
        self.save_str('name', self._dict['inst'], tmp)
        self.save_str('title', self._dict['title'], tmp)
        self.save_str('notes', self._dict['notes'], tmp)
        self.save_int('run_number', self._dict['run_number'], tmp)

        dur = self.save_float('duration', duration, tmp)
        dur.attrs.create('units', 'seconds'.encode(), dtype='S7')

        self.save_int('raw_frames', raw_frames, tmp)
        self.save_str('start_time',
                      convert_date_for_NXS(start_time),
                      tmp)
        self.save_str('end_time', convert_date_for_NXS(end_time), tmp)
        self.save_str('experiment_identifier', self._dict['ID'], tmp)

        tmp2 = tmp.require_group('instrument')
        self.save_str('name', self._dict['inst'], tmp2)

        return tmp


class RawData(_RawData):
    """
    A class for storing the "raw data" information for a
    muon nexus v2 file
    """
    def __init__(self, good_frames, IDF, definition, inst, title, notes,
                 run_number, duration, raw_frames, start_time, end_time, ID):
        """
        Creates the raw data object, which holds all of the information
        for the raw data section of a muon nexus v2 file
        :param good_frames: the number of good frames
        :param IDF: the version of the Instrument Definition File (IDF)
        :param definition: the definition (e.g. pulsedTD)
        :param inst: the instrument name
        :param title: the title of the experiment
        :param notes: the additional notes/comments
        :param run_number: the run number
        :param duration: the duration of the experiment
        :param raw_frames: the number of raw frames
        :param start_time: the start time of the experiment
        :param end_time: the end time of the experiment
        :param ID: a string identifier for the experiment
        """
        super().__init__(IDF, definition, inst, title, notes,
                         run_number, ID)

        self._dict['good_frames'] = good_frames
        self._dict['raw_frames'] = raw_frames
        self._dict['start'] = start_time
        self._dict['end'] = end_time
        self._dict['duration'] = duration

    def save_nxs2(self, file):
        """
        A method to save the information into a muon nexus v2 file
        :param file: the open file to write to.
        """
        super().save_nxs2(file,
                          self._dict['good_frames'],
                          self._dict['raw_frames'],
                          self._dict['start'],
                          self._dict['end'],
                          self._dict['duration'],
                          )


class EventsRawData(_RawData):
    """
    A class for storing the "raw data" information for a
    muon nexus v2 file
    """
    def __init__(self, cache, IDF, definition, inst, title, notes,
                 run_number, ID):
        """
        Creates the raw data object, which holds all of the information
        for the raw data section of a muon nexus v2 file
        :param cache: the cache for events data
        :param IDF: the version of the Instrument Definition File (IDF)
        :param definition: the definition (e.g. pulsedTD)
        :param inst: the instrument name
        :param title: the title of the experiment
        :param notes: the additional notes/comments
        :param run_number: the run number
        :param ID: a string identifier for the experiment
        """
        super().__init__(IDF, definition, inst, title, notes,
                         run_number, ID)

        self._cache = cache

    def save_nxs2(self, file):
        """
        A method to save the information into a muon nexus v2 file
        Will need to edit this for multi-period
        :param file: the open file to write to.
        """
        tmp = super().save_nxs2(file,
                                self._cache.get_good_frames[0],
                                self._cache.get_raw_frames[0],
                                self._cache.get_start_time,
                                self._cache.get_end_time,
                                self._cache.get_duration
                                )

        self.save_int('discarded_raw_frames',
                      self._cache.get_discarded_raw_frames[0],
                      tmp)

        dur = self.save_float('count_duration',
                              self._cache.get_count_duration[0],
                              tmp)

        dur.attrs.create('units', 'seconds'.encode(), dtype='S7')


def read_raw_data_from_histogram(file):
    """
    A function for reading the raw data information
    from a muon nexus v2 file
    :param file: the open file to read from
    :return: the RawData object
    """
    tmp = file['raw_data_1']
    return RawData(tmp['good_frames'][0],
                   tmp["IDF_version"][0],
                   tmp['definition'][0].decode(),
                   tmp['name'][0].decode(),
                   tmp['title'][0].decode(),
                   tmp['notes'][0].decode(),
                   tmp['run_number'][0],
                   tmp['duration'][0],
                   tmp['raw_frames'][0],
                   convert_date(tmp['start_time'][0].decode()),
                   convert_date(tmp['end_time'][0].decode()),
                   tmp['experiment_identifier'][0].decode())


def warning(name):
    print("WARNING:", f'The metadata {name} is missing. Using fallback values')


def read_raw_data_from_events(file):
    """
    A function for reading the additional raw data information
    from a muon nexus event file
    :param file: the open file to read from
    :return: the inputs for the event raw data object
    """
    tmp = file['raw_data_1']

    """
    At present (20/01/25) the event nexus file is not
    recording all of the metadata. Therefore,
    we will need to check if the metadata exists/occupied
    and if not replace it with some fall back values.
    The notes metadata is not present at all
    """
    run = tmp['run_number'][()]
    title = tmp['title'][()].decode(),
    notes = "Notes: test"
    exp_ID = tmp['experiment_identifier'][()].decode()
    name = tmp['name'][()].decode(),

    if run <= 0:
        warning("**RUN**")
        split = re.compile('([a-zA-Z]+)([0-9]+)')
        run = np.int32(split.match(name[0]).groups()[1])
    if title[0] == '':
        warning('**TITLE**')
        title = 'Title: test'
    if exp_ID == '':
        warning('**EXPERIMENT IDENTIFIER**')
        exp_ID = 'raw ID: test'

    return ((tmp["IDF_version"][()],
             'pulsedTD',
             name[0],
             title,
             notes,
             run,
             exp_ID),
            convert_date(tmp['start_time'][()].decode().split('+')[0]))
