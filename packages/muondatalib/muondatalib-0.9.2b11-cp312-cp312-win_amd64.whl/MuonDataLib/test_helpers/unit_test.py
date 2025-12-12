import numpy as np
import unittest


class TestHelper(unittest.TestCase):
    """
    A simple wrapper to make unit tests easier
    for nxs file
    """
    def compare_keys(self, nxs, expected):
        """
        Compares the options (keys) from a nexus file
        to an expected list
        :param nxs: the open nexus file (at the correct level)
        :param expected: the list of expected keys
        :return: the keys from the nexus file
        """
        keys = list(nxs.keys())
        # check same number of keys
        self.assertEqual(len(expected), len(keys))
        ref = expected
        # check keys match
        for value in keys:
            self.assertTrue(value in ref)
            ref.remove(value)
        # check all of the expected values have been seen
        self.assertEqual(len(ref), 0)
        return keys

    def assertString(self, group, key, expected):
        """
        The strings in nexus files are lists,
        with just one element. They also need
        decoding
        :param group: the open nexus group
        :param key: the key we want to check
        :param expected: the expected string
        """
        string_list = group[key]
        self.assertEqual(len(string_list), 1)
        self.assertEqual(string_list[0].decode(), expected)

    def assertArrays(self, array, ref):
        for j in range(len(array)):
            len_a = len(array)
            len_r = len(ref)
            msg = f'The arrays are not the same length: {len_a}, {len_r}'
            self.assertEqual(len_a, len_r, msg=msg)

            if isinstance(array[j], (list, np.ndarray)):
                self.assertArrays(array[j], ref[j])
            else:
                msg = f'values do not match in array {array[j]}, {ref[j]}'
                self.assertAlmostEqual(array[j], ref[j], 3, msg=msg)

    def assertMockOnce(self, mock, expected_args):
        """
        A method to check that a mock has the correct
        args. We assume that it is called once.
        This is needed as we often have arrays.
        :param mock: the mock object
        :param expected_args: the expected args for the
        call
        """
        mock.assert_called_once()
        args = mock.call_args[0]

        self.assertEqual(len(expected_args),
                         len(args))
        for k in range(len(args)):
            self.assertArrays(args[k],
                              expected_args[k])
