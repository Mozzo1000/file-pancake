from PyQt5.QtWidgets import QWidget, QDockWidget
from PyQt5.QtCore import Qt

class PreviewBase(QDockWidget):
    def __init__(self):
        super().__init__()
        # List of file extensions allowed to use the preview window, write extension without leading dot.
        self.allowed_file_types = []

    def get_allowed_file_types(self):
        """Get all file types

        Returns:
            dict: Allowed file types
        """
        return self.allowed_file_types

    def set_file(self, file_full_path):
        self.setWindowTitle(f'Preview - {file_full_path}')