from PyQt5.QtWidgets import QMessageBox, QWidget, QDockWidget, QToolBar, QMainWindow, QAction, QStyle, QVBoxLayout
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class PreviewBase(QDockWidget):
    def __init__(self):
        super().__init__()
        # List of file extensions allowed to use the preview window, write extension without leading dot.
        self.allowed_file_types = []
        self._file_full_path = None
        _inner_window = QMainWindow(self)
        _inner_window.setWindowFlags(Qt.Widget)
        _base_widget = QWidget(self)
        self.base = QVBoxLayout(_base_widget)

        self._toolbar = QToolBar(_inner_window)

        _open = QAction("Open", self)
        _open.triggered.connect(self.open_file)
        self._toolbar.addAction(_open)

        _refresh = QAction("Refresh", self)
        _refresh.triggered.connect(lambda: self.set_file(self._file_full_path))
        self._toolbar.addAction(_refresh)

        _inner_window.addToolBar(self._toolbar)
        self.setWidget(_inner_window)
        _inner_window.setCentralWidget(_base_widget)

    def open_file(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.get_file_full_path()))

    def get_allowed_file_types(self):
        """Get all file types

        Returns:
            dict: Allowed file types
        """
        return self.allowed_file_types

    def set_file(self, file_full_path):
        self._file_full_path = file_full_path
        self.setWindowTitle(f'Preview - {file_full_path}')

    def get_file_full_path(self):
        if self._file_full_path:
            return self._file_full_path
        else:
            QMessageBox.warning(self, 'Preview', 'Internal error occurred. File path not set in preview')

    def disable_toolbar(self):
        self._toolbar.hide()