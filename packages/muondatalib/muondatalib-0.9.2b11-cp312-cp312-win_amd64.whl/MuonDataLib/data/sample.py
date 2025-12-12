from MuonDataLib.data.hdf5 import HDF5


class Sample(HDF5):
    """
    A class for the sample information needed for a muon nexus v2 file
    """
    def __init__(self, ID, thickness, height, width, B_field, Temp, name):
        """
        The sample information for a muon nexus v2 file
        :param ID: the sample ID
        :param thickness: the thickness of the sample
        :param height: the height of the sample
        :param width: the width of the sample
        :param B_field: the magnetic field being applied to the sample
        :param Temp: the applied temperature to the sample
        :param name: the name of the sample
        """
        super().__init__()
        self._dict['ID'] = ID
        self._dict['thickness'] = thickness
        self._dict['height'] = height
        self._dict['width'] = width
        self._dict['B_field'] = B_field
        self._dict['Temp'] = Temp
        self._dict['name'] = name

    def save_nxs2(self, file):
        """
        A method to write the sample information into
        a muon nexus v2 file
        :param file: the open file to write the data to
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('sample')
        tmp.attrs['NX_class'] = 'NXsample'

        self.save_str('id', self._dict['ID'], tmp)
        self.save_str('name', self._dict['name'], tmp)
        self.save_float('thickness', self._dict['thickness'], tmp)
        self.save_float('height', self._dict['height'], tmp)
        self.save_float('width', self._dict['width'], tmp)
        self.save_float('magnetic_field', self._dict['B_field'], tmp)
        self.save_float('temperature', self._dict['Temp'], tmp)


def read_sample_from_histogram(file):
    """
    A function to read the sample information from
    a muon nexus v2 file
    :param file: the open file to read from
    :return: the Sample information
    """
    tmp = file['raw_data_1']['sample']
    return Sample(tmp['id'][0].decode(),
                  tmp['thickness'][0],
                  tmp['height'][0],
                  tmp['width'][0],
                  tmp['magnetic_field'][0],
                  tmp['temperature'][0],
                  tmp['name'][0].decode())
