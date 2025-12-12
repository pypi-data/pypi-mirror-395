from MuonDataLib.GUI.view_template import ViewTemplate

from dash import Input, Output, callback
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq


CURRENT = "Current File: "


class LoadBarView(ViewTemplate):
    """
    A class for the load bar's view.
    This follows the MVP pattern.
    """
    def generate(self):
        """
        Creates the view for the
        load bar widget
        :returns: the layout for the
        load bar widget.
        """
        return html.Div([
            dbc.Button('Load', id='Load',
                       color='primary', className='me-md-2'),
            dbc.Button('Load filters', id='load_filters', color='primary',
                       n_clicks=0, className='me-md-2'),
            html.Div(id='file_name', children=CURRENT, className='me-md-2'),

            dbc.Button(id='settings', color='primary',
                       n_clicks=0, className='bi-gear-fill ms-auto'),
            # code for the settings pop-up
            dbc.Modal(
                      [dbc.ModalHeader(dbc.ModalTitle("Settings")),
                       dbc.ModalFooter(
                                       dbc.Row(daq.PowerButton(on=False,
                                                               id='debug',
                                                               label='Debug',
                                                               color='#FF5E5E',
                                                               ),
                                               )
                                       ),
                       ],
                      id="settings_pop_up",
                      is_open=False,
                     )
            ], className="d-grid gap-2 d-md-flex justify-content-md-start")

    def set_callbacks(self, presenter):
        """
        This sets up the links between an action on the GUI
        and the code that needs to run in response.
        Most of the callbacks are in main_GUI.py so they
        can connect to the qt file finder.
        """
        callback(
             Output('settings_pop_up', 'is_open'),
             Input('settings', 'n_clicks'),
             prevent_initial_call=True)(self.open_settings)

        return

    def open_settings(self, state):
        """
        Sinple method for getting
        if the settings menu is open.
        This method is only trigerred
        when the settings buttonn is pressec
        :param: (unused) if the pop uo window
        is open.
        :returns: True (if the pop up is open)
        """
        return True
