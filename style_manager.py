from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

class StyleManager:
    """Class to manage application styling and themes"""
    
    @staticmethod
    def apply_dark_theme(app: QApplication):
        """Apply a dark theme to the application"""
        # Set Fusion style for a modern look
        app.setStyle("Fusion")
        
        # Define a color palette
        palette = app.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        
        # Apply custom stylesheet
        app.setStyleSheet(StyleManager.get_dark_stylesheet())
    
    @staticmethod
    def apply_light_theme(app: QApplication):
        """Apply a light theme to the application"""
        # Set Fusion style
        app.setStyle("Fusion")
        
        # Use default palette with some adjustments
        palette = app.palette()
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)
        
        # Apply custom stylesheet
        app.setStyleSheet(StyleManager.get_light_stylesheet())
    
    @staticmethod
    def get_dark_stylesheet():
        """Returns the dark theme stylesheet"""
        return """
        QMainWindow, QWidget {
            background-color: #353535;
            color: #FFFFFF;
        }
        QPushButton {
            background-color: #2a82da;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3a92ea;
        }
        QPushButton:pressed {
            background-color: #1a72ca;
        }
        QPushButton:disabled {
            background-color: #666666;
        }
        QLabel {
            padding: 4px;
            font-size: 14px;
        }
        QMenuBar {
            background-color: #444444;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #2a82da;
        }
        QMenu {
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
        }
        QMenu::item:selected {
            background-color: #2a82da;
        }
        QStatusBar {
            background-color: #444444;
            color: white;
        }
        """
    
    @staticmethod
    def get_light_stylesheet():
        """Returns the light theme stylesheet"""
        return """
        QMainWindow, QWidget {
            background-color: #F5F5F5;
            color: #333333;
        }
        QPushButton {
            background-color: #2a82da;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3a92ea;
        }
        QPushButton:pressed {
            background-color: #1a72ca;
        }
        QPushButton:disabled {
            background-color: #CCCCCC;
            color: #888888;
        }
        QLabel {
            padding: 4px;
            font-size: 14px;
        }
        QMenuBar {
            background-color: #E0E0E0;
        }
        QMenuBar::item:selected {
            background-color: #2a82da;
            color: white;
        }
        QMenu {
            background-color: #F5F5F5;
            border: 1px solid #CCCCCC;
        }
        QMenu::item:selected {
            background-color: #2a82da;
            color: white;
        }
        QStatusBar {
            background-color: #E0E0E0;
        }
        """