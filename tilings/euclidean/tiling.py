from abc import abstractmethod
from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QVector2D
from PySide6.QtWidgets import QSlider, QFormLayout, QDial, QComboBox
from numpy import array, cos, sin, pi, ndarray

from tilings.abstract.tiling import Tiling as AbstractTiling
from tilings.abstract.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.abstract.tiling import TilingOptions as AbstractTilingOptions
from utils.quandrangles import parallelogram, rectangle, square, reflect

SCALE_MIN = 10
SCALE_MAX = 80
SCALE_DEFAULT = 40
BASE_SCALE = 0.1

SHAPE_KEY_PARALLELOGRAM = 0
SHAPE_KEY_RECTANGLE = 1
SHAPE_KEY_SQUARE = 2

SHAPES_NAME = {
    SHAPE_KEY_PARALLELOGRAM: 'parallelogram',
    SHAPE_KEY_RECTANGLE: 'rectangle',
    SHAPE_KEY_SQUARE: 'square'
}


class TilingDrawing(AbstractTilingDrawing):
    VERTEX_SHADER = "shaders/vertex.glsl"
    FRAGMENT_SHADER = ""

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

        self._shape = None
        self._scale = SCALE_DEFAULT
        self._angle = 0

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def similarity(self) -> ndarray:
        """
        Return the similarity applied to the picture before computing the tiling
        """
        a = BASE_SCALE * self.scale
        homothety = array([
            [a, 0, 0],
            [0, a, 0],
            [0, 0, 1]
        ])

        alpha = pi * self.angle / 180
        c = cos(alpha)
        s = sin(alpha)
        rotation = array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
        return homothety @ rotation

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value
        self.update()

    def translations(self, v1: QVector2D, v2: QVector2D, v3: QVector2D) -> Tuple[QVector2D, QVector2D]:
        if self.shape == SHAPE_KEY_PARALLELOGRAM:
            u1, u2, _ = parallelogram(v1, v2, v3)
        elif self.shape == SHAPE_KEY_RECTANGLE:
            u1, u2, _ = rectangle(v1, v2, v3)
        elif self.shape == SHAPE_KEY_SQUARE:
            u1, u2, _ = square(v1, v2, v3)
        else:
            raise Exception("This shape is not supported")

        u1 = reflect(u1)
        u2 = reflect(u2)
        n = 1 / u1.length()
        return n * u1, n * u2

    @abstractmethod
    def setup_uniforms(self):
        raise Exception("This method must be implemented by subclasses")


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

        self.setMinimumWidth(parent.resolution.width())
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Créer d'abord tous les widgets
        self.scale_slider = QSlider()
        self.scale_slider.setOrientation(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(SCALE_MIN)
        self.scale_slider.setMaximum(SCALE_MAX)
        self.scale_slider.setValue(SCALE_DEFAULT)

        self.angle_dial = QDial()
        self.angle_dial.setRange(0, 360)

        self.select_shape = QComboBox()
        
        # Puis les ajouter au layout avec les traductions
        self.layout.addRow(self.window().tr('scale'), self.scale_slider)
        self.layout.addRow(self.window().tr('rotation'), self.angle_dial)
        
        # Remplir le combobox des formes si nécessaire
        if hasattr(parent, 'ALLOWED_SHAPES'):
            for key in parent.ALLOWED_SHAPES:
                self.select_shape.addItem(self.window().tr(SHAPES_NAME[key]), key)


class Tiling(AbstractTiling):
    KIND = 'pavage_euclidien'
    ALLOWED_SHAPES = []

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)

        self.options.scale_slider.valueChanged.connect(self.update_scale)
        self.options.angle_dial.valueChanged.connect(self.update_angle)

        if len(self.ALLOWED_SHAPES) > 1:
            self.options.layout.addRow(self.window().tr('shape'), self.options.select_shape)
            self.options.select_shape.currentIndexChanged.connect(self.update_shape)

    def update_scale(self, value):
        self.drawing.scale = value

    def update_angle(self, value):
        self.drawing.angle = value

    def update_shape(self, value):
        self.drawing.shape = self.options.select_shape.itemData(value)
