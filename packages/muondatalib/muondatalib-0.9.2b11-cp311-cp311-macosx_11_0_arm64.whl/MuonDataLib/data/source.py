from MuonDataLib.data.hdf5 import HDF5


class Source(HDF5):
    """
    A class to store the source information needed
    for a muon nexus v2 file
    """
    def __init__(self, name, probe, s_type):
        """
        A small class to store the source information
        :param name: the source name (e.g. ISIS)
        :param probe: the type of probe used
        :param type: the type of source (e.g. pulsed)
        """
        super().__init__()
        self._dict['name'] = name
        self._dict['probe'] = probe
        self._dict['type'] = s_type

    def save_nxs2(self, file):
        """
        Method to save the source information to a
        muon nexus v2 file
        :param file: the open file to write to
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('instrument')

        tmp = tmp.require_group('source')
        tmp.attrs['NX_class'] = 'NXsource'
        for key in self._dict.keys():
            self.save_str(key, self._dict[key], tmp)


def read_source_from_histogram(file):
    """
    A function to read the source information
    from a muon nexus v2 file
    :param file: the open file to read from
    :return: the source information
    """
    tmp = file['raw_data_1']['instrument']['source']
    return Source(tmp['name'][0].decode(),
                  tmp['probe'][0].decode(),
                  tmp['type'][0].decode())
