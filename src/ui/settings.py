from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox, \
    QListWidget, QWidget, QStackedWidget, QFormLayout, QSpinBox, \
    QGridLayout, QCheckBox
from PyQt5.QtCore import QSize, QSettings, QProcess, QCoreApplication
import sys

class SettingsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        self.settings = QSettings('pancake', 'app')
        self.main_widget = QWidget()
        self.layout = QGridLayout()

        self.stacked_widget = QStackedWidget(self)
        self.general_widget = QWidget(self)
        self.general_ui()

        self.statusbar_widget = QWidget(self)
        self.statusbar_ui()

        self.stacked_widget.addWidget(self.general_widget)
        self.stacked_widget.addWidget(self.statusbar_widget)

        settings_list = QListWidget(self)
        settings_list.currentRowChanged.connect(self.change_settings_view)
        settings_list.insertItem(0, 'General')
        settings_list.insertItem(1, 'Statusbar')
        settings_list.setSizeAdjustPolicy(QListWidget.AdjustToContents)

        save_btn = QPushButton('Save', self)
        save_btn.setToolTip('Save settings')
        save_btn.clicked.connect(self.save_settings)

        load_defaults_btn = QPushButton('Load defaults')
        load_defaults_btn.setToolTip('Load defaults')
        load_defaults_btn.clicked.connect(self.load_defaults)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setToolTip('Cancel any changes and close settings window')
        cancel_btn.clicked.connect(self.close)

        statusbar = self.statusBar()
        statusbar.addPermanentWidget(load_defaults_btn)
        statusbar.addPermanentWidget(cancel_btn)
        statusbar.addPermanentWidget(save_btn)

        self.layout.addWidget(settings_list, 0, 0)
        self.layout.addWidget(self.stacked_widget, 0, 1)
        self.main_widget.setLayout(self.layout)
        self.setStatusBar(statusbar)
        self.setCentralWidget(self.main_widget)

        self.load_settings()

    def general_ui(self):
        layout = QFormLayout()
        
        self.opened_panes_on_startup_input = QSpinBox(self)
        self.opened_panes_on_startup_input.setRange(1, 999)

        self.auto_open_preview_input = QCheckBox(self)

        layout.addRow("Directory panes on startup", self.opened_panes_on_startup_input)
        layout.addRow("Automatically open preview on left click", self.auto_open_preview_input)

        self.general_widget.setLayout(layout)

    def statusbar_ui(self):
        layout = QFormLayout()

        self.harddrive_update_input = QSpinBox(self)
        self.harddrive_update_input.setRange(1, 86400)
        
        layout.addRow("Harddrive usage update interval (in seconds)", self.harddrive_update_input)

        self.statusbar_widget.setLayout(layout)

    def change_settings_view(self, i):
        self.stacked_widget.setCurrentIndex(i)
    
    def load_settings(self):
        try:
            self.harddrive_update_input.setValue(self.settings.value('harddrive_update_interval'))
            self.opened_panes_on_startup_input.setValue(self.settings.value('opened_panes_on_startup'))
            self.auto_open_preview_input.setChecked(self.settings.value('auto_open_preview'))
        except TypeError:
            print("Failed to retrieve settings")
            QMessageBox.warning(self, "Settings - Error", "Failed to retrieve settings.\nReverting to default.")

    def load_defaults(self):
        self.settings.clear()
        self.settings.setValue('harddrive_update_interval', 300)
        self.settings.setValue('opened_panes_on_startup', 2)
        self.settings.setValue('auto_open_preview', False)
        self.show_restart_message()

    def save_settings(self):
        self.settings.setValue('harddrive_update_interval', self.harddrive_update_input.value())
        self.settings.setValue('opened_panes_on_startup', self.opened_panes_on_startup_input.value())
        self.settings.setValue('auto_open_preview', self.auto_open_preview_input.checkState())
        self.show_restart_message()

    def show_restart_message(self):
        message = QMessageBox(self)
        message.setWindowTitle('Settings')
        message.setText('Please restart the application for changes to take affect.')
        restart_btn = message.addButton('Restart', QMessageBox.YesRole)
        message.addButton('Cancel', QMessageBox.RejectRole)
        message.exec()
        if message.clickedButton() == restart_btn:
            QCoreApplication.quit()
            QProcess.startDetached(sys.executable, sys.argv)

