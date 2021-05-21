from PyQt5.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit, QWidget, QVBoxLayout, QHeaderView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QDir
import os

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
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree.doubleClicked.connect(self.item_clicked)
                
        self.tree.setAnimated(True) # Closing folder animation
        self.tree.setIndentation(20)
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setExpandsOnDoubleClick(False)

        self.search_input = QLineEdit()
        self.search_input.setText(QDir.homePath())
        self.search_input.returnPressed.connect(self.search_enter)
        self.search_input.setFocusPolicy(Qt.NoFocus)

        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.tree)
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

    def search_enter(self):
        self.tree.setRootIndex(self.model.index(self.search_input.text()))
        
    def item_clicked(self, event):
        file_name = self.model.filePath(event)
        if os.path.isfile(file_name) or file_name.endswith('.app'):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))
        elif os.path.isdir(file_name):
            self.tree.setRootIndex(self.model.index(file_name))
            self.search_input.setText(file_name)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.tree.setRootIndex(self.tree.rootIndex().parent())
            self.search_input.setText(self.model.filePath(self.tree.rootIndex()))
