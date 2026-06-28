import os
from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QListWidget,QListWidgetItem,QPushButton,QHBoxLayout,QMessageBox
from PyQt6.QtGui import QIcon,QPixmap
from PyQt6.QtCore import Qt, QSize



class AvatarChangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avatar_selectionne = None
        self.setWindowTitle("Changer Avatar")
        self.setFixedSize(420, 500)
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

        boutons = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_ok = QPushButton("Enregistrer")

        btn_annuler.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.enregistrer)

        boutons.addWidget(btn_annuler)
        boutons.addWidget(btn_ok)

        layout.addLayout(boutons)


    def charger_avatars(self):
        dossier = "assets/avatars"
        if not os.path.exists(dossier):
            return
        extensions = (".png", ".jpg", ".jpeg")
        for fichier in sorted(os.listdir(dossier)):
            if fichier.lower().endswith(extensions):
                chemin = os.path.join(dossier, fichier)
                item = QListWidgetItem()
                item.setIcon(QIcon(chemin))
                item.setText(os.path.splitext(fichier)[0])
                item.setData( Qt.ItemDataRole.UserRole, chemin)

                self.liste.addItem(item)

    def enregistrer(self):
        item = self.liste.currentItem()
        if item is None:
            QMessageBox.warning(
                self,
                "Avatar",
                "Veuillez choisir un avatar."
            )
            return

        self.avatar_selectionne = item.data(Qt.ItemDataRole.UserRole)

        self.accept()

    def avatar(self):
        return self.avatar_selectionne