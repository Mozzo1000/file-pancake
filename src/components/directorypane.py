from PyQt5.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit, QWidget, QVBoxLayout, QHeaderView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class DirectoryPane(QDockWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle('Explorer')

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('/Users/mozzo/Desktop'))
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree.doubleClicked.connect(self.item_clicked)
                
        self.tree.setAnimated(True) # Closing folder animation
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setAlternatingRowColors(True)

        self.search_input = QLineEdit()
        self.search_input.setText('/Users/mozzo/Desktop')
        self.search_input.returnPressed.connect(self.search_enter)

        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.tree)
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

    def search_enter(self):
        self.tree.setRootIndex(self.model.index(self.search_input.text()))
        
    def item_clicked(self, event):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.model.filePath(event)))