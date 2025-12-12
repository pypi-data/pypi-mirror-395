from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.filters.view import FilterView


class FilterPresenter(PresenterTemplate):
    """
    A class for the filter widget's presenter.
    This code follows the MVP template,
    note that the model is MuonDataLib.
    """
    def __init__(self):
        """
        Create the presenter.
        """
        self._view = FilterView(self)
