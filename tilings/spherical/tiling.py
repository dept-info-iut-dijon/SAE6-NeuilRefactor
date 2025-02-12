from abc import abstractmethod

from PySide6.QtCore import Qt, Slot, QElapsedTimer, QTimer
from PySide6.QtWidgets import QSlider, QFormLayout
from numpy import array, pi

from tilings.abstract.tiling import Tiling as AbstractTiling
from tilings.abstract.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.abstract.tiling import TilingOptions as AbstractTilingOptions
from utils.path_helper import get_resource_path

SPEED1_MIN = 10
SPEED1_MAX = 80
SPEED1_DEFAULT = 40

SPEED2_MIN = 10
SPEED2_MAX = 80
SPEED2_DEFAULT = 40

BASE_SPEED = 0.0005


class TilingDrawing(AbstractTilingDrawing):
    VERTEX_SHADER = get_resource_path("shaders/vertex.glsl")
    FRAGMENT_SHADER = get_resource_path("tilings/hyperbolic/s46/fragment.glsl")

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

        self.angles = array([0., 0.])
        self._speed1 = SPEED1_DEFAULT
        self._speed2 = SPEED2_DEFAULT

        self.timer = None
        self.e_timer = QElapsedTimer()

    @property
    def speed1(self):
        return self._speed1

    @speed1.setter
    def speed1(self, value):
        self._speed1 = value
        self.update()

    @property
    def speed2(self):
        return self._speed2

    @speed2.setter
    def speed2(self, value):
        self._speed2 = value
        self.update()

    def initializeGL(self):
        super().initializeGL()
        self.play()

    @Slot()
    def update_angles(self):
        self.angles += BASE_SPEED * array([self.speed1, self.speed2])
        self.angles %= 2 * pi
        self.update()

    def play(self):
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_angles)
        if not self.timer.isActive():
            self.timer.start(25)

    @abstractmethod
    def setup_uniforms(self):
        raise Exception("This method must be implemented by subclasses")


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

        self.setMinimumWidth(parent.resolution.width())

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.speed1_slider = QSlider()
        self.speed1_slider.setOrientation(Qt.Orientation.Horizontal)
        self.speed1_slider.setMinimum(SPEED1_MIN)
        self.speed1_slider.setMaximum(SPEED1_MAX)
        self.speed1_slider.setValue(SPEED1_DEFAULT)
        self.layout.addRow("Vitesse de rotation axe 1", self.speed1_slider)

        self.speed2_slider = QSlider()
        self.speed2_slider.setOrientation(Qt.Orientation.Horizontal)
        self.speed2_slider.setMinimum(SPEED2_MIN)
        self.speed2_slider.setMaximum(SPEED2_MAX)
        self.speed2_slider.setValue(SPEED2_DEFAULT)
        self.layout.addRow("Vitesse de rotation axe 2", self.speed2_slider)


class Tiling(AbstractTiling):
    KIND = 'Pavage sphérique'

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)

        self.options.speed1_slider.valueChanged.connect(self.update_speed1)
        self.options.speed2_slider.valueChanged.connect(self.update_speed2)

    def update_speed1(self, value):
        self.drawing.speed1 = value

    def update_speed2(self, value):
        self.drawing.speed2 = value
