from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QMainWindow, QLineEdit, QWidget, QMessageBox
import os


class CreateFolderDialog(QMainWindow):
    def __init__(self, parent, dir):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedHeight(110)
        self.setMinimumWidth(350)
        self.dir = dir
        layout = QVBoxLayout()
        layout_buttons = QHBoxLayout()
        widget = QWidget()

        label = QLabel('New folder')
        self.dir_input = QLineEdit()
        self.dir_input.textChanged.connect(self.set_button_status)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)

        self.create_button = QPushButton('Create')
        self.create_button.clicked.connect(self.create_dir)
        self.create_button.setDisabled(True)

        layout.addWidget(label)
        layout.addWidget(self.dir_input)
        layout.addLayout(layout_buttons)
        layout_buttons.addWidget(cancel_button)
        layout_buttons.addWidget(self.create_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_dir(self):
        new_dir = QDir(self.dir)
        if not new_dir.exists(self.dir_input.text()):
            if new_dir.mkpath(self.dir_input.text()):
                self.close()
            else:
                QMessageBox.warning(self, '', 'Unknown error occurred')
        else:
            QMessageBox.information(self, '', 'A folder with this name already exists')
    
    def set_button_status(self):
        if len(self.dir_input.text()) > 0:
            self.create_button.setDisabled(False)
        else:
            self.create_button.setDisabled(True)
