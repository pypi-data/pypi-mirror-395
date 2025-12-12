from MuonDataLib.GUI.utils.worker import Worker
from MuonDataLib.GUI.load_bar.view import CURRENT

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThreadPool
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QVBoxLayout
from time import sleep

from PyQt5.QtWidgets import QMainWindow, QFileDialog

from dash import ctx


class BasicMainDashWindow(QMainWindow):
    """
    A main window for embedding
    a dash app using pyqt.
    """

    def __init__(self, dash_app, parent=None):
        """
        Creates the main window for the dash app.
        :param dash_app: the dash app we want to embed,
        it should not be running or called
        :param parent: the parent of the GUI (typically
        None)
        """
        super().__init__(parent)
        self.set_window(dash_app)
        self.setCentralWidget(self.mainWidget)

    def set_window(self, dash_app):
        """
        A method for setting the dash app
        to the main window.
        :param dash_app: the dash app as
        a callable.
        """
        self.mainWidget = MainWidget(dash_app())

    def closeEvent(self, event):
        """
        When the GUI is closed, this makes
        sure that the Dash app and thread
        is terminated gracefully
        """
        super(BasicMainDashWindow, self).closeEvent(event)
        self.mainWidget.worker.terminate()


class MainDashWindow(BasicMainDashWindow):
    """
    A main window for the stand alone GUI
    that contains the dash app.
    This includes some pyqt for file
    browsing
    """
    open_file_signal = QtCore.pyqtSignal(str)
    save_file_signal = QtCore.pyqtSignal(str)

    def set_window(self, dash_app):
        """
        A method for setting the dash app
        to the main window.
        :param dash_app: the dash app as
        a callable.
        """
        self.mainWidget = MainWidget(dash_app(self.open,
                                              self.open_json,
                                              self.save))

    def __init__(self, dash_app, parent=None):
        """
        Creates the main window for the dash app,
        with some pyqt for file browsing
        :param dash_app: the dash app we want to embed,
        it should not be running
        :param parent: the parent of the GUI (typically
        None)
        """
        super().__init__(dash_app, parent)

        self.open_file_signal.connect(self.open_file_slot)
        self.save_file_signal.connect(self.save_file_slot)
        self.file = None

    @QtCore.pyqtSlot(str)
    def open_file_slot(self, extension):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        # will need to make the filter something we pass in (also want .json)
        file_dialog.setNameFilters([extension])
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.file = CURRENT + selected_files[0]
        else:
            self.file = CURRENT + 'None'

    def open_json(self, n_clicks):
        # should I add methods to allow us to alter the
        # muondata object from here via the app?
        self.file = None
        self.open_file_signal.emit('json (*.json)')
        """
        This is not nice, but we need to
        delay returning from this function
        until the file has been chosen.
        Which is in a different thread,
        so cannot just wait for a return.
        """
        while self.file is None:
            sleep(.01)
        return self.file

    def open(self, n_clicks):
        self.file = None
        self.open_file_signal.emit('nxs (*.nxs)')
        """
        This is not nice, but we need to
        delay returning from this function
        until the file has been chosen.
        Which is in a different thread,
        so cannot just wait for a return.
        """
        while self.file is None:
            sleep(.01)
        return self.file

    @QtCore.pyqtSlot(str)
    def save_file_slot(self, file_extension):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save File")
        # will need to make the filter something we pass in (also want .json)
        file_dialog.setNameFilters([file_extension])
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.file = selected_files[0]
        else:
            self.file = 'None'

    def save(self, n_nxs, n_json):
        dtype = ''
        self.file = None
        btn_pressed = ctx.triggered_id
        if btn_pressed == 'save_filters':
            self.save_file_signal.emit('json (*.json)')
            dtype = 'j'
        elif btn_pressed == 'Save':
            self.save_file_signal.emit('nxs (*.nxs)')
            dtype = 'n'
        """
        This is not nice, but we need to
        delay returning from this function
        until the file has been chosen.
        Which is in a different thread,
        so cannot just wait for a return.
        """
        while self.file is None:
            sleep(.01)
        return dtype + self.file


class MainWidget(QWidget):
    """
    This creates the main widget for the
    GUI. It is a light weight wrapper
    around dash. The expectation is that
    the GUI will be a Dash app.
    """
    def __init__(self, dash_app, parent=None):
        super().__init__(parent)
        self.threadpool = QThreadPool()
        self.worker = Worker(dash_app)
        self.threadpool.start(self.worker)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.worker.get_address))
        lay = QVBoxLayout(self)
        lay.addWidget(self.browser)
