from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget,QFrame
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QPoint

from views.dashboard_widget import DashboardWidget
#from views.table_widget import TableWidget
from views.depense_dialog import DepenseDialog
from views.recette_dialog import RecetteDialog
from views.economie_dialog import EconomieDialog
from views.profil_dialog import ProfilDialog
from utils.constants import *
from session import Session
from config import DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()
        self._old_pos = None
        self._is_maximized = False


    def _configurer_fenetre(self):
        self.setWindowTitle("ExpenseApp")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {FOND_PRINCIPAL};
                background-image: url("assets/avatars/logo.png");
                background-repeat: no-repeat;
                background-position: center;
            }}
            QPushButton#btn_close, QPushButton#btn_min, QPushButton#btn_max {{
                border: none;
                border-radius: 6px; 
                background-color: #374151; 
            }}
            QPushButton#btn_close {{ background-color: #ff5f56; }} 
            QPushButton#btn_min {{ background-color: #ffbd2e; }}   
            QPushButton#btn_max {{ background-color: #27c93f; }} 
        """)

    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self._old_pos is not None:
            delta = QPoint(event.globalPosition().toPoint() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event):
        self._old_pos = None

   
    def _construire_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        layout_principal.addWidget(self._creer_sidebar())
        layout_principal.addWidget(self._creer_contenu(), stretch=1)

    
    
    def _creer_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(150)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_SECONDAIRE};
                border-right: 1px solid {BORDURE};
            }}
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)

        layout.addWidget(self._creer_profil())
        layout.addSpacing(10)
        layout.addWidget(self._creer_nav_bouton("  Dashboard",  "assets/icons/home.png",     0))
        layout.addWidget(self._creer_nav_bouton("  Recettes",   "assets/icons/recette.png",   1))
        layout.addWidget(self._creer_nav_bouton("  Dépenses",   "assets/icons/depense.png",  2))
        layout.addWidget(self._creer_nav_bouton("  Économies",  "assets/icons/econimie.png",  3))
        layout.addWidget(self._creer_nav_bouton("  Historique", "assets/icons/historique.png",  4))
        layout.addStretch()  # pousse tout vers le haut

        return sidebar

    
    def _creer_profil(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_CARTE};
                border : none;
                padding: 16px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        avatar_btn = QPushButton()
        avatar_btn.setFixedSize(64, 64)
        avatar_btn.setStyleSheet("""
                                QPushButton {border-radius:32px; border:2px solid #3D9BE9; background-color:transparnet;}
                                QPushButton:hover {border:2px solid #FFFFFF;}
                                 """)

        pixmap = QPixmap(DB_CONFIG.get("avatar", "assets/avatars/young-man.png"))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(64, 64,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)
            avatar_btn.setIcon(QIcon(pixmap))
            avatar_btn.setIconSize(QSize(60,60))
        avatar_btn.clicked.connect(self._ouvrir_profil_dialog())

        # Nom
        nom_label = QLabel(f"{Session.utilisateur_prenom}")
        nom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nom_label.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 13px; font-weight: bold;")

        layout.addWidget(avatar_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nom_label)

        return frame

    
    def _creer_nav_bouton(self, texte: str, icone_path: str, index: int):
        btn = QPushButton(texte)
        btn.setIcon(QIcon(icone_path))
        btn.setIconSize(QSize(18, 18))
        btn.setFixedHeight(44)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXTE_SECONDAIRE};
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {FOND_CARTE};
                color: {TEXTE_PRINCIPAL};
                border-left: 3px solid {ACCENT_PRIMAIRE};
            }}
        """)
        # Chaque bouton connait son index de page
        btn.clicked.connect(lambda: self._naviguer(index))
        return btn

    
    def _creer_contenu(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._creer_topbar())

        # QStackedWidget = plusieurs pages, une seule visible à la fois
        self.pages = QStackedWidget()
        self.dashboard  = DashboardWidget()
        #self.table_widget = TableWidget()

        self.pages.addWidget(self.dashboard)    # index 0
        self.pages.addWidget(QWidget())         # index 1 — Recettes  (à compléter)
        #self.pages.addWidget(self.table_widget) # index 2 — Dépenses
        self.pages.addWidget(QWidget())         # index 3 — Économies (à compléter)
        self.pages.addWidget(QWidget())         # index 4 — Historique(à compléter)

        layout.addWidget(self.pages)
        return frame

    
    def _creer_topbar(self):
        topbar = QFrame()
        topbar.setFixedHeight(45)
        topbar.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_SECONDAIRE};
                border-bottom: 1px solid {BORDURE};
            }}
        """)

        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)

        titre = QLabel("Dashboard")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 14px; font-weight: bold;")
        self.titre_page = titre  # gardé en référence pour changer selon la page
        layout.addWidget(titre)
       
        layout.addStretch()
        btn_recette  = self._creer_action_bouton("+ Recette",  VERT_RECETTE)
        btn_depense  = self._creer_action_bouton("+ Dépense",  ROUGE_DEPENSE)
        btn_economie = self._creer_action_bouton("+ Économie", BLEU_ECONOMIE)
        btn_recette.clicked.connect(self._ouvrir_recette_dialog)
        btn_depense.clicked.connect(self._ouvrir_depense_dialog)
        btn_economie.clicked.connect(self._ouvrir_economie_dialog)
        layout.addWidget(btn_recette)
        layout.addWidget(btn_depense)
        layout.addWidget(btn_economie)

        
        layout.addStretch()
        layout.addSpacing(10)
        self.btn_min = QPushButton()
        self.btn_min.setObjectName("btn_min")
        self.btn_min.setFixedSize(12, 12)
        self.btn_min.clicked.connect(self.showMinimized)
        
        self.btn_max = QPushButton()
        self.btn_max.setObjectName("btn_max")
        self.btn_max.setFixedSize(12, 12)
        self.btn_max.clicked.connect(self._toggle_maximize)
        
        self.btn_frm = QPushButton()
        self.btn_frm.setObjectName("btn_close")
        self.btn_frm.setFixedSize(12, 12)
        self.btn_frm.clicked.connect(self.close)

        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_frm)

        return topbar
    
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self._is_maximized = True
        else:
            self.showMaximized()
            self._is_maximized = False
    
    def _creer_action_bouton(self, texte: str, couleur: str):
        btn = QPushButton(texte)
        btn.setFixedHeight(24)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {couleur};
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)
        return btn


    def _naviguer(self, index: int):
        self.pages.setCurrentIndex(index)
        titres = ["Dashboard", "Recettes", "Dépenses", "Économies", "Historique"]
        self.titre_page.setText(titres[index])

    def _ouvrir_profil_dialog(self):
        dialog = ProfilDialog(self)
        if dialog.exec():
            self._creer_profil()

    def _ouvrir_recette_dialog(self):
        dialog = RecetteDialog(self)
        if dialog.exec():           
            self._creer_profil()

    def _ouvrir_depense_dialog(self):
        dialog = DepenseDialog(self)
        if dialog.exec():
            self.dashboard.refresh()

    def _ouvrir_economie_dialog(self):
        dialog = EconomieDialog(self)
        if dialog.exec():
            self.dashboard.refresh()