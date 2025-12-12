from MuonDataLib.cython_ext.base_sample_logs import BaseSampleLogs
from MuonDataLib.data.hdf5 import HDF5


class SampleLogs(HDF5, BaseSampleLogs):
    """
    A simple class to store the sample log information
    needed for a muon nexus v2 file
    """
    def __init__(self):
        """
        Create an empty set of sample logs
        """
        super(HDF5, self).__init__()

    def save_nxs2(self, file):
        """
        Write the user information to a
        muon nexus v2 file.
        :param file: the open file to write to
        """
        selog = file.require_group('raw_data_1')
        selog = selog.require_group('selog')
        selog.attrs['NX_class'] = 'IXselog'
        for key in self._look_up.keys():
            dtype = self._look_up[key]
            if dtype == 'float':
                logs = self.get_sample_log(key)
                tmp = selog.require_group(key)
                tmp.attrs['NX_class'] = 'IXseblock'
                tmp = tmp.require_group('value_log')
                tmp.attrs['NX_class'] = 'NXlog'
                x, y = logs.get_values()
                self.save_float_array('time', x, tmp)
                self.save_float_array('value', y, tmp)
