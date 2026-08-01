from PyQt6.QtWidgets import QDialog,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from session import Session
from utils.constants import *
from utils.theme_manager import ThemeManager
theme = ThemeManager.theme()
from views.avatars_dialog import AvatarChangeDialog
from utils.avatar_manager import enregistrer_avatar


class AvatarViewerDialog(QDialog):
    avatar_changed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(320,420)
        self.setStyleSheet("""
            QDialog{
                background:"#1A2634";
                border-radius:10px;
            }

            QPushButton{
                background:#2196F3;
                color:white;
                border:none;
                border-radius:8px;
                padding:10px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#1976D2;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Avatar
        self.avatar = QLabel()
        pix = QPixmap(Session.avatar)
        pix = pix.scaled( 180, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.avatar.setPixmap(pix)
        self.avatar.setFixedSize(180,180)
        self.avatar.setScaledContents(True)
        layout.addWidget( self.avatar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nom
        nom = QLabel(f"{Session.utilisateur_prenom} {Session.utilisateur_nom}")
        nom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nom.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        layout.addWidget(nom)

        # Email
        email = QLabel(Session.utilisateur_email)
        email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(email)
        layout.addSpacing(15)

        #Boutton
        boutons_layout = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(self._style_bouton(theme['FOND_INPUT'], theme['TEXTE_SECONDAIRE']))
        btn_annuler.clicked.connect(self.reject) 

        btn_CA = QPushButton("Changer Avatar")
        btn_CA.clicked.connect(self.changer_avatar)

        boutons_layout.addWidget(btn_annuler)
        boutons_layout.addWidget(btn_CA)
        layout.addLayout(boutons_layout)

    def _style_bouton(self, bg: str, color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }}
        """


    def changer_avatar(self):
        dialog = AvatarChangeDialog(self)
        if dialog.exec():
            chemin = dialog.avatar()
            if chemin:
                enregistrer_avatar(Session.utilisateur_email,chemin)
                Session.avatar = chemin
                pix = QPixmap(chemin)
                pix = pix.scaled( 180, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                self.avatar.setPixmap(pix)
                self.avatar_changed.emit() # Alefaso ny signal fa niova ny avatar
                self.close()