import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp
from PyQt5.QtCore import Qt
from components.directorypane import DirectoryPane

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Pancake')

        directory_pane = DirectoryPane(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, directory_pane)

        self.showMaximized()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())