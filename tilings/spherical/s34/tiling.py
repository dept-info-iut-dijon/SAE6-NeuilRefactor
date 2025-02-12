from PySide6.QtGui import QMatrix3x3, QVector2D
from numpy import array, cos, sin

from tilings.spherical.tiling import Tiling as AbstractTiling
from tilings.spherical.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.spherical.tiling import TilingOptions as AbstractTilingOptions
from utils.path_helper import get_resource_path

class TilingDrawing(AbstractTilingDrawing):
    VERTEX_SHADER = get_resource_path("shaders/vertex.glsl")
    FRAGMENT_SHADER = get_resource_path("tilings/spherical/s34/fragment.glsl")

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

    def setup_uniforms(self):
        self.program.setUniformValue("sphereData", QVector2D(10, 2))
        self.program.setUniformValue("resolution", self.parent().resolution)

        shiftXP = array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ])
        shiftXN = array([
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0]
        ])
        shiftYP = array([
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0]
        ])
        shiftYN = array([
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0]
        ])
        shiftZP = array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        shiftZN = array([
            [0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1]
        ])

        c1 = cos(self.angles[0])
        s1 = sin(self.angles[0])
        rot1 = array([
            [c1, 0, -s1],
            [0, 1, 0],
            [s1, 0, c1]
        ])
        c2 = cos(self.angles[1])
        s2 = sin(self.angles[1])
        rot2 = array([
            [1, 0, 0],
            [0, c2, -s2],
            [0, s2, c2]
        ])
        isom = rot1 @ rot2

        self.program.setUniformValue("shiftXP", QMatrix3x3(shiftXP.flatten()))
        self.program.setUniformValue("shiftXN", QMatrix3x3(shiftXN.flatten()))
        self.program.setUniformValue("shiftYP", QMatrix3x3(shiftYP.flatten()))
        self.program.setUniformValue("shiftYN", QMatrix3x3(shiftYN.flatten()))
        self.program.setUniformValue("shiftZP", QMatrix3x3(shiftZP.flatten()))
        self.program.setUniformValue("shiftZN", QMatrix3x3(shiftZN.flatten()))
        self.program.setUniformValue("isometry", QMatrix3x3(isom.flatten()))

        self.program.setUniformValue("tileCorner0", self.rescaled_corners[0])
        self.program.setUniformValue("tileCorner1", self.rescaled_corners[1])
        self.program.setUniformValue("tileCorner2", self.rescaled_corners[2])


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)


class Tiling(AbstractTiling):
    CODE = '{3,4}'
    SHAPE = "triangle équilatéral"
    CORNER_NB = 3
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)
