from MuonDataLib.data.sample import read_sample_from_histogram
from MuonDataLib.data.raw_data import read_raw_data_from_histogram
from MuonDataLib.data.source import read_source_from_histogram
from MuonDataLib.data.user import read_user_from_histogram
from MuonDataLib.data.periods import read_periods_from_histogram
from MuonDataLib.data.detector1 import read_detector1_from_histogram
from MuonDataLib.data.muon_data import MuonData
import h5py


def load_nxs2(file_name):
    with h5py.File(file_name, 'r') as file:
        return MuonData(sample=read_sample_from_histogram(file),
                        raw_data=read_raw_data_from_histogram(file),
                        source=read_source_from_histogram(file),
                        user=read_user_from_histogram(file),
                        periods=read_periods_from_histogram(file),
                        detector1=read_detector1_from_histogram(file))
