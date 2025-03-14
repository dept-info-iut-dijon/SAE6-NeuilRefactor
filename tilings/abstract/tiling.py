from abc import abstractmethod
from typing import List
from OpenGL import GL
from PySide6.QtCore import QSize, QPointF
from PySide6.QtGui import QImage
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLTexture
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from numpy import array, float32
from utils.path_helper import get_resource_path


class TilingOptions(QWidget):
    """ Classe définissant les options de configuration du pavage. """

    def __init__(self, parent: 'Tiling'):
        super(TilingOptions, self).__init__(parent)

    @classmethod
    def init(cls, parent):
        return cls(parent)


class TilingDrawing(QOpenGLWidget):
    """
    Classe gérant l'affichage du pavage et l'intégration OpenGL.
    """

    VERTEX_SHADER = get_resource_path("")
    FRAGMENT_SHADER = get_resource_path("")

    def __init__(self, parent: 'Tiling', path, img_size, corners):
        super().__init__(parent)

        self.setMinimumSize(parent.resolution)
        self.img = QImage(path)
        self.img_size = img_size
        self.corners = corners

        self.rescaled_corners = [QPointF(p.x() / img_size.width(), p.y() / img_size.height()) for p in self.corners]

        self.vao = None
        self.program = None
        self.vertex_buffer = None
        self.texture = None

    @classmethod
    def init(cls, parent, path, img_size, corners):
        return cls(parent, path, img_size, corners)

    def initializeGL(self):
        """ Initialise OpenGL et réinitialise les buffers si nécessaire. """
        self.makeCurrent()

        self.cleanupGL()

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

    def cleanupGL(self):
        """ Libère proprement les ressources OpenGL pour éviter les crashs après fermeture. """
        if self.vertex_buffer:
            GL.glDeleteBuffers(1, [self.vertex_buffer])
            self.vertex_buffer = None
        if self.texture:
            self.texture.destroy()
            self.texture = None
        if self.program:
            self.program.release()
            self.program = None
        if self.vao:
            GL.glDeleteVertexArrays(1, [self.vao])
            self.vao = None

    @abstractmethod
    def setup_uniforms(self):
        raise Exception("This method must be implemented by subclasses")

    def paintGL(self):
        """ Effectue le rendu OpenGL du pavage. """
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
    """
    Classe principale définissant un pavage avec une gestion dynamique des sommets.
    """

    SHAPE = ''
    CORNER_NB = 0
    CODE = ''
    KIND = 'Abstract Tiling Class'
    DRAWING_CLASS = TilingDrawing
    OPTIONS_CLASS = TilingOptions

    def __init__(self, path, img_size: QSize, corners: List[QPointF], resolution=None):
        super().__init__()

        self.resolution = resolution if resolution is not None else QSize(600, 600)
        self.setWindowTitle(self.KIND)
        
        self.export_button = QPushButton("Exporter l'image", self)
        self.export_button.clicked.connect(self.export_image)

        self.options = self.OPTIONS_CLASS.init(self)
        self.drawing = self.DRAWING_CLASS.init(self, path, img_size, corners)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.drawing)
        self.layout.addWidget(self.options)
        self.layout.addWidget(self.export_button)
        
    def export_image(self):
        """
        Capture l'image du pavage et l'enregistre sous forme d'image.
        """ 
        return #To-Do

    def reset_tiling(self, new_corners):
        """
        Réinitialise le pavage lorsqu'un changement du nombre de sommets est détecté.
        """
        if not new_corners:
            print("⚠️ Aucun point défini. Réinitialisation annulée.")
            return

        if len(new_corners) != self.CORNER_NB:
            print(f"🔄 Mise à jour du pavage : {self.CORNER_NB} → {len(new_corners)} sommets")

            self.CORNER_NB = len(new_corners)

            self.drawing.makeCurrent()
            self.drawing.cleanupGL()
            self.drawing.initializeGL()
            self.drawing.doneCurrent()

        self.drawing.corners = new_corners
        self.drawing.rescaled_corners = [
            QPointF(p.x() / self.drawing.img_size.width(), p.y() / self.drawing.img_size.height())
            for p in new_corners
        ]
        self.drawing.update()

    def closeEvent(self, event):
        """ Nettoie les ressources OpenGL avant la fermeture de la fenêtre. """
        if self.drawing:
            self.drawing.makeCurrent()
            self.drawing.cleanupGL()
            self.drawing.doneCurrent()
        event.accept()

    @classmethod
    def init(cls, path, img_size, corners, resolution=None):
        return cls(path, img_size, corners, resolution)