from MuonDataLib.data.raw_data import read_raw_data_from_histogram

import h5py
import os
import datetime


class RawDataTestTemplate(object):

    """
    ---------IMPORTANT-------------------------------
    When inheriting this class, you will also need to
    inherit "unittest.TestCase" or "TestHelper" for it
    to work as a unit test. Cannot do it here as it
    will then treat this base class as a test
    (which will always fail).
    -------------------------------------------------
    """
    def create_data(self):
        start = datetime.datetime(2018, 12, 24, 13, 32, 1)
        end = datetime.datetime(2018, 12, 24, 18, 11, 52)
        return (10, 1, 'pulsed', 'python', 'raw data test',
                'testing', 42, 16791.0, 51, start, end, '19')

    def save(self, raw, file):
        raise NotImplementedError()

    def setUp(self):
        raise NotImplementedError()

    def test_raw_data_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        raw, start, end = self.create_data()

        self.assertEqual(raw._dict['IDF'], 1)
        self.assertEqual(raw._dict['def'], 'pulsed')
        self.assertEqual(raw._dict['inst'], 'python')
        self.assertEqual(raw._dict['title'], 'raw data test')
        self.assertEqual(raw._dict['notes'], 'testing')
        self.assertEqual(raw._dict['run_number'], 42)

        self.raw = raw

    def test_raw_data_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        raw, _, _ = self.create_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(raw, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXentry')

            keys = self.compare_keys(group, ['good_frames',
                                             'IDF_version',
                                             'definition',
                                             'name',
                                             'title',
                                             'notes',
                                             'run_number',
                                             'duration',
                                             'raw_frames',
                                             'start_time',
                                             'end_time',
                                             'experiment_identifier',
                                             'instrument'])

            self.assertArrays(group['good_frames'], [10])
            self.assertArrays(group['IDF_version'], [1])
            self.assertString(group, 'definition', 'pulsed')
            self.assertString(group, 'name', 'python')
            self.assertString(group, 'title', 'raw data test')
            self.assertString(group, 'notes', 'testing')
            self.assertArrays(group['run_number'], [42])
            self.assertArrays(group['duration'], [16791.0])
            self.assertArrays(group['raw_frames'], [51])
            self.assertString(group, 'start_time', '2018-12-24T13:32:01')
            self.assertString(group, 'end_time', '2018-12-24T18:11:52')

            group = group['instrument']
            self.compare_keys(group, ['name'])
            self.assertString(group, 'name', 'python')

        os.remove(self.filename)

    def test_load_raw_data_gets_correct_info(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        raw, start, end = self.create_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(raw, file)

        del raw

        with h5py.File(self.filename, 'r') as file:
            load_raw = read_raw_data_from_histogram(file)

        self.assertEqual(load_raw._dict['good_frames'], 10)
        self.assertEqual(load_raw._dict['IDF'], 1)
        self.assertEqual(load_raw._dict['def'], 'pulsed')
        self.assertEqual(load_raw._dict['inst'], 'python')
        self.assertEqual(load_raw._dict['title'], 'raw data test')
        self.assertEqual(load_raw._dict['notes'], 'testing')
        self.assertEqual(load_raw._dict['run_number'], 42)
        self.assertAlmostEqual(load_raw._dict['duration'], 16791.0, 3)
        self.assertEqual(load_raw._dict['raw_frames'], 51)
        self.assertEqual(load_raw._dict['start'], start)
        self.assertEqual(load_raw._dict['end'], end)

        os.remove(self.filename)
