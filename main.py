import sys
from typing import Optional, Type

from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat, QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QPushButton, QLabel, QMainWindow, QTextBrowser, QDialog, QVBoxLayout

from style_manager import StyleManager
from tile import TileWidget
from render_window import RenderWindow

from tilings.abstract.tiling import Tiling as AbstractTiling

from tilings.spherical.s34.tiling import Tiling as SphTiling34
from tilings.spherical.s43.tiling import Tiling as SphTiling43

from tilings.euclidean.cm.tiling import Tiling as EucTilingCM
from tilings.euclidean.cmm.tiling import Tiling as EucTilingCMM
from tilings.euclidean.p1.tiling import Tiling as EucTilingP1
from tilings.euclidean.p2.tiling import Tiling as EucTilingP2
from tilings.euclidean.p3.tiling import Tiling as EucTilingP3
from tilings.euclidean.p3m1.tiling import Tiling as EucTilingP3M1
from tilings.euclidean.p4.tiling import Tiling as EucTilingP4
from tilings.euclidean.p4g.tiling import Tiling as EucTilingP4G
from tilings.euclidean.p4m.tiling import Tiling as EucTilingP4M
from tilings.euclidean.p6.tiling import Tiling as EucTilingP6
from tilings.euclidean.p6m.tiling import Tiling as EucTilingP6M
from tilings.euclidean.p31m.tiling import Tiling as EucTilingP31M
from tilings.euclidean.pg.tiling import Tiling as EucTilingPG
from tilings.euclidean.pgg.tiling import Tiling as EucTilingPGG
from tilings.euclidean.pm.tiling import Tiling as EucTilingPM
from tilings.euclidean.pmg.tiling import Tiling as EucTilingPMG
from tilings.euclidean.pmm.tiling import Tiling as EucTilingPMM

from tilings.hyperbolic.s46.tiling import Tiling as HypTiling46
from utils.path_helper import get_resource_path

class MainWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # tile place holder
        self.tile = TileWidget(self)
        self.tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.tile, 0, 0, 1, 2)

        self.name = QLabel()
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.name, 1, 0, 1, 2)

        self.reset_corners_btn = QPushButton('Effacer les sommets')
        self.reset_corners_btn.clicked.connect(self.tile.reset_corners)
        self.layout.addWidget(self.reset_corners_btn, 2, 0)
        self.reset_corners_btn.setEnabled(False)

        self.render_btn = QPushButton('Dessiner le pavage')
        self.render_btn.clicked.connect(self.tile.render_tiling)
        self.layout.addWidget(self.render_btn, 2, 1)
        self.render_btn.setEnabled(False)

        self.update_status_tip()

        self.show()

    def load_file(self, path):
        self.tile.path = path
        self.toogle_reset_corners_btn()
        self.toogle_render_btn()
        self.update_status_tip()
        self.layout.update()

    def load_tiling(self, checked: bool, tiling: Optional[Type[AbstractTiling]]):
        self.tile.tiling_cls = tiling
        if self.tile.tiling_cls is not None:
            self.name.setText("{0} {1}".format(self.tile.tiling_cls.KIND, self.tile.tiling_cls.CODE))

        self.toogle_reset_corners_btn()
        self.toogle_render_btn()
        self.update_status_tip()

    def toogle_reset_corners_btn(self):
        """
        Enable / disable the reset corners button
        """
        if self.tile.path == "":
            self.reset_corners_btn.setEnabled(False)
            return

        if self.tile.tiling_cls is None:
            self.reset_corners_btn.setEnabled(False)
            return

        self.reset_corners_btn.setEnabled(True)

    def toogle_render_btn(self):
        """
        Enable / disable the render button
        """
        if self.tile.path == "":
            self.render_btn.setEnabled(False)
            return

        if self.tile.tiling_cls is None:
            self.render_btn.setEnabled(False)
            return

        if len(self.tile.corners) != self.tile.tiling_cls.CORNER_NB:
            self.render_btn.setEnabled(False)
            return

        self.render_btn.setEnabled(True)

    def update_status_tip(self):
        """
        Update the instruction in the status bar of the main window
        """
        if self.tile.path == "" and self.tile.tiling_cls is None:
            self.parent().statusBar().showMessage("Ouvrir un fichier et choisir un pavage")
            return

        if self.tile.path == "":
            self.parent().statusBar().showMessage("Ouvrir un fichier")
            return

        if self.tile.tiling_cls is None:
            self.parent().statusBar().showMessage("Choisir un pavage")
            return

        if len(self.tile.corners) != self.tile.tiling_cls.CORNER_NB:
            self.parent().statusBar().showMessage(
                "Délimiter les bords de la tuile. Forme : {0}. Nombre de points requis : {1}".format(
                    self.tile.tiling_cls.SHAPE,
                    self.tile.tiling_cls.CORNER_NB
                )
            )
            return

        self.parent().statusBar().showMessage("Dessiner le pavage")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pavages en tout genre')
        self.setGeometry(100, 100, 600, 400)
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        open_file_action = QAction("Ouvrir…", self)
        open_file_action.setShortcut(QKeySequence("Ctrl+o"))
        open_file_action.triggered.connect(self.open_file)

        close_action = QAction("Fermer", self)
        close_action.setShortcut(self.tr("CTRL+W"))
        close_action.triggered.connect(self.close)
        
        # Create a new action for opening the render window
        render_action = QAction("Dessiner le pavage", self)
        render_action.triggered.connect(self.open_render_window)
        
        menu = self.menuBar()
        file_menu = menu.addMenu("Fichier")
        file_menu.addAction(open_file_action)
        file_menu.addAction(close_action)
        
        # Add a new menu for drawing
        draw_menu = menu.addMenu("Dessin")
        draw_menu.addAction(render_action)

        # Add theme switching actions to a menu
        theme_menu = menu.addMenu("Thèmes")
        
        dark_theme_action = QAction("Thème sombre", self)
        dark_theme_action.triggered.connect(self.apply_dark_theme)
        theme_menu.addAction(dark_theme_action)
        
        light_theme_action = QAction("Thème clair", self)
        light_theme_action.triggered.connect(self.apply_light_theme)
        theme_menu.addAction(light_theme_action)


        # Spherical tilings
        sph_34_action = QAction(SphTiling34.CODE, self)
        sph_34_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, SphTiling34))

        sph_43_action = QAction(SphTiling43.CODE, self)
        sph_43_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, SphTiling43))

        # Euclidean tilings
        euc_cm_action = QAction(EucTilingCM.CODE, self)
        euc_cm_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingCM))

        euc_cmm_action = QAction(EucTilingCMM.CODE, self)
        euc_cmm_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingCMM))

        euc_p1_action = QAction(EucTilingP1.CODE, self)
        euc_p1_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP1))

        euc_p2_action = QAction(EucTilingP2.CODE, self)
        euc_p2_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP2))

        euc_p3_action = QAction(EucTilingP3.CODE, self)
        euc_p3_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP3))

        euc_p3m1_action = QAction(EucTilingP3M1.CODE, self)
        euc_p3m1_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP3M1))

        euc_p4_action = QAction(EucTilingP4.CODE, self)
        euc_p4_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP4))

        euc_p4g_action = QAction(EucTilingP4G.CODE, self)
        euc_p4g_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP4G))

        euc_p4m_action = QAction(EucTilingP4M.CODE, self)
        euc_p4m_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP4M))

        euc_p6_action = QAction(EucTilingP6.CODE, self)
        euc_p6_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP6))

        euc_p6m_action = QAction(EucTilingP6M.CODE, self)
        euc_p6m_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP6M))

        euc_p31m_action = QAction(EucTilingP31M.CODE, self)
        euc_p31m_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingP31M))

        euc_pg_action = QAction(EucTilingPG.CODE, self)
        euc_pg_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingPG))

        euc_pgg_action = QAction(EucTilingPGG.CODE, self)
        euc_pgg_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingPGG))

        euc_pm_action = QAction(EucTilingPM.CODE, self)
        euc_pm_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingPM))

        euc_pmg_action = QAction(EucTilingPMG.CODE, self)
        euc_pmg_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingPMG))

        euc_pmm_action = QAction(EucTilingPMM.CODE, self)
        euc_pmm_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, EucTilingPMM))

        # Hyperbolic tilings
        hyp_46_action = QAction(HypTiling46.CODE, self)
        hyp_46_action.triggered.connect(lambda checked: self.main_widget.load_tiling(checked, HypTiling46))

        spherical_menu = menu.addMenu("Pavages sphériques")
        spherical_menu.addAction(sph_34_action)
        spherical_menu.addAction(sph_43_action)

        euclidean_menu = menu.addMenu("Pavages euclidiens")
        euclidean_menu.addAction(euc_p1_action)
        euclidean_menu.addAction(euc_p2_action)
        euclidean_menu.addAction(euc_pm_action)
        euclidean_menu.addAction(euc_pg_action)
        euclidean_menu.addAction(euc_cm_action)
        euclidean_menu.addAction(euc_pmm_action)
        euclidean_menu.addAction(euc_pmg_action)
        euclidean_menu.addAction(euc_pgg_action)
        euclidean_menu.addAction(euc_cmm_action)
        euclidean_menu.addAction(euc_p4_action)
        euclidean_menu.addAction(euc_p4m_action)
        euclidean_menu.addAction(euc_p4g_action)
        euclidean_menu.addAction(euc_p3_action)
        euclidean_menu.addAction(euc_p3m1_action)
        euclidean_menu.addAction(euc_p31m_action)
        euclidean_menu.addAction(euc_p6_action)
        euclidean_menu.addAction(euc_p6m_action)

        hyperbolic_menu = menu.addMenu("Pavages hyperboliques")
        hyperbolic_menu.addAction(hyp_46_action)
        
        help_menu = menu.addMenu("Aide")
        help_action = QAction("Afficher l'aide", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        status_bar = self.statusBar()

        self.render_window = None
        

    def open_render_window(self):
        """
        Open a new window to render the tiling
        """
        # Create a new render window each time or reuse existing one
        if self.render_window is None or not self.render_window.isVisible():
            self.render_window = RenderWindow(self)  # Pass self (MainWindow) as a reference
        
        # Show the window
        self.render_window.show()
        self.render_window.raise_()
        self.render_window.activateWindow()

    def apply_dark_theme(self):
        StyleManager.apply_dark_theme(QApplication.instance())
    
    def apply_light_theme(self):
        StyleManager.apply_light_theme(QApplication.instance())


    def open_file(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(get_resource_path("downloads"))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.main_widget.load_file(filenames[0])
                
    def show_help(self):
        self.help_window = HelpWindow(self)
        self.help_window.show()


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aide")
        self.setGeometry(200, 200, 550, 450)

        layout = QVBoxLayout()

        self.help_text = QTextBrowser(self)
        self.help_text.setOpenExternalLinks(True)  # Permet l'ouverture des liens externes
        self.help_text.setHtml("""
            <style>
                h2 { text-align: center; }
                h3 { color: #0055aa; margin-top: 20px; }
                kbd { background-color: #e2e2e2; }
                li { margin-top: 5px; }
                ul { margin-bottom: 3px; }
            </style>
            
            <h2>Aide sur l'application</h2>
            <p>Bienvenue dans l'application de pavage !</p>

            <h3>Fonctionnalités principales :</h3>
            <ul>
                <li>Charger une image ou la dessiner pour la tuiler</li>
                <li>Choisir un type de pavage (sphérique, euclidien, hyperbolique)</li>
                <li>Dessiner un pavage</li>
            </ul>

            <h3>Raccourcis clavier :</h3>
            <ul>
                <li><kbd>Ctrl + O</kbd> : Ouvrir une image</li>
                <li><kbd>Ctrl + W</kbd> : Fermer l'application</li>
                <li><kbd>Échap</kbd> : Fermer cette aide</li>
            </ul>

            <h3>Ressources utiles :</h3>
            <ul>
                <li>Qu'est-ce qu'un pavage ?
                    <ul>
                        <li><a href='https://fr.wikipedia.org/wiki/Pavage'>Pavage du plan (Wikipedia)</a></li>
                        <li><a href='https://fr.wikipedia.org/wiki/Pavage_par_des_polygones_r%C3%A9guliers'>Pavages par des polygones réguliers (Wikipedia)</a></li>
                        <li><a href='https://fr.wikipedia.org/wiki/Pavage_de_la_sph%C3%A8re'>Pavage de la sphère (Wikipedia)</a></li>
                        <li><a href='https://www.imo.universite-paris-saclay.fr/~yves.benoist/prepubli/01pavage.pdf'>Pavages du plan par Yves Benoist (pdf)</a></li>
                    </ul>
                </li>
                <li><a href='https://doc.qt.io/qt-6/qtimageformats-index.html'>Formats d'image compatibles</a></li>
            </ul>

            <p>Besoin d'aide supplémentaire ? Consultez la documentation ou contactez le support.</p>
        """)
        
        layout.addWidget(self.help_text)
        self.setLayout(layout)

if __name__ == '__main__':
    # Set the surface format before creating the application instance
    qs_format = QSurfaceFormat()
    qs_format.setVersion(4, 1)
    qs_format.setProfile(QSurfaceFormat.CoreProfile)
    qs_format.setSamples(4)  # Enable antialiasing
    QSurfaceFormat.setDefaultFormat(qs_format)

    # Create the application
    app = QApplication([])
    
    # Apply styling using the StyleManager class
    StyleManager.apply_dark_theme(app)
    # Or if you prefer a light theme:
    # StyleManager.apply_light_theme(app)
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec())