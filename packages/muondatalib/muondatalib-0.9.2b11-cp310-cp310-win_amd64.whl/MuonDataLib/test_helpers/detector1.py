from MuonDataLib.data.detector1 import read_detector1_from_histogram

import h5py
import os
import numpy as np


class Det1TestTemplate(object):

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
        x = [1., 2., 3.]
        # counts: shape(periods, spec, x)
        counts = []
        for p in range(1):
            counts.append([])
            for j in range(4):
                tmp = (((j + 1) * np.ones(len(x))))
                counts[p].append([int(x) for x in tmp])
        """
        the plus one one last good is so that the
        correct result is 42. The last good is the
        last complete bin before the value. Since
        42*0.016 gives the start of a bin edge,
        we move it along to the next one.
        """
        return (0.016, x, [4, 5, 6, 7], counts, 'python',
                3*0.016, 4*0.016, (42 + 1)*0.016)

    def create_multiperiod_data(self):
        x = [1., 2., 3.]
        # counts: shape(periods, spec, x)
        counts = []
        for p in range(3):
            counts.append([])
            for j in range(2):
                tmp = (((p + 1) * np.ones(len(x))))
                counts[p].append([int(x) for x in tmp])

        return (0.016, x, [4, 5], counts, 'python', 3*0.016,
                4*0.016, (42 + 1)*0.016)

    def save(self, det, file):
        raise NotImplementedError()

    def setUp(self):
        raise NotImplementedError()

    def test_detector1_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        det = self.create_single_period_data()

        self.assertEqual(det._dict['resolution'], 0.016)
        self.assertArrays(det._dict['spectrum_index'], [4, 5, 6, 7])
        self.assertEqual(det._dict['inst'], 'python')
        self.assertAlmostEqual(det._dict['time_zero'], 3*0.016, 3)
        self.assertAlmostEqual(det._dict['first_good'], 4*0.016)
        self.assertAlmostEqual(det._dict['last_good'], (42 + 1)*0.016)

        self.det = det

    def test_detector1_object_saves_correct_info_single_period(self):
        det = self.create_single_period_data()
        res = self._detector1_object_saves_correct_info_single_period(det)
        self.assertEqual(res, 16000)

    def _detector1_object_saves_correct_info_single_period(self, det):
        """
        Test that the class can save to a nexus file
        correctly
        """

        with h5py.File(self.filename, 'w') as file:
            self.save(det, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            inst = file[keys[0]]

            keys = self.compare_keys(inst, ['instrument'])
            inst = inst[keys[0]]
            self.assertEqual(inst.attrs['NX_class'], 'NXinstrument')

            keys = self.compare_keys(inst, ['detector_1'])
            group = inst[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXdetector')

            keys = self.compare_keys(group, ['resolution',
                                             'raw_time',
                                             'spectrum_index',
                                             'counts',
                                             ])

            # check values
            res = group['resolution'][0]
            self.assertArrays(group['raw_time'][:], [1., 2., 3.])
            self.assertArrays(group['spectrum_index'][:], [4, 5, 6, 7])
            self.assertArrays(group['counts'][:], [
                                                   [[1, 1, 1],
                                                    [2, 2, 2],
                                                    [3, 3, 3],
                                                    [4, 4, 4]]])

            # check attributes
            tmp = group['resolution']
            self.assertEqual(tmp.attrs['units'].decode(), "picoseconds")

            tmp = group['raw_time']
            self.assertEqual(tmp.attrs['units'].decode(), 'microseconds')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'time')

            tmp = group['counts']
            self.assertEqual(tmp.attrs['axes'].decode(),
                             '[period index, spectrum index, raw time bin]')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'python')
            self.assertEqual(tmp.attrs['t0_bin'], 3)
            self.assertEqual(tmp.attrs['first_good_bin'], 4)
            self.assertEqual(tmp.attrs['last_good_bin'], 42)

        os.remove(self.filename)
        return res

    def test_load_detector1_gets_correct_info_single_period(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        det = self.create_single_period_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(det, file)
        del det

        with h5py.File(self.filename, 'r') as file:
            load_det = read_detector1_from_histogram(file)

        self.assertEqual(load_det._dict['resolution'], 0.016)
        self.assertArrays(load_det._dict['spectrum_index'], [4, 5, 6, 7])
        self.assertEqual(load_det._dict['inst'], 'python')
        self.assertEqual(load_det._dict['time_zero'], 0.048)
        self.assertEqual(load_det._dict['first_good'], 4*0.016)
        self.assertEqual(load_det._dict['last_good'], (42 + 1)*0.016)
        self.assertArrays(load_det._dict['raw_time'], [1, 2, 3])
        self.assertArrays(load_det._dict['counts'], [
                                                          [[1, 1, 1],
                                                           [2, 2, 2],
                                                           [3, 3, 3],
                                                           [4, 4, 4]]])
        self.assertEqual(load_det.N_x, 3)
        self.assertEqual(load_det.N_hist, 4)
        self.assertEqual(load_det.N_periods, 1)

        os.remove(self.filename)

    def test_detector1_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        det = self.create_multiperiod_data()

        self.assertEqual(det._dict['resolution'], 0.016)
        self.assertArrays(det._dict['spectrum_index'], [4, 5])
        self.assertEqual(det._dict['inst'], 'python')
        self.assertAlmostEqual(det._dict['time_zero'], 3*0.016, 3)
        self.assertAlmostEqual(det._dict['first_good'], 4*0.016, 3)
        self.assertAlmostEqual(det._dict['last_good'], (42 + 1)*0.016, 3)

        self.det = det

    def test_detector1_object_saves_correct_info_multiperiod(self):
        det = self.create_multiperiod_data()
        res = self._detector1_object_saves_correct_info_multiperiod(det)
        self.assertEqual(res, 16000)

    def _detector1_object_saves_correct_info_multiperiod(self, det):
        """
        Test that the class can save to a nexus file
        correctly
        """

        with h5py.File(self.filename, 'w') as file:
            self.save(det, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            inst = file[keys[0]]

            keys = self.compare_keys(inst, ['instrument'])
            inst = inst[keys[0]]
            self.assertEqual(inst.attrs['NX_class'], 'NXinstrument')

            keys = self.compare_keys(inst, ['detector_1'])
            group = inst[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXdetector')

            keys = self.compare_keys(group, ['resolution',
                                             'raw_time',
                                             'spectrum_index',
                                             'counts',
                                             ])

            # check values
            self.assertArrays(group['raw_time'][:], [1., 2., 3.])
            self.assertArrays(group['spectrum_index'][:], [4, 5])
            self.assertArrays(group['counts'][:], [
                                                   [[1, 1, 1], [1, 1, 1]],
                                                   [[2, 2, 2], [2, 2, 2]],
                                                   [[3, 3, 3], [3, 3, 3]]])

            # check attributes
            tmp = group['resolution']
            self.assertEqual(tmp.attrs['units'].decode(), "picoseconds")

            tmp = group['raw_time']
            self.assertEqual(tmp.attrs['units'].decode(), 'microseconds')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'time')

            tmp = group['counts']
            self.assertEqual(tmp.attrs['axes'].decode(),
                             '[period index, spectrum index, raw time bin]')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'python')
            self.assertEqual(tmp.attrs['t0_bin'], 3)
            self.assertEqual(tmp.attrs['first_good_bin'], 4)
            self.assertEqual(tmp.attrs['last_good_bin'], 42)
            res = group['resolution'][0]
        os.remove(self.filename)
        return res

    def test_load_detector1_gets_correct_info_multiperiod(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        det = self.create_multiperiod_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(det, file)
        del det

        with h5py.File(self.filename, 'r') as file:
            load_det = read_detector1_from_histogram(file)

        self.assertEqual(load_det._dict['resolution'], 0.016)
        self.assertArrays(load_det._dict['spectrum_index'], [4, 5])
        self.assertEqual(load_det._dict['inst'], 'python')
        self.assertAlmostEqual(load_det._dict['time_zero'], 3*0.016, 4)
        self.assertAlmostEqual(load_det._dict['first_good'], 4*0.016, 4)
        self.assertAlmostEqual(load_det._dict['last_good'], (42 + 1)*0.016, 4)
        self.assertArrays(load_det._dict['raw_time'], [1., 2., 3.])
        self.assertArrays(load_det._dict['counts'], [
                                                     [[1, 1, 1], [1, 1, 1]],
                                                     [[2, 2, 2], [2, 2, 2]],
                                                     [[3, 3, 3], [3, 3, 3]]])

        self.assertEqual(load_det.N_x, 3)
        self.assertEqual(load_det.N_hist, 2)
        self.assertEqual(load_det.N_periods, 3)

        os.remove(self.filename)
