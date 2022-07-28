from PyQt5.QtWidgets import QLabel, QScrollArea
from .preview_base import PreviewBase
from docx2python import docx2python

class WordPreview(PreviewBase):
    def __init__(self):
        super().__init__()
        self.allowed_file_types = ['doc', 'docx']

        self.label = QLabel()

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.label)
        scrollArea.setVisible(True)

        self.base.addWidget(scrollArea)
    
    def set_file(self, file_full_path):
        super().set_file(file_full_path)
        f = docx2python(file_full_path, html=True)
        print(f.body)


        self.label.setText(f.text)
        self.label.adjustSize()