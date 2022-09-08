from PyQt5.QtWidgets import QWidget, QDockWidget, QLabel, QScrollArea, QSizePolicy, QSlider
from PyQt5.QtGui import QPalette, QImage, QPixmap
from PyQt5.QtCore import Qt
from .preview_base import PreviewBase

class ImagePreview(PreviewBase):
    def __init__(self):
        super().__init__()
        self.allowed_file_types = ['png', 'jpg', 'jpeg', 'bmp', 'gif']

        self.label = QLabel()
        self.label.setBackgroundRole(QPalette.Base)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setScaledContents(True)

        self.scale_factor = 0.5

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMaximum(125)
        self.zoom_slider.setMinimum(0)
        self.zoom_slider.setValue(int(self.scale_factor * 100))
        self.zoom_slider.setTickPosition(QSlider.TicksAbove)
        self.zoom_slider.setTickInterval(5)
        self.zoom_slider.valueChanged.connect(self.on_zoom)
        self._toolbar.addWidget(self.zoom_slider)


        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.label)
        self.scrollArea.setVisible(True)

        self.base.addWidget(self.scrollArea)

    def scale_image(self, factor):
        self.scale_factor = factor
        self.label.resize(self.scale_factor * self.label.pixmap().size())
        self.scrollArea.horizontalScrollBar().setValue(int(factor * self.scrollArea.horizontalScrollBar().value() + ((factor - 1) * self.scrollArea.horizontalScrollBar().pageStep() / 2)))
        self.scrollArea.verticalScrollBar().setValue(int(factor * self.scrollArea.verticalScrollBar().value() + ((factor - 1) * self.scrollArea.verticalScrollBar().pageStep() / 2)))
    
    def on_zoom(self):
        self.scale_image(float(self.zoom_slider.value() / 10 ** 2))

    def set_file(self, file_full_path):
        super().set_file(file_full_path)
        image = QImage(file_full_path)
        self.label.setPixmap(QPixmap.fromImage(image))
        self.scale_image(self.scale_factor)