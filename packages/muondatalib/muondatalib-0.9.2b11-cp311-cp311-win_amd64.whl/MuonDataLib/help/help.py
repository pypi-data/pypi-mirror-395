from MuonDataLib.help.help_docs import tags
from MuonDataLib.help.muon_data import get_muon_data_docs
from MuonDataLib.help.utils import get_utils_docs
from MuonDataLib.help.figure import get_figure_docs
from MuonDataLib.help.load_events import get_load_docs

from dash import Dash, Input, Output, callback, dcc, html, State
import dash_bootstrap_components as dbc


class help_app(Dash):
    def __init__(self):
        """
        Creates a Dash app that can be used. This one is for
        API help pages.
        """
        super().__init__(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.docs = (get_load_docs() + get_muon_data_docs() +
                     get_utils_docs() + get_figure_docs())

        self.layout = dbc.Container(
            [
                html.H4(
                    "MuonDataLib API doc",
                    style={"textAlign": "center"},
                    className="mb-3",
                ),
                # ------------------------------------------------- #
                html.Div(
                    [
                        dbc.Button("Open Filters", id="open", n_clicks=0),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Filters")),
                                dbc.ModalBody(
                                    [
                                        # Filter within dbc Modal
                                        html.Label("Tag"),
                                        dcc.Dropdown(
                                            id="filter_dropdown",
                                            options=[
                                                {"label": x, "value": x}
                                                for x in tags
                                            ],
                                            multi=True,
                                        ),
                                    ]
                                ),
                            ],
                            id="filter_pop_up",
                            is_open=False,
                        ),
                    ],
                    className="mb-5",
                ),
                dcc.Markdown('''
                    #### Dummy text
                    production baby: Melody Lim
                ''', id='text'),
                html.Div(id="tabs-content"),
            ],
            fluid=True,
        )
        self.set_callbacks()

    def set_callbacks(self):
        """
        A method to setup all of the callbacks needed
        by the GUI.
        """
        callback(Output("text", "children"),
                 Input("filter_dropdown",
                       "value"))(self.get_filtered_text)

        callback(Output("filter_pop_up", "is_open"),
                 Input("open", "n_clicks"),
                 State("filter_pop_up", "is_open"))(self.pop_up)

    def get_text(self, page, tags):
        """
        Method to check if the help doc (page)
        contains the required tags.
        This uses 'and' logic for multiple filters.
        :param page: a Doc object
        :param tags: a list of tags to filter on.
        :returns: the string of the doc, if it
        is tags contain those requested.
        """
        for key in tags:
            if key not in page.tags:
                return ''
        return page.get_MD()

    def get_filtered_text(self, tags):
        """
        Method for getting the filtered text
        from the list of tags.
        :param tags: The tags to filter on
        :returns: a string of the filtered doc
        """
        text = ''
        if tags is None:
            for page in self.docs:
                text += page.get_MD() + '''\n'''
        else:
            for page in self.docs:
                text += self.get_text(page, tags)
        return text

    def pop_up(self, n1, is_open):
        """
        Handles the state of the filter pop up
        """
        if n1:
            return not is_open
        return is_open
