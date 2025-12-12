from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import pyqtSlot as Slot
import signal
import os


class Worker(QRunnable):
    """
    A simple class for running Dash on a different
    thread. This also includes code to
    allow a graceful exit of Dash when the GUI
    is closed.
    """
    def __init__(self, dash_app, port=8015, host='127.0.0.1'):
        """
        Sets up the worker
        :param dash_app: the dash app (not running)
        that we want to put onto a thread.
        :param port: the port to launch
        the dash app on (no need to change)
        :param host: the host to run the
        dash app on (no need to change)
        """
        super(Worker, self).__init__()
        self.app = dash_app
        self.port = port
        self.host = host

    @Slot()  # QtCore.Slot
    def run(self):
        """
        Runs the dash app. Due to the nature of Dash
        it keeps running in the background, until
        its closed (see terminate).
        Its important to set the port and host for
        later, so we can embed it.
        """
        self.app.run(debug=False, port=self.port, host=self.host)

    @property
    def get_address(self):
        """
        :returns: the web address for the dash app,
        needed for embedding into the GUI
        """
        return f'http://{self.host}:{self.port}/'

    @staticmethod
    def terminate():
        """
        A method to gracefully kill the Dash app
        and return the thread.
        """
        os.kill(os.getpid(), signal.SIGTERM)
