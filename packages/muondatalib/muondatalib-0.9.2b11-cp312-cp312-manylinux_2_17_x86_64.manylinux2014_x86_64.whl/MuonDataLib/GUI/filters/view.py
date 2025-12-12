from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html


class FilterView(ViewTemplate):
    """
    A class for the view of the filter
    widget. This follows the MVP
    pattern.
    """
    def generate(self):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """
        return html.Div([
            html.H3("Title: testing", id='title_test'),
            html.P("Filters", id='title_test_body'),
            ])
