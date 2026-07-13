import os
from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QListWidget,QListWidgetItem,QPushButton,QHBoxLayout,QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QDirIterator
from utils.constants import *
from views.message_dialog import CustomMessageDialog 
import resources_rc


class AvatarChangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avatar_selectionne = None
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(480, 500)
        self.construire_ui()

    def construire_ui(self):
        layout = QVBoxLayout(self)
        titre = QLabel("Choisissez votre avatar")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(titre)

        self.liste = QListWidget()
        self.liste.setIconSize(QSize(80,80))
        self.liste.setViewMode(QListWidget.ViewMode.IconMode)
        self.liste.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.liste.setMovement(QListWidget.Movement.Static)
        self.liste.setSpacing(15)

        layout.addWidget(self.liste)

        self.charger_avatars()

        #boutton
        boutons_layout = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(self._style_bouton(FOND_INPUT, TEXTE_SECONDAIRE))
        btn_annuler.clicked.connect(self.reject) 

        btn_enregstr = QPushButton("Enregistrer")
        btn_enregstr.clicked.connect(self.enregistrer)

        boutons_layout.addWidget(btn_annuler)
        boutons_layout.addWidget(btn_enregstr)
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


    def charger_avatars(self):
        prefix = ":/assets/avatars"
        it = QDirIterator(prefix)
        extensions = (".png", ".jpg", ".jpeg")
        while it.hasNext():
            chemin = it.next()
            if not chemin.lower().endswith(extensions):
                continue
            nom = os.path.splitext(os.path.basename(chemin))[0]

            item = QListWidgetItem()
            item.setIcon(QIcon(chemin))
            item.setText(nom)
            item.setData(Qt.ItemDataRole.UserRole, chemin)

            self.liste.addItem(item)


    def enregistrer(self):
        item = self.liste.currentItem()
        if item is None:
            CustomMessageDialog("Avatar","Veuillez choisir un avatar.","warning",self).exec()
            return

        self.avatar_selectionne = item.data(Qt.ItemDataRole.UserRole)

        self.accept()

    def avatar(self):
        return self.avatar_selectionne