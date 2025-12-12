from MuonDataLib.GUI.launch import launch_dash
from MuonDataLib.GUI.utils.main_window import BasicMainDashWindow
from MuonDataLib.help.help import help_app


def launch_help():
    """
    A simple method to launch the help pages.
    """
    launch_dash(help_app, BasicMainDashWindow)
