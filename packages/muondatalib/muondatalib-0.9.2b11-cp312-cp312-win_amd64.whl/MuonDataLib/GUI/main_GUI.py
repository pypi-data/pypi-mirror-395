from MuonDataLib.GUI.main_app.view import MainApp
from MuonDataLib.GUI.utils.main_window import MainDashWindow
from MuonDataLib.GUI.launch import launch_dash


def launch_GUI():
    """
    A simple method to launch the filtering GUI.
    """
    launch_dash(MainApp, MainDashWindow)
