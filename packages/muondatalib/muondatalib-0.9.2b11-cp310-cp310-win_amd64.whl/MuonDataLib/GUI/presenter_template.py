from MuonDataLib.GUI.view_template import ViewTemplate


class PresenterTemplate(object):
    """
    This is a template class for a
    presenter. This code uses the
    MVP pattern.
    """
    def __init__(self):
        """
        Creates a presenter with the
        view as a member
        """
        self._view = ViewTemplate(self)

    @property
    def layout(self):
        """
        Gets the view of the widget
        :returns: the layout of the view
        """
        return self._view.layout
