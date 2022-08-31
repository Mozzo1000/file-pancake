from PyQt5.QtWidgets import QLabel, QScrollArea, QAction, QTreeWidget, QTreeWidgetItem, QDockWidget
from PyQt5.QtCore import Qt
from .preview_base import PreviewBase
from docx2python import docx2python

class WordPreview(PreviewBase):
    def __init__(self):
        super().__init__()
        self.allowed_file_types = ['doc', 'docx']

        properties_button = QAction("Properties", self)
        properties_button.triggered.connect(self.show_properties)
        self._toolbar.addAction(properties_button)

        self.label = QLabel()
        self.label.setTextFormat(Qt.RichText)
        self.label.setWordWrap(True)


        scrollArea = QScrollArea()
        scrollArea.setWidget(self.label)
        scrollArea.setVisible(True)

        self.base.addWidget(scrollArea)
    
    def set_file(self, file_full_path):
        super().set_file(file_full_path)
        f = docx2python(file_full_path, html=True)

        self.label.setText(f.text)
        self.label.adjustSize()

    def show_properties(self):
        properties = docx2python(self.get_file_full_path()).core_properties
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle("Properties -" +  self.get_file_full_path())
        property_window = QTreeWidget()
        property_window.setHeaderLabels(["Property", "Value"])
        for key,value in properties.items():
            property_item = QTreeWidgetItem([key, value])
            property_window.addTopLevelItem(property_item)
        dock_widget.setWidget(property_window)
        self.base.addWidget(dock_widget)
        