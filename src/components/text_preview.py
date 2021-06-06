from PyQt5.QtWidgets import QWidget, QDockWidget, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from .preview_base import PreviewBase

class TextPreview(PreviewBase):
    def __init__(self):
        super().__init__()
        self.allowed_file_types = ['txt']

        self.label = QLabel()

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.label)
        scrollArea.setVisible(True)

        self.setWidget(scrollArea)
    
    def set_file(self, file_full_path):
        super().set_file(file_full_path)
        f = open(file_full_path, 'r')
        self.label.setText(f.read())
        f.close()
        self.label.adjustSize()