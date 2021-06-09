from PyQt5.QtWidgets import QMessageBox, QWidget, QDockWidget, QToolBar, QMainWindow, QAction, QStyle, QVBoxLayout
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class PreviewBase(QDockWidget):
    def __init__(self):
        super().__init__()
        # List of file extensions allowed to use the preview window, write extension without leading dot.
        self.allowed_file_types = []
        self.file_full_path = None
        inner_window = QMainWindow(self)
        inner_window.setWindowFlags(Qt.Widget)
        base_widget = QWidget(self)
        self.base = QVBoxLayout(base_widget)

        self.toolbar = QToolBar(inner_window)

        open = QAction("Open", self)
        open.triggered.connect(self.open_file)
        self.toolbar.addAction(open)

        inner_window.addToolBar(self.toolbar)
        self.setWidget(inner_window)
        inner_window.setCentralWidget(base_widget)

    def open_file(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.get_file_full_path()))

    def get_allowed_file_types(self):
        """Get all file types

        Returns:
            dict: Allowed file types
        """
        return self.allowed_file_types

    def set_file(self, file_full_path):
        self.file_full_path = file_full_path
        self.setWindowTitle(f'Preview - {file_full_path}')

    def get_file_full_path(self):
        if self.file_full_path:
            return self.file_full_path
        else:
            QMessageBox.warning(self, 'Preview', 'Internal error occurred. File path not set in preview')

    def disable_toolbar(self):
        self.toolbar.hide()