from PySide6.QtGui import QMatrix3x3

from tilings.euclidean.tiling import Tiling as AbstractTiling
from tilings.euclidean.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.euclidean.tiling import TilingOptions as AbstractTilingOptions
from utils.triangles import apex_permutation_angle


class TilingDrawing(AbstractTilingDrawing):
    FRAGMENT_SHADER = "tilings/euclidean/p31m/fragment.glsl"

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

    def setup_uniforms(self):
        sigma = apex_permutation_angle(tuple(self.corners))

        self.program.setUniformValue("resolution", self.parent().resolution)
        self.program.setUniformValue("similarity", QMatrix3x3(self.similarity().flatten()))

        self.program.setUniformValue("tileCorner0", self.rescaled_corners[sigma[0]])
        self.program.setUniformValue("tileCorner1", self.rescaled_corners[sigma[1]])
        self.program.setUniformValue("tileCorner2", self.rescaled_corners[sigma[2]])


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)


class Tiling(AbstractTiling):
    CODE = 'p31m (3*3)'
    SHAPE = "triangle isocèle"
    CORNER_NB = 3
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)

    def update_shape(self, value):
        self.drawing.shape = value
