from PyQt5.QtWidgets import QDockWidget, QFileSystemModel, QLabel, QTreeView, QLineEdit, QWidget, QVBoxLayout, QHeaderView, QMenu, QTreeWidget, QMessageBox, QShortcut, QCompleter, QStatusBar
from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtGui import QDesktopServices, QKeySequence
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel
import os
from ui.dialog import CreateFolderDialog
from send2trash import send2trash
from lib.properties import Properties
from components.drive_size import DriveSize
import pathlib
from ui.find import FindWindow

class DirectoryPane(QDockWidget):
    def __init__(self, parent, history, preview):
        super().__init__()
        self.parent = parent
        self.history = history
        self.preview = preview

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setReadOnly(True)
        self.model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(QHeaderView.Interactive)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tree.setSortingEnabled(True)
        self.tree.doubleClicked.connect(self.item_double_clicked)
        self.tree.clicked.connect(self.item_clicked)
                
        self.tree.setAnimated(True) # Closing folder animation
        self.tree.setIndentation(20)
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.tree.customContextMenuRequested.connect(self.customContextMenuEvent) 
        self.tree.itemDelegate().closeEditor.connect(self.onCloseEdit)

        self.search_input = QLineEdit()
        self.search_input.setText(QDir.homePath())
        self.search_input.returnPressed.connect(self.search_enter)
        self.search_input.setFocusPolicy(Qt.ClickFocus)
        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.search_input.setCompleter(self.completer)

        status = QStatusBar(self)
        status.setSizeGripEnabled(False)
        status.setStyleSheet("background-color: rgb(236,236,236);")
        self.drive_size_widget = DriveSize(self.get_current_dir())
        status.addPermanentWidget(self.drive_size_widget)

        find_shortcut = QShortcut(QKeySequence("CTRL+F"), self)
        find_shortcut.activated.connect(lambda: FindWindow(self, self.get_current_dir()).show())

        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(status)
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)
        self.tree.sortByColumn(0, 0)
        
        self.setWindowTitle(QDir(self.get_current_dir()).dirName())

    def onCloseEdit(self, editor):
        self.model.setReadOnly(True)

    def search_enter(self):
        self.tree.setRootIndex(self.model.index(self.search_input.text()))

    def run_or_open(self, file_name):
        if os.path.isfile(file_name) or file_name.endswith('.app'):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))
        elif os.path.isdir(file_name):
            self.tree.setRootIndex(self.model.index(file_name))
            self.search_input.setText(file_name)
            self.history.add_visit(self.model.filePath(self.model.index(file_name)))
            self.setWindowTitle(QDir(self.get_current_dir()).dirName())
            self.drive_size_widget.update_path(self.get_current_dir())
        
    def item_double_clicked(self, event):
        self.run_or_open(self.model.filePath(event))
    
    def item_clicked(self, event):
        if QSettings("pancake", "app").value('auto_open_preview'):
            path = self.model.filePath(event)
            ext = pathlib.Path(path).suffix.replace(".", "")
            if ext in self.preview.get_extensions():
                self.preview.open_preview_window(self.parent, path)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.tree.setRootIndex(self.tree.rootIndex().parent())
            self.search_input.setText(self.model.filePath(self.tree.rootIndex()))
            self.setWindowTitle(QDir(self.get_current_dir()).dirName())
            self.drive_size_widget.update_path(self.get_current_dir())
        if e.key() == Qt.Key_Return:
            if self.tree.selectionModel().selectedIndexes():
                self.run_or_open(self.model.filePath(self.tree.selectionModel().selectedIndexes()[0]))
    

    def customContextMenuEvent(self, event):
        contextMenu = QMenu(self)
        if self.tree.indexAt(event).data():
            open_action = contextMenu.addAction('Open')
            preview_action = contextMenu.addAction('Preview')
            rename_action = contextMenu.addAction('Rename')
            delete_action = contextMenu.addAction('Delete')
            contextMenu.addSeparator()
            properties_action = contextMenu.addAction('Properties')
            action = contextMenu.exec_(self.tree.mapToGlobal(event))
            if action is not None:
                if action == delete_action:
                    file_for_deletion = self.model.filePath(self.tree.indexAt(event))
                    question = QMessageBox.question(self, '', f'Do you really want to delete {file_for_deletion}', QMessageBox.Yes | QMessageBox.No)
                    if question == QMessageBox.Yes:
                        try:
                            send2trash(QDir.toNativeSeparators(file_for_deletion))
                            print(f'Deleted file {file_for_deletion}')
                        except send2trash.TrashPermissionError:
                            QMessageBox.warning(self, '', f'Permission error, unable to delete {file_for_deletion}')
                        except OSError:
                            QMessageBox.warning(self, '', f'Unkown error occurred, unable to delete {file_for_deletion}')
                if action == open_action:
                    self.run_or_open(self.model.filePath(self.tree.indexAt(event)))
                if action == properties_action:
                    properties_window = Properties(self, QDir.toNativeSeparators(self.model.filePath(self.tree.indexAt(event))))
                    properties_window.open_window()
                if action == preview_action:
                    self.preview.open_preview_window(self.parent, self.model.filePath(self.tree.indexAt(event)))
                if action == rename_action:
                    self.model.setReadOnly(False)
                    self.tree.edit(self.tree.indexAt(event))
        else:
            new_folder_action = contextMenu.addAction("New folder")
            action = contextMenu.exec_(self.tree.mapToGlobal(event))
            if action is not None:
                if action == new_folder_action:
                    dialog = CreateFolderDialog(self, self.search_input.text())
                    dialog.show()

    def get_current_dir(self):
        return self.model.filePath(self.tree.rootIndex())
