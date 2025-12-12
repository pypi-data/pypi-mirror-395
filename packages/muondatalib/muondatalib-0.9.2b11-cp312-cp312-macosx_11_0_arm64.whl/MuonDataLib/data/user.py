from MuonDataLib.data.hdf5 import HDF5


class User(HDF5):
    """
    A simple class to store the user information
    needed for a muon nexus v2 file
    """
    def __init__(self, name, affiliation):
        """
        Store the user information for muon nexus v2 file
        :param name: the user's name
        Param affiliation: the user's affiliation/institution
        """
        super().__init__()
        self._dict['name'] = name
        self._dict['affiliation'] = affiliation

    def save_nxs2(self, file):
        """
        Write the user information to a
        muon nexus v2 file.
        :param file: the open file to write to
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('user_1')
        tmp.attrs['NX_class'] = 'NXuser'

        for key in self._dict.keys():
            self.save_str(key, self._dict[key], tmp)


def read_user_from_histogram(file):
    """
    A function to read the histogram information
    from a muon nexus v2 file
    :param file: the open file to read from
    :return: the user information
    """
    tmp = file['raw_data_1']
    tmp = tmp['user_1']

    return User(tmp['name'][0].decode(),
                tmp['affiliation'][0].decode())
