from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap, QImage
import os

class DrawingCanvas(QWidget):
    """
    A widget for drawing on a white canvas
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.last_point = QPoint()
        self.image = QImage(800, 600, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        
        # Set minimum size for the canvas
        self.setMinimumSize(800, 600)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            current_point = event.position().toPoint()
            painter.drawLine(self.last_point, current_point)
            self.last_point = current_point
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
    
    def clear(self):
        self.image.fill(Qt.white)
        self.update()
    
    def get_image(self):
        """Returns a copy of the current image"""
        return self.image.copy()


class RenderWindow(QMainWindow):
    """
    A separate window for rendering the tiling
    """
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        
        self.setWindowTitle("Dessin du pavage")
        self.setGeometry(150, 150, 850, 700)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Add a title
        title_label = QLabel("Dessinez sur le canvas blanc")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Create drawing canvas
        self.canvas = DrawingCanvas()
        main_layout.addWidget(self.canvas)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Clear button
        clear_button = QPushButton("Effacer")
        clear_button.clicked.connect(self.canvas.clear)
        button_layout.addWidget(clear_button)
        
        # Save button
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_drawing)
        button_layout.addWidget(save_button)
        
        # Close button
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)
    
    def save_drawing(self):
        """Save the drawing as a PNG file and open it in the main window"""
        try:
            # Get the image from the canvas
            image = self.canvas.get_image()
            
            # Create a default filename
            default_path = os.path.join(os.path.expanduser("~"), "tiling_drawing.png")
            
            # Open a save dialog to get the location
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le dessin",
                default_path,
                "Images (*.png)"
            )
            
            if save_path:
                # Make sure the file has .png extension
                if not save_path.endswith('.png'):
                    save_path += '.png'
                
                # Save the image
                image.save(save_path)
                
                # Load the saved image in the main window
                if self.main_window and hasattr(self.main_window, 'main_widget'):
                    self.main_window.main_widget.load_file(save_path)
                    self.statusBar().showMessage(f"Dessin enregistré sous {save_path}", 2000)
                    
                    # Close the render window after saving
                    self.close()
        except Exception as e:
            self.statusBar().showMessage(f"Erreur: {str(e)}", 3000)