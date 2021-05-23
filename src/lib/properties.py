import sys
if sys.platform == 'win32':
    from lib.platform.properties_win import open_property_window_win
from PyQt5.QtWidgets import QMessageBox

class Properties():
    def __init__(self, parent_window, file_name):
        self.parent_window = parent_window
        self.file_name = file_name

    def open_window(self):
        if sys.platform == 'win32':
            open_property_window_win(self.file_name)
        else:
            QMessageBox.information(self.parent_window, '', f'Properties are currently not implemented on your system.\n System info: {sys.platform}')
