from MuonDataLib.data.periods import read_periods_from_histogram

import os
import h5py


class PeriodsTestTemplate(object):

    """
    ---------IMPORTANT-------------------------------
    When inheriting this class, you will also need to
    inherit "unittest.TestCase" or "TestHelper" for it
    to work as a unit test. Cannot do it here as it
    will then treat this base class as a test
    (which will always fail).
    -------------------------------------------------
    """
    def create_single_period_data(self):
        return 1, 'period 1', [1], [500], [1000], [0], [1.2e-5], [500]

    def create_multiperiod_data(self):
        return (2, 'period 1;period 2', [1, 2], [500, 400],
                [1000, 500], [0, 0], [1.2e-5, 4.5e-5], [500, 400])

    def save(self, periods, file):
        raise NotImplementedError()

    def setUp(self):
        raise NotImplementedError()

    def test_periods_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        period = self.create_single_period_data()

        self.assertEqual(period._dict['number'], 1)
        self.assertEqual(period._dict['labels'], 'period 1')
        self.assertArrays(period._dict['type'], [1])
        self.assertArrays(period._dict['output'], [0])

        self.period = period

    def test_periods_object_saves_correct_info_single_period(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        periods = self.create_single_period_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(periods, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            keys = self.compare_keys(group, ['periods'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXperiod')

            self.assertEqual(group['number'][0], 1)
            self.assertString(group, 'labels', 'period 1')
            self.assertArrays(group['type'], [1])
            self.assertArrays(group['frames_requested'], [500])
            self.assertArrays(group['raw_frames'], [1000])
            self.assertArrays(group['output'], [0])
            self.assertArrays(group['sequences'], [500])
            self.assertArrays(group['total_counts'], [12.e-6])

        os.remove(self.filename)

    def test_load_periods_gets_correct_info_single_period(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        period = self.create_single_period_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(period, file)
        del period

        with h5py.File(self.filename, 'r') as file:
            load_period = read_periods_from_histogram(file)

        self.assertEqual(load_period._dict['number'], 1)
        self.assertEqual(load_period._dict['labels'], 'period 1')
        self.assertArrays(load_period._dict['type'], [1])
        self.assertArrays(load_period._dict['requested'], [500])
        self.assertArrays(load_period._dict['raw'], [1000])
        self.assertArrays(load_period._dict['output'], [0])
        self.assertArrays(load_period._dict['sequences'], [500])
        self.assertArrays(load_period._dict['total_counts'], [12.e-6])

        os.remove(self.filename)

    def test_periods_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        period = self.create_multiperiod_data()

        self.assertEqual(period._dict['number'], 2)
        self.assertEqual(period._dict['labels'], 'period 1;period 2')
        self.assertArrays(period._dict['type'], [1, 2])
        self.assertArrays(period._dict['output'], [0, 0])

        self.period = period

    def test_periods_object_saves_correct_info_multiperiod(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        period = self.create_multiperiod_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(period, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            keys = self.compare_keys(group, ['periods'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXperiod')

            self.assertEqual(group['number'][0], 2)
            self.assertEqual(group['labels'][0].decode(), 'period 1;period 2')
            self.assertArrays(group['type'], [1, 2])
            self.assertArrays(group['frames_requested'], [500, 400])
            self.assertArrays(group['raw_frames'], [1000, 500])
            self.assertArrays(group['output'], [0, 0])
            self.assertArrays(group['sequences'], [500, 400])
            self.assertArrays(group['total_counts'], [12.e-6, 45.e-6])

        os.remove(self.filename)

    def test_load_period_gets_correct_info_multiperiod(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        period = self.create_multiperiod_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(period, file)
        del period

        with h5py.File(self.filename, 'r') as file:
            load_period = read_periods_from_histogram(file)

        self.assertEqual(load_period._dict['number'], 2)
        self.assertEqual(load_period._dict['labels'], 'period 1;period 2')
        self.assertArrays(load_period._dict['type'], [1, 2])
        self.assertArrays(load_period._dict['requested'], [500, 400])
        self.assertArrays(load_period._dict['raw'], [1000, 500])
        self.assertArrays(load_period._dict['output'], [0, 0])
        self.assertArrays(load_period._dict['sequences'], [500, 400])
        self.assertArrays(load_period._dict['total_counts'], [12.e-6, 45.e-6])

        os.remove(self.filename)
