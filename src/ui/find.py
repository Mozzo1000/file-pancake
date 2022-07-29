from PyQt5.QtCore import Qt, QDir, QDirIterator
from PyQt5.QtWidgets import qApp, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFormLayout, QMainWindow, QLineEdit, QWidget, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView, QProgressDialog
import humanize

class FindWindow(QMainWindow):
    def __init__(self, parent, current_dir):
        super().__init__(parent)
        self.current_dir = current_dir
        self.parent = parent

        self.resize(650, 260)
        self.move(self.screen().geometry().center() - self.frameGeometry().center())

        self.setWindowTitle("Find files")

        layout = QVBoxLayout()
        form_layout = QFormLayout()
        bottom_layout = QHBoxLayout()
        widget = QWidget()

        find_button = QPushButton("Find")
        find_button.clicked.connect(self.find_files)
        find_button.setAutoDefault(True)

        self.files_found_label = QLabel()

        self.file_input = QLineEdit(self)
        self.file_input.returnPressed.connect(find_button.click)
        self.directory_input = QLineEdit(self)
        self.directory_input.setText(self.current_dir)
        self.directory_input.returnPressed.connect(find_button.click)
        self.directory_input.setCompleter(self.parent.completer)

        self.file_table = QTableWidget(0, 2)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setHorizontalHeaderLabels(("File name", "Size"))
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.verticalHeader().hide()
        self.file_table.setShowGrid(False)
        self.file_table.cellActivated.connect(self.open_file)

        form_layout.addRow("File name: ", self.file_input)
        form_layout.addRow("Directory: ", self.directory_input)
        form_layout.addRow(self.file_table)

        bottom_layout.addWidget(self.files_found_label)
        bottom_layout.addWidget(find_button)

        layout.addLayout(form_layout)
        layout.addLayout(bottom_layout)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def find_files(self):
        self.file_table.setRowCount(0)

        file_name = self.file_input.text()
        path = self.directory_input.text()
        self.current_dir = self.directory_input.text()

        if not file_name:
            file_name = "*"
        
        progress = QProgressDialog(self)
        progress.setAutoClose(True)
        progress.setWindowTitle("Searching..")
        progress.setRange(0, 0)
        progress.show()

        files = QDirIterator(path, ["*" + file_name + "*"], QDir.Files|QDir.NoSymLinks|QDir.NoDotAndDotDot, QDirIterator.Subdirectories)
        count = 0
        while files.hasNext():
            files.next()
            progress.setValue(count)
            progress.setLabelText(f"Found {count} files..")
            qApp.processEvents()
            if progress.wasCanceled():
                break

            size = files.fileInfo().size()

            file_name_item = QTableWidgetItem(files.fileName())
            file_name_item.setData(Qt.UserRole, files.filePath())
            file_name_item.setFlags(file_name_item.flags() ^ Qt.ItemIsEditable)

            file_size_item = QTableWidgetItem(humanize.naturalsize(size))
            file_size_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            file_size_item.setFlags(file_size_item.flags() ^ Qt.ItemIsEditable)

            row = self.file_table.rowCount()
            self.file_table.insertRow(row)
            self.file_table.setItem(row, 0, file_name_item)
            self.file_table.setItem(row, 1, file_size_item)
            count+=1

        self.files_found_label.setText(f"{count} file(s) found")
        progress.close()

    def open_file(self, row, column):
        item = self.file_table.item(row, 0)
        self.parent.run_or_open(item.data(Qt.UserRole))

