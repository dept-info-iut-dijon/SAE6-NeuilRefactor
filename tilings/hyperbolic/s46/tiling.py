from PySide6.QtGui import QColor, QMatrix3x3, QVector2D, QVector4D
from PySide6.QtWidgets import QFormLayout, QLabel, QColorDialog, QPushButton
from numpy import array, pi
import OpenGL.GL as GL

from tilings.abstract.tiling import Tiling as AbstractTiling
from tilings.abstract.tiling import TilingDrawing as AbstractTilingDrawing
from tilings.abstract.tiling import TilingOptions as AbstractTilingOptions
from utils.polygon import Polygon
from utils.path_helper import get_resource_path

SCALE_MIN = 10
SCALE_MAX = 80
SCALE_DEFAULT = 40

BASE_SCALE = 0.02


class TilingDrawing(AbstractTilingDrawing):
    VERTEX_SHADER = get_resource_path("shaders/vertex.glsl")
    FRAGMENT_SHADER = get_resource_path("tilings/hyperbolic/s46/fragment.glsl")

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super(TilingDrawing, self).__init__(parent, path, img_size, corners)

    def initializeGL(self):
        super().initializeGL()
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def setup_uniforms(self):
        self.program.setUniformValue("resolution", self.parent().resolution)
        square = Polygon(4, pi / 3)
        ch_rho, sh_rho, ch_h, sh_h, ch_ell, sh_ell = square.lengths
        ch2 = ch_h * ch_h + sh_h * sh_h
        sh2 = 2 * sh_h * ch_h

        self.program.setUniformValue("iterations", 100)
        self.program.setUniformValue("tileData", QVector2D(ch_rho, sh_rho))

        shiftXP = array([
            [ch2, 0, sh2],
            [0, 1, 0],
            [sh2, 0, ch2]
        ]).flatten()
        shiftXN = array([
            [ch2, 0, -sh2],
            [0, 1, 0],
            [-sh2, 0, ch2]
        ]).flatten()
        shiftYP = array([
            [1, 0, 0],
            [0, ch2, sh2],
            [0, sh2, ch2]
        ]).flatten()
        shiftYN = array([
            [1, 0, 0],
            [0, ch2, -sh2],
            [0, -sh2, ch2]
        ]).flatten()
        isometry = array([
            [ch_ell, sh_ell * sh_h, -sh_ell * ch_h],
            [0, ch_h, -sh_h],
            [-sh_ell, -ch_ell * sh_h, ch_ell * ch_h]
        ]).transpose().flatten()

        self.program.setUniformValue("shiftXP", QMatrix3x3(shiftXP))
        self.program.setUniformValue("shiftXN", QMatrix3x3(shiftXN))
        self.program.setUniformValue("shiftYP", QMatrix3x3(shiftYP))
        self.program.setUniformValue("shiftYN", QMatrix3x3(shiftYN))
        self.program.setUniformValue("isometry", QMatrix3x3(isometry))

        self.program.setUniformValue("tileCorner0", self.rescaled_corners[0])
        self.program.setUniformValue("tileCorner1", self.rescaled_corners[1])
        self.program.setUniformValue("tileCorner2", self.rescaled_corners[2])
        self.program.setUniformValue("tileCorner3", self.rescaled_corners[3])

        bg_color = self.parent().background_color
        self.program.setUniformValue("backgroundColor", 
            QVector4D(bg_color.redF(), bg_color.greenF(), bg_color.blueF(), bg_color.alphaF()))


class TilingOptions(AbstractTilingOptions):
    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

        self.setMinimumWidth(parent.resolution.width())

        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.background_color_button = QPushButton("Choisir la couleur de fond")
        self.background_color_button.clicked.connect(self.choose_background_color)
        self.color_dialog = QColorDialog()
        self.color_dialog.setOption(QColorDialog.ShowAlphaChannel)
        self.layout.addRow("Couleur de fond:", self.background_color_button)

    def choose_background_color(self):
        self.color_dialog.setCurrentColor(self.parent().background_color)
        
        if self.color_dialog.exec() == QColorDialog.Accepted:
            color = self.color_dialog.currentColor()
            print(f"Couleur sélectionnée : {color.name()}")
            self.parent().background_color = color
            self.parent().drawing.setup_uniforms()
            self.parent().drawing.update()
        else:
            print("Aucune couleur valide sélectionnée.")


class Tiling(AbstractTiling):
    KIND = 'Pavage hyperbolique'
    CODE = '{4,6}'
    SHAPE = "carré"
    CORNER_NB = 4
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions

    def __init__(self, path, img_size, corners, resolution=None):
        super(Tiling, self).__init__(path, img_size, corners, resolution)
        self.background_color = QColor(255, 255, 255, 255)