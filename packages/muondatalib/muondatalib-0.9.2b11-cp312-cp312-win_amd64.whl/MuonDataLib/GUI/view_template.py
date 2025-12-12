

class ViewTemplate(object):
    """
    A template for creating a view.
    This code uses the MVP pattern.
    """
    def __init__(self, presenter):
        """
        This creates the view object for the
        widget. The responses to the callbacks
        will be in the presenter.
        """
        self._page = self.generate()
        self.set_callbacks(presenter)

    def generate(self):
        """
        This creates the view.
        However, in the template it raises
        an error to ensure it is implemented
        in all of the views.
        :returns: the widget layout
        """
        raise NotImplementedError("This view does not produce a widget")

    @property
    def layout(self):
        """
        :returns: the layout of the widget
        """
        return self._page

    def set_callbacks(self, presenter):
        """
        Sets the callbacks for the view.
        These are the responses to the
        view being interacted with.
        :param presenter: the presenter,
        which will contain the appropriate
        responses to the callback.
        """
        return
