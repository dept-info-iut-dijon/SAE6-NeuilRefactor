from abc import abstractmethod
from typing import List

from OpenGL import GL
from PySide6.QtCore import QSize, QPointF
from PySide6.QtGui import QImage
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLTexture
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout
from numpy import array, float32


class TilingOptions(QWidget):

    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

    @classmethod
    def init(cls, parent):
        return cls(parent)


class TilingDrawing(QOpenGLWidget):
    VERTEX_SHADER = ""
    FRAGMENT_SHADER = ""

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super().__init__(parent)

        self.setMinimumSize(parent.resolution)
        self.img = QImage(path)
        self.img_size = img_size
        self.corners = corners

        self.rescaled_corners = []
        for p in self.corners:
            rescaled_p = QPointF(
                p.x() / img_size.width(),
                p.y() / img_size.height()
            )
            self.rescaled_corners.append(rescaled_p)

        self.vao = None
        self.program = None
        self.vertex_buffer = None
        self.texture = None

    @classmethod
    def init(cls, parent, path, img_size, corners):
        return cls(parent, path, img_size, corners)

    def initializeGL(self):
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, self.VERTEX_SHADER)
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, self.FRAGMENT_SHADER)
        self.program.link()

        vertices = array([
            -1, -1,
            1, -1,
            1, 1,
            1, 1,
            -1, 1,
            -1, -1
        ], dtype=float32)

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices.tobytes(), GL.GL_STATIC_DRAW)

        GL.glClearColor(0.2, 0.2, 0.2, 1.0)

        self.texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        self.texture.create()
        self.texture.bind()

        self.texture.setData(self.img)
        self.texture.setMinMagFilters(QOpenGLTexture.Linear, QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.DirectionS, QOpenGLTexture.Repeat)
        self.texture.setWrapMode(QOpenGLTexture.DirectionT, QOpenGLTexture.Repeat)

    @abstractmethod
    def setup_uniforms(self):
        raise Exception("This method must be implemented by subclasses")

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.program.bind()
        position_attr = self.program.attributeLocation("in_vert")
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buffer)
        self.program.enableAttributeArray(position_attr)
        self.program.setAttributeBuffer(position_attr, GL.GL_FLOAT, 0, 2, 0)

        self.setup_uniforms()

        self.program.setUniformValue('tileTexture', 0)
        self.texture.bind()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        GL.glDisableVertexAttribArray(position_attr)
        self.program.release()


class Tiling(QWidget):
    SHAPE = ''
    CORNER_NB = 0
    CODE = ''
    KIND = 'Abstract Tiling Class'
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions

    def __init__(self, path, img_size: QSize, corners: List[QPointF], resolution=None):
        super().__init__()
        self.current_language = 'fr'  # Langue par défaut
        
        self.resolution = resolution if resolution is not None else QSize(600, 600)
        # Traduire le titre en fonction de la langue courante
        kind = self.KIND.lower().replace(' ', '_')
        self.setWindowTitle(self.tr(kind))

        self.options = self.OPTIONS_CLASS.init(self)
        self.drawing = self.DRAWING_CLASS.init(self, path, img_size, corners)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.drawing)
        self.layout.addWidget(self.options)

    def tr(self, key):
        """Fonction helper pour obtenir la traduction"""
        from main import translations  # Import ici pour éviter l'import circulaire
        return translations[self.current_language].get(key, key)

    @classmethod
    def init(cls, path, img_size, corners, resolution=None):
        return cls(path, img_size, corners, resolution)

    def update_translations(self):
        """Met à jour toutes les traductions de l'interface"""
        # Mettre à jour le titre de la fenêtre
        self.setWindowTitle(self.tr(self.KIND))
        
        # Mettre à jour les options
        if hasattr(self.options, 'scale_slider'):
            self.options.layout.labelForField(self.options.scale_slider).setText(self.tr('scale'))
        
        if hasattr(self.options, 'angle_dial'):
            self.options.layout.labelForField(self.options.angle_dial).setText(self.tr('rotation'))
            
        if hasattr(self.options, 'select_shape'):
            self.options.layout.labelForField(self.options.select_shape).setText(self.tr('shape'))
            # Mettre à jour les items du combobox
            if hasattr(self, 'ALLOWED_SHAPES'):  # Vérifier si la classe a des formes autorisées
                from tilings.euclidean.tiling import SHAPES_NAME  # Import local
                self.options.select_shape.clear()
                for key in self.ALLOWED_SHAPES:
                    self.options.select_shape.addItem(self.tr(SHAPES_NAME[key]), key)
                
        if hasattr(self.options, 'select_rotation'):
            self.options.layout.labelForField(self.options.select_rotation).setText(self.tr('rotation_direction'))
            self.options.select_rotation.setItemText(0, self.tr('x_axis'))
            self.options.select_rotation.setItemText(1, self.tr('y_axis'))
            
        if hasattr(self.options, 'select_reflection'):
            self.options.layout.labelForField(self.options.select_reflection).setText(self.tr('reflection_axis'))
            self.options.select_reflection.setItemText(0, self.tr('x_axis'))
            self.options.select_reflection.setItemText(1, self.tr('y_axis'))
            
        if hasattr(self.options, 'select_glide'):
            self.options.layout.labelForField(self.options.select_glide).setText(self.tr('glide_axis'))
            self.options.select_glide.setItemText(0, self.tr('x_axis'))
            self.options.select_glide.setItemText(1, self.tr('y_axis'))
