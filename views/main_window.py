from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QMenu, QSizeGrip
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import Qt, QSize, QPoint, pyqtSignal

from views.dashboard_widget import DashboardWidget
from views.table_widget import TableWidget
from views.depense_dialog import DepenseDialog
from views.recette_dialog import RecetteDialog
from views.economie_dialog import EconomieDialog
from views.profil_dialog import ProfilDialog
from views.avatars_dialog import AvatarChangeDialog
from views.avatar_viewer_dialog import AvatarViewerDialog
from utils import enregistrer_avatar
from utils.constants import *
from session import Session
import resources_rc


class ClickableAvatar(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class HoverMenuButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)      
    def enterEvent(self, event):
        if self.menu():
            self.menu().exec(self.mapToGlobal(QPoint(0, self.height())))
        super().enterEvent(event)



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
            /* Stylisation an'ireo bokotra Mac ankavia */
            QPushButton#btn_close, QPushButton#btn_min, QPushButton#btn_max {{
                border: none;
                border-radius: 6px; 
            }}
            QPushButton#btn_close {{ background-color: #ff5f56; }} 
            QPushButton#btn_min {{ background-color: #ffbd2e; }}   
            QPushButton#btn_max {{ background-color: #27c93f; }} 
            
            /* Stylisation an'ny Menu Dropdown */
            QMenu {{
                background-color: {FOND_SECONDAIRE};
                color: {TEXTE_PRINCIPAL};
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {ACCENT_PRIMAIRE};
                color: white;
            }}
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
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_SECONDAIRE};
            }}
            """)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)
        layout.addSpacing(15)
        layout.addLayout(self._creer_mac_buttons())
        layout.addSpacing(15)
        layout.addWidget(self._creer_profil())
        layout.addSpacing(10)
        layout.addWidget(self._creer_nav_bouton("  Dashboard",  ":/assets/icons/home.png",     0))
        layout.addWidget(self._creer_nav_bouton("  Recettes",   ":/assets/icons/recette.png",   1))
        layout.addWidget(self._creer_nav_bouton("  Dépenses",   ":/assets/icons/depense.png",  2))
        layout.addWidget(self._creer_nav_bouton("  Économies",  ":/assets/icons/economie.png",  3))
        layout.addWidget(self._creer_nav_bouton("  Historique", ":/assets/icons/historique.png",  4))
        layout.addStretch()  
        btn_parametres = self._creer_nav_bouton("  Paramètres", ":/assets/icons/settings.png", -1)
        btn_parametres.clicked.connect(self._ouvrir_profil_dialog)
        
        layout.addWidget(btn_parametres)
        return sidebar

    def _creer_mac_buttons(self):
        layout_mac = QHBoxLayout()
        layout_mac.setContentsMargins(15, 0, 0, 0)
        layout_mac.setSpacing(8)
        layout_mac.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btn_frm = QPushButton()
        self.btn_frm.setObjectName("btn_close")
        self.btn_frm.setFixedSize(12, 12)
        self.btn_frm.clicked.connect(self.close)
        self.btn_min = QPushButton()
        self.btn_min.setObjectName("btn_min")
        self.btn_min.setFixedSize(12, 12)
        self.btn_min.clicked.connect(self.showMinimized) 
        self.btn_max = QPushButton()
        self.btn_max.setObjectName("btn_max")
        self.btn_max.setFixedSize(12, 12)
        self.btn_max.clicked.connect(self._toggle_maximize)

        layout_mac.addWidget(self.btn_frm)
        layout_mac.addWidget(self.btn_min)
        layout_mac.addWidget(self.btn_max)
        
        return layout_mac

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
        
        self.avatar_label = ClickableAvatar()
        self.avatar_label.clicked.connect(self.ouvrir_avatar_change)
        self.avatar_label.setFixedSize(64, 64)
        self.avatar_label.setStyleSheet("border-radius:32px; border:2px solid #3D9BE9;")

        pixmap = QPixmap(Session.avatar)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.avatar_label.setPixmap(pixmap)
            self.avatar_label.setScaledContents(True)

        nom_label = QLabel(f"{Session.utilisateur_nom}")
        nom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nom_label.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 10px; font-weight: bold;")

        layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nom_label)
        return frame

    def refresh_avatar(self):
        pixmap = QPixmap(Session.avatar)
        if pixmap.isNull():
            return
        pixmap = pixmap.scaled(64,64,Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setScaledContents(True)

    def ouvrir_avatar_change(self):
        dialog = AvatarViewerDialog(self)
        # Ifandraiso ny signal avy amin'ny dialog mankany amin'ny method refresh_avatar
        dialog.avatar_changed.connect(self.refresh_avatar) 
        dialog.exec()


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
        if index != -1:
            btn.clicked.connect(lambda: self._naviguer(index))
        return btn

    def _creer_contenu(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._creer_topbar())

        self.pages = QStackedWidget()
        self.dashboard  = DashboardWidget()
        self.page_recette = TableWidget()
        self.page_recette.charger_table_recette()
        self.page_depense = TableWidget()
        self.page_depense.charger_table_depense()
        self.page_economie = TableWidget()
        self.page_economie.charger_table_economie()
        self.page_historique = TableWidget()
        self.page_historique.charger_table_historique() 

        self.pages.addWidget(self.dashboard)    
        self.pages.addWidget(self.page_recette)         
        self.pages.addWidget(self.page_depense)         
        self.pages.addWidget(self.page_economie)         
        self.pages.addWidget(self.page_historique)         

        layout.addWidget(self.pages)

        #agrandissement
        grip = QSizeGrip(frame)
        layout.addWidget(grip, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        return frame


    def _creer_topbar(self):
        topbar = QFrame()
        topbar.setFixedHeight(45)
        topbar.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_SECONDAIRE};
            }}
            """)

        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        layout.addStretch()
        titre = QLabel("Dashboard")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 14px; font-weight: bold;")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre_page = titre  
        layout.addWidget(titre)
        layout.addStretch()
        
        btn_plus = HoverMenuButton("+")
        btn_plus.setFixedSize(32, 32)
        btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_plus.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_PRIMAIRE};
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 16px;
            }}
            QPushButton:hover {{
                background-color: #2563EB;
            }}
            """)
        
        menu_plus = QMenu(self)
        act_recette = QAction("Recette", self)
        act_recette.triggered.connect(self._ouvrir_recette_dialog)
        act_depense = QAction("Dépense", self)
        act_depense.triggered.connect(self._ouvrir_depense_dialog)
        act_economie = QAction("Économie", self)
        act_economie.triggered.connect(self._ouvrir_economie_dialog)       
        menu_plus.addAction(act_recette)
        menu_plus.addAction(act_depense)
        menu_plus.addAction(act_economie)
        
        btn_plus.setMenu(menu_plus)       
        layout.addWidget(btn_plus)
        layout.addSpacing(10)

        return topbar
    
    def _toggle_maximize(self):
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
        else:
            self.showMaximized()
            self._is_maximized = True

    def _naviguer(self, index: int):
        self.pages.setCurrentIndex(index)
        titres = ["Dashboard", "Recettes", "Dépenses", "Économies", "Historique"]
        self.titre_page.setText(titres[index])

    def _ouvrir_profil_dialog(self):
        dialog = ProfilDialog(self)
        if dialog.exec():
            self.refresh_avatar()

    def _ouvrir_recette_dialog(self):
        dialog = RecetteDialog(self)
        if dialog.exec():           
            self.dashboard.refresh()

    def _ouvrir_depense_dialog(self):
        dialog = DepenseDialog(self)
        if dialog.exec():
            self.dashboard.refresh()

    def _ouvrir_economie_dialog(self):
        dialog = EconomieDialog(self)
        if dialog.exec():
            self.dashboard.refresh()