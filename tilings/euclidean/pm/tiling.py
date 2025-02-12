from PySide6.QtGui import QMatrix3x3, QVector2D
from PySide6.QtWidgets import QComboBox
from numpy import array
from numpy.linalg import inv

from tilings.euclidean.tiling import SHAPE_KEY_RECTANGLE, SHAPE_KEY_SQUARE
from tilings.euclidean.tiling import Tiling as AbstractTiling
from tilings.euclidean.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.euclidean.tiling import TilingOptions as AbstractTilingOptions

REFLECTION_X = 0
REFLECTION_Y = 1


class TilingDrawing(AbstractTilingDrawing):
    FRAGMENT_SHADER = "tilings/euclidean/pm/fragment.glsl"

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

        self._shape = SHAPE_KEY_RECTANGLE
        self._reflection = REFLECTION_X

        self.v1 = QVector2D(self.corners[1] - self.corners[0])
        self.v2 = QVector2D(self.corners[3] - self.corners[0])
        self.v3 = QVector2D(self.corners[2] - self.corners[0])

    @property
    def reflection(self):
        return self._reflection

    @reflection.setter
    def reflection(self, value):
        self._reflection = value
        self.update()

    def setup_uniforms(self):
        u1, u2 = self.translations(self.v1, self.v2, self.v3)

        self.program.setUniformValue("resolution", self.parent().resolution)

        if self.reflection == REFLECTION_Y:
            morph = array([
                [2 * u1.x(), u2.x(), 0],
                [2 * u1.y(), u2.y(), 0],
                [0, 0, 1]
            ])
        elif self.reflection == REFLECTION_X:
            morph = array([
                [u1.x(), 2 * u2.x(), 0],
                [u1.y(), 2 * u2.y(), 0],
                [0, 0, 1]
            ])
        else:
            raise Exception('This type of glide is not allowed')

        morph_inv = inv(morph)

        self.program.setUniformValue("morphInv", QMatrix3x3(morph_inv.flatten()))
        self.program.setUniformValue("similarity", QMatrix3x3(self.similarity().flatten()))
        self.program.setUniformValue("reflection", self.reflection)

        self.program.setUniformValue("tileCorner0", self.rescaled_corners[0])
        self.program.setUniformValue("tileCorner1", self.rescaled_corners[1])
        self.program.setUniformValue("tileCorner2", self.rescaled_corners[2])
        self.program.setUniformValue("tileCorner3", self.rescaled_corners[3])


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

        self.select_reflection = QComboBox()
        self.select_reflection.addItem("Axe des abscisses")
        self.select_reflection.addItem("Axe ordonnées")
        self.layout.addRow("Axe de la réflection", self.select_reflection)


class Tiling(AbstractTiling):
    CODE = 'pm (**)'
    SHAPE = "rectangle"
    CORNER_NB = 4
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions
    ALLOWED_SHAPES = [SHAPE_KEY_RECTANGLE, SHAPE_KEY_SQUARE]

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)

        self.options.select_reflection.currentIndexChanged.connect(self.update_reflection)

    def update_reflection(self, value):
        self.drawing.reflection = value
