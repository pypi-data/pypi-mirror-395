from MuonDataLib.GUI.view_template import ViewTemplate
import dash_bootstrap_components as dbc
from dash import html


class SaveBarView(ViewTemplate):
    """
    Creates the view of the Save Bar Widget.
    This code follows the MVP pattern.
    """

    def generate(self):
        """
        Gets the view for the widget
        :returns: the layout for the widget
        """
        return html.Div([
            dbc.Button('Save',
                       id='Save',
                       color='primary',
                       className='me-md-2'),
            dbc.Button('Save filters',
                       id='save_filters',
                       color='primary',
                       className='me-md-2'),

            html.Div(id='save_btn_dummy',
                     children="NONE",
                     hidden=True),
            html.Div(id='save_exe_dummy',
                     children="NONE",
                     hidden=True),
            ],
                        className="d-grid gap-2 d-md-flex "
                                  "justify-content-md-start")
