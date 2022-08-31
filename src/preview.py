from PyQt5.QtWidgets import QMessageBox, QWidget, QDockWidget
from PyQt5.QtCore import QFile, Qt, QFileInfo


class Preview():
    def __init__(self):
        super().__init__()
        self.preview_classes = {}

    def register_preview(self, preview_class):
        """Register a preview class.
           It will then be added to a list of available preview classes and be associated with the relevant file extensions.

        Args:
            preview_class (PreviewBase): Class which inherits PreviewBase
        """
        for item in preview_class.get_allowed_file_types():
            self.preview_classes[item] = preview_class.__class__
        print(self.preview_classes)
    
    def open_preview_window(self, parent_window, file_full_path):
        """Opens a preview window based on which extension the file_full_path has.
           Preview window is added as a dockable widget. A QMessageBox will be shown if there is no registered preview class for the supplied file type.

        Args:
            parent_window (QMainWindow): Parent window
            file_full_path (str): File path including filename and extension
        """
        file_info = QFileInfo(file_full_path)
        previewer = self.lookup_preview_from_ext(file_info.completeSuffix())
        if previewer:
            previewer = previewer()
            previewer.set_file(file_full_path)
            parent_window.addDockWidget(Qt.RightDockWidgetArea, previewer, Qt.Vertical)
        else:
            # Show a message box becuase 'previewer' returned None
            QMessageBox.information(parent_window, 'Preview', f'No preview available for files with extension {file_info.completeSuffix()}')

    def lookup_preview_from_ext(self, extension):
        """Lookup preview class based on extension

        Args:
            extension (str): File extension, eg jpg, mp4.. etc

        Returns:
            dict: Preview class
        """
        if extension in self.preview_classes:
            # Supplied extension has a registered preview class, return the class
            return self.preview_classes[extension]
        else:
            # A registered preview class can not be found, return None
            return None

    def get_extensions(self):
        return list(self.preview_classes.keys())