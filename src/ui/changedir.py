from PyQt5.QtCore import QStringListModel, Qt, QItemSelectionModel
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QPushButton, QVBoxLayout, QMainWindow, QLineEdit, QWidget, QMessageBox, QCompleter, QListWidgetItem, QListWidget

class ChangeDirWindow(QMainWindow):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.data = data
        self.parent = parent
        layout = QVBoxLayout()
        widget = QWidget()

        dir_input = QLineEdit()
        dir_input.textChanged.connect(self.search_changed)

        self.listwidget = QListWidget()
        self.populate_list()
        self.listwidget.setCurrentRow(0, QItemSelectionModel.Select)

        layout.addWidget(dir_input)
        layout.addWidget(self.listwidget)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Return:
            print(self.listwidget.selectedItems())
            self.parent.run_or_open(self.listwidget.selectedItems()[0].text())
            self.close()

    def populate_list(self):
        for i in self.data:
            item = QListWidgetItem(i[0])
            self.listwidget.addItem(item)

    def search_changed(self, event):
        items = self.listwidget.findItems(event, Qt.MatchRegularExpression)
        for x in range(self.listwidget.count()):
            self.listwidget.item(x).setHidden(True)
        for item in items:
            item.setHidden(False)
            item.setSelected(True)
