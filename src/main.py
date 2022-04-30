import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut, qApp, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QKeySequence, QIcon
from components.directorypane import DirectoryPane
from history import History
from preview import Preview
from components.text_preview import TextPreview
from ui.settings import SettingsWindow
from ui.changedir import ChangeDirWindow

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Pancake')

        self.history = History()
        self.preview = Preview()
        self.preview.register_preview(TextPreview())
        if QSettings("pancake", "app").contains('opened_panes_on_startup'):
            for i in range(QSettings("pancake", "app").value('opened_panes_on_startup')):
                self.create_pane()
        else:
            self.create_pane()

        self.create_menu()
        
        self.showMaximized()
        self.show()

    def create_pane(self):
        directory_pane = DirectoryPane(self, self.history, self.preview)
        self.addDockWidget(Qt.LeftDockWidgetArea, directory_pane)

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = QMenu('&File', self)
        window_menu = QMenu('&Window', self)

        open_settings_action = QAction('&Settings', self)
        open_settings_action.setStatusTip('Open settings')
        open_settings_action.triggered.connect(self.open_settings)

        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)

        new_explorer_window_action = QAction('&New pane window', self)
        new_explorer_window_action.triggered.connect(self.create_pane)
        new_explorer_window_action.setShortcut(QKeySequence('CTRL+N'))

        open_quick_search = QAction('&Open quich search', self)
        open_quick_search.triggered.connect(self.open_change_dir_window)
        open_quick_search.setShortcut(QKeySequence('CTRL+P'))

        file_menu.addAction(open_settings_action)
        file_menu.addAction(exit_action)
        window_menu.addAction(new_explorer_window_action)
        window_menu.addAction(open_quick_search)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(window_menu)

    def open_change_dir_window(self):
        change_dir_window = ChangeDirWindow(QApplication.focusWidget().parent().parent(), self.history.get_history())
        change_dir_window.show()
    
    def focus_changed(self):
        print("YES")

    def closeEvent(self, event):
        self.history.conn.close()
    
    def open_settings(self):
        settings = SettingsWindow(self)
        settings.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    app.setQuitOnLastWindowClosed(False)

    def focus():
        gui.setWindowState(gui.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        gui.show()
        gui.activateWindow()
        gui.raise_()

    icon = QIcon("icon.png")
    tray = QSystemTrayIcon()
    tray.activated.connect(focus)
    tray.setIcon(icon)
    tray.setVisible(True)
    
    menu = QMenu()
    open_window = QAction("Open")
    open_window.triggered.connect(focus)
    menu.addAction(open_window)

    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    
    tray.setContextMenu(menu)

    sys.exit(app.exec_())