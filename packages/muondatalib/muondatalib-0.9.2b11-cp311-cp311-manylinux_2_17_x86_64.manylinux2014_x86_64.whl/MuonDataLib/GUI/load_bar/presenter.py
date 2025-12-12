from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.load_bar.view import LoadBarView
from MuonDataLib.data.loader.load_events import load_events


class LoadBarPresenter(PresenterTemplate):
    """
    Class for the load bar's presenter.
    This follows the MVP pattern.
    The model is MuonDataLib.
    """
    def __init__(self):
        """
        Creates a load bar presenter
        """
        self._view = LoadBarView(self)
        self._data = None
        self._load_btn_press = 0
        self._load_filter_press = 0

    def load_filters(self, name):
        """
        Code to read a filter file and
        place the information into a
        string.
        :param name: the name of the filter
        file.
        :return: a string of the filters
        """
        self._data.load_filters(name)
        tmp = self._data.report_filters()
        result = ''
        for k in tmp.keys():
            a = tmp[k]
            for f in a.keys():
                result += f'{k}.{f}: {a[f]} \n'
        return result

    def load_nxs(self, name):
        """
        Reads a muon event nexus file
        and creates a MuonDataLib object
        """
        self._data = load_events(name, 64)

    @property
    def get_data(self):
        """
        :returns: the loaded MuonDataLib
        object.
        """
        return self._data
