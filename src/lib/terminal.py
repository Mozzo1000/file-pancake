import sys

if sys.platform == 'win32':
    from lib.platform.terminal_win import open_terminal_window_win
from PyQt5.QtWidgets import QMessageBox

class Terminal():
    def __init__(self, parent_window, path):
        self.parent_window = parent_window
        self.path = path

    def open_window(self):
        if sys.platform == 'win32':
            open_terminal_window_win(self.path)
        else:
            QMessageBox.information(self.parent_window, '', f'Open terminal is currently not implemented on your system.\n System info: {sys.platform}')
