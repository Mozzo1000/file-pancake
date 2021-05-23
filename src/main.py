import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut, qApp, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from components.directorypane import DirectoryPane
from history import History

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Pancake')

        self.history = History()

        directory_pane = DirectoryPane(self, self.history)
        self.addDockWidget(Qt.LeftDockWidgetArea, directory_pane)

        self.create_menu()

        self.showMaximized()
        self.show()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = QMenu('&File', self)
        window_menu = QMenu('&Window', self)

        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)

        new_explorer_window_action = QAction('&New pane window', self)
        new_explorer_window_action.triggered.connect(self.new_explorer_window)
        new_explorer_window_action.setShortcut(QKeySequence('CTRL+N'))


        file_menu.addAction(exit_action)
        window_menu.addAction(new_explorer_window_action)


        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(window_menu)

    def new_explorer_window(self):
        directory_pane = DirectoryPane(self)
        self.addDockWidget(Qt.RightDockWidgetArea, directory_pane)

    def closeEvent(self, event):
        self.history.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())