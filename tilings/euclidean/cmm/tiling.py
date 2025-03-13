from PySide6.QtGui import QMatrix3x3, QVector2D
from numpy import array
from numpy.linalg import inv

from tilings.euclidean.tiling import SHAPE_KEY_PARALLELOGRAM
from tilings.euclidean.tiling import Tiling as AbstractTiling
from tilings.euclidean.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.euclidean.tiling import TilingOptions as AbstractTilingOptions
from utils.quandrangles import reflect
from utils.triangles import apex_permutation_angle
from utils.path_helper import get_resource_path

class TilingDrawing(AbstractTilingDrawing):
    FRAGMENT_SHADER = get_resource_path("tilings/euclidean/cmm/fragment.glsl")

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

        self._shape = SHAPE_KEY_PARALLELOGRAM

    def setup_uniforms(self):
        sigma = apex_permutation_angle(tuple(self.corners))
        v1 = QVector2D(self.corners[sigma[1]] - self.corners[sigma[0]])
        v2 = QVector2D(self.corners[sigma[2]] - self.corners[sigma[0]])

        v1 = reflect(v1)
        v2 = reflect(v2)

        u1 = v1 + v2
        u2 = v1 - v2
        u1 = u1 / u1.length()
        u2 = u2 / u2.length()

        self.program.setUniformValue("resolution", self.parent().resolution)
        morph = array([
            [u1.x(), u2.x(), 0],
            [u1.y(), u2.y(), 0],
            [0, 0, 1]
        ])

        morph_inv = inv(morph)

        self.program.setUniformValue("morphInv", QMatrix3x3(morph_inv.flatten()))
        self.program.setUniformValue("similarity", QMatrix3x3(self.similarity().flatten()))

        self.program.setUniformValue("tileCorner0", self.rescaled_corners[sigma[0]])
        self.program.setUniformValue("tileCorner1", self.rescaled_corners[sigma[1]])
        self.program.setUniformValue("tileCorner2", self.rescaled_corners[sigma[2]])


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)


class Tiling(AbstractTiling):
    CODE = 'cmm (2*22)'
    SHAPE = "triangle rectangle"
    CORNER_NB = 3
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions
    ALLOWED_SHAPES = []

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)
